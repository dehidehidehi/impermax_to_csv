"""Adds pool address to previous csv files"""
import csv
from datetime import datetime
from pathlib import Path

from impermax.dirty_analyser.extract_data import load_csv, get_list_of_csv_paths

UP_TO_DATE_CSV = '/home/dehi/PycharmProjects/impermax_to_csv/output/impermax_7_days_2021-12-12T18-22.csv'


def update_rows_with_contract_address(reference_csv, loaded_csv) -> list[dict]:
    updated_pairs = list()
    for p in loaded_csv:
        contract = next((
            n['contract'] for n in reference_csv if
            n['blockchain'] == p['blockchain'] and
            n['pair'] == p['pair'] and
            n['dex'] == p['dex']
        ), None)
        if not contract:
            continue  # the pool was deleted (eg: ETH/NYAN on Arbitrum)
        p['contract'] = contract
        updated_pairs.append(p)
    return updated_pairs


def _overwrite_csv(the_path: Path, updated_rows: list[dict]) -> None:
    with open(str(the_path), mode='w+', encoding='UTF-8', newline='\n') as csv_file:
        headers = updated_rows[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)


def main():
    reference_csv = load_csv(UP_TO_DATE_CSV, the_date=datetime.now())
    for csv_file in get_list_of_csv_paths():
        loaded = load_csv(csv_file, the_date=datetime.now())
        updated_rows = update_rows_with_contract_address(reference_csv, loaded)
        for row in updated_rows:
            del row['datetime']
        _overwrite_csv(csv_file, updated_rows)
        ...


if __name__ == '__main__':
    main()