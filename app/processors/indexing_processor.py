from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.schemas.embedding_result import EmbeddingResult
from app.schemas.processing import ProcessingResult


class IndexingProcessor:
    """
    Persists processed documents and chunks.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository

    def process(
        self,
        result: ProcessingResult,
        embedding_results: list[EmbeddingResult],
    ):
        """
        Save document and all chunks.
        """

        document = self.document_repository.save(result)

        chunks = [
            DocumentChunk(
                document_id=document.id,
                chunk_index=item.chunk_index,
                content=item.content,
                embedding=item.embedding,
            )
            for item in embedding_results
        ]

        self.chunk_repository.save_many(chunks)

        return document