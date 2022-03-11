import logging
from dataclasses import dataclass
from functools import cached_property

from requests_html import HTMLResponse

from src.impermax.fetcher.enums import ImpermaxURLS

logger = logging.getLogger(__name__)


@dataclass
class IMXToken:
    contract: str
    ticker: str
    supply: float
    supply_apr: float
    borrowed: float
    borrowed_apr: float

    def __str__(self):
        token_data = [self.ticker, self.supply, self.supply_apr, self.borrowed, self.borrowed_apr, self.contract]
        return '\t'.join(str(c) for c in token_data)


@dataclass
class IMXPair:
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
        return '\t'.join(str(i) for i in d)


class IMXChainPageParser:

    def __init__(self, http_resp: HTMLResponse):
        self.chain_http_resp = http_resp

    @cached_property
    def blockchain_name(self) -> str:
        chain = ImpermaxURLS(self.chain_http_resp.url).name
        return chain

    def parse(self) -> list[IMXPair]:
        parsed_page = [self._mk_pair(split_row) for split_row in self._pairs_text]
        logger.debug(f'{self.chain_http_resp.url}\t\tParse OK')
        return parsed_page

    @cached_property
    def _pairs_text(self) -> list[list]:
        selector = 'a.pairs-table-row'
        pairs = [list(row.links) + row.text.split() for row in self.chain_http_resp.html.find(selector)]
        return pairs

    def _mk_pair(self, split_row: list[str]) -> IMXPair:
        chain = self.blockchain_name
        contract_address = split_row.pop(0)
        _, _, contract_address = contract_address.rpartition('/')

        pair, dex, leveraged_apr, leveraged_multiplier = split_row[0], split_row[1], split_row[-2], split_row[-1]
        t1_ticker, t1_supply, t1_borrowed, t1_supply_apr, t1_borrow_apr, *_ = tuple(split_row[2:-3:2])
        t1_supply, t1_supply_apr, t1_borrowed, t1_borrow_apr = self._clean_row_strings(t1_supply, t1_supply_apr, t1_borrowed, t1_borrow_apr)

        t2_ticker, t2_supply, t2_borrowed, t2_supply_apr, t2_borrow_apr, *_ = tuple(split_row[3:-2:2])
        t2_supply, t2_supply_apr, t2_borrowed, t2_borrow_apr = self._clean_row_strings(t2_supply, t2_supply_apr, t2_borrowed, t2_borrow_apr)

        t1 = IMXToken(contract=contract_address, ticker=t1_ticker, supply=t1_supply, supply_apr=t1_supply_apr, borrowed=t1_borrowed, borrowed_apr=t1_borrow_apr)
        t2 = IMXToken(contract=contract_address, ticker=t2_ticker, supply=t2_supply, supply_apr=t2_supply_apr, borrowed=t2_borrowed, borrowed_apr=t2_borrow_apr)
        pair = IMXPair(contract=contract_address, chain=chain, pair=pair, dex=dex, left=t1, right=t2, leveraged_apr=leveraged_apr,
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
