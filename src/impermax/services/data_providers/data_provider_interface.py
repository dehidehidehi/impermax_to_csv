from abc import ABC, abstractmethod

from src.impermax.services.data_providers.web_scraper._dataclasses import ImxPair


class DataProviderInterface(ABC):

    @abstractmethod
    def get(self, urls: list[str]) -> list[list[ImxPair]]:
        """"""