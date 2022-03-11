from impermax.common.extended_classes import ExtendedEnum
from impermax.fetcher.scraper.ascraper import _ScrapeImpermax


class ImpermaxURLS(str, ExtendedEnum):
    ETH = 'https://app.impermax.finance/'
    MATIC = 'https://polygon.impermax.finance/'
    ARB = 'https://arbitrum.impermax.finance/'
    AVAX = 'https://avalanche.impermax.finance/'
    MOONRIVER = 'https://moonriver.impermax.finance/'
    FANTOM = 'https://fantom.impermax.finance/'


class DataProvenances(ExtendedEnum):
    WEB_SCRAPER = _ScrapeImpermax