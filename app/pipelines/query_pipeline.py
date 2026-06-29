from app.retriever.retrieval_service import RetrievalService
from app.hybrid_search.hybrid_search_service import HybridSearchService
from app.reranker.rerank_service import RerankService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiService
from app.citation.citation_service import CitationService


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

        self.citation_service = CitationService()

    def run(
        self,
        query,
        top_k=5,
    ):

        search_results = self.hybrid_search.search(
            query=query,
            k=top_k,
        )

        fused_results = search_results["fused"]

        reranked_results = self.reranker.process(
            query=query,
            results=fused_results,
        )

        final_results = reranked_results[:top_k]

        prompt = self.prompt_builder.build(
            query=query,
            search_results=final_results,
        )

        answer = self.gemini.generate(
            prompt
        )

        citations = self.citation_service.build(
            final_results
        )

        return {
            "query": query,
            "answer": answer,
            "retrieved_chunks": final_results,
            "citations": citations,
            "prompt": prompt,
        }