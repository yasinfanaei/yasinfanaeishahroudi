from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")


class TypographyTests(unittest.TestCase):
    def test_default_english_font_is_times_new_roman_via_design_token(self):
        self.assertIn('--font-en: "Times New Roman",Times,serif;', CSS)
        self.assertIn('body { margin: 0; font-family:var(--font-en);', CSS)
        self.assertIn('h1 { font-family:var(--font-en);', CSS)
        self.assertIn('h2 { font-family:var(--font-en);', CSS)
        self.assertIn('.entry-title { font-family:var(--font-en);', CSS)

    def test_default_persian_font_is_b_nazanin_via_design_token(self):
        self.assertIn('--font-fa: "B Nazanin","Nazanin",Tahoma,serif;', CSS)
        self.assertIn('html[dir="rtl"] body { direction:rtl; text-align:right; font-family:var(--font-fa);', CSS)
        self.assertIn('html[dir="rtl"] h1, html[dir="rtl"] h2, html[dir="rtl"] .entry-title { font-family:var(--font-fa);', CSS)

    def test_persian_hero_has_dedicated_spacing_and_line_height(self):
        self.assertIn('html[dir="rtl"] .hero h1 {', CSS)
        self.assertIn('line-height:1.14;', CSS)
        self.assertIn('html[dir="rtl"] .lede { line-height:var(--line-height-fa);', CSS)


if __name__ == "__main__":
    unittest.main()
