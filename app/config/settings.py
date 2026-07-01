from dotenv import load_dotenv

import os


load_dotenv()


class Settings:

    # ===========================
    # API Keys
    # ===========================

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    # ===========================
    # Models
    # ===========================

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    # ===========================
    # Retrieval
    # ===========================

    DEFAULT_TOP_K = int(
        os.getenv(
            "DEFAULT_TOP_K",
            5,
        )
    )

    MAX_CONVERSATION_TURNS = int(
        os.getenv(
            "MAX_CONVERSATION_TURNS",
            5,
        )
    )

    # ===========================
    # Storage
    # ===========================

    STORAGE_DIR = os.getenv(
        "STORAGE_DIR",
        "storage",
    )

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

    # ===========================
    # Logging
    # ===========================

    LOG_DIR = os.getenv(
        "LOG_DIR",
        "logs",
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    # ===========================
    # Validation
    # ===========================

    @classmethod
    def validate(cls):

        if not cls.GEMINI_API_KEY:

            raise ValueError(
                "GEMINI_API_KEY is missing in .env file."
            )


settings = Settings()