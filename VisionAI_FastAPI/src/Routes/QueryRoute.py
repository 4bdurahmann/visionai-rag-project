"""HTTP API query routes: retrieval + gating + LLM generation + quality scoring."""

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from controllers.queryControllers import QueryRequest
from controllers.responseControllers import QueryResponse
from modules.engine import get_engine
from modules.pipeline import answer_query, score_from_cache

router = APIRouter()


class ScoreRequest(BaseModel):
    request_id: str


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Warm the embedding model + Chroma collection once on boot."""
    from core import config

    engine = get_engine()
    print(
        f"[visionai] engine ready: {engine.collection.name} "
        f"({engine.collection.count()} chunks, model={config.MODEL_NAME})"
    )
    yield


@router.get("/health")
def health() -> dict:
    from core import config

    engine = get_engine()
    return {
        "status": "ok",
        "model": config.MODEL_NAME,
        "collection": engine.collection.name,
        "n_chunks": engine.collection.count(),
    }


@router.post("/query")
@router.post("/query/")
def query(req: QueryRequest) -> QueryResponse:
    """Process a medical query (trailing slash tolerated, never 500s)."""
    try:
        result = answer_query(
            req.query,
            k=req.k,
            strategy=req.strategy,
            use_llm=req.use_llm,
            score=req.score,
        )
    except Exception as exc:  # noqa: BLE001 - graceful degradation, never 500
        result = {
            "query": req.query,
            "k": req.k,
            "strategy": req.strategy,
            "disclaimed": True,
            "reason": "internal_error",
            "message": f"(Query pipeline failed: {exc})",
            "hits": [],
            "quality": None,
            "request_id": None,
            "accuracy": None,
            "error": f"pipeline: {exc}",
        }
    return QueryResponse(**result)


@router.post("/query/score")
@router.post("/query/score/")
def query_score(req: ScoreRequest) -> dict:
    """Compute quality for an answer returned with score=false."""
    try:
        return score_from_cache(req.request_id)
    except Exception as exc:  # noqa: BLE001 - never 500
        return {"request_id": req.request_id, "quality": None, "status": f"error: {exc}"}