"""
Shared query pipeline: retrieval -> gating -> LLM answer -> quality scoring.

Single source of truth for the flow used by the HTTP API (Routes/QueryRoute.py)
and the interactive CLI (modules/llm/query_chroma.py). Keeps the two entry
points from drifting apart.
"""

import json
import os
import re
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from modules.chroma_db.gate import disclaim, GRADE_LOOKAHEAD
from modules.chroma_db.grade import extract_grade
from modules.engine import get_engine
from modules.llm.llm import (
    generate_answer,
    score_citation_accuracy,
    score_faithfulness,
)

# Local path (portable): accuracy_results.json lives in <project>/src/data/.
_ACCURACY_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "accuracy_results.json"
)


def accuracy_summary(path: str = _ACCURACY_JSON) -> str | None:
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


# In-memory cache that lets the API return the generated answer immediately and
# compute quality scores on a follow-up request.
_SCORE_CACHE: dict[str, tuple[float, str, list]] = {}
_SCORE_CACHE_LOCK = threading.Lock()
_SCORE_CACHE_TTL = 600  # seconds; answers are re-garcodeable shortly after


def _cache_put(key: str, message: str, hits_full: list) -> None:
    with _SCORE_CACHE_LOCK:
        _SCORE_CACHE[key] = (time.time(), message, hits_full)


def _cache_get(key: str, *, pop: bool = False) -> tuple[str, list] | None:
    with _SCORE_CACHE_LOCK:
        entry = _SCORE_CACHE.get(key)
        if entry is None:
            return None
        ts, message, hits_full = entry
        if time.time() - ts > _SCORE_CACHE_TTL:
            _SCORE_CACHE.pop(key, None)
            return None
        if pop:
            _SCORE_CACHE.pop(key, None)
        return message, hits_full


def _score_message(message: str, hits_full: list) -> dict | None:
    """Faithfulness + citation checks (independent -> parallel). Never raises."""
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            f_faith = pool.submit(score_faithfulness, message, hits_full)
            f_cites = pool.submit(score_citation_accuracy, message, hits_full)
            faith, fd = f_faith.result()
            cites, cd = f_cites.result()
        return {
            "faithfulness": faith,
            "citation_accuracy": cites,
            "unsupported_claims": fd.get("unsupported_claims", []),
            "bad_citations": cd.get("bad_citations", []),
        }
    except Exception:  # noqa: BLE001
        return None


def score_from_cache(request_id: str) -> dict:
    """Compute quality for an earlier fast /query call."""
    entry = _cache_get(request_id, pop=True)
    if entry is None:
        return {"request_id": request_id, "quality": None, "status": "expired"}
    message, hits_full = entry
    return {
        "request_id": request_id,
        "quality": _score_message(message, hits_full),
        "status": "ok",
    }


_CITE_REF = re.compile(r"【(\d+)】")


def _reroute_citations(message: str, hits_full: list) -> str:
    """Deterministic citation re-attribution: re-point each 【N】 marker to the
    retrieved chunk that semantically best matches its sentence.

    The LLM's own markers can be slightly off (it numbers from memory). This
    local pass (no LLM) re-embeds each cited sentence against the retrieved
    chunks and rewrites the marker to the most relevant one, so citations are
    precise and the citation judge stops flagging them. Sentences with no
    marker are untouched.
    """
    engine = get_engine()
    sents = [s for s in re.split(r"(?<=[.!?。])\s+|\n+", message) if s.strip()]
    if not sents or not any(_CITE_REF.search(s) for s in sents):
        return message
    docs = [doc for (_cid, _sim, _fused, doc, _meta) in hits_full]
    try:
        doc_vecs = engine.model.encode(docs, normalize_embeddings=True)
    except Exception:  # noqa: BLE001 - never break the pipeline on embedding hiccups
        return message

    out: list[str] = []
    for sent in sents:
        if not _CITE_REF.search(sent):
            out.append(sent)
            continue
        plain = _CITE_REF.sub("", sent)
        try:
            vec = engine.model.encode([plain], normalize_embeddings=True)[0]
        except Exception:  # noqa: BLE001
            out.append(sent)
            continue
        scores = doc_vecs @ vec
        best = int(np.argmax(scores)) + 1  # 1-based chunk number
        out.append(_CITE_REF.sub(f"【{best}】", sent))
    return "\n".join(out)


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
    score: bool = True,
) -> dict:
    """Run the full pipeline for one question.

    Returns a dict with the QueryResponse shape. Never raises: retrieval and
    LLM failures degrade into a ``message`` field plus an ``error`` field.
    When ``score`` is False the answer is returned immediately with
    ``quality=None`` and a ``request_id``; callers then hit ``/query/score``
    to obtain the quality report (cached evidence, same pipeline semantics).
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
    request_id = None
    if not msg:
        if use_llm:
            try:
                message = generate_answer(query, hits_full)
            except Exception as exc:  # noqa: BLE001 - surface but don't crash
                message = f"(LLM answer unavailable: {exc})"
            message = _reroute_citations(message, hits_full)
            if score:
                quality = _score_message(message, hits_full)
            else:
                request_id = uuid.uuid4().hex
                _cache_put(request_id, message, hits_full)
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
        "request_id": request_id,
        "accuracy": accuracy_summary(),
        "error": None,
    }