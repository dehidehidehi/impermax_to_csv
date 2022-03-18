import logging
from unittest import TestCase

import pandas as pd

from src.impermax.common.enums.contracts.imx_enums import ImpermaxPairs
from src.impermax.repositories.csv.csv_repository import CsvRepository


class _TestCsvRepositoryAssertions(TestCase):
    """
    Separates refactored assertions from tests.
    """
    def assertFindByTickerReturnsLikeTickerData(self, df, *some_expected_tickers):
        some_expected_tickers = [et.upper() for et in some_expected_tickers]
        response_tickers = set(df["ticker"])
        self.assertGreater(len(response_tickers), 1)
        for e_ticker in some_expected_tickers:
            self.assertTrue(any(t == e_ticker for t in response_tickers))

    def assertDataFrameOrderedByDatetimeAsc(self, df):
        pd.options.mode.chained_assignment = None  # default='warn'
        col = "datetime"
        should_be_ordered_asc: bool = df[col].is_monotonic
        self.assertTrue(should_be_ordered_asc)


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
        cls.csv_repo = CsvRepository()

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
        resp_tickers = set(resp['ticker'].values)
        self.assertFalse(resp.empty)
        self.assertTrue(all("IMX" in t for t in resp_tickers))

    def test_givenCall_whenFindByTicker_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_ticker("IMX")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUppercaseTicker_whenFindByTicker_returnsLikeTickerData(self):
        resp = self.csv_repo.find_by_ticker("IMX")
        self.assertFindByTickerReturnsLikeTickerData(resp, "IMX")

    def test_givenLowerCaseTicker_whenFindByTicker_returnsLikeTickerData(self):
        resp = self.csv_repo.find_by_ticker("imx")
        self.assertFindByTickerReturnsLikeTickerData(resp, "imx".upper())

    def test_givenCall_whenFindByTickers_returnsDataLikeTickers(self):
        resp = self.csv_repo.find_by_tickers("IMX", "USDC")
        resp_tickers = set(resp['ticker'].values)
        self.assertFalse(resp.empty)
        self.assertTrue(all(t in resp_tickers for t in {"IMX.M", "IMX.A", "USDC.E"}))

    def test_givenCall_whenFindByTickers_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_tickers("IMX", "USDC")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUppercaseTickers_whenFindByTicker_returnsLikeTickersData(self):
        resp = self.csv_repo.find_by_tickers("IMX", "USDC")
        self.assertFindByTickerReturnsLikeTickerData(resp, "IMX.M", "IMX.A", 'USDC.E')

    def test_givenLowerCaseTickers_whenFindByTicker_returnsLikeTickersData(self):
        resp = self.csv_repo.find_by_tickers("imx", "usdc")
        self.assertFindByTickerReturnsLikeTickerData(resp, "imx.m", "usdc.e")

    def test_givenCall_whenFindByTickerStrict_returnsDataOnlyEqualToTicker(self):
        resp = self.csv_repo.find_by_ticker_strict("IMX")
        resp_tickers = set(resp['ticker'].values)
        self.assertFalse(resp.empty)
        self.assertTrue(all("IMX" == t for t in resp_tickers))

    def test_givenCall_whenFindByTickerStrict_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseTicker_whenFindByTickerStrict_returnsOnlyTickerData(self):
        resp = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertEqual(1, len(set(resp["ticker"])))

    def test_givenLowerCaseTicker_whenFindByTickerStrict_returnsOnlyTickerData(self):
        resp = self.csv_repo.find_by_ticker_strict("imx")
        self.assertEqual(1, len(set(resp["ticker"])))


    def test_givenCall_whenFindByTickersStrict_returnsDataOnlyWithOnlyTickers(self):
        resp = self.csv_repo.find_by_tickers_strict("IMX", "USDC")
        resp_tickers = set(resp['ticker'].values)
        self.assertFalse(resp.empty)
        self.assertTrue(all(t in {"IMX", "USDC"} for t in resp_tickers))

    def test_givenCall_whenFindByTickersStrict_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_tickers_strict("IMX", "USDC")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenCall_whenFindByTickersStrict_DoesNotReturnLikeData(self):
        resp = self.csv_repo.find_by_tickers_strict("IMX", "USDC")
        resp_tickers = set(resp['ticker'].values)
        self.assertNotIn("IMX.M", resp_tickers)
        self.assertNotIn("USDC.E", resp_tickers)

    def test_givenUppercaseTickers_whenFindByTickerStrict_returnsOnlyTickersData(self):
        resp = self.csv_repo.find_by_tickers_strict("IMX", "USDC")
        self.assertFindByTickerReturnsLikeTickerData(resp, "IMX", "USDC")

    def test_givenLowerCaseTickers_whenFindByTickerStrict_returnsOnlyTickersData(self):
        resp = self.csv_repo.find_by_tickers_strict("imx", "usdc")
        self.assertFindByTickerReturnsLikeTickerData(resp, "imx", "usdc")


    def test_givenCall_whenFindByContract_returnsDataOnlyEqualToContract(self):
        resp = self.csv_repo.find_by_contract(self.contract)
        resp_contracts = set(resp['contract'].values)
        self.assertFalse(resp.empty)
        self.assertTrue(all(self.contract == c for c in resp_contracts))

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
        resp_contracts = set(resp['contract'].values)
        self.assertFalse(resp.empty)
        self.assertTrue(all(c in {self.contract, self.contract2} for c in resp_contracts))

    def test_givenCall_whenFindByContracts_returnsDataOrderedByDatetimeAsc(self):
        resp = self.csv_repo.find_by_contracts(self.contract, self.contract2)
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseContracts_whenFindByContracts_returnsOnlyContractData(self):
        resp = self.csv_repo.find_by_contracts(self.contract.upper(), self.contract2.upper())
        self.assertEqual(2, len(set(resp["contract"])))

    def test_givenLowerCaseContracts_whenFindByContracts_returnsOnlyContractData(self):
        resp = self.csv_repo.find_by_contracts(self.contract.lower(), self.contract2.lower())
        self.assertEqual(2, len(set(resp["contract"])))
