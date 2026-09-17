import unittest
class AccessibilityThemeTests(unittest.TestCase):
    def test_css_has_focus_reduced_motion_and_semantic_button_tokens(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        css=(root/'src/static/style.css').read_text(encoding='utf-8')
        self.assertIn(':focus-visible', css)
        self.assertIn('prefers-reduced-motion', css)
        self.assertIn('--button-secondary-text', css)
        self.assertIn('var(--button-secondary-text)', css)
if __name__=='__main__': unittest.main()

class MobileNavigationTests(unittest.TestCase):
    def test_header_has_keyboard_accessible_mobile_navigation_toggle(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        header=(root/'src/templates/partials/header.html').read_text(encoding='utf-8')
        js=(root/'src/static/site.js').read_text(encoding='utf-8')
        css=(root/'src/static/style.css').read_text(encoding='utf-8')
        self.assertIn('data-nav-toggle',header)
        self.assertIn('aria-expanded="false"',header)
        self.assertIn('data-nav-toggle',js)
        self.assertIn('.nav-toggle',css)
