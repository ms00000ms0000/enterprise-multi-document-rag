from app.retriever.vector_retriever import VectorRetriever


class RetrievalService:

    def __init__(
        self,
        vector_service,
    ):

        self.retriever = VectorRetriever(
            vector_service
        )

    def retrieve(
        self,
        query,
        k=5,
    ):

        return self.retriever.retrieve(
            query,
            k,
        )