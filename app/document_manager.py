from pathlib import Path

from app.document_loader.loader_factory import (
    LoaderFactory,
)


class DocumentManager:

    def __init__(self):

        self.supported_extensions = {

            extension.lower()

            for extension in LoaderFactory.supported_extensions()

        }

    def get_documents(
        self,
        folder_path,
    ):

        folder = Path(
            folder_path
        )

        if not folder.exists():

            raise FileNotFoundError(
                f"{folder_path} does not exist."
            )

        if not folder.is_dir():

            raise NotADirectoryError(
                f"{folder_path} is not a directory."
            )

        documents = [

            str(file)

            for file in sorted(
                folder.iterdir()
            )

            if (
                file.is_file()
                and file.suffix.lower()
                in self.supported_extensions
            )

        ]

        if not documents:

            raise ValueError(
                "No supported documents found."
            )

        return documents

    def supported_extensions_list(
        self,
    ):

        return sorted(
            self.supported_extensions
        )

    def is_supported(
        self,
        file_path,
    ):

        return (

            Path(
                file_path
            ).suffix.lower()

            in self.supported_extensions

        )