from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.schemas.embedding_result import EmbeddingResult
from app.schemas.processing import ProcessingResult


class IndexingProcessor:
    """
    Responsible for persisting processed documents and chunks.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository

    def process(
        self,
        result: ProcessingResult,
        embedding_results: list[EmbeddingResult],
    ):
        """
        Save the document and all of its chunks.
        """

        # Save document metadata
        document = self.document_repository.save(result)

        # Build chunk entities
        chunk_entities = [
            DocumentChunk(
                document_id=document.id,
                chunk_index=item.chunk_index,
                content=item.content,
                embedding=item.embedding,
            )
            for item in embedding_results
        ]

        # Save all chunks
        self.chunk_repository.save_many(chunk_entities)

        return document