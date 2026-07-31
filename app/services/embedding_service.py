from sentence_transformers import SentenceTransformer

from app.core.logger import logger


class EmbeddingService:
    """
    Generates sentence embeddings using a single shared model.
    """

    def __init__(self) -> None:
        logger.info("Loading SentenceTransformer model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        logger.info("SentenceTransformer loaded.")

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()


# Singleton instance used throughout the application.
embedding_service = EmbeddingService()