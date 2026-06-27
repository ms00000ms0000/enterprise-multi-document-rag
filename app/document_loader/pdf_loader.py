from pypdf import PdfReader

from app.document_loader.base_loader import BaseLoader


class PDFLoader(BaseLoader):

    def load(self, file_path: str):

        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            pages.append(
                {
                    "text": page.extract_text(),
                    "page": page_number,
                    "source": file_path,
                }
            )

        return pages