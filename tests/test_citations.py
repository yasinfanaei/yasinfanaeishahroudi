import unittest
from src.citations import citation_payload

class CitationTests(unittest.TestCase):
    def test_helpers_use_only_populated_fields(self):
        item={
            'id':'paper-1','type':'journal','title':'A Verified Title','authors':['A Author','B Author'],
            'venue':'Journal Name','year':'2026','doi':'10.1234/example','volume':'','issue':'','pages':'',
        }
        payload=citation_payload(item)
        self.assertIn('A Verified Title',payload['citation'])
        self.assertIn('10.1234/example',payload['citation'])
        self.assertIn('title = {A Verified Title}',payload['bibtex'])
        self.assertNotIn('volume =',payload['bibtex'])
        self.assertNotIn('issue =',payload['bibtex'])
        self.assertNotIn('pages =',payload['bibtex'])
        self.assertIn('DO  - 10.1234/example',payload['ris'])

    def test_missing_metadata_is_not_invented(self):
        item={'id':'paper-2','type':'conference','title':'Known Title','authors':['A Author'],'venue':'Known Venue','year':''}
        payload=citation_payload(item)
        self.assertNotIn('DOI',payload['citation'])
        self.assertNotIn('doi =',payload['bibtex'])
        self.assertNotIn('PY  -',payload['ris'])

if __name__=='__main__': unittest.main()
