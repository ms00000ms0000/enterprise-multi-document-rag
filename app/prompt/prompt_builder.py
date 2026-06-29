class PromptBuilder:

    def build(
        self,
        query,
        search_results,
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

        prompt = f"""
You are an Enterprise Multi-Document RAG Assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, reply exactly:

I could not find this information in the uploaded documents.

Never make assumptions.

==========================
Context
==========================

{context}

==========================
Question
==========================

{query}

==========================
Answer
==========================
"""

        return prompt