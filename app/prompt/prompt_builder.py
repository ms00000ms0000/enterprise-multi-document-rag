class PromptBuilder:

    def build(
        self,
        query,
        search_results,
        conversation_history,
    ):

        context_parts = []

        for result in search_results:

            chunk = result["chunk"]

            context_parts.append(
                f"""
Source: {chunk['source']}
Page: {chunk['page']}

{chunk['text']}
"""
            )

        context = "\n\n-------------------------\n\n".join(
            context_parts
        )

        history_parts = []

        for turn in conversation_history:

            history_parts.append(
                f"""
User:
{turn['question']}

Assistant:
{turn['answer']}
"""
            )

        history = "\n".join(
            history_parts
        )

        prompt = f"""
You are an Enterprise Multi-Document RAG Assistant.

Use the previous conversation only when it is relevant.

Answer ONLY from the provided document context.

If the answer is not present in the context, reply exactly:

I could not find this information in the uploaded documents.

Never make assumptions.

==========================
Conversation History
==========================

{history}

==========================
Retrieved Context
==========================

{context}

==========================
Current Question
==========================

{query}

==========================
Answer
==========================
"""

        return prompt