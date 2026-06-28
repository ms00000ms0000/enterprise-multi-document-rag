from app.document_loader.loader_factory import LoaderFactory
from app.chunking.chunking_service import ChunkingService
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_service import VectorService
from app.hybrid_search.bm25_service import BM25Service


class IndexPipeline:

    def __init__(self):

        self.loader_factory = LoaderFactory()

        self.chunking_service = ChunkingService()

        self.embedding_service = EmbeddingService()

        self.vector_service = None

        self.bm25_service = BM25Service()

    def run(
        self,
        file_path,
    ):

        loader = self.loader_factory.get_loader(
            file_path
        )

        documents = loader.load(
            file_path
        )

        chunks = self.chunking_service.chunk_documents(
            documents
        )

        embeddings = self.embedding_service.embed_documents(
            chunks
        )

        dimension = len(
            embeddings[0]
        )

        self.vector_service = VectorService(
            dimension
        )

        self.vector_service.index_documents(
            embeddings,
            chunks,
        )

        self.bm25_service.index(
            chunks
        )

        return {
            "vector_service": self.vector_service,
            "bm25_service": self.bm25_service,
            "chunks": chunks,
        }