from src.impermax.common.urls_enum import ImpermaxURLS
from src.impermax.dao.csv_dao import CsvDao
from src.impermax.dao.dao_interface import DaoInterface
from src.impermax.services.data_providers.data_provider_interface import DataProviderInterface
from src.impermax.services.data_providers.web_scraper.web_scraper_provider import WebScraperProvider


def enable_logging() -> None:
    import logging
    logging.basicConfig(level=logging.INFO)
    pyppeteer_logger = logging.getLogger('pyppeteer')
    pyppeteer_logger.setLevel(logging.ERROR)


def main() -> None:
    provider: DataProviderInterface = WebScraperProvider()
    imx_pairs = provider.get(ImpermaxURLS.list())
    persister: DaoInterface = CsvDao(imx_pairs)
    persister.save()


if __name__ == '__main__':
    enable_logging()
    main()
