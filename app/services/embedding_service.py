from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service responsible for generating embeddings using a single
    shared SentenceTransformer model.
    """

    _model: SentenceTransformer | None = None

    def __init__(self) -> None:
        if EmbeddingService._model is None:
            EmbeddingService._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        self.model = EmbeddingService._model

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """

        embedding = self.model.encode(
            text,
            show_progress_bar=False,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts in one batch.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
        )

        return embeddings.tolist()


# Singleton instance shared across the entire application.
embedding_service = EmbeddingService()