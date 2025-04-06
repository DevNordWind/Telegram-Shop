from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Base(ABC):

    @staticmethod
    @abstractmethod
    def build_key(*args) -> str:
        pass
