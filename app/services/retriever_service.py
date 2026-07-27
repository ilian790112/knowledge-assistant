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

        chunks = self.search_service.search(
            question=question,
            limit=limit,
        )

        logger.info("=" * 80)
        logger.info("RETRIEVED CHUNKS")
        logger.info("=" * 80)
        logger.info("Question: %s", question)
        logger.info("Chunks found: %d", len(chunks))

        for index, chunk in enumerate(chunks, start=1):
            logger.info(
                "%d. %s (chunk=%d, score=%.4f)",
                index,
                chunk.filename,
                chunk.chunk_index,
                chunk.score,
            )

        logger.info("=" * 80)

        return chunks