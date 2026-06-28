from pathlib import Path

from docx import Document

from app.pipelines.index_pipeline import IndexPipeline
from app.pipelines.query_pipeline import QueryPipeline


def main():

    print("=" * 60)
    print("Enterprise Multi-Document RAG Assistant")
    print("=" * 60)

    print("\nExample:")
    print("docs/company_policy.pdf")
    print()

    file_path = input(
        "Enter document path: "
    ).strip()

    if not Path(file_path).exists():
        print(f"\n❌ File not found: {file_path}")
        return

    print("\nIndexing document...\n")

    index_pipeline = IndexPipeline()

    index_result = index_pipeline.run(
        file_path
    )

    print("\n✅ Document indexed successfully!")

    query_pipeline = QueryPipeline(
        vector_service=index_result["vector_service"],
        bm25_service=index_result["bm25_service"],
    )

    while True:

        query = input(
            "\nAsk a question (type 'exit' to quit): "
        ).strip()

        if query.lower() == "exit":
            print("\n👋 Goodbye!")
            break

        print("\nSearching...\n")

        response = query_pipeline.run(
            query=query,
            top_k=5,
        )

        print("=" * 60)
        print("Answer")
        print("=" * 60)

        print(response["answer"])


if __name__ == "__main__":
    main()