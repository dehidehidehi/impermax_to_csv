import logging
from unittest import TestCase

from src.impermax.common.urls_enum import ImpermaxURLS
from src.impermax.services.data_providers.web_scraper._async_scraper import _AsyncWebScraper
from src.impermax.services.data_providers.web_scraper._html_parser import _ImxPageParser

logger = logging.getLogger(__name__)


class TestScraperHelper(TestCase):
    urls = ImpermaxURLS.list()
    html_resps = _AsyncWebScraper().get(urls)
    parsed_pairs = [_ImxPageParser(p).parse() for p in html_resps]
    logger.warning('Untested scraping parser, use with caution.')
