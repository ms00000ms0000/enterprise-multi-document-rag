from pathlib import Path
import os

from app.config.settings import settings
from app.logging.logger import app_logger


class StartupValidator:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
    }

    @staticmethod
    def validate(folder_path):

        StartupValidator.validate_api_key()

        StartupValidator.ensure_directories()

        StartupValidator.validate_document_folder(
            folder_path
        )

        StartupValidator.validate_documents(
            folder_path
        )

        app_logger.info(
            "Startup validation completed successfully."
        )

    @staticmethod
    def validate_api_key():

        if (
            not settings.GEMINI_API_KEY
            or settings.GEMINI_API_KEY.strip() == ""
        ):

            raise RuntimeError(
                "GEMINI_API_KEY is missing in .env"
            )

    @staticmethod
    def ensure_directories():

        os.makedirs(
            settings.STORAGE_DIR,
            exist_ok=True,
        )

        os.makedirs(
            "logs",
            exist_ok=True,
        )

    @staticmethod
    def validate_document_folder(
        folder_path,
    ):

        if not Path(folder_path).exists():

            raise FileNotFoundError(
                f"Folder not found: {folder_path}"
            )

    @staticmethod
    def validate_documents(
        folder_path,
    ):

        documents = []

        for extension in StartupValidator.SUPPORTED_EXTENSIONS:

            documents.extend(
                Path(folder_path).rglob(
                    f"*{extension}"
                )
            )

        if not documents:

            raise RuntimeError(
                "No supported documents found."
            )

        app_logger.info(
            f"Found {len(documents)} document(s)."
        )