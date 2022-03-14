import logging

from pandas import DataFrame

from src.impermax.common.enums.contracts.imx_enums import ImpermaxPairs
from src.impermax.common.tests.test_helper import WebScraperIntegrationTestsHelper
from src.impermax.repositories.csv.csv_repository import CsvRepository


class TestCsvRepository(WebScraperIntegrationTestsHelper):
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

    def assertFindByTickerReturnsLikeTickerData(self, ticker: str, df: DataFrame):
        tickers_in_resp = set(df["ticker"])
        self.assertGreater(len(tickers_in_resp), 1)
        self.assertTrue(all(ticker in t for t in set(df["ticker"])))

    def assertDataFrameOrderedByDatetimeAsc(self, df: DataFrame):
        def swap_first_and_last_values_of_series(df_: DataFrame, col_: str) -> None:
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

    def test_givenCall_whenSave_DoesNotRaise(self):
        self.csv_repo.save(data=self.parsed_pairs)

    def test_givenMultipleCalls_whenSave_DoesNotRaise(self):
        self.csv_repo.save(data=self.parsed_pairs)
        self.csv_repo.save(data=self.parsed_pairs)

    def test_givenSplitPairDataFuncCall_whenSave_returnsEqualLengthPairs(self):
        pairs = self.csv_repo.split_pair_data(pairs=self.parsed_pairs)
        all_pair_lengths = set(len(p) for p in pairs)
        self.assertEqual(len(all_pair_lengths), 1)

    def test_givenCall_whenFindAll_returnsFilledDataFrame(self):
        resp: DataFrame = self.csv_repo.find_all()
        self.assertFalse(resp.empty)

    def test_givenCall_whenFindAll_returnsDataOrderedByDatetimeAsc(self):
        resp: DataFrame = self.csv_repo.find_all()
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenCall_whenFindByTicker_returnsDataOrderedByDatetimeAsc(self):
        resp: DataFrame = self.csv_repo.find_by_ticker("IMX")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUppercaseTicker_whenFindByTicker_returnsLikeTickerData(self):
        resp: DataFrame = self.csv_repo.find_by_ticker("IMX")
        self.assertFindByTickerReturnsLikeTickerData("IMX", df=resp)

    def test_givenLowerCaseTicker_whenFindByTicker_returnsLikeTickerData(self):
        resp: DataFrame = self.csv_repo.find_by_ticker("imx")
        self.assertFindByTickerReturnsLikeTickerData("imx".upper(), df=resp)

    def test_givenCall_whenFindByTickerStrict_returnsDataOrderedByDatetimeAsc(self):
        resp: DataFrame = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseTicker_whenFindByTickerStrict_returnsOnlyTickerData(self):
        resp: DataFrame = self.csv_repo.find_by_ticker_strict("IMX")
        self.assertEqual(1, len(set(resp["ticker"])))

    def test_givenLowerCaseTicker_whenFindByTickerStrict_returnsOnlyTickerData(self):
        resp: DataFrame = self.csv_repo.find_by_ticker_strict("imx")
        self.assertEqual(1, len(set(resp["ticker"])))

    def test_givenCall_whenFindByContract_returnsDataOrderedByDatetimeAsc(self):
        resp: DataFrame = self.csv_repo.find_by_contract(self.contract)
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseContract_whenFindByContract_returnsOnlyContractData(self):
        resp: DataFrame = self.csv_repo.find_by_contract(self.contract.upper())
        self.assertEqual(1, len(set(resp["contract"])))

    def test_givenLowerCaseContract_whenFindByContract_returnsOnlyContractData(self):
        resp: DataFrame = self.csv_repo.find_by_contract(self.contract.lower())
        self.assertEqual(1, len(set(resp["contract"])))

    def test_givenCall_whenFindByContracts_returnsDataOrderedByDatetimeAsc(self):
        resp: DataFrame = self.csv_repo.find_by_contracts(
            {self.contract, self.contract2}
        )
        self.assertDataFrameOrderedByDatetimeAsc(resp)

    def test_givenUpperCaseContracts_whenFindByContracts_returnsOnlyContractData(self):
        resp: DataFrame = self.csv_repo.find_by_contracts(
            {self.contract.upper(), self.contract2.upper()}
        )
        self.assertEqual(2, len(set(resp["contract"])))

    def test_givenLowerCaseContracts_whenFindByContracts_returnsOnlyContractData(self):
        resp: DataFrame = self.csv_repo.find_by_contracts(
            {self.contract.lower(), self.contract2.lower()}
        )
        self.assertEqual(2, len(set(resp["contract"])))
