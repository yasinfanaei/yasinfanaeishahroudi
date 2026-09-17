from pathlib import Path
import json
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'assets/site.js').read_text(encoding='utf-8')
CSS=(ROOT/'assets/style.css').read_text(encoding='utf-8')
PAGES=['index.html','research.html','publications.html','experience.html','cv.html','contact.html','teaching.html','news.html','search.html']

class AcademicProSeoTests(unittest.TestCase):
    def test_static_seo_files_and_bilingual_404_exist(self):
        robots=(ROOT/'robots.txt')
        sitemap=(ROOT/'sitemap.xml')
        notfound=(ROOT/'404.html')
        self.assertTrue(robots.exists())
        self.assertTrue(sitemap.exists())
        self.assertTrue(notfound.exists())
        self.assertIn('Sitemap: https://yasinfanaei.github.io/sitemap.xml', robots.read_text(encoding='utf-8'))
        sm=sitemap.read_text(encoding='utf-8')
        for url in ('https://yasinfanaei.github.io/','https://yasinfanaei.github.io/fa/','https://yasinfanaei.github.io/news.html','https://yasinfanaei.github.io/fa/search.html'):
            self.assertIn(url,sm)
        nf=notfound.read_text(encoding='utf-8')
        self.assertIn('Page not found',nf)
        self.assertIn('صفحه پیدا نشد',nf)

    def test_all_fixed_pages_have_absolute_canonical_and_hreflang(self):
        for rel in PAGES:
            text=(ROOT/rel).read_text(encoding='utf-8')
            self.assertIn('rel="canonical" href="https://yasinfanaei.github.io/',text,rel)
            self.assertIn('hreflang="en" href="https://yasinfanaei.github.io/',text,rel)
            self.assertIn('hreflang="fa" href="https://yasinfanaei.github.io/fa/',text,rel)
        for rel in PAGES:
            text=(ROOT/'fa'/rel).read_text(encoding='utf-8')
            self.assertIn('rel="canonical" href="https://yasinfanaei.github.io/fa/',text,rel)
            self.assertIn('hreflang="en" href="https://yasinfanaei.github.io/',text,rel)
            self.assertIn('hreflang="fa" href="https://yasinfanaei.github.io/fa/',text,rel)

    def test_javascript_uses_page_seo_and_person_profilepage_structured_data(self):
        for token in ('page_seo','function updateStructuredData','application/ld+json','ProfilePage','Person','sameAs'):
            self.assertIn(token,JS)

    def test_analytics_is_opt_in_and_disabled_by_default(self):
        design=json.loads((ROOT/'content/settings/design.json').read_text(encoding='utf-8'))
        self.assertFalse(design['analytics']['enabled'])
        self.assertIn('function initAnalytics',JS)
        self.assertIn("analytics.enabled",JS)
        self.assertIn('googletagmanager.com/gtag/js',JS)

    def test_shared_seo_settings_are_cms_managed(self):
        design=json.loads((ROOT/'content/settings/design.json').read_text(encoding='utf-8'))
        self.assertEqual(design['seo']['site_url'],'https://yasinfanaei.github.io/yasinfanaeishahroudi')
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
