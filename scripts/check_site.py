#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.validation import validate_repository
LONG_NUMBER=re.compile(r'(?<!\d)\d{10,12}(?!\d)')
IRAN_MOBILE=re.compile(r'(?<!\d)0?9\d{2}[- ]?\d{3}[- ]?\d{4}(?!\d)')

def scan_docx_for_sensitive_numbers(path:Path):
    problems=[]
    try:
        with ZipFile(path) as archive:
            chunks=[]
            for name in archive.namelist():
                if name.endswith('.xml'):
                    try: root=ET.fromstring(archive.read(name))
                    except ET.ParseError: continue
                    chunks.extend(node.text or '' for node in root.iter() if node.tag.endswith('}t'))
    except Exception as exc: return [f'{path.name}: unable to inspect DOCX: {exc}']
    text=' '.join(chunks)
    if LONG_NUMBER.search(text): problems.append(f'{path.name}: contains a 10–12 digit numeric string')
    if IRAN_MOBILE.search(text): problems.append(f'{path.name}: contains a phone-number-like string')
    return problems

def _check_design_assets(root:Path):
    """Compatibility helper: return missing shared branding assets referenced by design settings."""
    import json
    root=Path(root); errors=[]
    try:
        design=json.loads((root/'content/settings/design.json').read_text(encoding='utf-8'))
    except Exception as exc:
        return [f'content/settings/design.json: {exc}']
    for key,value in design.get('branding',{}).items():
        if key not in {'favicon','profile_image','cv_pdf','cv_docx','open_graph_image','logo'}:
            continue
        if isinstance(value,str) and value and not value.startswith(('http://','https://')) and not (root/value.lstrip('/')).exists():
            errors.append(f'design branding.{key}: missing file {value}')
    return errors

def check_site(root:Path):
    root=Path(root); errors=validate_repository(root)
    if not (root/'.nojekyll').exists(): errors.append('.nojekyll is missing')
    errors.extend(_check_design_assets(root))
    for docx in (root/'assets/uploads').rglob('*.docx'): errors.extend(scan_docx_for_sensitive_numbers(docx))
    return errors
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]; problems=check_site(root)
    if problems:
        print('Site validation failed:'); [print(f'- {p}') for p in problems]; raise SystemExit(1)
    print('Site validation passed: source content, CMS, routes, themes, assets, and privacy checks are clean.')
