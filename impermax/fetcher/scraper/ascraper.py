import asyncio
import logging
from enum import IntEnum
from functools import cached_property

from requests_html import AsyncHTMLSession, HTMLResponse

from impermax.common.extended_classes import ExtendedEnum
from impermax.fetcher.abc import DataFetcherABC

logger = logging.getLogger(__name__)


class _ScrapeImpermax(DataFetcherABC):

    class Periods(ExtendedEnum, IntEnum):
        AVG_7_DAYS = 1
        AVG_24_HOURS = 2
        CURRENT = 3

    @cached_property
    def asession(self):
        return AsyncHTMLSession()

    def get(self, urls: list[str]):
        results = self.asession.run(lambda: self.aget_all(urls))
        return results[0]

    async def aget_all(self, urls):
        tasks = await asyncio.gather(*(self._aget_rendered(url) for url in urls))
        return tasks

    async def _aget_rendered(self, url: str):
        resp = await self.asession.get(url)
        await self._load_js_content(resp)
        return resp

    async def _load_js_content(self, r: HTMLResponse) -> None:
        await r.html.arender(wait=0, sleep=3, timeout=15, keep_page=True)
