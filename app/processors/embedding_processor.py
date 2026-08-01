import time

from app.core.logger import logger
from app.schemas.embedding_result import EmbeddingResult
from app.services.embedding_service import EmbeddingService


class EmbeddingProcessor:
    """
    Generates embeddings for document chunks.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service

    def process(
        self,
        chunks: list[str],
    ) -> list[EmbeddingResult]:
        """
        Generate embeddings for all chunks.
        """

        logger.info("=" * 80)
        logger.info("EMBEDDING PROCESSOR START")
        logger.info("Chunks to embed: %d", len(chunks))
        logger.info("=" * 80)

        start = time.perf_counter()

        results: list[EmbeddingResult] = []

        for index, chunk in enumerate(chunks):
            chunk_start = time.perf_counter()

            logger.info(
                "Embedding chunk %d/%d (%d characters)",
                index + 1,
                len(chunks),
                len(chunk),
            )

            embedding = self.embedding_service.generate_embedding(
                chunk
            )

            results.append(
                EmbeddingResult(
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )
            )

            logger.info(
                "Chunk %d embedded in %.2f seconds",
                index + 1,
                time.perf_counter() - chunk_start,
            )

        logger.info(
            "Generated %d embeddings in %.2f seconds",
            len(results),
            time.perf_counter() - start,
        )

        logger.info("=" * 80)
        logger.info("EMBEDDING PROCESSOR END")
        logger.info("=" * 80)

        return results