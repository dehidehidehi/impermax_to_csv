from src.impermax.common.extended_enum import ExtendedEnum


class PlottableColumns(str, ExtendedEnum):
    SUPPLY = "supply"
    SUPPLY_APR = "supply_apr"
    BORROWED = "borrowed"
    BORROWED_APR = "borrowed_apr"
