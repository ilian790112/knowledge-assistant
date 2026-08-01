from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service responsible for generating embeddings.
    """

    _model = None

    def __init__(self):
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
        Generate a single embedding.
        """

        return self.model.encode(text).tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings in batch.
        """

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
        )

        return embeddings.tolist()