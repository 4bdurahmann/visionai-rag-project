"""
Shared query pipeline: retrieval -> gating -> LLM answer -> quality scoring.

Single source of truth for the flow used by the HTTP API (routes/api.py) and
the interactive CLI (tools/query_chroma.py). Keeps the two entry points from
drifting apart.
"""

import json

from controllers.gate import disclaim, GRADE_LOOKAHEAD
from controllers.grade import extract_grade
from controllers.llm import (
    generate_answer,
    score_citation_accuracy,
    score_faithfulness,
)
from modules import config
from modules.engine import get_engine


def accuracy_summary(path: str = config.ACCURACY_JSON) -> str | None:
    """Human-readable model accuracy from the latest evaluation report."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        n, correct, acc = data.get("n_questions"), data.get("n_correct"), data.get("accuracy")
        if n and acc is not None:
            return (
                f"Model accuracy: {correct}/{n} = {acc * 100:.1f}% "
                f"({data.get('strategy')}, top-{data.get('top_k')})"
            )
    except (OSError, json.JSONDecodeError, AttributeError):
        pass
    return None


def _build_hits(hits: list) -> list[dict]:
    """Shape raw retrieval records into the API hit format."""
    return [
        {
            "rank": i,
            "similarity": round(sim, 4),
            "grade": meta.get("grade") or extract_grade(doc),
            "section": meta.get("heading"),
            "page": meta.get("page"),
            "org": meta.get("org"),
            "text": doc[:1500],
        }
        for i, (_cid, sim, _fused, doc, meta) in enumerate(hits, 1)
    ]


def answer_query(
    query: str,
    k: int = 5,
    strategy: str = "hybrid",
    use_llm: bool = True,
    sim_threshold: float = 0.30,
    use_grade_gate: bool = True,
) -> dict:
    """Run the full pipeline for one question.

    Returns a dict with the QueryResponse shape. Never raises: retrieval and
    LLM failures degrade into a ``message`` field plus an ``error`` field.
    """
    engine = get_engine()
    if strategy != engine.retriever.strategy:
        engine.retriever.strategy = strategy

    try:
        qv = engine.model.encode([query], normalize_embeddings=True)[0]
        hits_full = engine.retriever.search(query, qv, max(k, GRADE_LOOKAHEAD))
        msg, reason = disclaim(
            query,
            hits_full,
            sim_threshold=sim_threshold,
            use_grade_gate=use_grade_gate,
        )
        hits = hits_full[:k]
    except Exception as exc:  # noqa: BLE001 - never crash the API
        return {
            "query": query,
            "k": k,
            "strategy": strategy,
            "disclaimed": True,
            "reason": "internal_error",
            "message": f"(Retrieval failed: {exc})",
            "hits": [],
            "quality": None,
            "accuracy": accuracy_summary(),
            "error": f"retrieval: {exc}",
        }

    message = msg or "No confident match found."
    quality = None
    if not msg:
        if use_llm:
            try:
                message = generate_answer(query, hits_full)
            except Exception as exc:  # noqa: BLE001 - surface but don't crash
                message = f"(LLM answer unavailable: {exc})"
            # score the returned answer against the evidence the generator saw
            try:
                faith, fd = score_faithfulness(message, hits_full)
            except Exception as exc:  # noqa: BLE001
                faith, fd = None, {"error": str(exc)}
            try:
                cites, cd = score_citation_accuracy(message, hits_full)
            except Exception as exc:  # noqa: BLE001
                cites, cd = None, {"error": str(exc)}
            quality = {
                "faithfulness": faith,
                "citation_accuracy": cites,
                "unsupported_claims": fd.get("unsupported_claims", []),
                "bad_citations": cd.get("bad_citations", []),
            }
        else:
            message = "Answer not generated (use_llm=false)."

    return {
        "query": query,
        "k": k,
        "strategy": strategy,
        "disclaimed": bool(msg),
        "reason": reason,
        "message": message,
        "hits": _build_hits(hits),
        "quality": quality,
        "accuracy": accuracy_summary(),
        "error": None,
    }