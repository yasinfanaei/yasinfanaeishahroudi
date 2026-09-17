from pathlib import Path
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]

class AcademicProCiTests(unittest.TestCase):
    def test_validation_workflow_runs_full_checks_on_push_pr_and_manual_dispatch(self):
        path=ROOT/'.github/workflows/validate.yml'
        self.assertTrue(path.exists())
        text=path.read_text(encoding='utf-8')
        for token in ('workflow_dispatch:','push:','pull_request:','python -m unittest discover','python scripts/check_site.py','node --check src/static/site.js'):
            self.assertIn(token,text)
        self.assertIn('payload:',text)

    def test_pages_cms_exposes_validate_site_action(self):
        cfg=yaml.safe_load((ROOT/'.pages.yml').read_text(encoding='utf-8'))
        action=next((a for a in cfg.get('actions',[]) if a.get('name')=='validate-site'),None)
        self.assertIsNotNone(action)
        self.assertEqual(action.get('workflow'),'validate.yml')
        self.assertEqual(action.get('ref'),'current')

    def test_release_checker_covers_static_source_and_generated_build(self):
        source=(ROOT/'scripts/check_site.py').read_text(encoding='utf-8')
        built=(ROOT/'scripts/check_build.py').read_text(encoding='utf-8')
        self.assertIn('validate_repository',source)
        self.assertIn('rglob(',source)
        self.assertIn('*.docx',source)
        self.assertIn('search-index.en.json',built)
        self.assertIn('sitemap.xml',built)


if __name__=='__main__':unittest.main()
