import logging

from src.impermax.common.tests.test_helper import WebScraperIntegrationTestsHelper
from src.impermax.services.web_scraper._dataclasses import ImxPair

logger = logging.getLogger(__name__)


class TestScraperParser(WebScraperIntegrationTestsHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_parsed_pair_returns_list_of_imxpairs(self):
        for pair_str in self.parsed_pairs:
            self.assertIsInstance(pair_str, list)
            self.assertTrue(all(isinstance(p, ImxPair) for p in pair_str))
