from app.logging.logger import app_logger

from app.retriever.retrieval_service import RetrievalService
from app.hybrid_search.hybrid_search_service import HybridSearchService
from app.reranker.rerank_service import RerankService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiService
from app.citation.citation_service import CitationService
from app.memory.conversation_memory import ConversationMemory


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

        self.memory = ConversationMemory(
            max_turns=5
        )

        app_logger.info(
            "Query pipeline initialized."
        )

    def run(
        self,
        query,
        top_k=5,
    ):

        try:

            app_logger.info(
                f"Received query: {query}"
            )

            search_results = self.hybrid_search.search(
                query=query,
                k=top_k,
            )

            fused_results = search_results["fused"]

            app_logger.info(
                f"Hybrid search returned {len(fused_results)} results."
            )

            reranked_results = self.reranker.process(
                query=query,
                results=fused_results,
            )

            app_logger.info(
                "Cross-encoder reranking completed."
            )

            final_results = reranked_results[:top_k]

            app_logger.info(
                f"Top {len(final_results)} results selected."
            )

            conversation_history = (
                self.memory.get_history()
            )

            app_logger.info(
                f"Conversation history contains {len(conversation_history)} turn(s)."
            )

            prompt = self.prompt_builder.build(
                query=query,
                search_results=final_results,
                conversation_history=conversation_history,
            )

            app_logger.info(
                "Prompt constructed successfully."
            )

            answer = self.gemini.generate(
                prompt
            )

            app_logger.info(
                "Gemini response generated."
            )

            self.memory.add(
                query,
                answer,
            )

            app_logger.info(
                "Conversation memory updated."
            )

            citations = self.citation_service.build(
                final_results
            )

            app_logger.info(
                f"{len(citations)} citation(s) generated."
            )

            return {
                "query": query,
                "answer": answer,
                "retrieved_chunks": final_results,
                "citations": citations,
                "prompt": prompt,
                "conversation_history": conversation_history,
            }

        except Exception:

            app_logger.exception(
                "Query pipeline execution failed."
            )

            raise