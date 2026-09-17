from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'assets/site.js').read_text(encoding='utf-8')


class AcademicProPagesTests(unittest.TestCase):
    def test_search_and_news_pages_exist_in_both_locales(self):
        for rel, lang, direction, script in (
            ('search.html','en','', 'assets/site.js'),
            ('news.html','en','', 'assets/site.js'),
            ('fa/search.html','fa','dir="rtl"', '../assets/site.js'),
            ('fa/news.html','fa','dir="rtl"', '../assets/site.js'),
        ):
            path=ROOT/rel
            self.assertTrue(path.exists(), rel)
            text=path.read_text(encoding='utf-8')
            self.assertIn(f'lang="{lang}"', text)
            if direction:self.assertIn(direction,text)
            self.assertIn(script,text)

    def test_search_page_exposes_accessible_search_slots(self):
        for rel in ('search.html','fa/search.html'):
            text=(ROOT/rel).read_text(encoding='utf-8')
            self.assertIn('data-slot="search-input"', text)
            self.assertIn('data-slot="search-results"', text)
            self.assertIn('data-ui="search_title"', text)

    def test_news_page_and_homepage_expose_news_slots(self):
        for rel in ('news.html','fa/news.html'):
            text=(ROOT/rel).read_text(encoding='utf-8')
            self.assertIn('data-slot="news-intro"', text)
            self.assertIn('data-slot="news-list"', text)
        for rel in ('index.html','fa/index.html'):
            text=(ROOT/rel).read_text(encoding='utf-8')
            self.assertIn('data-home-section="news"', text)
            self.assertIn('data-slot="home-news-list"', text)

    def test_renderer_has_search_index_news_and_search_renderers(self):
        for token in (
            'function buildSearchIndex', 'function renderSearch', 'function renderNews',
            'function renderHomeNews', "search: ['profile'", "news: ['profile'"
        ):
            self.assertIn(token, JS)


if __name__ == '__main__':
    unittest.main()
