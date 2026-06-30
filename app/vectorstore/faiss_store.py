import json
import os
import pickle

import faiss
import numpy as np


class FAISSStore:

    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.chunks = []

        self.metadata = {}

    def add(
        self,
        embeddings,
        chunks,
    ):

        embeddings = np.array(
            embeddings,
            dtype="float32",
        )

        self.index.add(
            embeddings
        )

        self.chunks.extend(
            chunks
        )

    def search(
        self,
        query_embedding,
        k=5,
    ):

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

            if idx == -1:
                continue

            results.append(
                {
                    "chunk": self.chunks[idx],
                    "score": float(distance),
                }
            )

        return results

    def save(
        self,
        index_path,
        chunks_path,
        metadata_path,
    ):

        os.makedirs(
            os.path.dirname(index_path),
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            index_path,
        )

        with open(
            chunks_path,
            "wb",
        ) as file:

            pickle.dump(
                self.chunks,
                file,
            )

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.metadata,
                file,
                indent=4,
            )

    def load(
        self,
        index_path,
        chunks_path,
        metadata_path,
    ):

        self.index = faiss.read_index(
            index_path
        )

        with open(
            chunks_path,
            "rb",
        ) as file:

            self.chunks = pickle.load(
                file
            )

        if os.path.exists(
            metadata_path
        ):

            with open(
                metadata_path,
                "r",
                encoding="utf-8",
            ) as file:

                self.metadata = json.load(
                    file
                )

        else:

            self.metadata = {}

    def exists(
        self,
        index_path,
        chunks_path,
    ):

        return (
            os.path.exists(index_path)
            and os.path.exists(chunks_path)
        )