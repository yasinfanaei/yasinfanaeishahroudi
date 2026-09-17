from pathlib import Path
import json
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class AcademicProContentTests(unittest.TestCase):
    def test_news_content_exists_for_both_locales(self):
        for locale in ("en", "fa"):
            path = ROOT / "content" / locale / "news.json"
            self.assertTrue(path.exists(), f"missing {path}")
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("intro", data)
            self.assertIn("items", data)
            self.assertIsInstance(data["items"], list)

    def test_design_has_theme_dark_palette_analytics_and_academic_pro_controls(self):
        data = json.loads((ROOT / "content/settings/design.json").read_text(encoding="utf-8"))
        self.assertIn("dark_colors", data)
        self.assertIn("theme", data)
        self.assertIn("analytics", data)
        self.assertIn(data["theme"]["default_mode"], {"system", "light", "dark"})
        self.assertIn("show_theme_switch", data["controls"])
        self.assertIn("show_search", data["controls"])
        self.assertFalse(data["analytics"]["enabled"])
        self.assertIn("news", [item["id"] for item in data["home_sections"]])

    def test_publication_records_support_academic_pro_resources_without_fabricating_values(self):
        required = {
            "abstract", "keywords", "volume", "issue", "pages", "pdf",
            "data_url", "code_url", "replication_url"
        }
        for locale in ("en", "fa"):
            data = json.loads((ROOT / "content" / locale / "publications.json").read_text(encoding="utf-8"))
            self.assertTrue(data["items"])
            for item in data["items"]:
                self.assertTrue(required.issubset(item), (locale, item.get("id")))
                # Migration must not invent missing bibliographic/resource metadata.
                for key in ("volume", "issue", "pages", "pdf", "data_url", "code_url", "replication_url"):
                    self.assertEqual(item[key], "", (locale, item.get("id"), key))
                self.assertIsInstance(item["keywords"], list)

    def test_site_settings_have_news_search_and_page_seo_labels(self):
        for locale in ("en", "fa"):
            site = json.loads((ROOT / "content" / locale / "site.json").read_text(encoding="utf-8"))
            ids = [item["id"] for item in site["navigation"]]
            self.assertIn("news", ids)
            self.assertIn("page_seo", site)
            self.assertTrue(any(item.get("id") == "search" for item in site["page_seo"]))
            for key in ("news_title", "search_title", "search_placeholder", "search_no_results", "home_news_title"):
                self.assertIn(key, site["ui"])

    def test_pages_cms_uses_named_media_sources_and_exposes_news_and_validation_action(self):
        cfg = yaml.safe_load((ROOT / ".pages.yml").read_text(encoding="utf-8"))
        media = cfg.get("media")
        self.assertIsInstance(media, list)
        self.assertEqual({item["name"] for item in media}, {"images", "documents", "publication_files"})
        self.assertIn("actions", cfg)
        validate = next((a for a in cfg["actions"] if a.get("name") == "validate-site"), None)
        self.assertIsNotNone(validate)
        self.assertEqual(validate.get("workflow"), "validate.yml")

        def flatten(entries):
            for entry in entries:
                if entry.get("type") == "group":
                    yield from flatten(entry.get("items", []))
                else:
                    yield entry

        flat = {entry.get("name"): entry for entry in flatten(cfg.get("content", []))}
        for locale in ("en", "fa"):
            name = f"{locale}_news"
            self.assertIn(name, flat)
            self.assertEqual(flat[name]["path"], f"content/{locale}/news.json")

        design = flat["design_branding"]
        design_fields = {field["name"] for field in design["fields"]}
        self.assertTrue({"dark_colors", "theme", "analytics"}.issubset(design_fields))


if __name__ == "__main__":
    unittest.main()
