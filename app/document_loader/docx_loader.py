from docx import Document

from app.document_loader.base_loader import BaseLoader


class DOCXLoader(BaseLoader):

    def load(self, file_path: str):

        doc = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        return [
            {
                "text": text,
                "page": 1,
                "source": file_path,
            }
        ]