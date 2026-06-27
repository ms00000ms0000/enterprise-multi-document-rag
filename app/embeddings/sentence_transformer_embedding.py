from sentence_transformers import SentenceTransformer

from app.embeddings.base_embedding import BaseEmbedding


class SentenceTransformerEmbedding(BaseEmbedding):

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, texts):

        return self.model.encode(
            texts,
            convert_to_numpy=True,
        )

    def embed_query(self, text):

        return self.model.encode(
            text,
            convert_to_numpy=True,
        )