import json
import tempfile
import unittest
from pathlib import Path

class PageModelTests(unittest.TestCase):
    def test_repository_pages_have_unique_ids_slugs_and_translation_keys(self):
        from src.models import load_pages, translation_pairs
        root = Path(__file__).resolve().parents[1]
        for locale in ('en','fa'):
            pages = load_pages(root, locale)
            self.assertGreaterEqual(len(pages), 9)
            self.assertEqual(len({p['id'] for p in pages}), len(pages))
            self.assertEqual(len({p['slug'] for p in pages}), len(pages))
            self.assertEqual(len({p['translation_key'] for p in pages}), len(pages))
        pairs = translation_pairs(load_pages(root,'en'), load_pages(root,'fa'))
        self.assertIn('research', pairs)
        self.assertIn('en', pairs['research'])
        self.assertIn('fa', pairs['research'])

    def test_duplicate_translation_key_is_rejected(self):
        from src.models import validate_pages
        pages = [
            {'id':'a','slug':'a','translation_key':'x','title':'A','status':'published','layout':'standard','blocks':[]},
            {'id':'b','slug':'b','translation_key':'x','title':'B','status':'published','layout':'standard','blocks':[]},
        ]
        with self.assertRaisesRegex(ValueError, 'translation_key'):
            validate_pages(pages, 'en')

if __name__ == '__main__': unittest.main()
