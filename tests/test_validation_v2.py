import tempfile, unittest
from pathlib import Path

class ValidationV2Tests(unittest.TestCase):
    def test_image_block_requires_alt_text(self):
        from src.validation import validate_page_blocks
        page={'id':'x','blocks':[{'type':'image','id':'img','enabled':True,'image':'x.jpg','alt':''}]}
        with self.assertRaisesRegex(ValueError,'alt'):
            validate_page_blocks(page,'content/pages/en/x.json')
    def test_unsafe_urls_are_rejected_in_blocks(self):
        from src.validation import validate_page_blocks
        page={'id':'x','blocks':[{'type':'callout','id':'c','enabled':True,'body':'x','url':'javascript:alert(1)'}]}
        with self.assertRaisesRegex(ValueError,'unsafe'):
            validate_page_blocks(page,'x.json')
    def test_source_repository_validation_passes(self):
        from src.validation import validate_repository
        root=Path(__file__).resolve().parents[1]
        self.assertEqual(validate_repository(root),[])

    def test_build_checker_understands_project_site_base_path(self):
        from scripts.check_build import check_build
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'assets').mkdir()
            (root/'assets/style.css').write_text('body{}',encoding='utf-8')
            (root/'index.html').write_text(
                '<link rel="canonical" href="https://example.com/repo/">'
                '<link rel="stylesheet" href="/repo/assets/style.css">',
                encoding='utf-8'
            )
            for required in ('sitemap.xml','robots.txt','404.html','assets/site.js','search-index.en.json','search-index.fa.json'):
                path=root/required; path.parent.mkdir(parents=True,exist_ok=True); path.write_text('',encoding='utf-8')
            self.assertEqual(check_build(root),[])

    def test_build_checker_detects_broken_internal_link(self):
        from scripts.check_build import check_build
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'index.html').write_text('<a href="/missing/">x</a>',encoding='utf-8')
            errors=check_build(root)
            self.assertTrue(any('missing' in e for e in errors))
