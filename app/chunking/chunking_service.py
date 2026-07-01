from app.chunking.recursive_chunker import (
    RecursiveChunker,
)

from app.logging.logger import (
    app_logger,
)


class ChunkingService:

    def __init__(self):

        self.chunker = (
            RecursiveChunker()
        )

        app_logger.info(
            "Chunking service initialized."
        )

    def chunk_documents(
        self,
        documents,
    ):

        if not documents:

            app_logger.warning(
                "No documents received for chunking."
            )

            return []

        app_logger.info(
            f"Chunking {len(documents)} document(s)."
        )

        chunks = self.chunker.split(
            documents
        )

        app_logger.info(
            f"Generated {len(chunks)} chunk(s)."
        )

        return chunks