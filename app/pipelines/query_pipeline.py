from app.retriever.retrieval_service import RetrievalService
from app.hybrid_search.hybrid_search_service import HybridSearchService
from app.reranker.rerank_service import RerankService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiService


class QueryPipeline:

    def __init__(
        self,
        vector_service,
        bm25_service,
    ):

        self.retrieval_service = RetrievalService(
            vector_service
        )

        self.hybrid_search = HybridSearchService(
            bm25_service,
            self.retrieval_service,
        )

        self.reranker = RerankService()

        self.prompt_builder = PromptBuilder()

        self.gemini = GeminiService()

    def run(
        self,
        query,
        top_k=5,
    ):

        # Hybrid Search
        search_results = self.hybrid_search.search(
            query=query,
            k=top_k,
        )

        # RRF Output
        fused_results = search_results["fused"]

        # Cross-Encoder Reranking
        reranked_results = self.reranker.process(
            query=query,
            results=fused_results,
        )

        # Keep only top results
        final_results = reranked_results[:top_k]

        # Build Prompt
        prompt = self.prompt_builder.build(
            query=query,
            search_results=final_results,
        )

        # Generate Answer
        answer = self.gemini.generate(
            prompt
        )

        return {
            "query": query,
            "answer": answer,
            "retrieved_chunks": final_results,
            "prompt": prompt,
        }