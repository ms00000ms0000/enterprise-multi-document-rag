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

        if not results:
            return []

        pairs = [
            (
                query,
                result["chunk"]["text"],
            )
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for score, result in zip(
            scores,
            results,
        ):

            item = result.copy()
            item["score"] = float(score)
            reranked.append(item)

        reranked.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return reranked