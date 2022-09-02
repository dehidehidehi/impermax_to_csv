import asyncio
import logging
from enum import IntEnum, Enum
from functools import cached_property
from textwrap import dedent
from typing import Optional

import pyppeteer.errors
from pyppeteer.page import Page
from requests_html import AsyncHTMLSession, HTMLResponse, HTML, DEFAULT_ENCODING

from src.impermax.common.enums.imx_urls_enum import ImpermaxURLS
from src.impermax.common.extended_enum import ExtendedEnum

logger = logging.getLogger(__name__)


class _AsyncWebScraper:

    class Periods(ExtendedEnum, IntEnum):
        AVG_7_DAYS = 1
        AVG_24_HOURS = 2
        CURRENT = 3

    class TabSelectors(str, Enum):
        __DATA_TABLE_HEADER_ROW = ".pairs-table-header"

        # Note:
        # The issue with using the 7 days stat button as an indicator of a loaded page
        # is that, in fact, it is not the last element to be loaded.
        # We still need the selector for clicking on it via the headless browser, though.
        __DAYS_7_STATS_BUTTON_FAST = "div.home > div > div > div > div > div:nth-child(1) > span"  # fast
        __DAYS_7_STATS_BUTTON_SLOW = ".selector > .option:nth-child(1) > span"  # slow

        STATS_7DAYS_AVERAGE = __DAYS_7_STATS_BUTTON_FAST
        PAGE_IS_LOADED = __DATA_TABLE_HEADER_ROW

    timeout_seconds: int = 30

    @cached_property
    def asession(self):
        return AsyncHTMLSession(browser_args=['--no-sandbox'])

    def get(self, urls: list[str]):
        logger.info("Scraping Impermax pages...")
        results = self.asession.run(lambda: self._aget_all(urls))
        results = [r for r in results[0] if r is not None]
        return results

    async def _aget_all(self, urls):
        tasks = await asyncio.gather(*(self._aget_rendered(url) for url in urls))
        return tasks

    async def _aget_rendered(self, url: str) -> Optional[HTMLResponse]:
        logger.debug(f"{url}\t\tfetching...")
        resp: HTMLResponse = await self.asession.get(url)
        try:
            await self._wait_for_page_content_to_load(resp)
        except pyppeteer.errors.TimeoutError as e:
            msg = dedent(f"""
            Timeout when fetching {url}, you may want to check whether Impermax is having trouble loading pair data.
            Error msg: {e}""")
            logger.warning(msg)
            return

        await self._click_7_days_data_tab(resp)
        updated_content = await resp.html.page.content()

        await self._update_html_response_with_updated_content(resp, updated_content)
        logger.info(f"""{url}       OK""")
        return resp

    async def _wait_for_page_content_to_load(self, r: HTMLResponse) -> None:
        r.html.page: Page
        await r.html.arender(keep_page=True)
        await r.html.page.waitForSelector(
            self.TabSelectors.PAGE_IS_LOADED.value,
            # options={
            #     "visible": True,
            #     "timeout": self.timeout_seconds * 2000,
            # },
        )
        # artificial wait
        await asyncio.sleep(0.25)

    async def _click_7_days_data_tab(self, r: HTMLResponse) -> None:
        await r.html.page.click(selector=self.TabSelectors.STATS_7DAYS_AVERAGE.value)

    @staticmethod
    async def _update_html_response_with_updated_content(
        html_resp: HTMLResponse, new_content_html: str
    ) -> None:
        """Inspired by the source code of the Async HTML Response arender() method."""
        html = HTML(
            url=html_resp.url,
            html=new_content_html.encode(DEFAULT_ENCODING),
            default_encoding=DEFAULT_ENCODING,
        )
        html_resp.html.__dict__.update(html.__dict__)


if __name__ == '__main__':
    _AsyncWebScraper().get(ImpermaxURLS.list())
