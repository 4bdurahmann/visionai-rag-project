"""
Medical RAG - HTTP API
----------------------
Expose the local retrieval + Groq answer pipeline as a JSON API so another
device on the network can ask questions about the indexed guideline.

Heavy objects (embedding model, Chroma collection, retriever) are loaded once
at startup and reused across requests.

Run:
    rag/bin/python -m uvicorn api:app --host 0.0.0.0 --port 8000

Then your friend hits e.g.  http://<your-lan-ip>:8000/query  with:
    {"query": "What does the USPSTF recommend?", "k": 5}

Endpoints:
    GET  /health          -> {"status": "ok", "collection": ..., "n_chunks": ...}
    POST /query           -> JSON answer (see below)

Request body:
    query     (str)  required
    k         (int)  number of hits to return / answer window (default 5)
    strategy  (str)  "hybrid" or "vector" (default hybrid)
    use_llm   (bool) generate a Groq answer (default true)

Response:
    {
      "query", "k", "strategy",
      "disclaimed": bool, "reason": "low_similarity|low_fusion|no_grade_for_decision|none",
      "message":   "natural-language answer, or the disclaimer text",
      "hits":      [{"rank","similarity","fused","grade","section","org","text"}],
      "accuracy":  "Model accuracy: ... (or null)"
    }
"""

import json
from pathlib import Path

import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from retrieval import HybridRetriever
from grade import extract_grade
from gate import disclaim, GRADE_LOOKAHEAD, DEFAULT_SIM_THRESHOLD
from llm import generate_answer

DEFAULT_DB = str(Path(__file__).resolve().parent / "data" / "chroma")
MODEL_NAME = "NeuML/pubmedbert-base-embeddings"
ACCURACY_PATH = str(Path(__file__).resolve().parent / "data" / "accuracy_results.json")

# load once at import / startup
_model = SentenceTransformer(MODEL_NAME)
_client = chromadb.PersistentClient(path=DEFAULT_DB)
_collection = _client.get_collection("guidelines")
_retriever = HybridRetriever(_collection, strategy="hybrid")

app = FastAPI(title="Medical RAG", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    k: int = 5
    strategy: str = "hybrid"
    use_llm: bool = True


def _accuracy_summary() -> str | None:
    try:
        with open(ACCURACY_PATH, encoding="utf-8") as f:
            data = json.load(f)
        n, correct, acc = data.get("n_questions"), data.get("n_correct"), data.get("accuracy")
        if n and acc is not None:
            return f"Model accuracy: {correct}/{n} = {acc * 100:.1f}% ({data.get('strategy')}, top-{data.get('top_k')})"
    except (OSError, json.JSONDecodeError, AttributeError):
        pass
    return None


@app.get("/health")
def health():
    return {"status": "ok", "collection": _collection.name, "n_chunks": _collection.count()}


@app.get("/", include_in_schema=False)
def index():
    return {"status": "ok"}


@app.post("/query")
def query(req: QueryRequest):
    if req.strategy != _retriever.strategy:
        _retriever.strategy = req.strategy

    qv = _model.encode([req.query], normalize_embeddings=True)[0]
    hits_full = _retriever.search(req.query, qv, max(req.k, GRADE_LOOKAHEAD))
    msg, reason = disclaim(req.query, hits_full, sim_threshold=DEFAULT_SIM_THRESHOLD)
    hits = hits_full[: req.k]

    message = msg or "No confident match found."
    if not msg:
        if req.use_llm:
            try:
                message = generate_answer(req.query, hits_full)
            except Exception as exc:  # noqa: BLE001 - surface but don't crash
                message = f"(LLM answer unavailable: {exc})"
        else:
            message = "Answer not generated (use_llm=false)."

    return {
        "query": req.query,
        "k": req.k,
        "strategy": req.strategy,
        "disclaimed": bool(msg),
        "reason": reason,
        "message": message,
        "hits": [
            {
                "rank": i,
                "similarity": round(sim, 4),
                "fused": round(fused, 4),
                "grade": meta.get("grade") or extract_grade(doc),
                "section": meta.get("heading"),
                "org": meta.get("org"),
                "text": doc[:1500],
            }
            for i, (_cid, sim, fused, doc, meta) in enumerate(hits, 1)
        ],
        "accuracy": _accuracy_summary(),
    }
