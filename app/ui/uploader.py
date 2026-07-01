import shutil
from pathlib import Path

import streamlit as st

from app.ui.components import (
    success_message,
    error_message,
)

UPLOAD_DIR = Path(
    "uploaded_documents"
)


def save_uploaded_files(
    uploaded_files,
):

    UPLOAD_DIR.mkdir(
        exist_ok=True
    )

    saved_files = []

    for uploaded_file in uploaded_files:

        destination = (
            UPLOAD_DIR
            / uploaded_file.name
        )

        with open(
            destination,
            "wb",
        ) as file:

            shutil.copyfileobj(
                uploaded_file,
                file,
            )

        saved_files.append(
            str(destination)
        )

    return saved_files


def render_uploader():

    st.subheader(
        "📂 Upload Documents"
    )

    uploaded_files = st.file_uploader(

        label="",

        type=[
            "pdf",
            "docx",
            "txt",
        ],

        accept_multiple_files=True,

        help="Upload one or more supported documents.",

    )

    if not uploaded_files:

        st.info(
            "Upload PDF, DOCX or TXT files to begin."
        )

        return None

    with st.spinner(
        "Saving uploaded documents..."
    ):

        try:

            saved_files = (
                save_uploaded_files(
                    uploaded_files
                )
            )

            success_message(
                f"{len(saved_files)} document(s) uploaded successfully."
            )

            with st.expander(
                "Uploaded Files",
                expanded=True,
            ):

                for file in saved_files:

                    st.write(
                        f"📄 {Path(file).name}"
                    )

            return saved_files

        except Exception as error:

            error_message(
                str(error)
            )

            return None