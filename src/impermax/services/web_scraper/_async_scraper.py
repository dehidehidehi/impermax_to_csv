import asyncio
import logging
from enum import IntEnum, Enum
from functools import cached_property

from pyppeteer.page import Page
from requests_html import AsyncHTMLSession, HTMLResponse, HTML, DEFAULT_ENCODING

from src.impermax.common.extended_enum import ExtendedEnum

logger = logging.getLogger(__name__)


class _AsyncWebScraper:
    class Periods(ExtendedEnum, IntEnum):
        AVG_7_DAYS = 1
        AVG_24_HOURS = 2
        CURRENT = 3

    class TabSelectors(str, Enum):
        CSS_SELECTOR_7_DAYS = (
            "div.home > div > div > div > div > div:nth-child(1) > span"
        )
        XPATH_SELECTOR_7_DAYS = "//span[contains(., '7 days average')]"

    timeout_seconds: int = 30
    selector_7_days_tab = TabSelectors.CSS_SELECTOR_7_DAYS.value

    @cached_property
    def asession(self):
        return AsyncHTMLSession()

    def get(self, urls: list[str]):
        logger.info("Scraping Impermax pages...")
        results = self.asession.run(lambda: self.aget_all(urls))
        return results[0]

    async def aget_all(self, urls):
        tasks = await asyncio.gather(*(self._aget_rendered(url) for url in urls))
        return tasks

    async def _aget_rendered(self, url: str):
        logger.debug(f"{url}\t\tfetching...")
        resp: HTMLResponse = await self.asession.get(url)

        await self._wait_for_page_content_to_load(resp)
        await self._click_7_days_data_tab(resp)
        updated_content = await resp.html.page.content()

        await self._update_html_response_with_updated_content(resp, updated_content)
        logger.info(f"{url}\t\tOK")
        return resp

    async def _wait_for_page_content_to_load(self, r: HTMLResponse) -> None:
        r.html.page: Page
        await r.html.arender(keep_page=True)
        await r.html.page.waitForSelector(
            self.selector_7_days_tab,
            options={
                "visible": True,
                "timeout": self.timeout_seconds * 1000,
            },
        )

    async def _click_7_days_data_tab(self, r: HTMLResponse) -> None:
        await r.html.page.click(selector=self.selector_7_days_tab)

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
