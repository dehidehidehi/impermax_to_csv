from matplotlib import pyplot
from pandas import DataFrame

from src.impermax.repositories.csv.csv_repository import CsvRepository
from src.impermax.repositories.repository_interface import RepositoryInterface
from src.impermax.services.dirty_plotter.plotter import Plotter


def main():
    apr = "supply_apr"  # apr = "supply_apr"
    common_kwargs = dict(legend=True, apr_type=apr)

    repo: RepositoryInterface = CsvRepository()
    resp: DataFrame = repo.find_by_ticker("imx")
    Plotter(resp, **common_kwargs).plot()
    pyplot.show()


if __name__ == "__main__":
    main()
