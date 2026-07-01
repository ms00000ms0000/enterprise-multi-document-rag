from sentence_transformers import SentenceTransformer

from app.embeddings.base_embedding import BaseEmbedding


class SentenceTransformerEmbedding(BaseEmbedding):

    _model = None

    def __init__(self):

        if (
            SentenceTransformerEmbedding._model
            is None
        ):

            SentenceTransformerEmbedding._model = (
                SentenceTransformer(
                    "sentence-transformers/all-MiniLM-L6-v2"
                )
            )

        self.model = (
            SentenceTransformerEmbedding._model
        )

        self.query_cache = {}

    def embed_documents(
        self,
        texts,
    ):

        return self.model.encode(
            texts,
            convert_to_numpy=True,
        )

    def embed_query(
        self,
        text,
    ):

        text = text.strip()

        if text in self.query_cache:

            return self.query_cache[text]

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        self.query_cache[text] = embedding

        return embedding

    def clear_cache(self):

        self.query_cache.clear()