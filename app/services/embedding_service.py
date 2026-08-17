from threading import Lock

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates embeddings with one lazily initialized CPU model.

    Lazy initialization keeps application startup lightweight and avoids loading
    the transformer model when an instance only serves document-management
    endpoints.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    _model: SentenceTransformer | None = None
    _model_lock = Lock()

    def __init__(self) -> None:
        # Model initialization is intentionally deferred until first use.
        pass

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            with cls._model_lock:
                if cls._model is None:
                    cls._model = SentenceTransformer(
                        cls.MODEL_NAME,
                        device="cpu",
                    )

        return cls._model

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """Generate an embedding for one piece of text."""

        embeddings = self.generate_embeddings([text])

        if not embeddings:
            return []

        return embeddings[0]

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate a small batch of embeddings."""

        if not texts:
            return []

        model = self._get_model()

        embeddings = model.encode(
            texts,
            batch_size=min(8, len(texts)),
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()


# Shared service object; the transformer itself is loaded only on first use.
embedding_service = EmbeddingService()
