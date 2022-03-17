from abc import ABC, abstractmethod
from typing import Collection

from pandas import DataFrame

from src.impermax.common.path_consts import TARGET_CSV
from src.impermax.services.web_scraper._dataclasses import ImxPair


class RepositoryInterface(ABC):
    @abstractmethod
    def save(self, data: list[list[ImxPair]]) -> None:
        ...

    @abstractmethod
    def find_by_ticker(self, key: str) -> DataFrame:
        """
        Finds by ticker where key IN ticker. Not strict.
        """

    @abstractmethod
    def find_by_tickers(self, *tickers) -> DataFrame:
        """
        Finds by tickers where key IN ticker. Not strict.
        """

    @abstractmethod
    def find_by_ticker_strict(self, key: str) -> DataFrame:
        """
        Finds by ticker where key == ticker. Strict.
        """

    @abstractmethod
    def find_by_tickers_strict(self, *tickers) -> DataFrame:
        """
        Find by tickers where key == ticker. Strict.
        """

    @abstractmethod
    def find_by_contract(self, contract: str) -> DataFrame:
        ...

    @abstractmethod
    def find_by_contracts(self, contracts: Collection[str]) -> DataFrame:
        ...

    @abstractmethod
    def find_all(self) -> DataFrame:
        ...

    @staticmethod
    def _create_output_dir() -> None:
        TARGET_CSV.mkdir(exist_ok=True, parents=True)
