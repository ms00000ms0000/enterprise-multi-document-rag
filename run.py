from pathlib import Path

from app.logging.logger import app_logger

from app.pipelines.index_pipeline import (
    IndexPipeline,
)
from app.pipelines.query_pipeline import (
    QueryPipeline,
)


def main():

    try:

        app_logger.info(
            "Application started."
        )

        print("=" * 60)
        print("Enterprise Multi-Document RAG Assistant")
        print("=" * 60)

        print("\nExample:")
        print("docs")
        print()

        folder_path = input(
            "Enter documents folder: "
        ).strip()

        if not folder_path:

            folder_path = "docs"

        if not Path(folder_path).exists():

            app_logger.error(
                f"Folder not found: {folder_path}"
            )

            print(
                f"\n❌ Folder not found: {folder_path}"
            )

            return

        print(
            "\nScanning documents..."
        )

        app_logger.info(
            f"Scanning folder: {folder_path}"
        )

        index_pipeline = IndexPipeline()

        index_result = index_pipeline.run(
            folder_path
        )

        print(
            "\n✅ Documents indexed successfully!"
        )

        app_logger.info(
            "Documents indexed successfully."
        )

        query_pipeline = QueryPipeline(
            vector_service=index_result[
                "vector_service"
            ],
            bm25_service=index_result[
                "bm25_service"
            ],
        )

        while True:

            query = input(
                "\nAsk a question (type 'exit' to quit): "
            ).strip()

            if query.lower() == "exit":

                app_logger.info(
                    "Application closed by user."
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

            app_logger.info(
                f"User Query: {query}"
            )

            print(
                "\nSearching...\n"
            )

            try:

                response = query_pipeline.run(
                    query=query,
                    top_k=5,
                )

            except Exception as error:

                app_logger.exception(
                    "Query processing failed."
                )

                print(
                    "\n❌ Failed to process your query."
                )

                print(
                    "Check logs/application.log for details."
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

            if not citations:

                print(
                    "No citations found."
                )

            else:

                for index, citation in enumerate(
                    citations,
                    start=1,
                ):

                    print(
                        f"{index}. "
                        f"{citation['source']} "
                        f"(Page {citation['page']})"
                    )

    except KeyboardInterrupt:

        app_logger.warning(
            "Application interrupted by user."
        )

        print(
            "\n\n⚠ Application interrupted."
        )

    except Exception:

        app_logger.exception(
            "Fatal application error."
        )

        print(
            "\n❌ Unexpected application error."
        )

        print(
            "See logs/application.log for details."
        )


if __name__ == "__main__":

    main()