class RetrievalMetrics:

    @staticmethod
    def hit_at_k(
        retrieved_sources,
        expected_source,
    ):

        return expected_source in retrieved_sources

    @staticmethod
    def precision_at_k(
        retrieved_sources,
        expected_source,
    ):

        if not retrieved_sources:

            return 0.0

        relevant = sum(
            1
            for source in retrieved_sources
            if source == expected_source
        )

        return relevant / len(
            retrieved_sources
        )

    @staticmethod
    def recall_at_k(
        retrieved_sources,
        expected_source,
    ):

        return (
            1.0
            if expected_source in retrieved_sources
            else 0.0
        )

    @staticmethod
    def reciprocal_rank(
        retrieved_sources,
        expected_source,
    ):

        for index, source in enumerate(
            retrieved_sources,
            start=1,
        ):

            if source == expected_source:

                return 1 / index

        return 0.0