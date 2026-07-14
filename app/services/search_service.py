from app.repositories.search_repository import SearchRepository
from app.schemas.retrieved_chunk import RetrievedChunk
from app.services.embedding_service import EmbeddingService


class SearchService:
    """
    Performs semantic document search.
    """

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
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Search for the most relevant document chunks.
        """

        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        return self.repository.search(
            query_embedding=query_embedding,
            limit=limit,
        )