from app.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
)


class RerankService:

    def __init__(self):

        self.reranker = CrossEncoderReranker()

    def process(
        self,
        query,
        results,
    ):

        return self.reranker.rerank(
            query,
            results,
        )