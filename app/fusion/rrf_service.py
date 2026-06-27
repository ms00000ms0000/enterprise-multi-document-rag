from collections import defaultdict


class RRFService:

    def __init__(self, k=60):

        self.k = k

    def fuse(self, result_sets):

        scores = defaultdict(float)
        objects = {}

        for results in result_sets:

            for rank, result in enumerate(results, start=1):

                chunk = result["chunk"]

                key = (
                    chunk.source,
                    chunk.page,
                    chunk.text,
                )

                scores[key] += 1 / (self.k + rank)

                objects[key] = result

        fused = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            objects[key]
            for key, _ in fused
        ]