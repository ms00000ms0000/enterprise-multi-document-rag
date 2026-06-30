from collections import deque


class ConversationMemory:

    def __init__(
        self,
        max_turns=5,
    ):

        self.max_turns = max_turns

        self.memory = deque(
            maxlen=max_turns
        )

    def add(
        self,
        question,
        answer,
    ):

        self.memory.append(
            {
                "question": question,
                "answer": answer,
            }
        )

    def get_history(self):

        return list(
            self.memory
        )

    def clear(self):

        self.memory.clear()