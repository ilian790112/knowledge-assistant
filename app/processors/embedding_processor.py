from app.schemas.embedding_result import EmbeddingResult
from app.services.embedding_service import EmbeddingService


class EmbeddingProcessor:
    """
    Generates embeddings for document chunks.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
        self.embedding_service = embedding_service

    def process(
        self,
        chunks: list[str],
    ) -> list[EmbeddingResult]:
        """
        Generate embeddings for all chunks in one batch.
        """

        if not chunks:
            return []

        embeddings = self.embedding_service.generate_embeddings(chunks)

        return [
            EmbeddingResult(
                chunk_index=i,
                content=chunk,
                embedding=embedding,
            )
            for i, (chunk, embedding) in enumerate(
                zip(chunks, embeddings, strict=True)
            )
        ]