import json
import unittest
from pathlib import Path

class ThemeTests(unittest.TestCase):
    EXPECTED = {'classic-academic','oxford-navy','midnight-teal','burgundy-cream','forest-ivory','slate-blue','monochrome-editorial','custom'}
    TOKENS = {'background','surface','surface_alt','text','text_muted','border','accent','accent_hover','accent_text','link','link_hover','button_primary_bg','button_primary_text','button_secondary_bg','button_secondary_text','tag_bg','tag_text','focus_ring','success','warning','danger'}

    def test_all_theme_presets_exist_and_have_complete_light_dark_tokens(self):
        from src.themes import BUILTIN_THEMES
        self.assertTrue(self.EXPECTED - {'custom'} <= set(BUILTIN_THEMES))
        for name, modes in BUILTIN_THEMES.items():
            for mode in ('light','dark'):
                self.assertEqual(self.TOKENS - set(modes[mode]), set(), f'{name}/{mode}')

    def test_required_contrast_pairs_pass(self):
        from src.themes import BUILTIN_THEMES, contrast_ratio
        for name, modes in BUILTIN_THEMES.items():
            for mode, t in modes.items():
                pairs = [
                    ('text','background',4.5), ('text','surface',4.5), ('text_muted','background',4.5),
                    ('button_primary_text','button_primary_bg',4.5),
                    ('button_secondary_text','button_secondary_bg',4.5),
                    ('tag_text','tag_bg',4.5), ('link','background',4.5), ('focus_ring','background',3.0),
                ]
                for fg,bg,minimum in pairs:
                    self.assertGreaterEqual(contrast_ratio(t[fg],t[bg]), minimum, f'{name}/{mode} {fg}/{bg}')

    def test_design_selects_single_preset_and_layout_presets(self):
        root=Path(__file__).resolve().parents[1]
        design=json.loads((root/'content/settings/design.json').read_text(encoding='utf-8'))
        self.assertEqual(design['theme']['preset'], 'classic-academic')
        for key in ('content_width','hero_style','section_density','card_style','header_style','corner_style'):
            self.assertIn(key, design['layout_presets'])

    def test_dark_secondary_button_regression(self):
        from src.themes import BUILTIN_THEMES, contrast_ratio
        for name,modes in BUILTIN_THEMES.items():
            dark=modes['dark']
            self.assertGreaterEqual(contrast_ratio(dark['button_secondary_text'],dark['button_secondary_bg']),4.5,name)

if __name__=='__main__': unittest.main()

class CustomThemeReadinessTests(unittest.TestCase):
    def test_custom_theme_is_prepopulated_and_immediately_selectable(self):
        import json
        from pathlib import Path
        from src.themes import SEMANTIC_TOKENS, get_theme
        root=Path(__file__).resolve().parents[1]
        design=json.loads((root/'content/settings/design.json').read_text(encoding='utf-8'))
        for mode in ('light','dark'):
            self.assertEqual(set(SEMANTIC_TOKENS)-set(design['custom_theme'][mode]),set())
        theme=get_theme('custom',design)
        self.assertEqual(set(SEMANTIC_TOKENS)-set(theme['light']),set())
