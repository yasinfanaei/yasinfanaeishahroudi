from __future__ import annotations
from .routes import public_path
from .urls import validate_external_url, site_href

def _resolve(item: dict, pages_by_id: dict, locale: str, depth: int = 0, site_url: str = "") -> dict | None:
    if not item.get('enabled', True):
        return None
    if depth > 1:
        raise ValueError('navigation supports one submenu level only')
    dest=item.get('destination','page')
    out={'label':str(item.get('label','')).strip(),'target':'','rel':''}
    if dest=='page':
        pid=item.get('page') or item.get('id')
        page=pages_by_id.get(pid)
        if not page or page.get('status')!='published':
            raise ValueError(f'navigation references missing page: {pid}')
        out['href']=site_href(site_url, public_path(locale,page.get('slug','')))
    elif dest=='section':
        anchor=str(item.get('section','')).strip().lstrip('#')
        if not anchor: raise ValueError('section destination requires section')
        out['href']=site_href(site_url, public_path(locale,'')) + f'#{anchor}'
    elif dest=='external':
        url=str(item.get('url','')).strip(); validate_external_url(url)
        if not url.startswith('https://'): raise ValueError('external navigation URL must use https')
        out['href']=url
        if item.get('new_tab'):
            out['target']='_blank'; out['rel']='noopener noreferrer'
    elif dest=='file':
        url=str(item.get('url','')).strip()
        if not url: raise ValueError('file destination requires url')
        out['href']=site_href(site_url, '/' + url.lstrip('/'))
    else:
        raise ValueError(f'unknown navigation destination: {dest}')
    children=[]
    for child in item.get('children',[]) or []:
        resolved=_resolve(child,pages_by_id,locale,depth+1,site_url)
        if resolved: children.append(resolved)
    out['children']=children
    return out

def resolve_navigation(navigation: list[dict], pages: list[dict], locale: str, site_url: str = "") -> list[dict]:
    pages_by_id={p['id']:p for p in pages}
    result=[]
    for item in navigation or []:
        resolved=_resolve(item,pages_by_id,locale,site_url=site_url)
        if resolved: result.append(resolved)
    return result
