class HybridSearchService:

    def __init__(
        self,
        bm25_service,
        vector_retriever,
    ):

        self.bm25 = bm25_service
        self.vector = vector_retriever

    def search(
        self,
        query,
        k=5,
    ):

        bm25_results = self.bm25.search(
            query,
            k
        )

        vector_results = self.vector.retrieve(
            query,
            k
        )

        return {
            "bm25": bm25_results,
            "vector": vector_results,
        }