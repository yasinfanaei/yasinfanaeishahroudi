import tempfile
import unittest
from pathlib import Path

class StaticRenderingTests(unittest.TestCase):
    def test_built_home_contains_primary_content_without_runtime_fetch(self):
        from src.build_site import build_site
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'_site'; build_site(root,out)
            html=(out/'index.html').read_text(encoding='utf-8')
            self.assertIn('Yasin Fanaei Shahroudi',html)
            self.assertIn('<header',html); self.assertIn('<main',html); self.assertIn('<footer',html)
            self.assertIn('skip-link',html)
            self.assertNotIn('fetch("content/',html)
            self.assertEqual(html.count('<h1'),1)
    def test_persian_output_declares_rtl(self):
        from src.build_site import build_site
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'_site'; build_site(root,out)
            html=(out/'fa/index.html').read_text(encoding='utf-8')
            self.assertIn('lang="fa"',html)
            self.assertIn('dir="rtl"',html)
