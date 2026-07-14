from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.embedding_service import EmbeddingService


class ReindexService:
    """
    Regenerates embeddings for document chunks that don't have one.
    """

    def __init__(
        self,
        chunk_repository: DocumentChunkRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service

    def reindex_embeddings(self) -> int:
        """
        Generate embeddings for all chunks with NULL embeddings.

        Returns:
            Number of updated chunks.
        """

        chunks = self.chunk_repository.get_chunks_without_embeddings()

        if not chunks:
            return 0

        for chunk in chunks:
            chunk.embedding = self.embedding_service.generate_embedding(
                chunk.content
            )

        self.chunk_repository.commit()

        return len(chunks)