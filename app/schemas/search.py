from pydantic import BaseModel


class SearchRequest(BaseModel):
    question: str
    limit: int = 5

class SearchResponse(BaseModel):
    document_id: int
    chunk_index: int
    content: str