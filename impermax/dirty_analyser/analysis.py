from dataclasses import dataclass
from functools import cached_property

from pandas import DataFrame

from impermax.dirty_analyser.extract_data import load_all_csv
from impermax.fetcher.enums import ImpermaxURLS

ALL_CSV_DATA = load_all_csv()


@dataclass
class PairDataFilter:
    chain: str
    pair: str

    @cached_property
    def _pair_data(self) -> list[dict]:
        pair_data = [n for n in ALL_CSV_DATA if n['blockchain'] == self.chain and n['pair'] == self.pair]
        if not pair_data:
            raise ValueError(f'is {self.pair} a valid pair? is {self.chain} a valid chain?')
        pair_data.sort(key=lambda x: x['datetime'])
        return pair_data

    @cached_property
    def left(self) -> list[dict]:
        left_ticker, _, _ = self.pair.rpartition('/')
        left_ticker_data = [n for n in self._pair_data if n['ticker'] == left_ticker]
        return left_ticker_data

    @cached_property
    def right(self) -> list[dict]:
        _, _, right_ticker = self.pair.rpartition('/')
        right_ticker_data = [n for n in self._pair_data if n['ticker'] == right_ticker]
        return right_ticker_data


@dataclass
class NumpyAnalytics:
    _the_data: list[dict]

    def __post_init__(self):
        self._df = DataFrame(data=self._the_data)
        self._df.set_index('datetime', inplace=True)
        self._interpolate_df()

    @property
    def df(self) -> DataFrame:
        return self._df

    def _interpolate_df(self) -> None:
        target_idx = self._df.asfreq('1D').index
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

        self._df = self._df.reindex(target_idx)


def analyse_pairs(pairs: list[tuple[str, list[str]]]):
    for blockchain, pairs in pairs:
        for pair_ in pairs:
            filtered_data = PairDataFilter(chain=blockchain, pair=pair_)
            left = NumpyAnalytics(filtered_data.left).df
            right = NumpyAnalytics(filtered_data.right).df
            ...


if __name__ == '__main__':
    pairs = [
        (ImpermaxURLS.AVAX.name, ['USDC.e/USDT.e',]),
        (ImpermaxURLS.MATIC.name, ['USDC/USDT',]),
    ]
    analyse_pairs(pairs)
    ...
