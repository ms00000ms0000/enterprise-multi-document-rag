from app.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.logging.logger import app_logger


class EmbeddingService:

    _embedding_model = None

    DEFAULT_BATCH_SIZE = 64

    def __init__(self):

        if EmbeddingService._embedding_model is None:

            app_logger.info(
                "Loading embedding model..."
            )

            EmbeddingService._embedding_model = (
                SentenceTransformerEmbedding()
            )

            app_logger.info(
                "Embedding model loaded successfully."
            )

        self.embedding_model = (
            EmbeddingService._embedding_model
        )

    def embed_documents(
        self,
        chunks,
        batch_size=None,
    ):

        if batch_size is None:

            batch_size = (
                self.DEFAULT_BATCH_SIZE
            )

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = []

        total = len(texts)

        app_logger.info(
            f"Generating embeddings for {total} chunks "
            f"(batch size={batch_size})."
        )

        for start in range(
            0,
            total,
            batch_size,
        ):

            end = min(
                start + batch_size,
                total,
            )

            batch = texts[start:end]

            batch_embeddings = (
                self.embedding_model.embed_documents(
                    batch
                )
            )

            embeddings.extend(
                batch_embeddings
            )

        app_logger.info(
            "Embedding generation completed."
        )

        return embeddings

    def embed_query(
        self,
        query,
    ):

        return (
            self.embedding_model.embed_query(
                query
            )
        )