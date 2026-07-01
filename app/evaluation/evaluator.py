from app.evaluation.metrics import (
    RetrievalMetrics,
)


class Evaluator:

    def evaluate(
        self,
        expected_source,
        retrieved_results,
    ):

        retrieved_sources = [

            result["chunk"]["source"]

            for result in retrieved_results

        ]

        return {

            "Hit@K": RetrievalMetrics.hit_at_k(
                retrieved_sources,
                expected_source,
            ),

            "Precision@K": round(
                RetrievalMetrics.precision_at_k(
                    retrieved_sources,
                    expected_source,
                ),
                3,
            ),

            "Recall@K": round(
                RetrievalMetrics.recall_at_k(
                    retrieved_sources,
                    expected_source,
                ),
                3,
            ),

            "MRR": round(
                RetrievalMetrics.reciprocal_rank(
                    retrieved_sources,
                    expected_source,
                ),
                3,
            ),
        }