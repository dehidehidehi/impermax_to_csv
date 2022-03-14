import logging
from typing import Any

from src.impermax.services.web_scraper._async_scraper import (
    _AsyncWebScraper,
)
from src.impermax.services.web_scraper._dataclasses import ImxPair
from src.impermax.services.web_scraper._html_parser import _ImxPageParser

logger = logging.getLogger(__name__)


class WebScraperProvider:
    def get(self, urls: list[str]) -> list[list[ImxPair]]:
        pages = self._scrape(urls)
        logger.info("Parsing Impermax pages...")
        return [self._parse(p) for p in pages]

    @staticmethod
    def _scrape(urls: list[str]) -> list[list[Any]]:
        scraper = _AsyncWebScraper()
        logger.info("Scraping Impermax HTML...")
        results = scraper.asession.run(lambda: scraper.aget_all(urls))
        return results[0]

    @staticmethod
    def _parse(resp) -> list[ImxPair]:
        parser = _ImxPageParser(resp)
        logger.debug("Parsing Impermax page...")
        return parser.parse()
