class CitationService:

    def build(
        self,
        search_results,
    ):

        citations = []

        seen = set()

        for result in search_results:

            chunk = result["chunk"]

            source = chunk.get(
                "source",
                "Unknown"
            )

            page = chunk.get(
                "page",
                "N/A"
            )

            key = (
                source,
                page,
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            citations.append(
                {
                    "source": source,
                    "page": page,
                }
            )

        return citations

    # ----------------------------------
    # Statistics
    # ----------------------------------

    def total_sources(
        self,
        citations,
    ):

        return len(
            citations
        )

    def unique_documents(
        self,
        citations,
    ):

        return len(

            {

                citation["source"]

                for citation in citations

            }

        )

    def get_statistics(
        self,
        citations,
    ):

        return {

            "total_sources": self.total_sources(
                citations
            ),

            "unique_documents": self.unique_documents(
                citations
            ),

        }