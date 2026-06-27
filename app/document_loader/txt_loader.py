from app.document_loader.base_loader import BaseLoader


class TXTLoader(BaseLoader):

    def load(self, file_path: str):

        with open(file_path, "r", encoding="utf-8") as f:

            text = f.read()

        return [
            {
                "text": text,
                "page": 1,
                "source": file_path,
            }
        ]