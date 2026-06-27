from app.vectorstore.faiss_store import FAISSStore


class VectorService:

    def __init__(self, dimension):

        self.store = FAISSStore(dimension)

    def index_documents(
        self,
        embeddings,
        chunks,
    ):

        self.store.add(
            embeddings,
            chunks,
        )

    def search(
        self,
        query_embedding,
        k=5,
    ):

        return self.store.search(
            query_embedding,
            k,
        )