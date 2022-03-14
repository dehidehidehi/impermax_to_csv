from src.impermax.common.extended_enum import ExtendedEnum


class ImpermaxURLS(str, ExtendedEnum):
    ETH = "https://app.impermax.finance/"
    MATIC = "https://polygon.impermax.finance/"
    ARB = "https://arbitrum.impermax.finance/"
    AVAX = "https://avalanche.impermax.finance/"
    MOONRIVER = "https://moonriver.impermax.finance/"
    FANTOM = "https://fantom.impermax.finance/"
