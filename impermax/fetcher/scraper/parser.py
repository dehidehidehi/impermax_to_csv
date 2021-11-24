from dataclasses import dataclass
from functools import cached_property
from typing import Union

from requests_html import HTMLResponse

from impermax.fetcher.enums import ImpermaxURLS


@dataclass
class IMXToken:
    ticker: str
    supply: float
    supply_apr: float
    borrowed: float
    borrowed_apr: float

    def __str__(self):
        token_data = [self.ticker, self.supply, self.supply_apr, self.borrowed, self.borrowed_apr]
        return '\t'.join(str(c) for c in token_data)


@dataclass
class IMXPair:
    chain: str
    pair: str
    dex: str
    left: IMXToken
    right: IMXToken
    leveraged_apr: float
    leveraged_apr_multiplier: float


class IMXChainPageParser:

    def __init__(self, http_resp: HTMLResponse):
        self.chain_http_resp = http_resp

    @cached_property
    def blockchain_name(self) -> str:
        chain = ImpermaxURLS(self.chain_http_resp.url).name
        return chain

    def parse(self) -> list[IMXPair]:
        return [self._mk_pair(row) for row in self._pairs_text]

    @cached_property
    def _pairs_text(self) -> list[str]:
        selector = 'a.pairs-table-row'
        pairs = [row.text for row in self.chain_http_resp.html.find(selector)]
        return pairs

    def _mk_pair(self, row: str) -> IMXPair:
        split_text = row.split()
        chain = self.blockchain_name
        pair, dex, leveraged_apr, leveraged_multiplier = split_text[0], split_text[1], split_text[-2], split_text[-1]
        t1_ticker, t1_supply, t1_borrowed, t1_supply_apr, t1_borrow_apr = tuple(split_text[2:-3:2])
        t1_supply, t1_supply_apr, t1_borrowed, t1_borrow_apr = self._clean_row_strings(t1_supply, t1_supply_apr, t1_borrowed, t1_borrow_apr)

        t2_ticker, t2_supply, t2_borrowed, t2_supply_apr, t2_borrow_apr = tuple(split_text[3:-2:2])
        t2_supply, t2_supply_apr, t2_borrowed, t2_borrow_apr = self._clean_row_strings(t2_supply, t2_supply_apr, t2_borrowed, t2_borrow_apr)

        t1 = IMXToken(ticker=t1_ticker, supply=t1_supply, supply_apr=t1_supply_apr, borrowed=t1_borrowed, borrowed_apr=t1_borrow_apr)
        t2 = IMXToken(ticker=t2_ticker, supply=t2_supply, supply_apr=t2_supply_apr, borrowed=t2_borrowed, borrowed_apr=t2_borrow_apr)
        pair = IMXPair(chain=chain, pair=pair, dex=dex, left=t1, right=t2, leveraged_apr=leveraged_apr,
                       leveraged_apr_multiplier=leveraged_multiplier)
        return pair

    @staticmethod
    def _clean_row_strings(supply: str, supply_apr: str, borrowed: str, borrowed_apr: str) -> tuple[float, ...]:
        supply = float(supply.replace('$', '').replace(',', ''))
        supply_apr = float(supply_apr.replace('%', '')) / 100
        borrowed = float(borrowed.replace('$', '').replace(',', ''))
        borrowed_apr = float(borrowed_apr.replace('%', '')) / 100
        return supply, supply_apr, borrowed, borrowed_apr


def parse_impermax_chains(http_resps: list[HTMLResponse]) -> list[list[IMXPair]]:
    return [IMXChainPageParser(resp).parse() for resp in http_resps]
