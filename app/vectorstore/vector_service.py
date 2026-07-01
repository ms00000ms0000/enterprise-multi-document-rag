from app.logging.logger import app_logger

from app.vectorstore.faiss_store import (
    FAISSStore,
)


class VectorService:

    def __init__(
        self,
        dimension,
    ):

        self.store = FAISSStore(
            dimension
        )

        app_logger.info(
            f"VectorService initialized "
            f"(dimension={dimension})."
        )

    def index_documents(
        self,
        embeddings,
        chunks,
    ):

        if len(
            embeddings
        ) != len(
            chunks
        ):

            raise ValueError(
                "Embeddings and chunks count do not match."
            )

        app_logger.info(
            f"Indexing {len(chunks)} chunks."
        )

        self.store.add(
            embeddings,
            chunks,
        )

        app_logger.info(
            "Vector indexing completed."
        )

    def search(
        self,
        query_embedding,
        k=5,
    ):

        if (
            query_embedding is None
        ):

            app_logger.warning(
                "Query embedding is None."
            )

            return []

        return self.store.search(
            query_embedding,
            k,
        )

    def save(
        self,
        index_path,
        chunks_path,
        metadata_path,
    ):

        self.store.save(
            index_path,
            chunks_path,
            metadata_path,
        )

        app_logger.info(
            "Vector index saved."
        )

    def load(
        self,
        index_path,
        chunks_path,
        metadata_path,
    ):

        self.store.load(
            index_path,
            chunks_path,
            metadata_path,
        )

        app_logger.info(
            "Vector index loaded."
        )

    def exists(
        self,
        index_path,
        chunks_path,
    ):

        return self.store.exists(
            index_path,
            chunks_path,
        )

    # ----------------------------------
    # Retrieval Statistics
    # ----------------------------------

    def get_statistics(
        self,
    ):

        metadata = (
            self.store.metadata
        )

        return {

            "documents": metadata.get(
                "total_documents",
                0,
            ),

            "pages": metadata.get(
                "total_pages",
                0,
            ),

            "chunks": metadata.get(
                "total_chunks",
                len(
                    self.store.chunks
                ),
            ),

            "dimension": metadata.get(
                "embedding_dimension",
                self.store.dimension,
            ),

            "vectors": metadata.get(
                "indexed_vectors",
                self.store.total_vectors(),
            ),

        }