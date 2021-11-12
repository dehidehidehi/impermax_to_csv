import logging

from impermax.common.tests.test_common import TestScraperHelper
from impermax.fetcher.scraper.parser import IMXPair

logger = logging.getLogger(__name__)


class TestScraperParser(TestScraperHelper):

    def test_parsed_pair_returns_list_of_imxpairs(self):
        for pair_str in self.parsed_pairs:
            self.assertIsInstance(pair_str, list)
            self.assertTrue(all(isinstance(p, IMXPair) for p in pair_str))
