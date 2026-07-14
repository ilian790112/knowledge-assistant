from pydantic import BaseModel


class EmbeddingResult(BaseModel):
    """
    Represents a text chunk together with its embedding.
    """

    chunk_index: int

    content: str

    embedding: list[float]