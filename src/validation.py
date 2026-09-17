from __future__ import annotations
import json, re
from pathlib import Path
import yaml
from .models import load_pages, normalize_contacts
from .navigation import resolve_navigation
from .urls import validate_external_url
from .themes import BUILTIN_THEMES, SEMANTIC_TOKENS, contrast_ratio, get_theme

BANNED_KEYS={'national_id','nationalId','marital_status','maritalStatus','date_of_birth','dateOfBirth','private_phone','password'}
LONG_NUMBER=re.compile(r'(?<!\d)\d{10,12}(?!\d)')

def _check_optional_url(value: str, location: str):
    if not value: return
    if value.startswith('/') or value.startswith('#'): return
    validate_external_url(value)

def validate_page_blocks(page: dict, location: str) -> None:
    seen=set()
    for i,block in enumerate(page.get('blocks',[])):
        where=f'{location}.blocks[{i}]'
        bid=str(block.get('id','')).strip()
        if not bid: raise ValueError(f'{where}: block id is required')
        if bid in seen: raise ValueError(f'{where}: duplicate block id {bid}')
        seen.add(bid)
        if not block.get('enabled',True): continue
        if block.get('type')=='image' and not str(block.get('alt','')).strip():
            raise ValueError(f'{where}: image alt text is required')
        for key in ('url','data_url','code_url','replication_url'):
            if key in block: _check_optional_url(str(block.get(key,'')).strip(),f'{where}.{key}')
        for list_key in ('items',):
            for j,item in enumerate(block.get(list_key,[]) or []):
                if isinstance(item,dict) and item.get('url'):
                    _check_optional_url(str(item['url']),f'{where}.{list_key}[{j}].url')
                if block.get('type')=='cards' and isinstance(item,dict) and item.get('image') and not str(item.get('alt','')).strip():
                    raise ValueError(f'{where}.{list_key}[{j}]: image alt text is required')

def _privacy_scan_value(value, location, errors, allow_public_phone=False):
    if isinstance(value,dict):
        is_public_phone=value.get('type') in {'phone','whatsapp'} and bool(value.get('enabled',True))
        for k,v in value.items():
            if k in BANNED_KEYS: errors.append(f'{location}: prohibited field name {k!r}')
            if k=='value' and is_public_phone: continue
            _privacy_scan_value(v,f'{location}.{k}',errors)
    elif isinstance(value,list):
        for i,v in enumerate(value): _privacy_scan_value(v,f'{location}[{i}]',errors)
    elif isinstance(value,str) and LONG_NUMBER.search(value):
        errors.append(f'{location}: contains a 10–12 digit number; review for sensitive identity data')

def validate_repository(root: Path) -> list[str]:
    root=Path(root); errors=[]
    # Required source files
    for required in ('.pages.yml','content/settings/design.json','content/settings/redirects.json','src/build_site.py','src/static/style.css','src/static/site.js'):
        if not (root/required).exists(): errors.append(f'missing required source: {required}')
    # YAML config
    try: cfg=yaml.safe_load((root/'.pages.yml').read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'.pages.yml: {exc}'); cfg={}
    if isinstance(cfg,dict):
        text=(root/'.pages.yml').read_text(encoding='utf-8')
        for marker in ('content/pages/en','content/pages/fa','type: block','name: contacts','name: navigation'):
            if marker not in text: errors.append(f'.pages.yml: missing Academic Pro 2 control {marker!r}')
    # Pages, navigation, blocks, contacts
    pages_by={}
    for locale in ('en','fa'):
        try: pages=load_pages(root,locale); pages_by[locale]=pages
        except Exception as exc: errors.append(str(exc)); continue
        ids={p['id'] for p in pages}
        for required in ('home','research','publications','experience','news','cv','contact','search','teaching'):
            if required not in ids: errors.append(f'content/pages/{locale}: missing core page {required!r}')
        for p in pages:
            try:
                validate_page_blocks(p,f'content/pages/{locale}/{p["id"]}.json')
                override=str(p.get('seo',{}).get('canonical_override','')).strip()
                if override and not override.startswith('https://'):
                    raise ValueError(f'content/pages/{locale}/{p["id"]}.json.seo.canonical_override: must use https')
            except ValueError as exc: errors.append(str(exc))
        profile_path=root/f'content/{locale}/profile.json'
        try:
            profile=json.loads(profile_path.read_text(encoding='utf-8'))
            contacts=normalize_contacts(profile)
            for contact in contacts:
                if contact.get('url'):
                    try: validate_external_url(contact['url'])
                    except ValueError as exc: errors.append(f'content/{locale}/profile.json.contacts[{contact["id"]}].url: {exc}')
            _privacy_scan_value(profile,f'content/{locale}/profile.json',errors)
        except Exception as exc: errors.append(f'{profile_path.relative_to(root)}: {exc}')
        site_path=root/f'content/{locale}/site.json'
        try:
            site=json.loads(site_path.read_text(encoding='utf-8')); resolve_navigation(site.get('navigation',[]),pages,locale); _privacy_scan_value(site,f'content/{locale}/site.json',errors)
        except Exception as exc: errors.append(f'{site_path.relative_to(root)}: {exc}')
        # all other dataset JSONs
        for path in (root/f'content/{locale}').glob('*.json'):
            if path.name in {'profile.json','site.json'}: continue
            try: _privacy_scan_value(json.loads(path.read_text(encoding='utf-8')),str(path.relative_to(root)),errors)
            except Exception as exc: errors.append(f'{path.relative_to(root)}: {exc}')
    # Theme completeness and contrast
    try:
        design=json.loads((root/'content/settings/design.json').read_text(encoding='utf-8'))
        preset=design.get('theme',{}).get('preset','classic-academic'); theme=get_theme(preset,design)
        for mode,tokens in theme.items():
            missing=set(SEMANTIC_TOKENS)-set(tokens)
            if missing: errors.append(f'theme {preset}/{mode}: missing tokens {sorted(missing)}')
            for fg,bg,minimum in [('text','background',4.5),('text_muted','background',4.5),('button_primary_text','button_primary_bg',4.5),('button_secondary_text','button_secondary_bg',4.5),('tag_text','tag_bg',4.5),('focus_ring','background',3.0)]:
                if contrast_ratio(tokens[fg],tokens[bg]) < minimum: errors.append(f'theme {preset}/{mode}: contrast failure {fg}/{bg}')
        for key,value in design.get('branding',{}).items():
            if isinstance(value,str) and value and not value.startswith('http') and key in {'favicon','profile_image','cv_pdf','cv_docx','open_graph_image','logo'} and not (root/value.lstrip('/')).exists(): errors.append(f'design branding.{key}: missing file {value}')
    except Exception as exc: errors.append(f'content/settings/design.json: {exc}')
    return errors
