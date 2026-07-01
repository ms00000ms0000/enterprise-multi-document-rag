import json

import streamlit as st


def _build_markdown(
    messages,
):

    lines = [
        "# Enterprise Multi-Document RAG Chat",
        "",
    ]

    for message in messages:

        role = (
            "User"
            if message["role"] == "user"
            else "Assistant"
        )

        lines.append(
            f"## {role}"
        )

        lines.append(
            message["content"]
        )

        lines.append("")

        citations = message.get(
            "citations",
            [],
        )

        if citations:

            lines.append(
                "**Sources**"
            )

            for citation in citations:

                lines.append(
                    f"- {citation['source']} (Page {citation['page']})"
                )

            lines.append("")

    return "\n".join(
        lines
    )


def _build_text(
    messages,
):

    lines = []

    for message in messages:

        role = (
            "USER"
            if message["role"] == "user"
            else "ASSISTANT"
        )

        lines.append(
            f"{role}:"
        )

        lines.append(
            message["content"]
        )

        lines.append("")

    return "\n".join(
        lines
    )


def render_downloads():

    if (
        "messages"
        not in st.session_state
    ):

        return

    messages = (
        st.session_state.messages
    )

    if not messages:

        return

    st.subheader(
        "📥 Export Conversation"
    )

    markdown_data = (
        _build_markdown(
            messages
        )
    )

    text_data = _build_text(
        messages
    )

    json_data = json.dumps(
        messages,
        indent=4,
        ensure_ascii=False,
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        st.download_button(

            "📄 Download Markdown",

            markdown_data,

            file_name="chat_history.md",

            mime="text/markdown",

            use_container_width=True,

        )

        st.download_button(

            "📝 Download TXT",

            text_data,

            file_name="chat_history.txt",

            mime="text/plain",

            use_container_width=True,

        )

    with col2:

        st.download_button(

            "💾 Download JSON",

            json_data,

            file_name="chat_history.json",

            mime="application/json",

            use_container_width=True,

        )

        if st.button(

            "🗑 Clear Chat",

            use_container_width=True,

        ):

            st.session_state.messages = []

            st.rerun()