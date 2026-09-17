import unittest

class RedirectTests(unittest.TestCase):
    def test_aliases_are_normalized_and_collision_rejected(self):
        from src.seo import validate_redirects
        pages={'/research/','/fa/research/'}
        aliases={'/research.html':'/research/','/fa/research.html':'/fa/research/'}
        validate_redirects(aliases,pages)
        with self.assertRaisesRegex(ValueError,'collides'):
            validate_redirects({'/research/':'/fa/research/'},pages)
    def test_redirect_loop_rejected(self):
        from src.seo import validate_redirects
        with self.assertRaisesRegex(ValueError,'loop'):
            validate_redirects({'/a.html':'/b.html','/b.html':'/a.html'},set())
