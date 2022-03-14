from src.impermax.common.enums.imx_urls_enum import ImpermaxURLS
from src.impermax.repositories.csv.csv_repository import CsvRepository
from src.impermax.repositories.repository_interface import RepositoryInterface
from src.impermax.services.web_scraper._dataclasses import ImxPair
from src.impermax.services.web_scraper.web_scraper_provider import WebScraperProvider


def enable_logging() -> None:
    import logging

    logging.basicConfig(level=logging.INFO)
    pyppeteer_logger = logging.getLogger("pyppeteer")
    pyppeteer_logger.setLevel(logging.WARNING)


def main() -> None:
    provider: DataProviderInterface = WebScraperProvider()
    imx_pairs: list[list[ImxPair]] = provider.get(ImpermaxURLS.list())
    persister: RepositoryInterface = CsvRepository()
    persister.save(imx_pairs)


if __name__ == "__main__":
    enable_logging()
    main()
