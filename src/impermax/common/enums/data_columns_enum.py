from enum import Enum


class PlottableColumns(str, Enum):
    SUPPLY = "supply"
    SUPPLY_APR = "supply_apr"
    BORROWED = "borrowed"
    BORROWED_APR = "borrowed_apr"
