from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    """
    Internal representation of a retrieved chunk.
    """

    chunk_id: int

    document_id: int

    filename: str

    chunk_index: int

    content: str

    score: float