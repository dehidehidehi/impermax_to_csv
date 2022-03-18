from typing import Callable
from unittest import TestCase

from src.impermax.common.enums.contracts.imx_enums import ImpermaxPairs
from src.impermax.common.enums.data_columns_enum import PlottableColumns
from src.impermax.repositories.csv.csv_repository import CsvRepository
from src.impermax.services.plotter.plotter import Plotter


class PlotterIntegrationTests(TestCase):

    repo = None
    stable_coins = ['USDC', 'USDT', 'STATIK', 'MAI', 'DAI', 'FAKESTABLECOINTICKER']

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = CsvRepository()

    @staticmethod
    def prepare_plot_data_for_all_columns(get_data: Callable) -> None:
        for column_name in PlottableColumns.list():
            _ = Plotter(get_data(), to_plot=column_name).data_interpolated_per_contract
            # The actual plot function increases time by 10x.
            # we just need to check the plot data is ok here.

    def test_givenRepoFindByTicker_whenPrepared_DoesNotRaiseException(self):
        self.prepare_plot_data_for_all_columns(lambda: self.repo.find_by_ticker('IMX'))

    def test_givenRepoFindByTickers_whenPrepared_DoesNotRaiseException(self):
        self.prepare_plot_data_for_all_columns(lambda: self.repo.find_by_tickers(*self.stable_coins))

    def test_givenRepoFindByTickerStrict_whenPrepared_DoesNotRaiseException(self):
        self.prepare_plot_data_for_all_columns(lambda: self.repo.find_by_ticker_strict('IMX'))

    def test_givenRepoFindByTickersStrict_whenPrepared_DoesNotRaiseException(self):
        self.prepare_plot_data_for_all_columns(lambda: self.repo.find_by_tickers_strict(*self.stable_coins))

    def test_givenRepoFindByContract_whenPrepared_DoesNotRaiseException(self):
        contract = ImpermaxPairs.ETHEREUM_IMX_ETH_UNISWAP.value
        self.prepare_plot_data_for_all_columns(lambda: self.repo.find_by_contract(contract))

    def test_givenRepoFindByContracts_whenPrepared_DoesNotRaiseException(self):
        contract = ImpermaxPairs.ETHEREUM_IMX_ETH_UNISWAP.value
        contract2 = ImpermaxPairs.POLYGON_IMX_WETH_QUICKSWAP.value
        self.prepare_plot_data_for_all_columns(lambda: self.repo.find_by_contracts(contract, contract2))
