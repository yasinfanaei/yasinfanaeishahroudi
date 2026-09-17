from __future__ import annotations
from pathlib import Path
from typing import Iterable
from .content_loader import load_json
from .routes import validate_slug

REQUIRED_PAGE_FIELDS = {'id','slug','translation_key','title','status','layout','blocks'}

def validate_pages(pages: list[dict], locale: str) -> None:
    seen_ids, seen_slugs, seen_keys = set(), set(), set()
    for page in pages:
        missing = REQUIRED_PAGE_FIELDS - set(page)
        if missing:
            raise ValueError(f'{locale}: page missing fields: {sorted(missing)}')
        pid = page['id']
        if pid in seen_ids:
            raise ValueError(f'{locale}: duplicate page id: {pid}')
        seen_ids.add(pid)
        slug = page['slug']
        validate_slug(slug, home=(pid == 'home'))
        if slug in seen_slugs:
            raise ValueError(f'{locale}: duplicate page slug: {slug}')
        seen_slugs.add(slug)
        key = page['translation_key']
        if key in seen_keys:
            raise ValueError(f'{locale}: duplicate translation_key: {key}')
        seen_keys.add(key)
        if page['status'] not in {'published','draft'}:
            raise ValueError(f'{locale}: invalid status for {pid}: {page["status"]}')
        if not isinstance(page['blocks'], list):
            raise ValueError(f'{locale}: blocks must be a list for {pid}')

def load_pages(root: Path, locale: str) -> list[dict]:
    folder = Path(root) / 'content' / 'pages' / locale
    if not folder.exists():
        return []
    pages = [load_json(path) for path in sorted(folder.glob('*.json'))]
    validate_pages(pages, locale)
    return pages

def page_by_id(pages: Iterable[dict]) -> dict[str, dict]:
    return {page['id']: page for page in pages}

def translation_pairs(en_pages: list[dict], fa_pages: list[dict]) -> dict[str, dict]:
    pairs: dict[str, dict] = {}
    for locale, pages in (('en', en_pages), ('fa', fa_pages)):
        for page in pages:
            pairs.setdefault(page['translation_key'], {})[locale] = page
    return pairs

def normalize_contacts(profile: dict) -> list[dict]:
    contacts = profile.get('contacts')
    if contacts is None:
        contacts = []
        if profile.get('email'):
            contacts.append({
                'id': 'academic-email', 'type': 'email', 'label': 'Email',
                'value': profile['email'], 'url': '', 'enabled': True,
                'show_home': False, 'show_contact': True, 'show_footer': False,
            })
    if not isinstance(contacts, list):
        raise ValueError('contacts must be a list')
    seen = set()
    normalized = []
    for item in contacts:
        cid = str(item.get('id','')).strip()
        if not cid:
            raise ValueError('contact id is required')
        if cid in seen:
            raise ValueError(f'duplicate contact id: {cid}')
        seen.add(cid)
        ctype = item.get('type','custom')
        if ctype not in {'email','phone','whatsapp','telegram','website','office','location','custom'}:
            raise ValueError(f'invalid contact type: {ctype}')
        obj = {
            'id': cid,
            'type': ctype,
            'label': str(item.get('label','')).strip(),
            'value': str(item.get('value','')).strip(),
            'url': str(item.get('url','')).strip(),
            'enabled': bool(item.get('enabled', True)),
            'show_home': bool(item.get('show_home', False)),
            'show_contact': bool(item.get('show_contact', True)),
            'show_footer': bool(item.get('show_footer', False)),
        }
        normalized.append(obj)
    return normalized
