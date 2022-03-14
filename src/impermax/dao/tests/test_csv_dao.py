import logging

from src.impermax.common.tests.test_helper import TestScraperHelper
from src.impermax.dao.csv_dao import CsvDao


class TestCSVCreation(TestScraperHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        csv_output_logger = logging.getLogger("src.impermax.dao.csv_dao")
        csv_output_logger.setLevel(logging.WARNING)

    def setUp(self) -> None:
        self.csv_converter = CsvDao(self.parsed_pairs)

    def test_creating_does_not_raise(self):
        self.csv_converter.save()

    def test_saving_over_existing_file_does_not_raise(self):
        self.csv_converter.save()
        self.csv_converter.save()

    def test_all_csv_rows_have_same_length(self):
        pairs = self.csv_converter.split_pair_data
        all_pair_lengths = set(len(p) for p in pairs)
        self.assertEqual(len(all_pair_lengths), 1)
