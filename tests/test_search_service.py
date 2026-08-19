import unittest
from unittest.mock import MagicMock

from app.services.search_service import SearchService


class SearchServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.embedding_service = MagicMock()
        self.repository = MagicMock()
        self.service = SearchService(
            embedding_service=self.embedding_service,
            repository=self.repository,
        )

    def test_generates_embedding_and_passes_it_to_repository(self) -> None:
        embedding = [0.1, 0.2, 0.3]
        results = [MagicMock()]
        self.embedding_service.generate_embedding.return_value = embedding
        self.repository.search.return_value = results

        response = self.service.search("What is RAG?", limit=3)

        self.assertIs(response, results)
        self.embedding_service.generate_embedding.assert_called_once_with(
            "What is RAG?"
        )
        self.repository.search.assert_called_once_with(
            query_embedding=embedding,
            question="What is RAG?",
            limit=3,
        )

    def test_uses_configured_limit_when_limit_is_omitted(self) -> None:
        embedding = [0.4, 0.5]
        self.embedding_service.generate_embedding.return_value = embedding
        self.repository.search.return_value = []

        response = self.service.search("Question")

        self.assertEqual(response, [])
        self.repository.search.assert_called_once_with(
            query_embedding=embedding,
            question="Question",
            limit=5,
        )

    def test_returns_repository_results_unchanged(self) -> None:
        self.embedding_service.generate_embedding.return_value = [0.1]
        expected = [MagicMock(), MagicMock(), MagicMock()]
        self.repository.search.return_value = expected

        response = self.service.search("Question", limit=2)

        self.assertIs(response, expected)


if __name__ == "__main__":
    unittest.main()
