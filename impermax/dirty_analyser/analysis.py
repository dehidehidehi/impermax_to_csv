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
        pair_data = [n for n in ALL_CSV_DATA if n['pair'] == self.pair]
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
        self.df = DataFrame(data=self._the_data)
        self._interpolate_df()
        ...

    def _interpolate_df(self) -> None:
        self.df.set_index('datetime', inplace=True)
        target_idx = self.df.asfreq('1D').index
        new_idx = self.df.index.union(target_idx)
        self.df = self.df.reindex(new_idx)

        self.df['blockchain'] = self.df['blockchain'].interpolate(method='bfill')
        self.df['pair'] = self.df['pair'].interpolate(method='bfill')
        self.df['dex'] = self.df['dex'].interpolate(method='bfill')
        self.df['ticker'] = self.df['ticker'].interpolate(method='bfill')

        self.df['supply'] = self.df['supply'].astype(float).interpolate(method='polynomial', order=2).astype(int)

        self.df['supply_apr'] = self.df['supply_apr'].astype(float).interpolate(method='polynomial', order=2)
        self.df['borrowed_apr'] = self.df['borrowed_apr'].astype(float).interpolate(method='polynomial', order=2)
        self.df['borrowed'] = self.df['supply_apr'].astype(float).interpolate(method='polynomial', order=2)

        self.df['leveraged_apr'] = self.df['leveraged_apr'].interpolate(method='bfill')
        self.df['leveraged_apr_multiplier'] = self.df['leveraged_apr_multiplier'].interpolate(method='bfill')

        self.df = self.df.reindex(target_idx)


if __name__ == '__main__':
    filtered_data = PairDataFilter(chain=ImpermaxURLS.AVAX.name, pair='USDC.e/USDT.e')
    usdc = filtered_data.left
    usdt = filtered_data.right
    usdc_analysis = NumpyAnalytics(usdc)
    usdc_analysis.df