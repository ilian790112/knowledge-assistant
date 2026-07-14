from app.schemas.retrieved_chunk import RetrievedChunk
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
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a question.
        """

        return self.search_service.search(
            question=question,
            limit=limit,
        )