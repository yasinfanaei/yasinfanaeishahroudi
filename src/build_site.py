from __future__ import annotations
import argparse, json, shutil
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

if __package__ in {None, ""}:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.content_loader import load_json
    from src.models import load_pages, page_by_id, translation_pairs, normalize_contacts
    from src.routes import output_path, public_path
    from src.navigation import resolve_navigation
    from src.themes import get_theme, css_variables
    from src.blocks import render_blocks
    from src.citations import citation_payload
    from src.richtext import render_rich_text
    from src.urls import site_href
    from src.seo import page_seo_context, page_indexable, page_in_sitemap, absolute_url, build_sitemap, build_robots, validate_redirects
else:
    from .content_loader import load_json
    from .models import load_pages, page_by_id, translation_pairs, normalize_contacts
    from .routes import output_path, public_path
    from .navigation import resolve_navigation
    from .themes import get_theme, css_variables
    from .blocks import render_blocks
    from .citations import citation_payload
    from .richtext import render_rich_text
    from .urls import site_href
    from .seo import page_seo_context, page_indexable, page_in_sitemap, absolute_url, build_sitemap, build_robots, validate_redirects


def _dataset(root, locale, name):
    return load_json(root/f'content/{locale}/{name}.json')


def _contact_href(item):
    if item.get('url'):
        return item['url']
    if item['type']=='email':
        return 'mailto:'+item['value']
    if item['type']=='phone':
        return 'tel:'+''.join(ch for ch in item['value'] if ch.isdigit() or ch=='+')
    if item['type']=='whatsapp':
        return 'https://wa.me/'+''.join(ch for ch in item['value'] if ch.isdigit())
    if item['type']=='telegram':
        return 'https://t.me/'+item['value'].lstrip('@')
    if item['type']=='website' and item['value'].startswith('https://'):
        return item['value']
    return ''


def _theme_css(design):
    preset=design.get('theme',{}).get('preset','classic-academic')
    theme=get_theme(preset,design)
    layout=design.get('layout',{})
    extra={
        '--content-width':f"{int(layout.get('max_width',1100))}px",
        '--section-space':f"{int(layout.get('section_spacing',62))}px",
        '--portrait-size':f"{int(layout.get('portrait_size',300))}px",
        '--portrait-radius':f"{int(layout.get('portrait_radius',18))}px",
        '--button-radius':f"{int(layout.get('button_radius',8))}px",
        '--card-radius':f"{int(layout.get('card_radius',14))}px",
        '--nav-gap':f"{int(layout.get('nav_gap',20))}px",
    }
    extra_css=';'.join(f'{k}:{v}' for k,v in extra.items())
    return ':root{'+css_variables(theme['light'])+';'+extra_css+'}html[data-theme="dark"]{'+css_variables(theme['dark'])+'}'


def _flatten_text(value):
    if isinstance(value,dict):
        return ' '.join(_flatten_text(v) for v in value.values())
    if isinstance(value,list):
        return ' '.join(_flatten_text(v) for v in value)
    return str(value or '')


def _public_news(news):
    clean=dict(news or {})
    clean['items']=[item for item in (clean.get('items') or []) if item.get('published',True)]
    return clean


def _search_text_for_page(page, data, profile):
    """Build a public-only index document from blocks actually used on this page."""
    parts=[page.get('title',''), page.get('seo',{}).get('description','')]
    for block in page.get('blocks',[]):
        if not block.get('enabled',True):
            continue
        btype=block.get('type')
        # Include user-authored block text but omit structural fields.
        parts.append(_flatten_text({k:v for k,v in block.items() if k not in {'id','type','enabled'}}))
        if btype=='profile_hero':
            parts.append(_flatten_text({k:v for k,v in profile.items() if k not in {'contacts'}}))
            parts.append(_flatten_text(data.get('research',{}).get('interests',[])))
        elif btype=='research_themes': parts.append(_flatten_text(data.get('research',{})))
        elif btype=='education_timeline': parts.append(_flatten_text(data.get('education',{})))
        elif btype=='publication_index': parts.append(_flatten_text(data.get('publications',{})))
        elif btype=='news_list': parts.append(_flatten_text(_public_news(data.get('news',{}))))
        elif btype=='experience_list': parts.append(_flatten_text(data.get('experience',{})))
        elif btype=='projects_list': parts.append(_flatten_text(data.get('projects',{})))
        elif btype=='awards_list': parts.append(_flatten_text(data.get('awards',{})))
        elif btype=='skills_list': parts.append(_flatten_text(data.get('skills',{})))
    return ' '.join(x for x in parts if x).strip()


