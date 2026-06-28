from app.chunking.recursive_chunker import RecursiveChunker


class ChunkingService:

    def __init__(self):

        self.chunker = RecursiveChunker()

    def chunk_documents(
        self,
        documents,
    ):

        return self.chunker.split(
            documents
        )