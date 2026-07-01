import json
import os
import pickle

import faiss
import numpy as np

from app.logging.logger import app_logger


class FAISSStore:

    DEFAULT_BATCH_SIZE = 512

    def __init__(
        self,
        dimension,
    ):

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
        batch_size=None,
    ):

        if batch_size is None:

            batch_size = (
                self.DEFAULT_BATCH_SIZE
            )

        if len(
            embeddings
        ) != len(
            chunks
        ):

            raise ValueError(
                "Embeddings and chunks count do not match."
            )

        total = len(
            embeddings
        )

        if total == 0:

            app_logger.warning(
                "No embeddings supplied for indexing."
            )

            return

        app_logger.info(
            f"Adding {total} embeddings to FAISS "
            f"(batch size={batch_size})."
        )

        for start in range(
            0,
            total,
            batch_size,
        ):

            end = min(
                start + batch_size,
                total,
            )

            batch_embeddings = np.asarray(
                embeddings[start:end],
                dtype="float32",
            )

            self.index.add(
                batch_embeddings
            )

            self.chunks.extend(
                chunks[start:end]
            )

        app_logger.info(
            f"FAISS indexing completed. "
            f"Total vectors: {self.index.ntotal}"
        )

    def search(
        self,
        query_embedding,
        k=5,
    ):

        if self.index.ntotal == 0:

            app_logger.warning(
                "Search attempted on an empty FAISS index."
            )

            return []

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        k = min(
            k,
            self.index.ntotal,
        )

        distances, indices = (
            self.index.search(
                query_embedding,
                k,
            )
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
                    "score": float(
                        distance
                    ),
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
            os.path.dirname(
                index_path
            ),
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

        app_logger.info(
            "FAISS index saved successfully."
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

                self.metadata = (
                    json.load(
                        file
                    )
                )

        else:

            self.metadata = {}

        app_logger.info(
            f"Loaded FAISS index "
            f"({self.index.ntotal} vectors)."
        )

    def exists(
        self,
        index_path,
        chunks_path,
    ):

        return (

            os.path.exists(
                index_path
            )

            and

            os.path.exists(
                chunks_path
            )

        )

    # ----------------------------------
    # Statistics Helpers
    # ----------------------------------

    def total_vectors(
        self,
    ):

        return self.index.ntotal

    def total_chunks(
        self,
    ):

        return len(
            self.chunks
        )

    def embedding_dimension(
        self,
    ):

        return self.dimension

    def get_metadata(
        self,
    ):

        return self.metadata

    def is_empty(
        self,
    ):

        return (
            self.index.ntotal == 0
        )