"""
HTTP API routes.

Exposes the retrieval + gating + LLM-generate + quality-scoring pipeline (see
controllers/query.py) as a JSON API for other devices on the network.

Run from the project root:
    rag/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000

Then e.g.:
    curl -X POST http://<host>:8000/query \
         -H 'Content-Type: application/json' \
         -d '{"query":"What does the USPSTF recommend?","k":5}'

Endpoints:
    GET  /health   -> {"status": "ok", "collection": ..., "n_chunks": ...}
    POST /query    -> JSON answer with retrieval hits + quality report
    POST /query/   -> same as above (trailing slash tolerated, no redirect)
"""

from fastapi import APIRouter

from controllers.query import answer_query
from modules import config
from modules.engine import get_engine
from modules.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.get("/health")
def health() -> dict:
    engine = get_engine()
    return {
        "status": "ok",
        "model": config.MODEL_NAME,
        "collection": engine.collection.name,
        "n_chunks": engine.collection.count(),
    }


@router.get("/", include_in_schema=False)
def index() -> dict:
    return {"status": "ok"}


@router.post("/query")
@router.post("/query/")
def query(req: QueryRequest) -> QueryResponse:
    result = answer_query(
        req.query,
        k=req.k,
        strategy=req.strategy,
        use_llm=req.use_llm,
    )
    return QueryResponse(**result)