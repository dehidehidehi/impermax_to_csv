from impermax.converters._csv import ImpermaxToCSV
from impermax.fetcher.enums import DataProvenances, ImpermaxURLS
from impermax.fetcher.scraper.parser import IMXChainPageParser
from impermax.fetcher.strategy import DataFetcher


def main() -> None:
    fetcher = DataFetcher(fetcher=DataProvenances.WEB_SCRAPER)
    responses = fetcher.get(ImpermaxURLS.list())
    parsed_resps = list(IMXChainPageParser(p).parse() for p in responses)
    ImpermaxToCSV(parsed_resps).save()


if __name__ == '__main__':
    main()