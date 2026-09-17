import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AcademicPro2AcceptanceTests(unittest.TestCase):
    def _copy_repo(self, td):
        dst = Path(td) / 'repo'
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('_site','__pycache__','*.pyc'))
        return dst

    def _build(self, root, td):
        from src.build_site import build_site
        out = Path(td) / 'site'
        build_site(root, out)
        return out

    def test_contact_marked_show_home_is_rendered_on_homepage(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._copy_repo(td)
            path = root / 'content/en/profile.json'
            profile = json.loads(path.read_text(encoding='utf-8'))
            profile['contacts'].append({
                'id':'public-office','type':'office','label':'Office','value':'Room 204',
                'url':'','enabled':True,'show_home':True,'show_contact':False,'show_footer':False
            })
            path.write_text(json.dumps(profile,ensure_ascii=False,indent=2),encoding='utf-8')
            out = self._build(root, td)
            html = (out/'index.html').read_text(encoding='utf-8')
            self.assertIn('Room 204', html)
            self.assertIn('Office', html)

    def test_unpublished_news_is_not_leaked_into_search_index(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._copy_repo(td)
            path = root / 'content/en/news.json'
            news = json.loads(path.read_text(encoding='utf-8'))
            news.setdefault('items',[]).append({'title':'UNPUBLISHED-SECRET-NEWS','date':'2026-09-16','summary':'private draft','published':False,'featured':False,'url':''})
            path.write_text(json.dumps(news,ensure_ascii=False,indent=2),encoding='utf-8')
            out = self._build(root, td)
            index = (out/'search-index.en.json').read_text(encoding='utf-8')
            self.assertNotIn('UNPUBLISHED-SECRET-NEWS', index)
            self.assertNotIn('private draft', index)

    def test_publication_page_has_text_type_status_year_filters_and_citation_helpers(self):
        with tempfile.TemporaryDirectory() as td:
            out = self._build(ROOT, td)
            html = (out/'publications/index.html').read_text(encoding='utf-8')
            for marker in ('data-publication-search','data-publication-type','data-publication-status','data-publication-year','data-citation-copy','data-bibtex','data-ris'):
                self.assertIn(marker, html)
            js = (out/'assets/site.js').read_text(encoding='utf-8')
            for marker in ('publicationType','publicationStatus','publicationYear','data-citation-copy','data-bibtex','data-ris'):
                self.assertIn(marker, js)

    def test_layout_presets_are_emitted_as_body_classes_and_have_css_rules(self):
        with tempfile.TemporaryDirectory() as td:
            out = self._build(ROOT, td)
            html = (out/'index.html').read_text(encoding='utf-8')
            for cls in ('layout-width-standard','layout-density-standard','layout-card-border','layout-header-standard','layout-corners-subtle'):
                self.assertIn(cls, html)
            css = (out/'assets/style.css').read_text(encoding='utf-8')
            for selector in ('.layout-width-narrow','.layout-width-wide','.layout-density-compact','.layout-density-spacious','.layout-card-elevated','.layout-corners-rounded'):
                self.assertIn(selector, css)

    def test_analytics_is_absent_by_default_and_opt_in_when_configured(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._copy_repo(td)
            out = self._build(root, td)
            self.assertNotIn('googletagmanager.com/gtag/js', (out/'index.html').read_text(encoding='utf-8'))
            path = root/'content/settings/design.json'
            design = json.loads(path.read_text(encoding='utf-8'))
            design['analytics']={'enabled':True,'provider':'google_analytics','measurement_id':'G-TEST12345'}
            path.write_text(json.dumps(design,ensure_ascii=False,indent=2),encoding='utf-8')
            out2 = Path(td)/'site2'
            from src.build_site import build_site
            build_site(root,out2)
            html=(out2/'index.html').read_text(encoding='utf-8')
            self.assertIn('googletagmanager.com/gtag/js?id=G-TEST12345',html)
            self.assertIn("gtag('config', 'G-TEST12345')",html)

    def test_new_custom_page_and_navigation_reference_build_without_code_changes(self):
        with tempfile.TemporaryDirectory() as td:
            root=self._copy_repo(td)
            page={
                'id':'working-papers','slug':'working-papers','translation_key':'working-papers','title':'Working Papers','menu_label':'Working Papers',
                'status':'published','layout':'standard','show_breadcrumbs':True,'show_in_sitemap':True,'redirect_from':[],
                'seo':{'title':'Working Papers | Yasin Fanaei Shahroudi','description':'Current working papers.','image':'','noindex':False},
                'blocks':[{'type':'heading','id':'working-papers-heading','enabled':True,'title':'Current work','level':'h2','lead':'Research in progress.'}]
            }
            (root/'content/pages/en/working-papers.json').write_text(json.dumps(page,ensure_ascii=False,indent=2),encoding='utf-8')
            site_path=root/'content/en/site.json'; site=json.loads(site_path.read_text(encoding='utf-8'))
            site['navigation'].append({'id':'working-papers-nav','label':'Working Papers','enabled':True,'destination':'page','page':'working-papers','url':'','section':'','new_tab':False,'children':[]})
            site_path.write_text(json.dumps(site,ensure_ascii=False,indent=2),encoding='utf-8')
            out=self._build(root,td)
            html=(out/'working-papers/index.html').read_text(encoding='utf-8')
            home=(out/'index.html').read_text(encoding='utf-8')
            self.assertIn('Current work',html)
            self.assertIn('Research in progress.',html)
            self.assertIn('href="/yasinfanaeishahroudi/working-papers/"',home)
            self.assertIn('Working Papers',home)

if __name__=='__main__': unittest.main()
