import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_URL = 'https://yasinfanaei.github.io/yasinfanaeishahroudi'
BASE = '/yasinfanaeishahroudi'

class ProjectSiteBasePathTests(unittest.TestCase):
    def _build_project_site(self, td: str) -> Path:
        work = Path(td) / 'repo'
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('_site', '__pycache__', '*.pyc'))
        design_path = work / 'content/settings/design.json'
        design = json.loads(design_path.read_text(encoding='utf-8'))
        design['seo']['site_url'] = PROJECT_URL
        design_path.write_text(json.dumps(design, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        out = Path(td) / 'site'
        from src.build_site import build_site
        build_site(work, out)
        return out

    def test_project_site_prefixes_browser_routes_assets_and_search_index(self):
        with tempfile.TemporaryDirectory() as td:
            out = self._build_project_site(td)
            home = (out / 'index.html').read_text(encoding='utf-8')
            search = (out / 'search/index.html').read_text(encoding='utf-8')
            index = json.loads((out / 'search-index.en.json').read_text(encoding='utf-8'))
            not_found = (out / '404.html').read_text(encoding='utf-8')

            self.assertIn(f'href="{BASE}/assets/style.css"', home)
            self.assertIn(f'src="{BASE}/assets/site.js"', home)
            self.assertIn(f'href="{BASE}/research/"', home)
            self.assertIn(f'href="{BASE}/fa/"', home)
            self.assertIn(f'data-index-url="{BASE}/search-index.en.json"', search)
            self.assertTrue(index)
            self.assertTrue(all(item['url'].startswith(BASE + '/') for item in index), index)
            self.assertIn(f'href="{BASE}/"', not_found)
            self.assertIn(f'href="{BASE}/fa/"', not_found)

    def test_project_site_keeps_canonical_and_sitemap_on_project_url(self):
        with tempfile.TemporaryDirectory() as td:
            out = self._build_project_site(td)
            home = (out / 'index.html').read_text(encoding='utf-8')
            research = (out / 'research/index.html').read_text(encoding='utf-8')
            sitemap = (out / 'sitemap.xml').read_text(encoding='utf-8')
            robots = (out / 'robots.txt').read_text(encoding='utf-8')

            self.assertIn(f'<link rel="canonical" href="{PROJECT_URL}/">', home)
            self.assertIn(f'<link rel="canonical" href="{PROJECT_URL}/research/">', research)
            self.assertIn(f'<loc>{PROJECT_URL}/research/</loc>', sitemap)
            self.assertIn(f'Sitemap: {PROJECT_URL}/sitemap.xml', robots)

if __name__ == '__main__':
    unittest.main()
