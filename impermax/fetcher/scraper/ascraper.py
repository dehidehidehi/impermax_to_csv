import asyncio
import logging
from enum import IntEnum, Enum
from functools import cached_property

from requests_html import AsyncHTMLSession, HTMLResponse, HTML, DEFAULT_ENCODING

from impermax.common.extended_classes import ExtendedEnum
from impermax.fetcher.abc import DataFetcherABC

logger = logging.getLogger(__name__)


class _ScrapeImpermax(DataFetcherABC):

    sleep_seconds: int = 7

    class Periods(ExtendedEnum, IntEnum):
        AVG_7_DAYS = 1
        AVG_24_HOURS = 2
        CURRENT = 3

    class TabSelectors(str, Enum):
        CSS_SELECTOR_7_DAYS = '#impermax-app > div > div > div > div.home > div.mt-4.container > div > div.text-right.col-sm-6 > div > div:nth-child(1) > span'
        XPATH_SELECTOR_7_DAYS = "//span[contains(., '7 days average')]"

    @cached_property
    def asession(self):
        return AsyncHTMLSession()

    def get(self, urls: list[str]):
        logger.info('Scraping Impermax pages...')
        results = self.asession.run(lambda: self.aget_all(urls))
        return results[0]

    async def aget_all(self, urls):
        tasks = await asyncio.gather(*(self._aget_rendered(url) for url in urls))
        return tasks

    async def _aget_rendered(self, url: str):
        logger.debug(f'{url}\t\tfetching...')
        resp = await self.asession.get(url)
        await self._load_js_content(resp)
        await self._click_7_days_data_tab(resp)
        updated_content = await resp.html.page.content()
        await self._update_HTMLResponse_with_updated_content(resp, updated_content)
        logger.info(f'{url}\t\tOK')
        return resp

    async def _load_js_content(self, r: HTMLResponse) -> None:
        await r.html.arender(wait=0, sleep=self.sleep_seconds, timeout=15, keep_page=True)

    @staticmethod
    async def _click_7_days_data_tab(r: HTMLResponse) -> None:
        """Xpath cheatsheet: https://devhints.io/xpath"""
        selector = _ScrapeImpermax.TabSelectors.CSS_SELECTOR_7_DAYS.value
        script = """
            () => {
                const item = document.querySelector("%s");
                item.click();
            }
        """ % selector
        await r.html.page.evaluate(script)

    @staticmethod
    async def _update_HTMLResponse_with_updated_content(html_resp: HTMLResponse, new_content_html: str) -> None:
        """Inspired by the source code of the Async HTML Response arender() method."""
        html = HTML(url=html_resp.url, html=new_content_html.encode(DEFAULT_ENCODING), default_encoding=DEFAULT_ENCODING)
        html_resp.html.__dict__.update(html.__dict__)
