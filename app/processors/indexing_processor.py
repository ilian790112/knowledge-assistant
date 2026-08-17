from collections.abc import Iterator

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
    Persists a document and streams its chunks into PostgreSQL in batches.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        batch_size: int = 32,
    ) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0.")

        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.batch_size = batch_size

    def process(
        self,
        result: ProcessingResult,
        embedding_results: Iterator[EmbeddingResult],
    ):
        """
        Save the document first, then stream embeddings into batch inserts.
        """

        document = self.document_repository.save(result)
        batch: list[DocumentChunk] = []
        chunk_count = 0

        try:
            for item in embedding_results:
                if result.embedding_dimensions == 0:
                    result.embedding_dimensions = len(item.embedding)
                    result.embedding_preview = item.embedding[:10]

                batch.append(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=item.chunk_index,
                        content=item.content,
                        embedding=item.embedding,
                    )
                )
                chunk_count += 1

                if len(batch) >= self.batch_size:
                    self.chunk_repository.save_many(batch)
                    batch.clear()

            if batch:
                self.chunk_repository.save_many(batch)

            result.chunks = chunk_count
            self.document_repository.update_status(
                document.id,
                "processed",
            )

            return document

        except Exception:
            self.document_repository.update_status(
                document.id,
                "failed",
            )
            raise
