#!/usr/bin/env python3
from __future__ import annotations
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]; self.canonical=''
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in {'a','link'} and d.get('href'): self.refs.append(d['href'])
        if tag=='link' and d.get('rel')=='canonical' and d.get('href'): self.canonical=d['href']
        if tag in {'img','script'} and d.get('src'): self.refs.append(d['src'])

def _target(root:Path, current:Path, ref:str, base_path:str=''):
    u=urlsplit(ref)
    if u.scheme or ref.startswith('#') or ref.startswith('mailto:') or ref.startswith('tel:'): return None
    path=u.path
    if not path: return None
    if path.startswith('/'):
        if base_path and (path == base_path or path.startswith(base_path + '/')):
            path = path[len(base_path):] or '/'
        rel=path.lstrip('/')
        p=root/rel
    else: p=current.parent/path
    if path.endswith('/'): p=p/'index.html'
    return p

def check_build(root:Path)->list[str]:
    root=Path(root); errors=[]; base_path=''
    if not (root/'index.html').exists(): errors.append('missing index.html')
    else:
        home_parser=Parser(); home_parser.feed((root/'index.html').read_text(encoding='utf-8',errors='ignore'))
        if home_parser.canonical:
            base_path=urlsplit(home_parser.canonical).path.rstrip('/')
    for html in root.rglob('*.html'):
        parser=Parser(); parser.feed(html.read_text(encoding='utf-8',errors='ignore'))
        for ref in parser.refs:
            target=_target(root,html,ref,base_path)
            if target is not None and not target.exists(): errors.append(f'{html.relative_to(root)}: broken local reference {ref!r}')
    for required in ('sitemap.xml','robots.txt','404.html','assets/style.css','assets/site.js','search-index.en.json','search-index.fa.json'):
        if not (root/required).exists(): errors.append(f'missing build artifact: {required}')
    return errors

if __name__=='__main__':
    root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
    errors=check_build(root)
    if errors:
        print('Build validation failed:'); [print(f'- {e}') for e in errors]; raise SystemExit(1)
    print('Build validation passed.')
