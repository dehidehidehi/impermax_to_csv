from unittest import TestCase

from src.impermax.common.urls_enum import ImpermaxURLS
from src.impermax.dao.csv_dao import CsvDao
from src.impermax.services.data_providers.web_scraper.web_scraper_provider import WebScraperProvider


class TestCSVCreation(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.urls = ImpermaxURLS.list()
        cls.parsed_pairs = WebScraperProvider().get(cls.urls)
        cls.csv_converter = CsvDao(cls.parsed_pairs)

    def test_creating_does_not_raise(self):
        self.csv_converter.save()

    def test_saving_over_existing_file_does_not_raise(self):
        self.csv_converter.save()
        self.csv_converter.save()

    def test_all_csv_rows_have_same_length(self):
        pairs = self.csv_converter.split_pair_data
        all_pair_lengths = set(len(p) for p in pairs)
        self.assertEqual(len(all_pair_lengths), 1)
