#!/usr/bin/env python3
from pathlib import Path
import yaml

def validate_pages_config(root:Path):
    p=Path(root)/'.pages.yml'; errors=[]
    if not p.exists(): return ['.pages.yml is missing']
    try: cfg=yaml.safe_load(p.read_text(encoding='utf-8'))
    except yaml.YAMLError as exc: return [f'.pages.yml: invalid YAML: {exc}']
    if not isinstance(cfg,dict): return ['.pages.yml must be an object']
    media=cfg.get('media',[]); names={x.get('name') for x in media if isinstance(x,dict)}
    for name in {'images','documents','publication_files'}:
        if name not in names: errors.append(f'missing media source {name}')
    text=p.read_text(encoding='utf-8')
    for marker in ('content/pages/en','content/pages/fa','type: block','blockKey: type','name: contacts','name: navigation','classic-academic'):
        if marker not in text: errors.append(f'missing CMS feature: {marker}')
    if not any(a.get('name')=='validate-site' for a in cfg.get('actions',[]) if isinstance(a,dict)): errors.append('missing validate-site action')
    return errors
if __name__=='__main__':
    import sys
    problems=validate_pages_config(Path(__file__).resolve().parents[1])
    if problems: [print(f'ERROR: {x}') for x in problems]; sys.exit(1)
    print('Pages CMS configuration validation passed.')
