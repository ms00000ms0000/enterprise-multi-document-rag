import argparse

from app.config.settings import settings
from app.logging.logger import app_logger

from app.pipelines.index_pipeline import (
    IndexPipeline,
)
from app.pipelines.query_pipeline import (
    QueryPipeline,
)
from app.session.session_manager import (
    SessionManager,
)
from app.utils.startup_validator import (
    StartupValidator,
)


def build_argument_parser():

    parser = argparse.ArgumentParser(
        description="Enterprise Multi-Document RAG Assistant"
    )

    parser.add_argument(
        "--docs",
        type=str,
        default=None,
        help="Documents folder",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=settings.DEFAULT_TOP_K,
        help="Number of retrieved chunks",
    )

    return parser


def print_banner():

    print("=" * 60)
    print("Enterprise Multi-Document RAG Assistant")
    print("=" * 60)

    print("\nExample:")
    print("python run.py --docs docs")
    print()


def main():

    try:

        app_logger.info(
            "Application started."
        )

        settings.validate()

        parser = build_argument_parser()

        args = parser.parse_args()

        print_banner()

        folder_path = args.docs

        if not folder_path:

            folder_path = input(
                "Enter documents folder: "
            ).strip()

        if not folder_path:

            folder_path = "docs"

        try:

            StartupValidator.validate(
                folder_path
            )

        except Exception as error:

            app_logger.exception(
                "Startup validation failed."
            )

            print(
                f"\n❌ {error}"
            )

            return

        top_k = args.top_k

        app_logger.info(
            f"Folder : {folder_path}"
        )

        app_logger.info(
            f"Top K  : {top_k}"
        )

        print(
            "\nScanning documents..."
        )

        index_pipeline = IndexPipeline()

        index_result = index_pipeline.run(
            folder_path
        )

        print(
            "\n✅ Documents indexed successfully!"
        )

        query_pipeline = QueryPipeline(
            vector_service=index_result[
                "vector_service"
            ],
            bm25_service=index_result[
                "bm25_service"
            ],
        )

        session = SessionManager()

        print("\nSession Started")
        print("-" * 60)
        print(
            f"Session ID : {session.session_id}"
        )

        while True:

            query = input(
                "\nAsk a question (type 'exit' to quit): "
            ).strip()

            if query.lower() == "exit":

                app_logger.info(
                    "Application closed."
                )

                print(
                    "\n👋 Goodbye!"
                )

                break

            if not query:

                print(
                    "\n⚠ Please enter a question."
                )

                continue

            print(
                "\nSearching...\n"
            )

            try:

                response = query_pipeline.run(
                    query=query,
                    top_k=top_k,
                )

                session.increment_queries()

            except Exception:

                app_logger.exception(
                    "Query failed."
                )

                print(
                    "\n❌ Failed to process query."
                )

                continue

            print("=" * 60)
            print("Answer")
            print("=" * 60)

            print(
                response["answer"]
            )

            print("\n" + "=" * 60)
            print("Sources")
            print("=" * 60)

            citations = response[
                "citations"
            ]

            if citations:

                for i, citation in enumerate(
                    citations,
                    start=1,
                ):

                    print(
                        f"{i}. "
                        f"{citation['source']} "
                        f"(Page {citation['page']})"
                    )

            else:

                print(
                    "No citations found."
                )

            metrics = response[
                "metrics"
            ]

            print("\n" + "=" * 60)
            print("Performance")
            print("=" * 60)

            print(
                f"Hybrid Search : {metrics['retrieval_time']} sec"
            )

            print(
                f"Reranking     : {metrics['rerank_time']} sec"
            )

            print(
                f"Prompt Build  : {metrics['prompt_time']} sec"
            )

            print(
                f"Gemini        : {metrics['llm_time']} sec"
            )

            print(
                f"Total Time    : {metrics['total_time']} sec"
            )

            print(
                f"Retrieved     : {metrics['retrieved_chunks']} chunks"
            )

            print(
                f"Final         : {metrics['final_chunks']} chunks"
            )

            print("\n" + "=" * 60)
            print("Session Information")
            print("=" * 60)

            session_info = session.get_info()

            print(
                f"Session ID    : {session_info['session_id']}"
            )

            print(
                f"Queries Asked : {session_info['queries']}"
            )

            print(
                f"Uptime        : {session_info['uptime_seconds']} sec"
            )

    except KeyboardInterrupt:

        app_logger.warning(
            "Application interrupted."
        )

        print(
            "\n\nApplication interrupted."
        )

    except Exception:

        app_logger.exception(
            "Fatal application error."
        )

        print(
            "\nUnexpected application error."
        )


if __name__ == "__main__":

    main()