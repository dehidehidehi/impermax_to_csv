"""Fast and dirty way to do some data analysis from the generated CSV files."""

import csv
from datetime import datetime
from pathlib import Path
from typing import Union

from impermax.common.consts import OUTPUT_PATH


def get_list_of_csv_paths(csv_dir: Union[str, Path] = OUTPUT_PATH) -> list[Path]:
    return list(csv_dir.iterdir())

def load_csv(path: str, the_date: datetime) -> ...:
    parsed_rows = list()
    with open(path, mode='r', encoding='UTF-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            row['datetime'] = the_date
            parsed_rows.append(row)
    return parsed_rows

def extract_datetime_from_csv_title(name: str) -> datetime:
    _, _, str_date = name.replace('.csv', '').rpartition('_')
    the_date, _, the_time = str_date.rpartition('T')
    the_time = the_time.replace('-', ':')
    the_datetime = datetime.fromisoformat(the_date + 'T' + the_time)
    return the_datetime

def load_all_csv() -> list[dict]:
    all_data = list()
    for p in get_list_of_csv_paths():
        dt = extract_datetime_from_csv_title(p.name)
        parsed_csv = load_csv(str(p), dt)
        all_data.extend(parsed_csv)
    return all_data



if __name__ == '__main__':
    all_data = load_all_csv()
    ...
