import csv
import logging
from datetime import datetime
from itertools import chain
from pathlib import Path

from src.impermax.common.path_consts import TARGET_CSV
from src.impermax.dao.dao_interface import DaoInterface
from src.impermax.services.data_providers.web_scraper._dataclasses import ImxPair

logger = logging.getLogger(__name__)


class CsvDao(DaoInterface):
    def __init__(self, pairs: list[list[ImxPair]]):
        self.pairs = pairs

    @property
    def file_name(self) -> str:
        current_date = (
            datetime.now().isoformat()[:16].replace(":", "-")
        )  # removes illegal filename chars ':'
        return f"impermax_7_days_{current_date}.csv"

    @property
    def full_file_path(self) -> Path:
        return TARGET_CSV / self.file_name

    @property
    def split_pair_data(self) -> list[list[str]]:
        all_pairs = list(chain.from_iterable(self.pairs))
        left_pairs = [
            (
                p.chain,
                p.pair,
                p.dex,
                *str(p.left).split("\t"),
                p.leveraged_apr,
                p.leveraged_apr_multiplier,
            )
            for p in all_pairs
        ]
        right_pairs = [
            (
                p.chain,
                p.pair,
                p.dex,
                *str(p.right).split("\t"),
                p.leveraged_apr,
                p.leveraged_apr_multiplier,
            )
            for p in all_pairs
        ]
        successive_pairs = list()
        for lp, rp in zip(left_pairs, right_pairs):
            successive_pairs.append(lp)
            successive_pairs.append(rp)
        return successive_pairs

    def save(self) -> None:
        self._save_as_csv()
        self._assert_csv_exists()

    def _save_as_csv(self) -> None:
        self._create_output_dir()
        with open(
            str(self.full_file_path), mode="w+", encoding="UTF-8", newline="\n"
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
            writer.writerows(self.split_pair_data)

    def _assert_csv_exists(self) -> None:
        if not self.full_file_path.exists():
            raise FileNotFoundError(
                f"CSV failed to save without raising an exception in {self.full_file_path}"
            )
        logger.info(f"Saved results to {self.full_file_path}")
