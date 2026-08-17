from app.core.config import settings
from app.core.logger import logger
from app.services.search_service import SearchService


class RetrieverService:
    """Retrieves the most relevant chunks for a question."""

    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service

    def retrieve(
        self,
        question: str,
        limit: int | None = None,
    ):
        retrieval_limit = limit or settings.retrieval_limit

        logger.info(
            "Retrieving up to %d chunks for question",
            retrieval_limit,
        )

        chunks = self.search_service.search(
            question=question,
            limit=retrieval_limit,
        )

        logger.info("Retrieved %d chunks", len(chunks))
        return chunks
