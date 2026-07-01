import time

from app.fusion.rrf_service import (
    RRFService,
)
from app.logging.logger import (
    app_logger,
)


class HybridSearchService:

    def __init__(
        self,
        bm25_service,
        vector_retriever,
    ):

        self.bm25 = bm25_service

        self.vector = vector_retriever

        self.rrf = RRFService()

        app_logger.info(
            "HybridSearchService initialized."
        )

    def search(
        self,
        query,
        k=5,
    ):

        if not query.strip():

            raise ValueError(
                "Query cannot be empty."
            )

        start_time = (
            time.perf_counter()
        )

        # --------------------------
        # BM25 Retrieval
        # --------------------------

        bm25_results = self.bm25.search(
            query,
            k,
        )

        # --------------------------
        # Vector Retrieval
        # --------------------------

        vector_results = (
            self.vector.retrieve(
                query,
                k,
            )
        )

        # --------------------------
        # Reciprocal Rank Fusion
        # --------------------------

        fused_results = self.rrf.fuse(
            [
                bm25_results,
                vector_results,
            ]
        )

        elapsed = round(
            time.perf_counter()
            - start_time,
            3,
        )

        app_logger.info(
            f"Hybrid search completed "
            f"(BM25={len(bm25_results)}, "
            f"Vector={len(vector_results)}, "
            f"Fused={len(fused_results)}, "
            f"{elapsed}s)"
        )

        return {

            "bm25": bm25_results,

            "vector": vector_results,

            "fused": fused_results,

            "hybrid_time": elapsed,

        }