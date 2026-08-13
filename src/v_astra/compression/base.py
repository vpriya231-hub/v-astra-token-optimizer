from abc import ABC, abstractmethod


class Compressor(ABC):
    @abstractmethod
    def compress(self, content: str) -> str:
        raise NotImplementedError
