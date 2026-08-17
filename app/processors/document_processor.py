from collections.abc import Iterator
from itertools import chain

from app.core.logger import logger
from app.processors.chunk_processor import ChunkProcessor
from app.processors.embedding_processor import EmbeddingProcessor
from app.processors.indexing_processor import IndexingProcessor
from app.processors.ingestion_processor import IngestionProcessor
from app.schemas.processing import ProcessingResult


class DocumentProcessor:
    """
    Coordinates document ingestion, chunking, embedding, and indexing.

    The pipeline intentionally streams chunks and embeddings so large PDFs do
    not require the complete document representation to live in memory at once.
    """

    def __init__(
        self,
        ingestion_processor: IngestionProcessor,
        chunk_processor: ChunkProcessor,
        embedding_processor: EmbeddingProcessor,
        indexing_processor: IndexingProcessor,
    ) -> None:
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
        logger.info("Step 1: starting ingestion: %s", filename)

        saved_path, cleaned_text = self.ingestion_processor.ingest(
            temp_path=temp_path,
            filename=filename,
        )

        logger.info(
            "Step 1 complete: %d characters extracted",
            len(cleaned_text),
        )

        logger.info("Step 2: creating lazy chunk stream")

        chunk_iterator = iter(
            self.chunk_processor.process(cleaned_text)
        )
        first_chunk = next(chunk_iterator, None)

        if first_chunk is None:
            chunks: Iterator[str] = iter(())
            chunk_count = 0
        else:
            chunks = chain((first_chunk,), chunk_iterator)
            chunk_count = 1

        logger.info("First chunk prepared; indexing will stream the remainder")

        result = ProcessingResult(
            filename=filename,
            content_type=content_type,
            path=str(saved_path),
            status="processing",
            characters=len(cleaned_text),
            chunks=chunk_count,
            embedding_dimensions=0,
            embedding_preview=[],
            preview=first_chunk[:500] if first_chunk else "",
        )

        logger.info("Step 3: generating embeddings and saving chunks")

        embedding_results = self.embedding_processor.process(chunks)

        document = self.indexing_processor.process(
            result=result,
            embedding_results=embedding_results,
        )

        logger.info(
            "Document processing completed: id=%s filename=%s",
            document.id,
            filename,
        )

        return document
