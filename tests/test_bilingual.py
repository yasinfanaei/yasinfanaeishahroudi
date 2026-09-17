from pathlib import Path
import json
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "research.html", "publications.html", "experience.html", "cv.html", "contact.html", "teaching.html", "news.html", "search.html"]
CONTENT = ["profile.json", "education.json", "research.json", "publications.json", "projects.json", "experience.json", "awards.json", "skills.json", "site.json", "news.json"]


class BilingualSiteTests(unittest.TestCase):
    def test_locale_content_trees_exist(self):
        for locale in ("en", "fa"):
            directory = ROOT / "content" / locale
            self.assertTrue(directory.is_dir(), locale)
            self.assertEqual({p.name for p in directory.glob("*.json")}, set(CONTENT))

    def test_persian_pages_are_mirrored_and_rtl(self):
        for page in PAGES:
            path = ROOT / "fa" / page
            self.assertTrue(path.exists(), page)
            text = path.read_text(encoding="utf-8")
            self.assertIn('lang="fa"', text, page)
            self.assertIn('dir="rtl"', text, page)
            self.assertIn('data-locale="fa"', text, page)
            self.assertIn('../assets/site.js', text, page)
            self.assertIn('hreflang="en"', text, page)
            self.assertIn('hreflang="fa"', text, page)

    def test_english_pages_declare_locale_and_language_switch(self):
        for page in PAGES:
            text = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn('data-locale="en"', text, page)
            self.assertIn('data-slot="language-switch"', text, page)
            self.assertIn('hreflang="en"', text, page)
            self.assertIn('hreflang="fa"', text, page)

    def test_verified_academic_links_are_present(self):
        expected = {
            "orcid": "https://orcid.org/0009-0005-9508-604X",
            "researchgate": "https://www.researchgate.net/profile/Yasin-Fanaei",
            "google_scholar": "https://scholar.google.com/citations?user=6_vY6vkAAAAJ&hl=en",
            "linkedin": "https://www.linkedin.com/in/yasin-fanaei-4b5959354",
            "github": "https://github.com/yasinfanaei",
        }
        for locale in ("en", "fa"):
            profile = json.loads((ROOT / "content" / locale / "profile.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["links"], expected)

    def test_pages_cms_has_all_bilingual_content_paths(self):
        cfg = yaml.safe_load((ROOT / ".pages.yml").read_text(encoding="utf-8"))
        def flatten(entries):
            for entry in entries:
                if entry.get("type") == "group":
                    yield from flatten(entry.get("items", []))
                else:
                    yield entry
        paths = {entry.get("path") for entry in flatten(cfg.get("content", []))}
        expected = {f"content/{locale}/{name}" for locale in ("en", "fa") for name in CONTENT}
        expected.update({"content/settings/design.json", "content/pages/en", "content/pages/fa"})
        self.assertEqual(paths, expected)


if __name__ == "__main__":
    unittest.main()
