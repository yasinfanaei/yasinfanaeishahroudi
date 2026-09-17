from __future__ import annotations
import html
from urllib.parse import urlparse

def absolute_url(site_url: str, path: str) -> str:
    return site_url.rstrip('/') + '/' + path.lstrip('/')

def page_indexable(page: dict, indexing_enabled: bool = True) -> bool:
    return bool(indexing_enabled and page.get('status') == 'published' and not page.get('seo',{}).get('noindex'))

def page_in_sitemap(page: dict, indexing_enabled: bool = True) -> bool:
    return bool(page_indexable(page,indexing_enabled) and page.get('show_in_sitemap', True))

def public_indexable(page: dict, indexing_enabled: bool = True) -> bool:
    # Backward-compatible name: public/search indexing is independent from sitemap visibility.
    return page_indexable(page,indexing_enabled)

def validate_redirects(aliases: dict[str,str], real_paths: set[str]) -> None:
    for src,dst in aliases.items():
        if src in real_paths:
            raise ValueError(f'redirect alias collides with real route: {src}')
        if not src.startswith('/') or not dst.startswith('/'):
            raise ValueError('redirect paths must be internal absolute paths')
        if src == dst:
            raise ValueError(f'redirect loop: {src}')
    for start in aliases:
        seen=set(); cur=start
        while cur in aliases:
            if cur in seen:
                raise ValueError(f'redirect loop involving {start}')
            seen.add(cur); cur=aliases[cur]

def breadcrumb_jsonld(site_url: str, locale: str, page: dict, home_title: str) -> dict:
    from .routes import public_path
    return {
      '@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':home_title,'item':absolute_url(site_url, public_path(locale,''))},
        {'@type':'ListItem','position':2,'name':page['title'],'item':absolute_url(site_url, public_path(locale,page['slug']))},
      ]
    }

def page_seo_context(locale: str, page: dict, pairs: dict, design: dict, profile: dict) -> dict:
    from .routes import public_path
    site_url=design.get('seo',{}).get('site_url','https://yasinfanaei.github.io').rstrip('/')
    pseo=page.get('seo',{})
    canonical_override=str(pseo.get('canonical_override','')).strip()
    canonical=canonical_override if canonical_override.startswith('https://') else absolute_url(site_url, public_path(locale,page['slug']))
    title=pseo.get('title') or page['title']
    description=pseo.get('description','')
    indexing_enabled=design.get('seo',{}).get('indexing_enabled') is not False
    robots='index,follow' if page_indexable(page,indexing_enabled) else 'noindex,nofollow'
    alternates=[]; pair=pairs.get(page['translation_key'],{})
    for lang in ('en','fa'):
        other=pair.get(lang)
        if other and other.get('status')=='published':
            alternates.append({'lang':lang,'href':absolute_url(site_url,public_path(lang,other['slug']))})
    en=pair.get('en')
    if en and en.get('status')=='published': alternates.append({'lang':'x-default','href':absolute_url(site_url,public_path('en',en['slug']))})
    image=pseo.get('image') or design.get('branding',{}).get('open_graph_image','')
    if image and not image.startswith('http'): image=absolute_url(site_url,'/'+image.lstrip('/'))
    jsonld=[]
    if design.get('seo',{}).get('structured_data_enabled',True):
        if page['id']=='home':
            person={'@type':'Person','name':profile.get('name'),'url':canonical}
            if profile.get('headline'): person['jobTitle']=profile['headline']
            if profile.get('affiliation'): person['affiliation']={'@type':'EducationalOrganization','name':profile['affiliation']}
            same=[v for v in profile.get('links',{}).values() if v]
            if same: person['sameAs']=same
            if image: person['image']=image
            jsonld.append({'@context':'https://schema.org','@type':'ProfilePage','url':canonical,'mainEntity':person})
        else:
            jsonld.append(breadcrumb_jsonld(site_url,locale,page,'خانه' if locale=='fa' else 'Home'))
    return {'title':title,'description':description,'canonical':canonical,'robots':robots,'alternates':alternates,'image':image,'jsonld':jsonld}

def build_sitemap(entries: list[dict]) -> str:
    rows=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for entry in entries:
        rows.append(f"  <url><loc>{html.escape(entry['url'])}</loc></url>")
    rows.append('</urlset>')
    return '\n'.join(rows)+'\n'

def build_robots(site_url: str, indexing_enabled: bool) -> str:
    if indexing_enabled:
        return f'User-agent: *\nAllow: /\n\nSitemap: {absolute_url(site_url,"/sitemap.xml")}\n'
    return 'User-agent: *\nDisallow: /\n'
