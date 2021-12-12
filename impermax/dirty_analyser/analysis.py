from dataclasses import dataclass
from functools import cached_property

from matplotlib import pyplot
from pandas import DataFrame

from impermax.dirty_analyser.enums import AvalancheStables, STABLECOIN_TICKERS, MoonRiverStables, ArbitrumStables, \
    MaticStables, EthereumStables
from impermax.dirty_analyser.extract_data import load_all_csv
from impermax.fetcher.enums import ImpermaxURLS

ALL_CSV_DATA = load_all_csv()


@dataclass
class PoolDataFilter:
    contract: str

    @cached_property
    def _pair_data(self) -> list[dict]:
        _pool_data = [n for n in ALL_CSV_DATA if n['contract'] == self.contract]
        if not _pool_data:
            raise ValueError(f'is {self.contract} a valid pool address?')
        _pool_data.sort(key=lambda x: x['datetime'])
        return _pool_data

    @cached_property
    def left(self) -> list[dict]:
        pair = self._pair_data[0]['pair']
        left, _, right = pair.rpartition('/')
        left_ticker_data = [n for n in self._pair_data if n['ticker'] == left]
        return left_ticker_data

    @cached_property
    def right(self) -> list[dict]:
        pair = self._pair_data[0]['pair']
        left, _, right = pair.rpartition('/')
        right_ticker_data = [n for n in self._pair_data if n['ticker'] == right]
        return right_ticker_data


@dataclass
class NumpyAnalytics:
    _the_data: list[dict]

    def __post_init__(self):
        self._freq = '1D'
        self._df = DataFrame(data=self._the_data)
        self._df.set_index('datetime', inplace=True)
        self._interpolate_df()

    @property
    def df(self) -> DataFrame:
        return self._df

    def _interpolate_df(self) -> None:
        target_idx = self._df.asfreq(self._freq).index
        self._df = self._df.reindex(self._df.index.union(target_idx))

        self._df['blockchain'] = self._df['blockchain'].interpolate(method='bfill')
        self._df['pair'] = self._df['pair'].interpolate(method='bfill')
        self._df['dex'] = self._df['dex'].interpolate(method='bfill')
        self._df['ticker'] = self._df['ticker'].interpolate(method='bfill')

        self._df['supply'] = self._df['supply'].astype(float).interpolate(method='polynomial', order=2).astype(int)

        self._df['supply_apr'] = self._df['supply_apr'].astype(float).interpolate(method='polynomial', order=2)
        self._df['borrowed_apr'] = self._df['borrowed_apr'].astype(float).interpolate(method='polynomial', order=2)
        self._df['borrowed'] = self._df['supply_apr'].astype(float).interpolate(method='polynomial', order=2)

        self._df['leveraged_apr'] = self._df['leveraged_apr'].interpolate(method='bfill')
        self._df['leveraged_apr_multiplier'] = self._df['leveraged_apr_multiplier'].interpolate(method='bfill')
        self._df['contract'] = self._df['contract'].interpolate(method='bfill')

        self._df = self._df.reindex(target_idx)

def is_stablecoin(side: DataFrame) -> bool:
    return any(stable in side['ticker'][0] for stable in STABLECOIN_TICKERS)

def plot_pools(pool_addresses: list[str], **plot_kwargs):
    for pool in pool_addresses:
        filtered_data = PoolDataFilter(contract=pool)
        left = NumpyAnalytics(filtered_data.left).df
        right = NumpyAnalytics(filtered_data.right).df
        if is_stablecoin(right):
            label = ', '.join([right['ticker'][0], right['pair'][0], right['dex'][0], right['blockchain'][0]])
            right[label] = right['supply_apr']  # changing column name for plot
            right[label].plot(**plot_kwargs)
        if is_stablecoin(left):
            label = ', '.join([left['ticker'][0], left['pair'][0], left['dex'][0], left['blockchain'][0]])
            left[label] = left['supply_apr']  # changing column name for plot
            left[label].plot(**plot_kwargs)


if __name__ == '__main__':
    common_kwargs = dict(legend=True)
    # common_kwargs = dict()
    # plot_pools(MoonRiverStables.list(), color='yellow', **common_kwargs)
    plot_pools(AvalancheStables.list(), **common_kwargs)
    # plot_pools(MaticStables.list(), color='pink', **common_kwargs)
    # plot_pools(ArbitrumStables.list(), color='grey', **common_kwargs)
    # plot_pools(EthereumStables.list(), color='black', **common_kwargs)
    pyplot.show()
    ...
