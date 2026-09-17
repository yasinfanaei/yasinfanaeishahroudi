from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_repository_is_release_ready(self):
        checker = ROOT / "scripts" / "check_site.py"
        self.assertTrue(checker.exists(), "scripts/check_site.py is missing")
        sys.path.insert(0, str(ROOT / "scripts"))
        from check_site import check_site
        self.assertEqual(check_site(ROOT), [])

    def test_readme_documents_github_pages_and_pages_cms(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GitHub Pages", text)
        self.assertIn("Pages CMS", text)
        self.assertIn("main", text)
        self.assertIn("GitHub Actions", text)
        self.assertIn("deploy-pages.yml", text)

    def test_public_cv_docx_has_sensitive_number_scanner(self):
        import importlib
        sys.path.insert(0, str(ROOT / "scripts"))
        module = importlib.import_module("check_site")
        self.assertTrue(hasattr(module, "scan_docx_for_sensitive_numbers"), "DOCX privacy scanner is missing")
        scan = module.scan_docx_for_sensitive_numbers
        design = json.loads((ROOT / "content" / "settings" / "design.json").read_text(encoding="utf-8"))
        cv_docx = design["branding"]["cv_docx"]
        self.assertTrue(cv_docx, "Design settings must reference a public CV DOCX")
        self.assertEqual(scan(ROOT / cv_docx), [])

    def test_release_checker_validates_shared_design_assets(self):
        import importlib
        sys.path.insert(0, str(ROOT / "scripts"))
        module = importlib.import_module("check_site")
        self.assertTrue(hasattr(module, "_check_design_assets"), "shared design asset checker is missing")



if __name__ == "__main__":
    unittest.main()
