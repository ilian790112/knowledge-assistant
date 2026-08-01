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
        Generate embeddings in batches instead of one at a time.
        """

        if not chunks:
            return []

        embeddings = self.embedding_service.generate_embeddings(chunks)

        results: list[EmbeddingResult] = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            results.append(
                EmbeddingResult(
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )
            )

        return results