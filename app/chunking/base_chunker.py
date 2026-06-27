from abc import ABC, abstractmethod


class BaseChunker(ABC):

    @abstractmethod
    def split(self, documents):
        pass