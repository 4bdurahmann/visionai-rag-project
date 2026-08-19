"""Pydantic request/response schemas for the HTTP API."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Body of a POST /query request."""

    query: str
    k: int = 5
    strategy: str = "hybrid"
    use_llm: bool = True


class Hit(BaseModel):
    """A retrieved source chunk surfaced alongside the answer."""

    rank: int
    similarity: float
    grade: str | None = None
    section: str | None = None
    page: int | None = None
    org: str | None = None
    text: str


class QualityReport(BaseModel):
    """Per-answer faithfulness / citation checks (null when not applicable)."""

    faithfulness: float | None = None
    citation_accuracy: float | None = None
    unsupported_claims: list[str] = []
    bad_citations: list[dict] = []


class QueryResponse(BaseModel):
    """Shape returned by POST /query."""

    query: str
    k: int
    strategy: str
    disclaimed: bool
    reason: str
    message: str
    hits: list[Hit] = []
    quality: QualityReport | None = None
    accuracy: str | None = None
    error: str | None = None