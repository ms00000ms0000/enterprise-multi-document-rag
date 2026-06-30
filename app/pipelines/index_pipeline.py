from app.config.settings import settings
from app.logging.logger import app_logger

from app.document_manager import DocumentManager
from app.document_loader.loader_factory import LoaderFactory
from app.chunking.chunking_service import ChunkingService
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_service import VectorService
from app.hybrid_search.bm25_service import BM25Service
from app.services.document_hash_service import (
    DocumentHashService,
)


class IndexPipeline:

    def __init__(self):

        self.document_manager = DocumentManager()

        self.loader_factory = LoaderFactory()

        self.chunking_service = ChunkingService()

        self.embedding_service = EmbeddingService()

        self.vector_service = None

        self.bm25_service = BM25Service()

        self.hash_service = DocumentHashService(
            settings.HASH_PATH
        )

    def run(
        self,
        folder_path,
    ):

        try:

            app_logger.info(
                f"Scanning folder: {folder_path}"
            )

            document_paths = self.document_manager.get_documents(
                folder_path
            )

            if not document_paths:

                app_logger.warning(
                    "No supported documents found."
                )

                raise FileNotFoundError(
                    "No supported documents found."
                )

            app_logger.info(
                f"Found {len(document_paths)} document(s)."
            )

            rebuild_required = False

            for path in document_paths:

                if self.hash_service.has_changed(
                    path
                ):

                    rebuild_required = True

                    app_logger.info(
                        f"Detected changes in: {path}"
                    )

                    break

            all_documents = []

            for path in document_paths:

                app_logger.info(
                    f"Loading document: {path}"
                )

                loader = self.loader_factory.get_loader(
                    path
                )

                docs = loader.load(
                    path
                )

                all_documents.extend(
                    docs
                )

            app_logger.info(
                f"Loaded {len(all_documents)} pages."
            )

            chunks = self.chunking_service.chunk_documents(
                all_documents
            )

            app_logger.info(
                f"Created {len(chunks)} chunks."
            )

            embeddings = self.embedding_service.embed_documents(
                chunks
            )

            dimension = len(
                embeddings[0]
            )

            app_logger.info(
                f"Embedding dimension: {dimension}"
            )

            self.vector_service = VectorService(
                dimension
            )

            index_exists = self.vector_service.exists(
                settings.INDEX_PATH,
                settings.CHUNKS_PATH,
            )

            if (
                index_exists
                and not rebuild_required
            ):

                app_logger.info(
                    "Loading existing FAISS index."
                )

                print(
                    "📂 Loading existing FAISS index..."
                )

                self.vector_service.load(
                    settings.INDEX_PATH,
                    settings.CHUNKS_PATH,
                    settings.METADATA_PATH,
                )

                self.bm25_service.index(
                    self.vector_service.store.chunks
                )

                app_logger.info(
                    "Existing index loaded successfully."
                )

                return {
                    "vector_service": self.vector_service,
                    "bm25_service": self.bm25_service,
                    "chunks": self.vector_service.store.chunks,
                }

            if rebuild_required:

                print(
                    "\n📄 Document changes detected."
                )

                print(
                    "♻ Rebuilding FAISS index..."
                )

                app_logger.info(
                    "Rebuilding FAISS index."
                )

            else:

                print(
                    "\n🛠 Building new FAISS index..."
                )

                app_logger.info(
                    "Creating new FAISS index."
                )

            self.vector_service.index_documents(
                embeddings,
                chunks,
            )

            self.vector_service.store.metadata = {

                "documents": [

                    {
                        "file": path,
                    }

                    for path in document_paths
                ],

                "total_chunks": len(chunks),

                "embedding_dimension": dimension,

            }

            self.vector_service.save(
                settings.INDEX_PATH,
                settings.CHUNKS_PATH,
                settings.METADATA_PATH,
            )

            for path in document_paths:

                self.hash_service.update_hash(
                    path
                )

            app_logger.info(
                "Hashes updated."
            )

            print(
                "\n💾 FAISS index saved."
            )

            app_logger.info(
                "FAISS index saved successfully."
            )

            self.bm25_service.index(
                chunks
            )

            app_logger.info(
                "BM25 index built successfully."
            )

            return {

                "vector_service": self.vector_service,

                "bm25_service": self.bm25_service,

                "chunks": chunks,

            }

        except Exception:

            app_logger.exception(
                "Index pipeline failed."
            )

            raise