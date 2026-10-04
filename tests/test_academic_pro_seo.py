from pathlib import Path
import json
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'assets/site.js').read_text(encoding='utf-8')
CSS=(ROOT/'assets/style.css').read_text(encoding='utf-8')
BASE='https://yasinfanaei.github.io/yasinfanaeishahroudi'
NAME_VARIANTS=[
    'یاسین فنائی',
    'یاسین فنایی',
    'yasinfanaei',
    'Yasin Fanaei Shahroudi',
    'yasinfanaeishahroudi',
    'yasin fanaei shahroudi',
]

class AcademicProSeoTests(unittest.TestCase):
    def test_static_seo_files_and_bilingual_404_exist(self):
        robots=(ROOT/'robots.txt')
        sitemap=(ROOT/'sitemap.xml')
        notfound=(ROOT/'404.html')
        self.assertTrue(robots.exists())
        self.assertTrue(sitemap.exists())
        self.assertTrue(notfound.exists())
        self.assertIn(f'Sitemap: {BASE}/sitemap.xml', robots.read_text(encoding='utf-8'))
        sm=sitemap.read_text(encoding='utf-8')
        for url in (f'{BASE}/',f'{BASE}/fa/',f'{BASE}/news.html',f'{BASE}/fa/search.html'):
            self.assertIn(url,sm)
        nf=notfound.read_text(encoding='utf-8')
        self.assertIn('Page not found',nf)
        self.assertIn('صفحه پیدا نشد',nf)

    def test_project_homepages_have_project_canonical_and_hreflang(self):
        en=(ROOT/'index.html').read_text(encoding='utf-8')
        fa=(ROOT/'fa/index.html').read_text(encoding='utf-8')
        self.assertIn(f'rel="canonical" href="{BASE}/"',en)
        self.assertIn(f'hreflang="en" href="{BASE}/"',en)
        self.assertIn(f'hreflang="fa" href="{BASE}/fa/"',en)
        self.assertIn(f'rel="canonical" href="{BASE}/fa/"',fa)
        self.assertIn(f'hreflang="en" href="{BASE}/"',fa)
        self.assertIn(f'hreflang="fa" href="{BASE}/fa/"',fa)

    def test_javascript_uses_project_site_url_for_rendered_canonicals(self):
        design=json.loads((ROOT/'content/settings/design.json').read_text(encoding='utf-8'))
        self.assertEqual(design['seo']['site_url'],BASE)
        for token in ('function canonicalUrl','function updateStructuredData','application/ld+json','ProfilePage','Person','sameAs'):
            self.assertIn(token,JS)

    def test_homepages_expose_identity_without_javascript(self):
        en=(ROOT/'index.html').read_text(encoding='utf-8')
        fa=(ROOT/'fa/index.html').read_text(encoding='utf-8')
        for token in ('Yasin Fanaei Shahroudi','PhD Student in Public Economics','Semnan University','application/ld+json','https://schema.org','sameAs'):
            self.assertIn(token,en)
        for token in ('یاسین فنائی شاهرودی','دانشجوی دکتری اقتصاد بخش عمومی','دانشگاه سمنان','application/ld+json','https://schema.org','sameAs'):
            self.assertIn(token,fa)

    def test_name_variants_are_structured_metadata_without_visual_changes(self):
        for locale in ('en','fa'):
            profile=json.loads((ROOT/f'content/{locale}/profile.json').read_text(encoding='utf-8'))
            site=json.loads((ROOT/f'content/{locale}/site.json').read_text(encoding='utf-8'))
            for variant in NAME_VARIANTS:
                self.assertIn(variant, profile.get('alternate_names', []), f'{locale} profile missing {variant}')
                self.assertIn(variant, site.get('keywords', []), f'{locale} keywords missing {variant}')
        for html_path in (ROOT/'index.html', ROOT/'fa/index.html'):
            html=html_path.read_text(encoding='utf-8')
            for variant in NAME_VARIANTS:
                self.assertIn(variant, html, f'{html_path} missing {variant}')
        self.assertIn('profile.alternate_names', JS)
        self.assertIn('person.alternateName', JS)

    def test_google_search_console_verification_tag_is_on_project_homepage(self):
        en=(ROOT/'index.html').read_text(encoding='utf-8')
        self.assertIn('<meta name="google-site-verification" content="WaiorulwqNLqZ582mRY0-LFz59F2rAhdh12W2OpY1uM"', en)

    def test_analytics_is_opt_in_and_disabled_by_default(self):
        design=json.loads((ROOT/'content/settings/design.json').read_text(encoding='utf-8'))
        self.assertFalse(design['analytics']['enabled'])
        self.assertIn('function initAnalytics',JS)
        self.assertIn("analytics.enabled",JS)
        self.assertIn('googletagmanager.com/gtag/js',JS)

    def test_shared_seo_settings_are_cms_managed(self):
        cfg=yaml.safe_load((ROOT/'.pages.yml').read_text(encoding='utf-8'))
        entry=next(e for e in cfg['content'] if e.get('name')=='design_branding')
        names={f['name'] for f in entry['fields']}
        self.assertIn('seo',names)

    def test_indexing_policy_is_dashboard_controlled(self):
        design=json.loads((ROOT/'content/settings/design.json').read_text(encoding='utf-8'))
        self.assertTrue(design['seo']['indexing_enabled'])
        self.assertIn('indexing_enabled', JS)
        self.assertIn('meta[name=\"robots\"]', JS)
        self.assertIn('noindex,nofollow', JS)

    def test_accessibility_and_performance_hooks_are_present(self):
        self.assertIn(':focus-visible',CSS)
        self.assertIn('@media (prefers-reduced-motion: reduce)',CSS)
        self.assertIn('decoding="async"',JS)
        self.assertIn('fetchpriority="high"',JS)

if __name__=='__main__':unittest.main()
