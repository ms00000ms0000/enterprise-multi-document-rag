from rank_bm25 import BM25Okapi


class BM25Service:

    def __init__(self):

        self.bm25 = None
        self.chunks = []

    def index(self, chunks):

        self.chunks = chunks

        tokenized = [
            chunk.text.lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, k=5):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.chunks),
            reverse=True,
            key=lambda x: x[0]
        )

        return ranked[:k]