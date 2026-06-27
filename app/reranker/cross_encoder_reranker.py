from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        results,
    ):

        pairs = [
            (query, result["chunk"].text)
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        reranked = sorted(
            zip(scores, results),
            reverse=True,
            key=lambda x: x[0]
        )

        return [
            result
            for score, result in reranked
        ]