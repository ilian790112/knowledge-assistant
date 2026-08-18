import sys
import types
import unittest
from unittest.mock import MagicMock, patch


# The embedding model is an optional runtime dependency for these unit tests.
# Stub the module so importing EmbeddingService does not download/load PyTorch.
_sentence_transformers = types.ModuleType("sentence_transformers")
_sentence_transformers.SentenceTransformer = object
sys.modules.setdefault("sentence_transformers", _sentence_transformers)

from app.services.embedding_service import EmbeddingService


class EmbeddingServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = EmbeddingService()
        EmbeddingService._model = None

    def tearDown(self) -> None:
        EmbeddingService._model = None

    def test_empty_batch_returns_empty_list_without_loading_model(self) -> None:
        with patch.object(EmbeddingService, "_get_model") as get_model:
            result = self.service.generate_embeddings([])

        self.assertEqual(result, [])
        get_model.assert_not_called()

    def test_generate_embedding_uses_batch_method(self) -> None:
        with patch.object(
            self.service,
            "generate_embeddings",
            return_value=[[0.1, 0.2, 0.3]],
        ) as generate_embeddings:
            result = self.service.generate_embedding("hello")

        self.assertEqual(result, [0.1, 0.2, 0.3])
        generate_embeddings.assert_called_once_with(["hello"])

    def test_generate_embedding_returns_empty_for_empty_result(self) -> None:
        with patch.object(
            self.service,
            "generate_embeddings",
            return_value=[],
        ):
            self.assertEqual(self.service.generate_embedding("hello"), [])

    def test_generate_embeddings_configures_small_normalized_cpu_batch(self) -> None:
        model = MagicMock()
        model.encode.return_value = MagicMock(
            tolist=lambda: [[0.6, 0.8], [0.0, 1.0]]
        )

        with patch.object(EmbeddingService, "_get_model", return_value=model):
            result = self.service.generate_embeddings(["one", "two"])

        self.assertEqual(result, [[0.6, 0.8], [0.0, 1.0]])
        model.encode.assert_called_once_with(
            ["one", "two"],
            batch_size=2,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )


if __name__ == "__main__":
    unittest.main()
