import csv
import logging
from functools import cached_property
from typing import Optional, Collection

from pandas import DataFrame

from src.impermax.common.path_consts import TARGET_CSV
from src.impermax.repositories.csv.csv_repository_helper import _CsvRepositoryHelper
from src.impermax.repositories.repository_interface import RepositoryInterface
from src.impermax.services.web_scraper._dataclasses import ImxPair

logger = logging.getLogger(__name__)


class CsvRepository(RepositoryInterface, _CsvRepositoryHelper):


    def __init__(self, file_name: Optional[str] = None):
        self.file_name = file_name or self.mk_file_name()

    @cached_property
    def all_csv_data(self) -> DataFrame:
        csv_df = self.load_all_csvs()
        csv_df['ticker'] = csv_df['ticker'].str.upper()  # required for pairs with mixed upper/lowercase like 'IMX.m'
        return csv_df

    def find_all(self) -> DataFrame:
        return self.all_csv_data

    def find_by_ticker(self, ticker: str) -> DataFrame:
        ticker = ticker.upper()
        return self.all_csv_data[self.all_csv_data["ticker"].str.contains(ticker)]

    def find_by_tickers(self, *tickers) -> DataFrame:
        tickers = {t.upper() for t in tickers}
        return self.all_csv_data[self.all_csv_data['ticker'].str.contains('|'.join(tickers))]

    def find_by_ticker_strict(self, ticker: str) -> DataFrame:
        ticker = ticker.upper()
        return self.all_csv_data[self.all_csv_data["ticker"].isin({ticker})]

    def find_by_tickers_strict(self, *tickers) -> DataFrame:
        tickers = {t.upper() for t in tickers}
        return self.all_csv_data[self.all_csv_data['ticker'].isin(tickers)]

    def find_by_contract(self, contract: str) -> DataFrame:
        contract = contract.lower()
        return self.all_csv_data[
            self.all_csv_data["contract"].str.lower().isin({contract})
        ]

    def find_by_contracts(self, *contracts) -> DataFrame:
        contracts = {c.lower() for c in contracts}
        return self.all_csv_data[
            self.all_csv_data["contract"].str.lower().isin(contracts)
        ]

    def save(self, data: list[list[ImxPair]]) -> None:
        self._save_as_csv(self.file_name, data)
        self._assert_csv_exists(self.file_name)

    def _save_as_csv(self, file_name: str, pairs: list[list[ImxPair]]) -> None:
        self._create_output_dir()
        full_file_path = TARGET_CSV / file_name
        with open(
            str(full_file_path), mode="w+", encoding="UTF-8", newline="\n"
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    "blockchain",
                    "pair",
                    "dex",
                    "ticker",
                    "supply",
                    "supply_apr",
                    "borrowed",
                    "borrowed_apr",
                    "contract",
                    "leveraged_apr",
                    "leveraged_apr_multiplier",
                ]
            )
            writer.writerows(CsvRepository.split_pair_data(pairs))


if __name__ == "__main__":
    CsvRepository().find_by_ticker(ticker="imx")
