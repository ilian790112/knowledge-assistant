from pydantic import BaseModel


class ProcessingResult(BaseModel):
    filename: str
    content_type: str
    path: str
    status: str
    characters: int
    chunks: int
    embedding_dimensions: int
    embedding_preview: list[float]
    preview: str