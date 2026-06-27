from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.chunking.base_chunker import BaseChunker


class RecursiveChunker(BaseChunker):

    def __init__(
        self,
        chunk_size=700,
        chunk_overlap=100,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(self, documents):

        chunks = []

        for document in documents:

            texts = self.splitter.split_text(
                document["text"]
            )

            for chunk in texts:

                chunks.append(
                    {
                        "text": chunk,
                        "page": document["page"],
                        "source": document["source"],
                    }
                )

        return chunks