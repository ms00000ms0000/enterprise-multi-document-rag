import streamlit as st


def page_header(
    title="🤖 Enterprise Multi-Document RAG Assistant",
    subtitle=(
        "Upload multiple documents, ask questions, "
        "and receive AI-powered answers with citations."
    ),
):

    st.title(
        title
    )

    st.caption(
        subtitle
    )


def section_header(
    title,
):

    st.subheader(
        title
    )

    st.divider()


def info_card(
    title,
    value,
):

    st.metric(
        label=title,
        value=value,
    )


def success_message(
    message,
):

    st.success(
        message
    )


def error_message(
    message,
):

    st.error(
        message
    )


def warning_message(
    message,
):

    st.warning(
        message
    )


def status_badge(
    label,
    status=True,
):

    if status:

        st.success(
            f"✅ {label}"
        )

    else:

        st.error(
            f"❌ {label}"
        )


def empty_state():

    st.info(
        "Upload documents to begin chatting."
    )


def loading_spinner(
    message="Processing...",
):

    return st.spinner(
        message
    )