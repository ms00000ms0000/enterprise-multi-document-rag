from pathlib import Path


class DocumentManager:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
    }

    def get_documents(
        self,
        folder_path,
    ):

        folder = Path(folder_path)

        if not folder.exists():

            raise FileNotFoundError(
                f"{folder_path} does not exist."
            )

        documents = []

        for file in sorted(
            folder.iterdir()
        ):

            if (
                file.is_file()
                and file.suffix.lower()
                in self.SUPPORTED_EXTENSIONS
            ):

                documents.append(
                    str(file)
                )

        if not documents:

            raise ValueError(
                "No supported documents found."
            )

        return documents