import streamlit as st

from app.ui.components import (
    error_message,
)


def initialize_chat():

    if "messages" not in st.session_state:

        st.session_state.messages = []


def add_user_message(
    message,
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message,
        }
    )


def add_assistant_message(
    message,
    citations=None,
    metrics=None,
):

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message,
            "citations": citations or [],
            "metrics": metrics or {},
        }
    )


def clear_chat():

    st.session_state.messages = []


def render_chat(
    query_pipeline=None,
    top_k=5,
):

    initialize_chat()

    st.subheader(
        "💬 Chat"
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if (
                message["role"]
                == "assistant"
            ):

                citations = message.get(
                    "citations",
                    []
                )

                if citations:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for citation in citations:

                            st.write(
                                f"• {citation['source']} "
                                f"(Page {citation['page']})"
                            )

    prompt = st.chat_input(
        "Ask something about your documents..."
    )

    if not prompt:

        return

    add_user_message(
        prompt
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking..."
        ):

            try:

                if query_pipeline is None:

                    response = {

                        "answer": (
                            "QueryPipeline has not been connected yet."
                        ),

                        "citations": [],

                        "metrics": {},

                    }

                else:

                    response = (
                        query_pipeline.run(
                            query=prompt,
                            top_k=top_k,
                        )
                    )

                st.markdown(
                    response["answer"]
                )

                citations = response.get(
                    "citations",
                    []
                )

                if citations:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for citation in citations:

                            st.write(
                                f"• {citation['source']} "
                                f"(Page {citation['page']})"
                            )

                add_assistant_message(
                    response["answer"],
                    citations,
                    response.get(
                        "metrics",
                        {},
                    ),
                )

            except Exception as error:

                error_message(
                    str(error)
                )