from pydantic import BaseModel


class Source(BaseModel):
    """
    Source metadata returned to the client.
    """

    document_id: int

    filename: str

    chunk_id: int

    chunk_index: int

    score: float