def _layout_classes(design):
    presets=design.get('layout_presets',{})
    classes=[
        f"layout-width-{presets.get('content_width','standard')}",
        f"layout-density-{presets.get('section_density','standard')}",
        f"layout-card-{presets.get('card_style','border')}",
        f"layout-header-{presets.get('header_style','standard')}",
        f"layout-corners-{presets.get('corner_style','subtle')}",
    ]
    controls=design.get('controls',{})
    if not controls.get('show_shadows',True): classes.append('design-no-shadow')
    if not controls.get('sticky_header',True): classes.append('design-header-static')
    side=design.get('layout',{}).get('portrait_side','automatic')
    if side in {'left','right','hidden'}: classes.append(f'design-portrait-{side}')
    return ' '.join(classes)


def _analytics_context(design):
    a=design.get('analytics',{})
    measurement=str(a.get('measurement_id','')).strip()
    enabled=bool(a.get('enabled')) and a.get('provider')=='google_analytics' and measurement.startswith('G-')
    return {'enabled':enabled,'measurement_id':measurement if enabled else ''}


def _prepare_publications(data):
    items=[]
    for raw in data.get('publications',{}).get('items',[]):
        item=dict(raw)
        item['_citation']=citation_payload(item)
        items.append(item)
    data['publications']=dict(data.get('publications',{}), items=items)
    return {
        'types':sorted({str(i.get('type','')).strip() for i in items if str(i.get('type','')).strip()}),
        'statuses':sorted({str(i.get('status','')).strip() for i in items if str(i.get('status','')).strip()}),
        'years':sorted({str(i.get('year','')).strip() for i in items if str(i.get('year','')).strip()}, reverse=True),
    }


