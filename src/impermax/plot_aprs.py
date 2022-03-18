from typing import Type

from matplotlib import pyplot
from pandas import DataFrame

from src.impermax.common.enums.data_columns_enum import PlottableColumns
from src.impermax.repositories.csv.csv_repository import CsvRepository
from src.impermax.services.dirty_plotter.plotter import Plotter


def plot(repository_data: DataFrame, data_to_plot: Type[PlottableColumns] = PlottableColumns.SUPPLY_APR) -> None:
    common_kwargs = dict(legend=True, apr_type=data_to_plot.value)
    Plotter(repository_data, **common_kwargs).plot()
    pyplot.show()


if __name__ == '__main__':
    repo = CsvRepository()
    r = repo.find_by_ticker('IMX')
    plot(repository_data=r)
