import tempfile
import unittest
from pathlib import Path

class RouteTests(unittest.TestCase):
    def test_clean_public_paths(self):
        from src.routes import public_path
        self.assertEqual(public_path('en', ''), '/')
        self.assertEqual(public_path('en', 'research'), '/research/')
        self.assertEqual(public_path('fa', ''), '/fa/')
        self.assertEqual(public_path('fa', 'research'), '/fa/research/')

    def test_output_paths_are_directory_indexes(self):
        from src.routes import output_path
        root = Path('/tmp/site')
        self.assertEqual(output_path('en', '', root), root / 'index.html')
        self.assertEqual(output_path('en', 'research', root), root / 'research' / 'index.html')
        self.assertEqual(output_path('fa', '', root), root / 'fa' / 'index.html')
        self.assertEqual(output_path('fa', 'research', root), root / 'fa' / 'research' / 'index.html')

    def test_invalid_slugs_are_rejected(self):
        from src.routes import validate_slug
        for bad in ['Research', 'two words', '../x', 'x/y', '_bad', 'bad_underscore']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate_slug(bad)
        validate_slug('working-papers')
        validate_slug('', home=True)

if __name__ == '__main__': unittest.main()
