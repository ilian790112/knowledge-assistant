import unittest
from unittest.mock import MagicMock

from app.services.retriever_service import RetrieverService


class RetrieverServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.search_service = MagicMock()
        self.service = RetrieverService(self.search_service)

    def test_uses_configured_limit_by_default(self) -> None:
        results = [MagicMock(), MagicMock()]
        self.search_service.search.return_value = results

        response = self.service.retrieve("What is RAG?")

        self.assertIs(response, results)
        self.search_service.search.assert_called_once_with(
            question="What is RAG?",
            limit=5,
        )

    def test_explicit_limit_overrides_configured_limit(self) -> None:
        results = [MagicMock()]
        self.search_service.search.return_value = results

        response = self.service.retrieve("Question", limit=2)

        self.assertIs(response, results)
        self.search_service.search.assert_called_once_with(
            question="Question",
            limit=2,
        )

    def test_empty_search_results_are_returned_unchanged(self) -> None:
        self.search_service.search.return_value = []

        response = self.service.retrieve("Question", limit=3)

        self.assertEqual(response, [])
        self.search_service.search.assert_called_once_with(
            question="Question",
            limit=3,
        )


if __name__ == "__main__":
    unittest.main()
