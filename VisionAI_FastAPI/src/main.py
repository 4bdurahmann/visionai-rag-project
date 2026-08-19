"""
VisionAI Medical RAG - FastAPI application entry point.

Assembles the routes package into the ASGI app. Run from the ``src`` directory:

    ../rag/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000

Or, for a development reload loop:

    ../rag/bin/python -m uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Routes.QueryRoute import router as queryRouter, lifespan
from Routes.RootRoute import router as rootRouter

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

app.include_router(rootRouter)
app.include_router(queryRouter)