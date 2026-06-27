from app.embeddings.embedding_service import EmbeddingService


class VectorRetriever:

    def __init__(
        self,
        vector_service,
    ):

        self.vector_service = vector_service

        self.embedding_service = EmbeddingService()

    def retrieve(
        self,
        query,
        k=5,
    ):

        embedding = self.embedding_service.embedding_model.embed_query(
            query
        )

        return self.vector_service.search(
            embedding,
            k,
        )