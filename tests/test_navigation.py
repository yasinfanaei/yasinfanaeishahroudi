import json
import tempfile
import unittest
from pathlib import Path

class NavigationTests(unittest.TestCase):
    def test_navigation_uses_page_references_and_supports_one_submenu_level(self):
        from src.navigation import resolve_navigation
        pages=[{'id':'home','slug':'','status':'published'},{'id':'research','slug':'research','status':'published'}]
        nav=[{'label':'Research','enabled':True,'destination':'page','page':'research','children':[
          {'label':'Home','enabled':True,'destination':'page','page':'home','children':[]}
        ]}]
        out=resolve_navigation(nav,pages,'en')
        self.assertEqual(out[0]['href'],'/research/')
        self.assertEqual(out[0]['children'][0]['href'],'/')
    def test_missing_page_reference_is_rejected(self):
        from src.navigation import resolve_navigation
        with self.assertRaisesRegex(ValueError,'missing page'):
            resolve_navigation([{'label':'X','enabled':True,'destination':'page','page':'x','children':[]}],[], 'en')
    def test_external_links_receive_safe_rel(self):
        from src.navigation import resolve_navigation
        out=resolve_navigation([{'label':'X','enabled':True,'destination':'external','url':'https://example.com','new_tab':True,'children':[]}],[], 'en')
        self.assertEqual(out[0]['target'],'_blank')
        self.assertIn('noopener',out[0]['rel'])

class SectionNavigationTests(unittest.TestCase):
    def test_section_navigation_points_to_locale_home_anchor(self):
        from src.navigation import resolve_navigation
        pages=[{'id':'home','slug':'','status':'published'}]
        item={'label':'About','enabled':True,'destination':'section','section':'about','children':[]}
        self.assertEqual(resolve_navigation([item],pages,'en')[0]['href'],'/#about')
        self.assertEqual(resolve_navigation([item],pages,'fa')[0]['href'],'/fa/#about')
