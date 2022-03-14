import logging
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Union

import pandas as pd
from pandas import DataFrame

from src.impermax.common.path_consts import TARGET_CSV
from src.impermax.services.web_scraper._dataclasses import ImxPair

logger = logging.getLogger(__name__)


class _CsvRepositoryHelper:
    """
    Helper class to make main CsvDao class more readable.
    """

    @staticmethod
    def mk_file_name() -> str:
        current_date = (
            datetime.now().isoformat()[:16].replace(":", "-")
        )  # removes illegal filename chars ':'
        return f"impermax_7_days_{current_date}.csv"

    @staticmethod
    def get_list_of_csv_paths(csv_dir: Union[str, Path] = TARGET_CSV) -> list[Path]:
        return list(n for n in csv_dir.iterdir() if n.name.endswith(".csv"))

    @staticmethod
    def load_all_csvs(path: str = TARGET_CSV) -> DataFrame:
        def find_dt(name_):
            return _CsvRepositoryHelper.extract_datetime_from_csv_title(name_)

        csv_paths: list[Path] = _CsvRepositoryHelper.get_list_of_csv_paths(path)
        df = pd.concat(
            (pd.read_csv(f).assign(datetime=find_dt(f.name)) for f in csv_paths)
        )
        df.sort_values("datetime", ascending=True, inplace=True)
        return df

    @staticmethod
    def extract_datetime_from_csv_title(name: str) -> datetime:
        _, _, str_date = name.replace(".csv", "").rpartition("_")
        the_date, _, the_time = str_date.rpartition("T")
        the_time = the_time.replace("-", ":")
        the_datetime = datetime.fromisoformat(the_date + "T" + the_time)
        return the_datetime

    @staticmethod
    def split_pair_data(pairs: list[list[ImxPair]]) -> list[list[str]]:
        all_pairs = list(chain.from_iterable(pairs))
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

    @staticmethod
    def _assert_csv_exists(file_name: str) -> None:
        full_file_path = TARGET_CSV / file_name
        if not full_file_path.exists():
            raise FileNotFoundError(
                f"CSV failed to save without raising an exception in {full_file_path}"
            )
        logger.info(f"Saved results to {full_file_path}")
