from dotenv import load_dotenv

import os

load_dotenv()


class Settings:

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    STORAGE_DIR = "storage"

    INDEX_PATH = os.path.join(
        STORAGE_DIR,
        "faiss.index",
    )

    CHUNKS_PATH = os.path.join(
        STORAGE_DIR,
        "chunks.pkl",
    )

    HASH_PATH = os.path.join(
        STORAGE_DIR,
        "document_hashes.json",
    )

    METADATA_PATH = os.path.join(
        STORAGE_DIR,
        "metadata.json",
    )


settings = Settings()