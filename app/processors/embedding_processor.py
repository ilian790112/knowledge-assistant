from collections.abc import Iterator

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
    ) -> Iterator[EmbeddingResult]:
        """
        Generate embeddings lazily, one chunk at a time.
        """

        for index, chunk in enumerate(chunks):
            embedding = self.embedding_service.generate_embedding(
                chunk,
            )

            yield EmbeddingResult(
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )