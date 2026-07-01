import time

from app.config.settings import settings
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

        self.vector_service = (
            vector_service
        )

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
            max_turns=settings.MAX_CONVERSATION_TURNS
        )

        app_logger.info(
            "Query pipeline initialized."
        )

    def run(
        self,
        query,
        top_k=None,
    ):

        try:

            if top_k is None:

                top_k = settings.DEFAULT_TOP_K

            pipeline_start = (
                time.perf_counter()
            )

            app_logger.info(
                f"Received query: {query}"
            )

            # --------------------------
            # Hybrid Retrieval
            # --------------------------

            retrieval_start = (
                time.perf_counter()
            )

            search_results = (
                self.hybrid_search.search(
                    query=query,
                    k=top_k,
                )
            )

            retrieval_time = (
                time.perf_counter()
                - retrieval_start
            )

            bm25_results = (
                search_results["bm25"]
            )

            vector_results = (
                search_results["vector"]
            )

            fused_results = (
                search_results["fused"]
            )

            app_logger.info(
                f"Hybrid search returned "
                f"{len(fused_results)} results."
            )

            # --------------------------
            # Reranking
            # --------------------------

            rerank_start = (
                time.perf_counter()
            )

            reranked_results = (
                self.reranker.process(
                    query=query,
                    results=fused_results,
                )
            )

            rerank_time = (
                time.perf_counter()
                - rerank_start
            )

            final_results = (
                reranked_results[:top_k]
            )

            # --------------------------
            # Conversation History
            # --------------------------

            conversation_history = (
                self.memory.get_history()
            )

            # --------------------------
            # Prompt Building
            # --------------------------

            prompt_start = (
                time.perf_counter()
            )

            prompt = (
                self.prompt_builder.build(
                    query=query,
                    search_results=final_results,
                    conversation_history=conversation_history,
                )
            )

            prompt_time = (
                time.perf_counter()
                - prompt_start
            )

            # --------------------------
            # Gemini
            # --------------------------

            llm_start = (
                time.perf_counter()
            )

            answer = (
                self.gemini.generate(
                    prompt
                )
            )

            llm_time = (
                time.perf_counter()
                - llm_start
            )

            self.memory.add(
                query,
                answer,
            )

            citations = (
                self.citation_service.build(
                    final_results
                )
            )

            total_time = (
                time.perf_counter()
                - pipeline_start
            )

            # --------------------------
            # Retrieval Statistics
            # --------------------------

            index_stats = (
                self.vector_service.get_statistics()
            )

            metrics = {

                # Performance

                "retrieval_time": round(
                    retrieval_time,
                    3,
                ),

                "rerank_time": round(
                    rerank_time,
                    3,
                ),

                "prompt_time": round(
                    prompt_time,
                    3,
                ),

                "llm_time": round(
                    llm_time,
                    3,
                ),

                "total_time": round(
                    total_time,
                    3,
                ),

                # Retrieval Counts

                "bm25_results": len(
                    bm25_results
                ),

                "vector_results": len(
                    vector_results
                ),

                "fused_results": len(
                    fused_results
                ),

                "reranked_results": len(
                    reranked_results
                ),

                "final_chunks": len(
                    final_results
                ),

                # Index Statistics

                "documents": index_stats[
                    "documents"
                ],

                "pages": index_stats[
                    "pages"
                ],

                "chunks": index_stats[
                    "chunks"
                ],

                "embedding_dimension": index_stats[
                    "dimension"
                ],

                "indexed_vectors": index_stats[
                    "vectors"
                ],
            }

            app_logger.info(
                f"Pipeline Metrics: {metrics}"
            )

            return {

                "query": query,

                "answer": answer,

                "retrieved_chunks": final_results,

                "citations": citations,

                "prompt": prompt,

                "conversation_history": conversation_history,

                "metrics": metrics,
            }

        except Exception:

            app_logger.exception(
                "Query pipeline execution failed."
            )

            raise