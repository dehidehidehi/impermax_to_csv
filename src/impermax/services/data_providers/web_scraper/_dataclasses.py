from dataclasses import dataclass


@dataclass
class IMXToken:
    contract: str
    ticker: str
    supply: float
    supply_apr: float
    borrowed: float
    borrowed_apr: float

    def __str__(self):
        token_data = [
            self.ticker,
            self.supply,
            self.supply_apr,
            self.borrowed,
            self.borrowed_apr,
            self.contract,
        ]
        return "\t".join(str(c) for c in token_data)


@dataclass
class ImxPair:
    contract: str
    chain: str
    pair: str
    dex: str
    left: IMXToken
    right: IMXToken
    leveraged_apr: float
    leveraged_apr_multiplier: float

    def __str__(self):
        d = [self.chain, self.pair, self.dex, self.contract]
        return "\t".join(str(i) for i in d)