def build_site(root: Path, output: Path) -> None:
    root=Path(root); output=Path(output)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    env=Environment(loader=FileSystemLoader(root/'src/templates'),autoescape=select_autoescape(['html','xml']))
    design=load_json(root/'content/settings/design.json')
    site_url=design.get('seo',{}).get('site_url','https://yasinfanaei.github.io').rstrip('/')
    env.filters['site_href']=lambda value: site_href(site_url,value)
    env.filters['safe_rich_text']=lambda value: render_rich_text(value,site_url)
    pages_by_locale={loc:load_pages(root,loc) for loc in ('en','fa')}
    pairs=translation_pairs(pages_by_locale['en'],pages_by_locale['fa'])
    sitemap_entries=[]; search_indexes={'en':[],'fa':[]}; aliases={}; real_paths=set()
    for locale in ('en','fa'):
        pages=pages_by_locale[locale]; by_id=page_by_id(pages); site=_dataset(root,locale,'site'); profile=_dataset(root,locale,'profile')
        data={name:_dataset(root,locale,name) for name in ('education','research','publications','projects','experience','awards','skills','news')}
        publication_filters=_prepare_publications(data)
        contacts=normalize_contacts(profile)
        def prepared_contacts(flag):
            out=[]
            for c in contacts:
                if c['enabled'] and c.get(flag):
                    d=dict(c); d['href']=_contact_href(c); out.append(d)
            return out
        navigation=resolve_navigation(site.get('navigation',[]),pages,locale,site_url)
        for page in pages:
            route=public_path(locale,page['slug']); real_paths.add(route)
            if page['status']!='published':
                continue
            pair=pairs.get(page['translation_key'],{}); other_locale='fa' if locale=='en' else 'en'; other=pair.get(other_locale)
            seo=page_seo_context(locale,page,pairs,design,profile)
            default_mode=design.get('theme',{}).get('default_mode','system')
            ctx={
                'locale':locale,'page':page,'site':site,'profile':profile,'design':design,'data':data,'navigation':navigation,
                'home_href':site_href(site_url,public_path(locale,by_id['home']['slug'])),'search_href':site_href(site_url,public_path(locale,by_id['search']['slug'])),
                'language_href':site_href(site_url,public_path(other_locale,other['slug'])) if other and other.get('status')=='published' else site_href(site_url,public_path(other_locale,'')),
                'other_locale':other_locale,'initial_theme':default_mode if default_mode in {'light','dark'} else 'light','default_theme':default_mode,
                'theme_css':_theme_css(design),'favicon':design.get('branding',{}).get('favicon',''),'build_year':datetime.now().year,
                'contact_methods':prepared_contacts('show_contact'),'home_contacts':prepared_contacts('show_home'),'footer_contacts':prepared_contacts('show_footer'),
                'academic_links':[(k.replace('_',' ').title(),v) for k,v in profile.get('links',{}).items() if v],
                'page_links':{pid:site_href(site_url,public_path(locale,p['slug'])) for pid,p in by_id.items()},'seo':seo,'site_url':site_url,
                'layout_classes':_layout_classes(design),'analytics':_analytics_context(design),'publication_filters':publication_filters,
            }
            ctx['rendered_blocks']=render_blocks(env,page,ctx)
            html=env.get_template('page.html').render(**ctx)
            dest=output_path(locale,page['slug'],output); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(html,encoding='utf-8')
            indexing_enabled=design.get('seo',{}).get('indexing_enabled') is not False
            if page_in_sitemap(page,indexing_enabled):
                sitemap_entries.append({'url':seo['canonical']})
            if page_indexable(page,indexing_enabled):
                search_indexes[locale].append({'id':page['id'],'title':page['title'],'url':site_href(site_url,route),'text':_search_text_for_page(page,data,profile)})
            for alias in page.get('redirect_from',[]) or []:
                src='/' + ('fa/' if locale=='fa' else '') + str(alias).lstrip('/')
                aliases[src]=route
    extra=load_json(root/'content/settings/redirects.json').get('aliases',[])
    if isinstance(extra,list):
        for item in extra:
            if item.get('from') and item.get('to'):
                aliases[item['from']]=item['to']
    validate_redirects(aliases,real_paths)
    for src,target in aliases.items():
        dest=output/src.lstrip('/'); dest.parent.mkdir(parents=True,exist_ok=True)
        locale='fa' if src.startswith('/fa/') else 'en'; canonical=absolute_url(site_url,target); browser_target=site_href(site_url,target)
        dest.write_text(env.get_template('redirect.html').render(locale=locale,target=browser_target,canonical=canonical),encoding='utf-8')
    for locale,index in search_indexes.items():
        (output/f'search-index.{locale}.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (output/'sitemap.xml').write_text(build_sitemap(sitemap_entries),encoding='utf-8')
    (output/'robots.txt').write_text(build_robots(site_url,design.get('seo',{}).get('indexing_enabled') is not False),encoding='utf-8')
    (output/'404.html').write_text(env.get_template('404.html').render(home_href=site_href(site_url,'/'),fa_home_href=site_href(site_url,'/fa/'),style_href=site_href(site_url,'/assets/style.css')),encoding='utf-8')
    (output/'.nojekyll').write_text('',encoding='utf-8')
    (output/'assets').mkdir(exist_ok=True)
    shutil.copy2(root/'src/static/style.css',output/'assets/style.css')
    shutil.copy2(root/'src/static/site.js',output/'assets/site.js')
    favicon=root/'assets/favicon.svg'
    if favicon.exists(): shutil.copy2(favicon,output/'assets/favicon.svg')
    uploads=root/'assets/uploads'
    if uploads.exists(): shutil.copytree(uploads,output/'assets/uploads',dirs_exist_ok=True)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='_site'); args=parser.parse_args(); build_site(Path.cwd(),Path(args.output))


if __name__=='__main__':
    main()
