import os

from app.document_loader.pdf_loader import (
    PDFLoader,
)
from app.document_loader.docx_loader import (
    DOCXLoader,
)
from app.document_loader.txt_loader import (
    TXTLoader,
)


class LoaderFactory:

    _LOADERS = {

        ".pdf": PDFLoader,

        ".docx": DOCXLoader,

        ".txt": TXTLoader,

    }

    @classmethod
    def get_loader(
        cls,
        file_path,
    ):

        extension = os.path.splitext(
            file_path
        )[1].lower()

        loader = cls._LOADERS.get(
            extension
        )

        if loader is None:

            supported = ", ".join(

                sorted(
                    cls._LOADERS.keys()
                )

            )

            raise ValueError(

                f"Unsupported file type: "
                f"{extension}. "
                f"Supported types: {supported}"

            )

        return loader()

    @classmethod
    def supported_extensions(
        cls,
    ):

        return sorted(
            cls._LOADERS.keys()
        )

    @classmethod
    def register_loader(
        cls,
        extension,
        loader_class,
    ):

        cls._LOADERS[
            extension.lower()
        ] = loader_class