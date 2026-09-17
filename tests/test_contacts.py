import json
import unittest
from pathlib import Path

class ContactTests(unittest.TestCase):
    def test_profiles_expose_ordered_contacts_and_keep_public_email(self):
        from src.models import normalize_contacts
        root = Path(__file__).resolve().parents[1]
        for locale in ('en','fa'):
            profile = json.loads((root/f'content/{locale}/profile.json').read_text(encoding='utf-8'))
            contacts = normalize_contacts(profile)
            self.assertGreaterEqual(len(contacts), 1)
            self.assertEqual(contacts[0]['type'], 'email')
            self.assertEqual(contacts[0]['value'], profile['email'])
            self.assertTrue(contacts[0]['show_contact'])

    def test_duplicate_contact_ids_are_rejected(self):
        from src.models import normalize_contacts
        profile = {'contacts': [
            {'id':'x','type':'email','label':'A','value':'a@example.com','enabled':True},
            {'id':'x','type':'phone','label':'B','value':'123','enabled':True},
        ]}
        with self.assertRaisesRegex(ValueError, 'duplicate contact id'):
            normalize_contacts(profile)

    def test_legacy_email_is_migrated_when_contacts_missing(self):
        from src.models import normalize_contacts
        contacts = normalize_contacts({'email':'a@example.com'})
        self.assertEqual(contacts[0]['value'], 'a@example.com')
        self.assertEqual(contacts[0]['id'], 'academic-email')

if __name__ == '__main__': unittest.main()

class ContactUrlSafetyTests(unittest.TestCase):
    def test_unsafe_contact_url_is_rejected_by_repository_validation(self):
        import json, shutil, tempfile
        from pathlib import Path
        from src.validation import validate_repository
        root0=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'repo'; shutil.copytree(root0,root,ignore=shutil.ignore_patterns('_site','__pycache__','*.pyc'))
            p=root/'content/en/profile.json'; data=json.loads(p.read_text(encoding='utf-8'))
            data['contacts'].append({'id':'bad-contact','type':'custom','label':'Bad','value':'Bad','url':'javascript:alert(1)','enabled':True,'show_home':True,'show_contact':True,'show_footer':False})
            p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
            errors=validate_repository(root)
            self.assertTrue(any('bad-contact' in e or 'javascript' in e or 'profile.json' in e for e in errors), errors)
