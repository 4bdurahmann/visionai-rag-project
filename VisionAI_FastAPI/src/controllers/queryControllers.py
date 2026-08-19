"""Request schema for the query endpoint."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Body of a POST /query request."""

    query: str
    k: int = 5
    strategy: str = "hybrid"
    use_llm: bool = True
