from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'assets/site.js').read_text(encoding='utf-8')
CSS=(ROOT/'assets/style.css').read_text(encoding='utf-8')

class AcademicProPublicationTests(unittest.TestCase):
    def test_publication_pages_have_filter_controls_slot(self):
        for rel in ('publications.html','fa/publications.html'):
            text=(ROOT/rel).read_text(encoding='utf-8')
            self.assertIn('data-slot="publication-tools"', text)
            self.assertIn('data-slot="publication-list"', text)

    def test_renderer_has_filter_and_citation_utilities(self):
        for token in (
            'function renderPublicationTools', 'function filterPublications',
            'function publicationCitation', 'function publicationBibtex',
            'function publicationRis', 'function copyText'
        ):
            self.assertIn(token, JS)

    def test_publication_renderer_supports_resource_links_and_abstract_keywords(self):
        for token in ('abstract_label','keywords_label','data_url','code_url','replication_url','publication-resource-links'):
            self.assertIn(token, JS)
        self.assertIn('.publication-tools', CSS)
        self.assertIn('.citation-actions', CSS)

if __name__=='__main__':unittest.main()
