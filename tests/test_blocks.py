import unittest
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class BlockTests(unittest.TestCase):
    def setUp(self):
        self.root=Path(__file__).resolve().parents[1]
        self.env=Environment(loader=FileSystemLoader(self.root/'src/templates'),autoescape=select_autoescape(['html']))
    def test_disabled_blocks_are_not_rendered_and_heading_dispatches(self):
        from src.blocks import render_blocks
        page={'blocks':[
            {'type':'heading','id':'a','enabled':True,'title':'Visible','level':'h2'},
            {'type':'heading','id':'b','enabled':False,'title':'Hidden','level':'h2'}]}
        html=render_blocks(self.env,page,{'locale':'en'})
        self.assertIn('Visible',html)
        self.assertNotIn('Hidden',html)
        self.assertIn('<h2',html)
    def test_unknown_block_fails_actionably(self):
        from src.blocks import render_blocks
        with self.assertRaisesRegex(ValueError,'unknown block type'):
            render_blocks(self.env,{'blocks':[{'type':'mystery','enabled':True}]},{'locale':'en'})
