from abc import ABC, abstractmethod


class DataFetcherABC(ABC):

    @abstractmethod
    def get(self, urls: list[str]):
        """"""