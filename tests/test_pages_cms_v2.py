import unittest, yaml
from pathlib import Path

class PagesCmsV2Tests(unittest.TestCase):
    def setUp(self):
        self.root=Path(__file__).resolve().parents[1]
        self.text=(self.root/'.pages.yml').read_text(encoding='utf-8')
        self.cfg=yaml.safe_load(self.text)
    def test_page_collections_contacts_navigation_theme_blocks_and_action_are_exposed(self):
        self.assertIn('components:',self.text)
        self.assertIn('type: block',self.text)
        self.assertIn('blockKey: type',self.text)
        self.assertIn('content/pages/en',self.text)
        self.assertIn('content/pages/fa',self.text)
        self.assertIn('name: contacts',self.text)
        self.assertIn('show_footer',self.text)
        self.assertIn('name: navigation',self.text)
        self.assertIn('name: children',self.text)
        self.assertIn('type: reference',self.text)
        self.assertIn('classic-academic',self.text)
        self.assertIn('midnight-teal',self.text)
        actions=self.cfg.get('actions',[])
        self.assertTrue(any(a.get('name')=='validate-site' for a in actions))
    def test_named_media_sources_remain(self):
        names={m['name'] for m in self.cfg['media']}
        self.assertTrue({'images','documents','publication_files'} <= names)
