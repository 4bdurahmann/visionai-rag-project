"""Retrieved-source model for the query response."""

from pydantic import BaseModel


class HitModel(BaseModel):
    """A retrieved source chunk surfaced alongside the answer."""

    rank: int
    similarity: float
    grade: str | None = None
    section: str | None = None
    page: int | None = None
    org: str | None = None
    text: str
