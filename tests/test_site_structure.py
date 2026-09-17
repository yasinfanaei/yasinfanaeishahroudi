from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "research.html", "publications.html", "experience.html",
    "cv.html", "contact.html", "teaching.html",
]


class SiteStructureTests(unittest.TestCase):
    def test_pages_load_shared_renderer_and_declarative_page_name(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('src="assets/site.js"', text, name)
            self.assertIn('data-page="', text, name)

    def test_static_academic_records_are_removed_from_page_markup(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("GPA 18.89/20", index)
        pubs = (ROOT / "publications.html").read_text(encoding="utf-8")
        self.assertNotIn("Money Laundering", pubs)

    def test_expected_render_slots_exist(self):
        expectations = {
            "index.html": ["profile-hero", "about", "research-themes", "education-list"],
            "research.html": ["research-intro", "research-themes", "thesis", "projects"],
            "publications.html": ["publication-list"],
            "experience.html": ["experience-list", "awards-list", "skills-groups"],
            "cv.html": ["cv-header", "cv-education", "cv-interests", "cv-publications", "cv-projects", "cv-service"],
            "contact.html": ["contact-grid", "profile-links"],
        }
        for filename, slots in expectations.items():
            text = (ROOT / filename).read_text(encoding="utf-8")
            for slot in slots:
                self.assertIn(f'data-slot="{slot}"', text, f"{filename}: {slot}")


if __name__ == "__main__":
    unittest.main()
