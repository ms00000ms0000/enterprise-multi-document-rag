import os

from app.document_loader.pdf_loader import PDFLoader
from app.document_loader.docx_loader import DOCXLoader
from app.document_loader.txt_loader import TXTLoader


class LoaderFactory:

    @staticmethod
    def get_loader(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFLoader()

        if extension == ".docx":
            return DOCXLoader()

        if extension == ".txt":
            return TXTLoader()

        raise ValueError(f"Unsupported file type: {extension}")