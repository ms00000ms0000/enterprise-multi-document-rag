import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import hashlib
import streamlit as st

from app.pipelines.index_pipeline import (
    IndexPipeline,
)
from app.pipelines.query_pipeline import (
    QueryPipeline,
)

from app.ui.sidebar import (
    render_sidebar,
)

from app.ui.uploader import (
    render_uploader,
)

from app.ui.chat import (
    render_chat,
)

from app.ui.metrics import (
    render_metrics,
)

from app.ui.downloads import (
    render_downloads,
)

from app.ui.components import (
    page_header,
    success_message,
    error_message,
)

st.set_page_config(
    page_title="Enterprise Multi-Document RAG",
    page_icon="📚",
    layout="wide",
)


def initialize_session():

    defaults = {

        "query_pipeline": None,

        "metrics": {},

        "documents_loaded": False,

        "uploaded_signature": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


def generate_signature(
    uploaded_files,
):

    hasher = hashlib.md5()

    for file_path in sorted(uploaded_files):

        path = Path(file_path)

        hasher.update(
            path.name.encode("utf-8")
        )

        with open(
            path,
            "rb",
        ) as file:

            hasher.update(
                file.read()
            )

    return hasher.hexdigest()


def build_pipeline(
    uploaded_files,
):

    with st.spinner(
        "Indexing documents..."
    ):

        index_pipeline = IndexPipeline()

        result = index_pipeline.run(
            "uploaded_documents"
        )

        query_pipeline = QueryPipeline(
            vector_service=result[
                "vector_service"
            ],
            bm25_service=result[
                "bm25_service"
            ],
        )

    st.session_state.query_pipeline = (
        query_pipeline
    )

    st.session_state.documents_loaded = True

    success_message(
        "Documents indexed successfully."
    )


def main():

    initialize_session()

    page_header()

    render_sidebar()

    uploaded_files = render_uploader()

    if uploaded_files:

        current_signature = (
            generate_signature(
                uploaded_files
            )
        )

        if (
            st.session_state.uploaded_signature
            != current_signature
        ):

            try:

                build_pipeline(
                    uploaded_files
                )

                st.session_state.uploaded_signature = (
                    current_signature
                )

            except Exception as error:

                error_message(
                    str(error)
                )

    render_chat(
        query_pipeline=st.session_state.query_pipeline
    )

    if st.session_state.metrics:

        render_metrics(
            st.session_state.metrics
        )

    render_downloads()


if __name__ == "__main__":

    main()