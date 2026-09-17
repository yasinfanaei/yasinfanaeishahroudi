from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / "assets/site.js").read_text(encoding="utf-8")
CSS = (ROOT / "assets/style.css").read_text(encoding="utf-8")


class AcademicProThemeTests(unittest.TestCase):
    def test_javascript_supports_system_light_dark_and_persistence(self):
        for token in (
            "function applyThemeSettings", "function resolveThemeMode", "function setThemePreference",
            "academic-theme", "matchMedia('(prefers-color-scheme: dark)')", "data-theme"
        ):
            self.assertIn(token, JS)

    def test_javascript_renders_theme_and_search_header_controls(self):
        self.assertIn("function renderHeaderControls", JS)
        self.assertIn("show_theme_switch", JS)
        self.assertIn("show_search", JS)
        self.assertIn("theme-switch", JS)
        self.assertIn("search-link", JS)

    def test_css_has_dark_theme_keyboard_focus_and_reduced_motion(self):
        self.assertIn('html[data-theme="dark"]', CSS)
        self.assertIn(':focus-visible', CSS)
        self.assertIn('@media (prefers-reduced-motion: reduce)', CSS)
        self.assertIn('.theme-switch', CSS)
        self.assertIn('.search-link', CSS)


if __name__ == "__main__":
    unittest.main()
