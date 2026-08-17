from app.core.config import settings
from app.core.logger import logger
from app.repositories.search_repository import SearchRepository
from app.schemas.retrieved_chunk import RetrievedChunk
from app.services.embedding_service import EmbeddingService


class SearchService:
    """Coordinates query embedding and hybrid document search."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        repository: SearchRepository,
    ) -> None:
        self.embedding_service = embedding_service
        self.repository = repository

    def search(
        self,
        question: str,
        limit: int | None = None,
    ) -> list[RetrievedChunk]:
        retrieval_limit = limit or settings.retrieval_limit

        logger.info("Generating query embedding")
        query_embedding = self.embedding_service.generate_embedding(question)

        logger.info("Searching vector and full-text indexes")
        results = self.repository.search(
            query_embedding=query_embedding,
            question=question,
            limit=retrieval_limit,
        )

        logger.info("Search returned %d chunks", len(results))
        return results
