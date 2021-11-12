from impermax.common.tests.test_common import TestScraperHelper


class TestScraper(TestScraperHelper):

    def test_returns_true(self):
        self.assertTrue(self.html_resps)

    def test_html_resps_same_length_as_urls_in_str_enum(self):
        self.assertEqual(len(self.urls), len(self.html_resps))

    def test_html_resps_are_unique(self):
        unique_scraped_urls = set(r.url for r in self.html_resps)
        self.assertEqual(len(unique_scraped_urls), len(set(self.urls)))

    def test_html_resps_rendered_lending_pool_data(self):
        for r in self.html_resps:
            resp_includes_lending_pool_data: bool = any('lending-pool' in lk for lk in r.html.links)
            self.assertTrue(resp_includes_lending_pool_data, f'No lending pool data for: {r.url}')
