import streamlit as st

from app.ui.components import (
    section_header,
    info_card,
)


def render_sidebar(
    session_info=None,
):

    with st.sidebar:

        st.header(
            "📊 Session Dashboard"
        )

        st.divider()

        if session_info is None:

            session_info = {}

        documents = session_info.get(
            "documents",
            []
        )

        info_card(
            "Documents",
            len(documents),
        )

        info_card(
            "Chunks",
            session_info.get(
                "chunks",
                0,
            ),
        )

        info_card(
            "Embedding Model",
            session_info.get(
                "embedding_model",
                "Unknown",
            ),
        )

        info_card(
            "Vector Dimension",
            session_info.get(
                "dimension",
                "-",
            ),
        )

        info_card(
            "Conversation Turns",
            session_info.get(
                "conversation_turns",
                0,
            ),
        )

        st.divider()

        section_header(
            "Uploaded Documents"
        )

        if documents:

            for document in documents:

                st.markdown(
                    f"📄 {document}"
                )

        else:

            st.caption(
                "No documents indexed."
            )

        st.divider()

        section_header(
            "Retrieval Settings"
        )

        st.write(
            f"**Top K:** {session_info.get('top_k', '-')}"
        )

        st.write(
            f"**Hybrid Search:** Enabled"
        )

        st.write(
            f"**Reranking:** Enabled"
        )

        st.write(
            f"**Conversation Memory:** Enabled"
        )

        st.divider()

        section_header(
            "About"
        )

        st.caption(
            """
Enterprise Multi-Document RAG Assistant

• FAISS Vector Search

• BM25 Retrieval

• Reciprocal Rank Fusion

• Cross-Encoder Reranker

• Gemini 2.5 Flash

• Multi-Document QA
"""
        )