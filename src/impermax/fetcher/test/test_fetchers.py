from functools import cached_property
from itertools import chain
from unittest import TestCase

from src.impermax.fetcher.enums import DataProvenances, ImpermaxURLS


class TestDataHelper(TestCase):

    @cached_property
    def strat_resps(self):
        urls = ImpermaxURLS.list()
        data_from_sources = [data_source().get(urls) for data_source in DataProvenances.list()]
        return data_from_sources


class TestDataFetcherABC(TestDataHelper):

    def test_get_method_on_all_base_classes(self):
        for d in (flattened_resps := list(chain.from_iterable(self.strat_resps))):
            self.assertTrue(d.ok)


class TestDataFetcher(TestDataHelper):
    """Testing all strategies at once."""
    pass