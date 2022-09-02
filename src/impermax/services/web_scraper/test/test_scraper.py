import logging
from itertools import chain

from src.impermax.common.tests.test_helper import (
    WebScraperIntegrationTestsHelper,
)
from src.impermax.services.web_scraper._async_scraper import (
    _AsyncWebScraper,
)


class TestScraper(WebScraperIntegrationTestsHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        classpath = "src.impermax.services.data_providers.web_scraper._async_scraper"
        imx_page_scraping_status_output = logging.getLogger(classpath)
        imx_page_scraping_status_output.setLevel(logging.WARNING)

    def test_returns_true(self):
        self.assertTrue(self.html_resps)

    def test_html_resps_same_length_as_urls_in_str_enum(self):
        self.assertEqual(len(self.urls), len(self.html_resps))

    def test_html_resps_are_unique(self):
        unique_scraped_urls = set(r.url for r in self.html_resps)
        self.assertEqual(len(unique_scraped_urls), len(set(self.urls)))

    def test_html_resps_rendered_lending_pool_data(self):
        for r in self.html_resps:
            resp_includes_lending_pool_data: bool = any(
                "lending-pool" in lk for lk in r.html.links
            )
            self.assertTrue(
                resp_includes_lending_pool_data, f"No lending pool data for: {r.url}"
            )

    def test_7_days_average_apr_tab_was_selected_for_all_pages(self):
        selector_7day_stats = _AsyncWebScraper.TabSelectors.STATS_7DAYS_AVERAGE
        all_tabs_from_all_pages = list(
            chain.from_iterable(r.html.find(selector_7day_stats) for r in self.html_resps)
        )
        all_text_from_all_tabs = list(tab.text for tab in all_tabs_from_all_pages)
        self.assertEqual(
            all_text_from_all_tabs.count("7 days average"), len(self.html_resps)
        )
