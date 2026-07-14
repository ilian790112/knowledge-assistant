from app.schemas.embedding_result import EmbeddingResult
from app.services.embedding_service import EmbeddingService


class EmbeddingProcessor:
    """
    Responsible for generating embeddings for document chunks.
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
        Generate an embedding for each text chunk.
        """

        results: list[EmbeddingResult] = []

        for index, chunk in enumerate(chunks):
            embedding = self.embedding_service.generate_embedding(chunk)

            results.append(
                EmbeddingResult(
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )
            )

        return results