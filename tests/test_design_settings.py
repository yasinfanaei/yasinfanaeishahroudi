from pathlib import Path
import json
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class DesignSettingsTests(unittest.TestCase):
    def test_shared_design_settings_exist_with_safe_sections(self):
        path = ROOT / "content" / "settings" / "design.json"
        self.assertTrue(path.exists(), "content/settings/design.json is missing")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"branding", "colors", "dark_colors", "typography", "layout", "controls", "home_sections", "theme", "custom_theme", "layout_presets", "analytics", "seo"})
        self.assertEqual([item["id"] for item in data["home_sections"]], ["hero", "about", "research", "education", "news"])
        self.assertTrue(all("enabled" in item for item in data["home_sections"]))
        self.assertIn("english_font", data["typography"])
        self.assertIn("persian_font", data["typography"])
        self.assertIn("max_width", data["layout"])
        self.assertIn("favicon", data["branding"])
        for key in ("logo", "profile_image", "cv_pdf", "cv_docx", "open_graph_image"):
            self.assertIn(key, data["branding"])

    def test_css_exposes_dashboard_design_tokens(self):
        css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
        required = [
            "--font-en", "--font-fa", "--base-font-size", "--section-space",
            "--portrait-size", "--portrait-radius", "--button-radius", "--card-radius",
            "--hero-space-top", "--hero-space-bottom", "--nav-gap"
        ]
        for token in required:
            self.assertIn(token, css, token)
        self.assertIn("html.design-header-static .site-header", css)
        self.assertIn("html.design-no-shadow", css)
        self.assertIn("html.design-portrait-left", css)
        self.assertIn("html.design-portrait-right", css)

    def test_javascript_loads_and_applies_shared_settings(self):
        js = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("content/settings/design.json", js)
        self.assertIn("function applyDesignSettings", js)
        self.assertIn("function applyHomeSections", js)
        self.assertIn("function updateMetadata", js)
        self.assertIn("item.enabled !== false", js)
        self.assertIn("function sharedAsset", js)

    def test_homepages_expose_stable_section_hooks(self):
        for rel in ("index.html", "fa/index.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            for section_id in ("hero", "about", "research", "education", "news"):
                self.assertIn(f'data-home-section="{section_id}"', text, f"{rel}: {section_id}")

    def test_cms_exposes_design_branding_editor(self):
        cfg = yaml.safe_load((ROOT / ".pages.yml").read_text(encoding="utf-8"))
        entries = {entry.get("name"): entry for entry in cfg.get("content", []) if isinstance(entry, dict)}
        self.assertIn("design_branding", entries)
        self.assertEqual(entries["design_branding"].get("path"), "content/settings/design.json")
        fields = {field.get("name") for field in entries["design_branding"].get("fields", [])}
        self.assertTrue({"branding", "colors", "dark_colors", "typography", "layout", "controls", "home_sections", "theme", "analytics", "seo"}.issubset(fields))
        branding = next(field for field in entries["design_branding"]["fields"] if field.get("name") == "branding")
        branding_fields = {field.get("name") for field in branding.get("fields", [])}
        self.assertTrue({"logo", "profile_image", "cv_pdf", "cv_docx", "favicon", "open_graph_image"}.issubset(branding_fields))

    def test_locale_site_navigation_items_have_enabled_switch(self):
        for locale in ("en", "fa"):
            site = json.loads((ROOT / "content" / locale / "site.json").read_text(encoding="utf-8"))
            self.assertTrue(all("enabled" in item for item in site["navigation"]))
            self.assertIn("keywords", site)
            self.assertIn("announcement_enabled", site)

    def test_main_interface_labels_are_cms_managed(self):
        for locale in ("en", "fa"):
            site = json.loads((ROOT / "content" / locale / "site.json").read_text(encoding="utf-8"))
            self.assertIn("ui", site)
            for key in ("home_about_title", "research_title", "publications_title", "experience_title", "contact_title", "teaching_title", "cv_education_label"):
                self.assertIn(key, site["ui"])
        js = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("function uiLabel", js)
        self.assertIn("[data-ui]", js)
        self.assertIn('data-ui="home_about_title"', (ROOT / "index.html").read_text(encoding="utf-8"))



if __name__ == "__main__":
    unittest.main()
