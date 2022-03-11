from src.impermax.converters._csv import ImpermaxToCSV
from src.impermax.fetcher.enums import DataProvenances, ImpermaxURLS
from src.impermax.fetcher.scraper.parser import IMXChainPageParser
from src.impermax.fetcher.strategy import DataFetcher


def enable_logging() -> None:
    import logging
    logging.basicConfig(level=logging.INFO)
    pyppeteer_logger = logging.getLogger('pyppeteer')
    pyppeteer_logger.setLevel(logging.ERROR)


def main() -> None:
    fetcher = DataFetcher(fetcher=DataProvenances.WEB_SCRAPER)
    responses = fetcher.get(ImpermaxURLS.list())
    parsed_resps = list(IMXChainPageParser(p).parse() for p in responses)
    ImpermaxToCSV(parsed_resps).save()


if __name__ == '__main__':
    enable_logging()
    main()
