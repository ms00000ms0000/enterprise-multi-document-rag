from app.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)


class EmbeddingService:

    def __init__(self):

        self.embedding_model = SentenceTransformerEmbedding()

    def process(self, chunks):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        return embeddings