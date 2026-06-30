import hashlib
import json
from pathlib import Path


class DocumentHashService:

    def __init__(self, hash_file):

        self.hash_file = Path(hash_file)

    def calculate_hash(
        self,
        file_path,
    ):

        sha = hashlib.sha256()

        with open(
            file_path,
            "rb",
        ) as file:

            while True:

                data = file.read(8192)

                if not data:
                    break

                sha.update(data)

        return sha.hexdigest()

    def load_hashes(self):

        if not self.hash_file.exists():

            return {}

        with open(
            self.hash_file,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save_hashes(
        self,
        hashes,
    ):

        self.hash_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.hash_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                hashes,
                file,
                indent=4,
            )

    def has_changed(
        self,
        file_path,
    ):

        current_hash = self.calculate_hash(
            file_path
        )

        hashes = self.load_hashes()

        filename = Path(file_path).name

        saved_hash = hashes.get(
            filename
        )

        return current_hash != saved_hash

    def update_hash(
        self,
        file_path,
    ):

        hashes = self.load_hashes()

        filename = Path(file_path).name

        hashes[filename] = self.calculate_hash(
            file_path
        )

        self.save_hashes(
            hashes
        )