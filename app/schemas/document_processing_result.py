from pydantic import BaseModel

from app.schemas.document_metadata import DocumentMetadata
from app.schemas.embedding_result import EmbeddingResult


class DocumentProcessingResult(BaseModel):
    """
    Complete result of the AI pipeline.
    """

    metadata: DocumentMetadata

    characters: int

    chunks: list[EmbeddingResult]