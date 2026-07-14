from pydantic import BaseModel

from app.schemas.source import Source


class ChatResponse(BaseModel):
    """
    Response returned by the RAG pipeline.
    """

    answer: str

    sources: list[Source]