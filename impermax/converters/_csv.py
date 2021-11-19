import csv
from datetime import datetime
from itertools import chain

from impermax.common.consts import OUTPUT_PATH
from impermax.converters.abc import ImpermaxOutputABC
from impermax.fetcher.scraper.parser import IMXPair


class ImpermaxToCSV(ImpermaxOutputABC):

    def __init__(self, pairs: list[list[IMXPair]]):
        self.pairs = pairs

    @property
    def file_name(self) -> str:
        current_date = datetime.now().isoformat()[:16].replace(':', '-')  # removes illegal filename chars ':'
        return f'impermax_7_days_{current_date}.csv'

    @property
    def split_pair_data(self) -> list[list[str]]:
        all_pairs = list(chain.from_iterable(self.pairs))
        left_pairs = [(p.chain, p.pair, p.dex, *str(p.left).split('\t'), p.leveraged_apr, p.leveraged_apr_multiplier) for p in all_pairs]
        right_pairs = [(p.chain, p.pair, p.dex, *str(p.right).split('\t'), p.leveraged_apr, p.leveraged_apr_multiplier) for p in all_pairs]
        successive_pairs = list()
        for lp, rp in zip(left_pairs, right_pairs):
            successive_pairs.append(lp)
            successive_pairs.append(rp)
        return successive_pairs

    def save(self) -> None:
        self._save_as_csv()

    def _save_as_csv(self) -> None:
        self._create_output_dir()
        with open(str(OUTPUT_PATH / self.file_name), mode='w+', encoding='UTF-8', newline='\n') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['blockchain', 'pair', 'dex', 'ticker', 'supply', 'supply_apr', 'borrowed', 'borrowed_apr', 'leveraged_apr', 'leveraged_apr_multiplier'])
            writer.writerows(self.split_pair_data)
