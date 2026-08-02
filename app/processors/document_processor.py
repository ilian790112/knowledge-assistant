from fastapi import UploadFile

from app.core.logger import logger
from app.processors.chunk_processor import ChunkProcessor
from app.processors.embedding_processor import EmbeddingProcessor
from app.processors.indexing_processor import IndexingProcessor
from app.processors.ingestion_processor import IngestionProcessor
from app.schemas.processing import ProcessingResult


class DocumentProcessor:
    """
    Coordinates the complete document processing pipeline.

    Pipeline:
        Save File
            ↓
        Extract Text
            ↓
        Chunk Text
            ↓
        Generate Embeddings
            ↓
        Store in Database
    """

    def __init__(
        self,
        ingestion_processor: IngestionProcessor,
        chunk_processor: ChunkProcessor,
        embedding_processor: EmbeddingProcessor,
        indexing_processor: IndexingProcessor,
    ):
        self.ingestion_processor = ingestion_processor
        self.chunk_processor = chunk_processor
        self.embedding_processor = embedding_processor
        self.indexing_processor = indexing_processor

    def process(
        self,
        temp_path: str,
        filename: str,
        content_type: str,
    ):
        """
        Execute the complete AI document processing pipeline.
        """

        logger.info("Step 1: Starting ingestion")

        saved_path, cleaned_text = self.ingestion_processor.ingest(
            temp_path=temp_path,
            filename=filename,
        )

        logger.info(
            "Step 1 complete: %d characters extracted",
            len(cleaned_text),
        )

        logger.info("Step 2: Chunking document")

        chunks = self.chunk_processor.process(cleaned_text)

        logger.info(
            "Step 2 complete: %d chunks created",
            len(chunks),
        )

        logger.info("Step 3: Generating embeddings")

        embedding_results = self.embedding_processor.process(chunks)

        logger.info(
            "Step 3 complete: %d embeddings generated",
            len(embedding_results),
        )

        logger.info("Step 4: Building processing result")

        result = ProcessingResult(
            filename=filename,
            content_type=content_type,
            path=str(saved_path),
            status="processed",
            characters=len(cleaned_text),
            chunks=len(chunks),
            embedding_dimensions=(
                len(embedding_results[0].embedding)
                if embedding_results
                else 0
            ),
            embedding_preview=(
                embedding_results[0].embedding[:10]
                if embedding_results
                else []
            ),
            preview=(
                embedding_results[0].content[:500]
                if embedding_results
                else ""
            ),
        )

        logger.info("Step 5: Saving document and chunks")

        document = self.indexing_processor.process(
            result=result,
            embedding_results=embedding_results,
        )

        logger.info(
            "Step 5 complete: Document saved with id=%s",
            document.id,
        )

        logger.info("Document processing completed successfully")

        return document