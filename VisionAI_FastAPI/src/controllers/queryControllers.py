"""Request schema for the query endpoint."""

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """Body of a POST /query request."""

    query: str = Field(description="The medical question to answer.")
    k: int = Field(default=5, ge=1, le=20, description="Number of retrieved chunks to return (1-20).")
    strategy: str = Field(default="hybrid", description="Retrieval strategy: hybrid or vector.")
    use_llm: bool = Field(default=True, description="Generate an LLM answer when the gates pass.")
    score: bool = Field(default=True, description="Compute quality inline; when false, return fast with a request_id for /query/score.")

    @field_validator("query")
    @classmethod
    def _query_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("query must not be blank")
        return v.strip()
