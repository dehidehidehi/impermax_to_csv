import logging
from unittest import TestCase

from impermax.common.consts import BASE_PATH
from impermax.fetcher.enums import ImpermaxURLS
from impermax.fetcher.scraper.ascraper import _ScrapeImpermax
from impermax.fetcher.scraper.parser import parse_impermax_chains

logger = logging.getLogger(__name__)


class TestCommonDir(TestCase):

    def test_base_path_points_to_base_impermax_dir(self):
        self.assertEqual(BASE_PATH.name, 'impermax')


class TestScraperHelper(TestCase):

    urls = ImpermaxURLS.list()
    html_resps = _ScrapeImpermax().get(urls)
    parsed_pairs = parse_impermax_chains(html_resps)
    logger.warning('Untested scraping parser, use with caution.')