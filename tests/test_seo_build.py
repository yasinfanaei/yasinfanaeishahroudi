import json, tempfile, unittest
from pathlib import Path

class SeoBuildTests(unittest.TestCase):
    def setUp(self): self.root=Path(__file__).resolve().parents[1]
    def test_build_emits_absolute_canonical_hreflang_jsonld_sitemap_robots_and_indexes(self):
        from src.build_site import build_site
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'_site'; build_site(self.root,out)
            html=(out/'research/index.html').read_text(encoding='utf-8')
            self.assertIn('rel="canonical" href="https://yasinfanaei.github.io/yasinfanaeishahroudi/research/"',html)
            self.assertIn('hreflang="fa" href="https://yasinfanaei.github.io/yasinfanaeishahroudi/fa/research/"',html)
            self.assertIn('BreadcrumbList',html)
            home=(out/'index.html').read_text(encoding='utf-8')
            self.assertIn('ProfilePage',home); self.assertIn('Person',home)
            sitemap=(out/'sitemap.xml').read_text(encoding='utf-8')
            self.assertIn('https://yasinfanaei.github.io/yasinfanaeishahroudi/research/',sitemap)
            self.assertNotIn('.html</loc>',sitemap)
            robots=(out/'robots.txt').read_text(encoding='utf-8')
            self.assertIn('Sitemap: https://yasinfanaei.github.io/yasinfanaeishahroudi/sitemap.xml',robots)
            index=json.loads((out/'search-index.en.json').read_text(encoding='utf-8'))
            self.assertTrue(any(x['url']=='/yasinfanaeishahroudi/research/' for x in index))
    def test_site_url_setting_migrates_all_absolute_seo(self):
        from src.seo import absolute_url
        self.assertEqual(absolute_url('https://example.com/','/fa/research/'),'https://example.com/fa/research/')
    def test_draft_and_noindex_pages_are_excluded_from_sitemap_and_search(self):
        from src.seo import public_indexable
        self.assertFalse(public_indexable({'status':'draft','seo':{}},True))
        self.assertFalse(public_indexable({'status':'published','seo':{'noindex':True}},True))
        self.assertTrue(public_indexable({'status':'published','seo':{}},True))

class SitemapToggleSemanticsTests(unittest.TestCase):
    def test_sitemap_toggle_does_not_force_noindex(self):
        from src.seo import page_indexable, page_in_sitemap
        page={'status':'published','show_in_sitemap':False,'seo':{'noindex':False}}
        self.assertTrue(page_indexable(page,True))
        self.assertFalse(page_in_sitemap(page,True))

class CanonicalOverrideTests(unittest.TestCase):
    def test_explicit_https_canonical_override_is_supported(self):
        from src.seo import page_seo_context
        page={'id':'custom','slug':'custom','translation_key':'custom','title':'Custom','status':'published','show_in_sitemap':True,'seo':{'description':'x','canonical_override':'https://example.org/preferred/','noindex':False}}
        pairs={'custom':{'en':page}}
        design={'seo':{'site_url':'https://example.com','indexing_enabled':True,'structured_data_enabled':False},'branding':{}}
        ctx=page_seo_context('en',page,pairs,design,{'name':'Test'})
        self.assertEqual(ctx['canonical'],'https://example.org/preferred/')
