from app.fusion.rrf_service import RRFService


class HybridSearchService:

    def __init__(
        self,
        bm25_service,
        vector_retriever,
    ):

        self.bm25 = bm25_service
        self.vector = vector_retriever
        self.rrf = RRFService()

    def search(
        self,
        query,
        k=5,
    ):

        # BM25 Retrieval
        bm25_results = self.bm25.search(
            query,
            k
        )

        # Vector Retrieval
        vector_results = self.vector.retrieve(
            query,
            k
        )

        # Reciprocal Rank Fusion
        fused_results = self.rrf.fuse(
            [
                bm25_results,
                vector_results,
            ]
        )

        return {
            "bm25": bm25_results,
            "vector": vector_results,
            "fused": fused_results,
        }