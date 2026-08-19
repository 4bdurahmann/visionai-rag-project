"""Response schemas for the query endpoint."""

from pydantic import BaseModel

from controllers.hitControllers import HitModel


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
    hits: list[HitModel] = []
    quality: QualityReport | None = None
    accuracy: str | None = None
    error: str | None = None
