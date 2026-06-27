import faiss
import numpy as np


class FAISSStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)

        self.chunks = []

    def add(self, embeddings, chunks):

        embeddings = np.array(
            embeddings,
            dtype="float32",
        )

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    def search(self, query_embedding, k=5):

        query_embedding = np.array(
            [query_embedding],
            dtype="float32",
        )

        distances, indices = self.index.search(
            query_embedding,
            k,
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0],
        ):

            results.append(
                {
                    "chunk": self.chunks[idx],
                    "score": float(distance),
                }
            )

        return results