from src.impermax.common.tests.test_common import TestScraperHelper
from src.impermax.converters._csv import ImpermaxToCSV


class TestCSVCreation(TestScraperHelper):

    @classmethod
    def setUpClass(cls) -> None:
        cls.csv_converter = ImpermaxToCSV(pairs=cls.parsed_pairs)

    def test_creating_does_not_raise(self):
        self.csv_converter.save()

    def test_saving_over_existing_file_does_not_raise(self):
        self.csv_converter.save()
        self.csv_converter.save()

    def test_all_csv_rows_have_same_length(self):
        pairs = self.csv_converter.split_pair_data
        all_pair_lengths = set(len(p) for p in pairs)
        self.assertEqual(len(all_pair_lengths), 1)
