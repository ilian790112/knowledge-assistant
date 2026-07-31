from __future__ import annotations

from app.core.logger import logger
from app.services.search_service import SearchService


class RetrieverService:
    """
    Retrieves the most relevant document chunks for a question.
    """

    def __init__(
        self,
        search_service: SearchService,
    ) -> None:
        self.search_service = search_service

    def retrieve(
        self,
        question: str,
        limit: int = 3,
    ):
        """
        Retrieve the most relevant chunks for a question.
        """

        logger.info("=" * 80)
        logger.info("RETRIEVER")
        logger.info("=" * 80)
        logger.info("Question: %s", question)
        logger.info("Limit: %d", limit)

        chunks = self.search_service.search(
            question=question,
            limit=limit,
        )

        logger.info("Retrieved %d chunks", len(chunks))

        if not chunks:
            logger.warning("No relevant chunks found.")
            logger.info("=" * 80)
            return []

        for index, chunk in enumerate(chunks, start=1):
            logger.info(
                "[%d] document=%s chunk=%d score=%.4f",
                index,
                chunk.filename,
                chunk.chunk_index,
                chunk.score,
            )

            logger.info(
                "Preview: %s",
                chunk.content[:200].replace("\n", " "),
            )

        logger.info("=" * 80)

        return chunks