from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.embedding_service import EmbeddingService


class ReindexService:
    """Regenerates embeddings for chunks that do not have one."""

    def __init__(
        self,
        chunk_repository: DocumentChunkRepository,
        embedding_service: EmbeddingService,
        batch_size: int = 8,
    ) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0.")

        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service
        self.batch_size = batch_size

    def reindex_embeddings(self) -> int:
        """Regenerate missing embeddings in bounded batches."""

        updated = 0

        while True:
            chunks = self.chunk_repository.get_chunks_without_embeddings(
                limit=self.batch_size,
            )

            if not chunks:
                return updated

            embeddings = self.embedding_service.generate_embeddings(
                [chunk.content for chunk in chunks]
            )

            if len(embeddings) != len(chunks):
                raise RuntimeError(
                    "Embedding service returned a different number of embeddings."
                )

            for chunk, embedding in zip(chunks, embeddings, strict=True):
                chunk.embedding = embedding

            self.chunk_repository.commit()
            updated += len(chunks)
