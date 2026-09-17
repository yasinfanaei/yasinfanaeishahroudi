from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PagesConfigTests(unittest.TestCase):
    def test_pages_cms_configuration_matches_content_model(self):
        validator = ROOT / "scripts" / "validate_pages_config.py"
        self.assertTrue(validator.exists(), "scripts/validate_pages_config.py is missing")
        self.assertTrue((ROOT / ".pages.yml").exists(), ".pages.yml is missing")
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_pages_config import validate_pages_config
        self.assertEqual(validate_pages_config(ROOT), [])

    def test_upload_directory_is_repository_tracked(self):
        self.assertTrue((ROOT / "assets" / "uploads" / ".gitkeep").exists())


if __name__ == "__main__":
    unittest.main()
