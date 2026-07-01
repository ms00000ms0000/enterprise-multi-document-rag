import streamlit as st


def render_metrics(
    metrics,
):

    if not metrics:

        return

    st.divider()

    st.subheader(
        "📊 Retrieval Metrics"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Hybrid Search",
            f"{metrics.get('retrieval_time', 0)} sec",
        )

        st.metric(
            "Prompt Build",
            f"{metrics.get('prompt_time', 0)} sec",
        )

        st.metric(
            "Retrieved Chunks",
            metrics.get(
                "retrieved_chunks",
                0,
            ),
        )

    with col2:

        st.metric(
            "Reranking",
            f"{metrics.get('rerank_time', 0)} sec",
        )

        st.metric(
            "Gemini",
            f"{metrics.get('llm_time', 0)} sec",
        )

        st.metric(
            "Final Chunks",
            metrics.get(
                "final_chunks",
                0,
            ),
        )

    with col3:

        st.metric(
            "Total Time",
            f"{metrics.get('total_time', 0)} sec",
        )

        if (
            metrics.get(
                "total_time",
                0,
            )
            <= 2
        ):

            status = "🟢 Excellent"

        elif (
            metrics.get(
                "total_time",
                0,
            )
            <= 5
        ):

            status = "🟡 Good"

        else:

            status = "🔴 Slow"

        st.metric(
            "Performance",
            status,
        )