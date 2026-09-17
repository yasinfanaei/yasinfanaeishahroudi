import unittest
from src.richtext import render_rich_text

class RichTextTests(unittest.TestCase):
    def test_allowed_formatting_is_preserved_and_script_is_removed(self):
        html=render_rich_text('<p>Hello <strong>world</strong> <a href="https://example.com">link</a></p><script>alert(1)</script>')
        self.assertIn('<strong>world</strong>',str(html))
        self.assertIn('href="https://example.com"',str(html))
        self.assertNotIn('<script',str(html))
        self.assertNotIn('alert(1)',str(html))

    def test_unsafe_link_scheme_is_removed(self):
        html=render_rich_text('<p><a href="javascript:alert(1)">bad</a></p>')
        self.assertIn('>bad</a>',str(html))
        self.assertNotIn('javascript:',str(html))

    def test_plain_text_becomes_paragraphs(self):
        html=render_rich_text('First paragraph\n\nSecond paragraph')
        self.assertEqual(str(html),'<p>First paragraph</p><p>Second paragraph</p>')

if __name__=='__main__': unittest.main()
