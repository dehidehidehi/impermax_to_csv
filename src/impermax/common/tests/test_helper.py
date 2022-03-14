import logging
from abc import ABC, abstractmethod
from unittest import TestCase

from src.impermax.common.enums.imx_urls_enum import ImpermaxURLS
from src.impermax.common.tests.singleton_meta import SingletonMeta
from src.impermax.impermax_to_csv import enable_logging
from src.impermax.services.web_scraper._async_scraper import (
    _AsyncWebScraper,
)
from src.impermax.services.web_scraper._html_parser import _ImxPageParser

logger = logging.getLogger(__name__)


class _SingletonTestHelper(metaclass=SingletonMeta):
    def __init__(self):
        # Side effects
        enable_logging()
        self._increase_timeout_limit_for_tests_ci_cd()

        # Attributes
        self.urls = [ImpermaxURLS.list()[0]]  # just one page, for performance
        logger.info(f"Fetching only one page from Impermax for testing purposes.")

        self.html_resps = self._fetch_sample_html_responses_for_tests()
        self.parsed_pairs = self._parse_html_resps_for_tests()

    @staticmethod
    def _increase_timeout_limit_for_tests_ci_cd():
        _AsyncWebScraper.timeout_seconds = 90
        logger.info(f"Set timeout to {_AsyncWebScraper.timeout_seconds} seconds.")

    def _parse_html_resps_for_tests(self):
        logger.debug(f"_fetch_sample_html_responses_for_tests")
        return [_ImxPageParser(p).parse() for p in self.html_resps]

    def _fetch_sample_html_responses_for_tests(self):
        logger.debug(f"_fetch_sample_html_responses_for_tests")
        return _AsyncWebScraper().get(self.urls)


class WebScraperIntegrationTestsHelper(ABC, TestCase):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Reminding the call to this super.__init__() will silence verbose logging modules."""
        super().__init__(*args, **kwargs)
        singleton = _SingletonTestHelper()
        self.urls = singleton.urls
        self.html_resps = singleton.html_resps
        self.parsed_pairs = singleton.parsed_pairs
