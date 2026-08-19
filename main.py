"""
VisionAI Medical RAG - FastAPI application entry point.

Assembles the routes package into the ASGI app. Run from the project root:

    rag/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000

Or, for a development reload loop:

    rag/bin/python -m uvicorn main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules import config


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Warm the embedding model + Chroma collection once on boot."""
    from modules.engine import get_engine

    engine = get_engine()
    print(
        f"[visionai] engine ready: {engine.collection.name} "
        f"({engine.collection.count()} chunks, model={config.MODEL_NAME})"
    )
    yield


app = FastAPI(
    title="VisionAI Medical RAG",
    description=(
        "Cited question-answering over the USPSTF behavioral-counseling "
        "guideline: hybrid retrieval, confidence gating, LLM generation, and "
        "per-answer faithfulness / citation-quality scoring."
    ),
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.api import router  # noqa: E402 - must come after app creation

app.include_router(router)