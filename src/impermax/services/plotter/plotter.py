from functools import cached_property
from itertools import product
from typing import Type, Union, Tuple, Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame, Series

from src.impermax.common.enums.data_columns_enum import PlottableColumns


class Plotter:
    def __init__(
        self,
            repository_data: DataFrame,
            to_plot: Type[PlottableColumns] = PlottableColumns.SUPPLY_APR,
    ):
        self.plotted_col: Type[PlottableColumns] = to_plot
        self.freq = "1D"
        self.df = repository_data
        self._process_df(self.df)
        Plotter.set_matplotlib_backend("TkAgg")
        pd.options.mode.chained_assignment = None

    def plot(self) -> None:
        df = self.data_interpolated_per_contract
        title = f"{self.plotted_col} over time"
        contracts = list(set(df['contract']))
        contracts.sort()

        fig, ax = plt.subplots(figsize=(15, 7))
        fig: Figure
        ax: Axes

        ax.set_title(title)
        ax.yaxis.tick_right()
        ax.grid(True)

        lines_handles = []
        for contract in contracts:
            subset = df[df['contract'] == contract]
            label = self.mk_string_label(subset.head(1))
            line, *_ = ax.plot(subset.index, subset[self.plotted_col], label=label)
            lines_handles.append(line)

        fig.tight_layout()
        fig.subplots_adjust(left=0.05, right=0.70)
        ax.legend(handles=lines_handles, loc='upper left', bbox_to_anchor=(1.05, 1.015))

    @cached_property
    def data_interpolated_per_contract(self) -> DataFrame:
        to_concat = []
        combinations = product(set(self.df['ticker']), set(self.df['contract']))
        for ticker, contract in combinations:
            subset_series = self.df[(self.df['contract'] == contract) & (self.df['ticker'] == ticker)]
            subset_series = self._interpolate(subset_series, self.freq)
            to_concat.append(subset_series)
        concatenated_df: DataFrame = pd.concat(to_concat)
        return concatenated_df

    @staticmethod
    def mk_string_label(df: DataFrame) -> str:
        head: DataFrame = df.head(1)
        my_list = [
            head["ticker"].iloc[0],
            head["pair"].iloc[0],
            head["dex"].iloc[0],
            head["blockchain"].iloc[0],
        ]
        return ", ".join(my_list)

    def _process_df(self, df) -> None:
        def cast_types() -> None:
            df["datetime"].astype("datetime64[s]")
            df["supply"].astype(float)
            df["supply_apr"].astype(float)
            df["borrowed"].astype(float)
            df["borrowed_apr"].astype(float)

        def remove_nans() -> None:
            df.dropna(subset=[self.plotted_col], inplace=True)

        cast_types()
        df.set_index("datetime", inplace=True)
        remove_nans()

    @staticmethod
    def set_matplotlib_backend(backend: str) -> None:
        mpl.use(backend)

    @staticmethod
    def _interpolate(series: Series, freq: str) -> Series:
        target_idx = series.asfreq(freq).index
        series = series.reindex(series.index.union(target_idx))

        series["blockchain"].interpolate(method="bfill", inplace=True)
        series["pair"].interpolate(method="bfill", inplace=True)
        series["dex"].interpolate(method="bfill", inplace=True)
        series["ticker"].interpolate(method="bfill", inplace=True)
        series["contract"].interpolate(method="bfill", inplace=True)

        series["supply"].interpolate(method="polynomial", order=2, inplace=True)
        series["supply"].astype(int)
        series["supply_apr"].interpolate(method="polynomial", order=2, inplace=True)
        series["borrowed"].interpolate(method="polynomial", order=2, inplace=True)
        series["borrowed_apr"].interpolate(method="polynomial", order=2, inplace=True)
        series["leveraged_apr"].interpolate(method="bfill", inplace=True)
        series["leveraged_apr_multiplier"].interpolate(method="bfill", inplace=True)

        series.reindex(target_idx)
        return series
