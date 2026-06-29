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

            if key not in seen:

                seen.add(key)

                citations.append(
                    {
                        "source": source,
                        "page": page,
                    }
                )

        return citations