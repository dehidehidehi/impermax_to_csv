from typing import Generator, Collection

import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame, Series


class Plotter:
    def __init__(
        self, repository_data: DataFrame, apr_type: str = "supply_apr", **plot_kwargs
    ):
        self.apr_type = apr_type
        self.plot_kwargs = plot_kwargs
        self.freq = "1D"
        self.df = repository_data
        self._process_df(self.df)
        Plotter.set_matplotlib_backend_to_gui()

    def plot(self) -> None:
        contracts = set(self.df["contract"])
        plt.title(f"{self.apr_type} over time")
        for i, contract_df in enumerate(
            self.processed_contract_series_generator(contracts)
        ):
            if contract_df.empty:
                continue
            label = self.mk_string_label(contract_df)
            contract_df[self.apr_type].plot(label=label, **self.plot_kwargs)

    def processed_contract_series_generator(
        self, contracts: Collection[str]
    ) -> Generator[DataFrame, None, None]:
        for contract in contracts:
            filtered_series: Series = self.df[self.df["contract"] == contract]
            processed_series: Series = self._process_series(filtered_series)
            yield processed_series

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

        def reindex() -> None:
            df.set_index("datetime", inplace=True)

        def remove_nans() -> None:
            df.dropna(subset=[self.apr_type], inplace=True)

        cast_types()
        reindex()
        remove_nans()

    def _process_series(self, series: Series) -> Series:
        return self._interpolate_series(series, self.freq)

    @staticmethod
    def set_matplotlib_backend_to_gui() -> None:
        matplotlib.use("TkAgg")

    @staticmethod
    def _interpolate_series(series: Series, freq: str) -> Series:
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
