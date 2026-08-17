from collections.abc import Iterator

from app.schemas.embedding_result import EmbeddingResult
from app.services.embedding_service import EmbeddingService


class EmbeddingProcessor:
    """
    Generates embeddings in small batches while yielding results lazily.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        batch_size: int = 8,
    ) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0.")

        self.embedding_service = embedding_service
        self.batch_size = batch_size

    def process(
        self,
        chunks: Iterator[str],
    ) -> Iterator[EmbeddingResult]:
        """
        Generate embeddings without materializing the complete document.
        """

        batch: list[str] = []
        indices: list[int] = []

        for index, chunk in enumerate(chunks):
            batch.append(chunk)
            indices.append(index)

            if len(batch) >= self.batch_size:
                yield from self._embed_batch(batch, indices)
                batch.clear()
                indices.clear()

        if batch:
            yield from self._embed_batch(batch, indices)

    def _embed_batch(
        self,
        chunks: list[str],
        indices: list[int],
    ) -> Iterator[EmbeddingResult]:
        embeddings = self.embedding_service.generate_embeddings(chunks)

        if len(embeddings) != len(chunks):
            raise RuntimeError(
                "Embedding service returned a different number of embeddings."
            )

        for index, chunk, embedding in zip(
            indices,
            chunks,
            embeddings,
            strict=True,
        ):
            yield EmbeddingResult(
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )
