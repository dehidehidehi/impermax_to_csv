import logging

from src.impermax.services.data_providers.web_scraper._dataclasses import ImxPair
from src.impermax.services.data_providers.web_scraper.test._helper import TestScraperHelper

logger = logging.getLogger(__name__)


class TestScraperParser(TestScraperHelper):

    def test_parsed_pair_returns_list_of_imxpairs(self):
        for pair_str in self.parsed_pairs:
            self.assertIsInstance(pair_str, list)
            self.assertTrue(all(isinstance(p, ImxPair) for p in pair_str))
