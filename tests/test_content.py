from pathlib import Path
import json,re,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'profile.json','education.json','research.json','publications.json','projects.json','experience.json','awards.json','skills.json','site.json','news.json'}
class ContentTests(unittest.TestCase):
 def test_content_files_parse_and_validate(self):
  sys.path.insert(0,str(ROOT/'scripts'));from validate_content import validate_site
  for locale in ('en','fa'):self.assertEqual({p.name for p in (ROOT/'content'/locale).glob('*.json')},REQUIRED)
  self.assertEqual(validate_site(ROOT),[])
 def test_no_sensitive_identity_keys_or_long_id_numbers(self):
  banned={'national_id','nationalId','marital_status','maritalStatus','date_of_birth','dateOfBirth','phone','private_phone'}
  for locale in ('en','fa'):
   for path in (ROOT/'content'/locale).glob('*.json'):
    data=json.loads(path.read_text(encoding='utf-8'));text=json.dumps(data,ensure_ascii=False)
    self.assertFalse(any(f'"{k}"' in text for k in banned),str(path));self.assertIsNone(re.search(r'(?<!\d)\d{10,12}(?!\d)',text),str(path))
if __name__=='__main__':unittest.main()
