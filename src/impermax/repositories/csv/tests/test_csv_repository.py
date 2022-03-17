import logging
from typing import Callable
from unittest import TestCase

import pandas as pd
from pandas import DataFrame

from src.impermax.common.enums.contracts.imx_enums import ImpermaxPairs
from src.impermax.common.tests.test_helper import WebScraperIntegrationTestsHelper
from src.impermax.repositories.csv.csv_repository import CsvRepository


class _TestCsvRepositoryAssertions(TestCase):
    """
    Separates refactored assertions from tests.
    """
    def assertFindByTickerReturnsLikeTickerData(self, df, *expected_tickers):
        expected_tickers = [et.upper() for et in expected_tickers]
        response_tickers = set(df["ticker"])
        self.assertGreater(len(response_tickers), 1)
        for r_ticker in response_tickers:
            self.assertTrue(any(t in r_ticker for t in expected_tickers))

    def assertDataFrameOrderedByDatetimeAsc(self, df):
        pd.options.mode.chained_assignment = None  # default='warn'

        def swap_first_and_last_values_of_series(df_, col_: str) -> None:
            df_[col_].iloc[0], df_[col_].iloc[-1] = (
                df_[col_].iloc[-1],
                df_[col_].iloc[0],
            )

        col = "datetime"
        should_be_ordered_asc: bool = df[col].is_monotonic
        self.assertTrue(should_be_ordered_asc)

        swap_first_and_last_values_of_series(df, col)
        should_not_be_not_ordered_asc: bool = df[col].is_monotonic
        self.assertFalse(should_not_be_not_ordered_asc)


class TestCsvRepository(_TestCsvRepositoryAssertions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        csv_output_logger = logging.getLogger(
            "src.impermax.repositories.csv.csv_repository_helper"
        )
        csv_output_logger.setLevel(logging.WARNING)
        cls.contract = ImpermaxPairs.ETHEREUM_IMX_ETH_UNISWAP.value
        cls.contract2 = ImpermaxPairs.POLYGON_IMX_WETH_QUICKSWAP.value

    def setUp(self) -> None:
        self.csv_repo = CsvRepository()

    # def test_givenCall_whenSave_DoesNotRaise(self):
    #     self.csv_repo.save(data=self.parsed_pairs)
    #
    # def test_givenMultipleCalls_whenSave_DoesNotRaise(self):
    #     self.csv_repo.save(data=self.parsed_pairs)
    #     self.csv_repo.save(data=self.parsed_pairs)
    #
    # def test_givenSplitPairDataFuncCall_whenSave_returnsEqualLengthPairs(self):
    #     pairs = self.csv_repo.split_pair_data(pairs=self.parsed_pairs)
    #     all_pair_lengths = set(len(p) for p in pairs)
    #     self.assertEqual(len(all_pair_lengths), 1)

    def test_givenCall_whenFindAll_returnsFilledDataFrame(self):
        resp = self.csv_repo.find_all()
        self.assertFalse(resp.empty)

    def test_givenCall_whenFindAll_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_all()
        self.assertDataFrameOrderedByDatetimeAsc(resp)
        
    def test_givenCall_whenFindByTicker_returnsDataOnlyWithLikeTicker(self):
        resp = self.csv_repo.find_by_ticker("IMX")
        self.assertFalse(resp.empty)
        self.assertTrue(all("IMX" in t for t in resp['ticker']))

    def test_givenCall_whenFindByTicker_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_ticker("IMX")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUppercaseTicker_whenFindByTicker_returnsLikeTickerData(self):
        resp = self.csv_repo.find_by_ticker("IMX")
        self.assertFindByTickerReturnsLikeTickerData(resp, "IMX")

    def test_givenLowerCaseTicker_whenFindByTicker_returnsLikeTickerData(self):
        resp = self.csv_repo.find_by_ticker("imx")
        self.assertFindByTickerReturnsLikeTickerData(resp, "imx".upper())

    def test_givenCall_whenFindByTickers_returnsDataOnlyWithLikeTickers(self):
        resp = self.csv_repo.find_by_tickers("IMX", "IMX.m", "IMX.a")
        self.assertFalse(resp.empty)
        self.assertTrue(all(t in {"IMX", "IMX.M", "IMX.A"} for t in resp['ticker']))

    def test_givenCall_whenFindByTickers_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_tickers("IMX", "IMX.m", "IMX.a")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUppercaseTickers_whenFindByTicker_returnsLikeTickersData(self):
        resp = self.csv_repo.find_by_tickers("IMX", "IMX.M", "IMX.A")
        self.assertFindByTickerReturnsLikeTickerData(resp, "IMX", "IMX.M", "IMX.A")

    def test_givenLowerCaseTickers_whenFindByTicker_returnsLikeTickersData(self):
        resp = self.csv_repo.find_by_tickers("imx", "imx.m", "imx.a")
        self.assertFindByTickerReturnsLikeTickerData(resp, "imx", "imx.m", "imx.a")

    def test_givenCall_whenFindByTickerStrict_returnsDataOnlyEqualToTicker(self):
        resp = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertFalse(resp.empty)
        self.assertTrue(all("IMX" == t for t in resp['ticker']))

    def test_givenCall_whenFindByTickerStrict_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseTicker_whenFindByTickerStrict_returnsOnlyTickerData(self):
        resp = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertEqual(1, len(set(resp["ticker"])))

    def test_givenLowerCaseTicker_whenFindByTickerStrict_returnsOnlyTickerData(self):
        resp = self.csv_repo.find_by_ticker_strict("imx")
        self.assertEqual(1, len(set(resp["ticker"])))

    def test_givenCall_whenFindByContract_returnsDataOnlyEqualToContract(self):
        resp = self.csv_repo.find_by_contract(self.contract)
        self.assertFalse(resp.empty)
        self.assertTrue(all(self.contract == c for c in resp['contract']))

    def test_givenCall_whenFindByContract_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_contract(self.contract)
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseContract_whenFindByContract_returnsOnlyContractData(self):
        resp = self.csv_repo.find_by_contract(self.contract.upper())
        self.assertEqual(1, len(set(resp["contract"])))

    def test_givenLowerCaseContract_whenFindByContract_returnsOnlyContractData(self):
        resp = self.csv_repo.find_by_contract(self.contract.lower())
        self.assertEqual(1, len(set(resp["contract"])))

    def test_givenCall_whenFindByContracts_returnsDataWithContractInContracts(self):
        resp = self.csv_repo.find_by_contracts(self.contract, self.contract2)
        self.assertFalse(resp.empty)
        self.assertTrue(all(c in {self.contract, self.contract2} for c in resp['contract']))

    def test_givenCall_whenFindByContracts_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_contracts(self.contract, self.contract2)
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseContracts_whenFindByContracts_returnsOnlyContractData(self):
        resp = self.csv_repo.find_by_contracts(self.contract.upper(), self.contract2.upper())
        self.assertEqual(2, len(set(resp["contract"])))

    def test_givenLowerCaseContracts_whenFindByContracts_returnsOnlyContractData(self):
        resp = self.csv_repo.find_by_contracts(self.contract.lower(), self.contract2.lower())
        self.assertEqual(2, len(set(resp["contract"])))
