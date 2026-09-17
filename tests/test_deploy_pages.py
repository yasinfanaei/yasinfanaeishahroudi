import unittest
from pathlib import Path

class DeployPagesWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.root=Path(__file__).resolve().parents[1]
        self.text=(self.root/'.github/workflows/deploy-pages.yml').read_text(encoding='utf-8') if (self.root/'.github/workflows/deploy-pages.yml').exists() else ''
    def test_workflow_builds_validates_and_uses_official_pages_artifact(self):
        self.assertIn('python -m unittest discover', self.text)
        self.assertIn('python scripts/check_site.py', self.text)
        self.assertIn('python -m src.build_site --output _site', self.text)
        self.assertIn('python scripts/check_build.py _site', self.text)
        self.assertIn('actions/configure-pages@', self.text)
        self.assertIn('actions/upload-pages-artifact@', self.text)
        self.assertIn('actions/deploy-pages@', self.text)
        self.assertIn('needs: build', self.text)
        self.assertIn('path: _site', self.text)
    def test_workflow_has_pages_permissions_and_main_push(self):
        self.assertIn('pages: write', self.text)
        self.assertIn('id-token: write', self.text)
        self.assertIn('branches: [main]', self.text)
