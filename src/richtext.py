from __future__ import annotations
from html import escape
from html.parser import HTMLParser
from markupsafe import Markup
from urllib.parse import urlsplit
from .urls import site_href

ALLOWED_TAGS={'p','br','strong','b','em','i','u','s','a','ul','ol','li','h2','h3','h4','blockquote','code','pre','hr'}
VOID_TAGS={'br','hr'}
SUPPRESS_TAGS={'script','style','iframe','object','embed','svg','math'}


def _safe_href(value:str, site_url:str="")->str:
    value=(value or '').strip()
    if not value:
        return ''
    if value.startswith('#'):
        return value
    if value.startswith('/'):
        return site_href(site_url, value)
    parts=urlsplit(value)
    if parts.scheme.lower() in {'https','mailto','tel'}:
        return value
    return ''


class _Sanitizer(HTMLParser):
    def __init__(self, site_url: str = ""):
        super().__init__(convert_charrefs=True)
        self.site_url=site_url
        self.out=[]
        self.suppress=0
    def handle_starttag(self,tag,attrs):
        tag=tag.lower()
        if tag in SUPPRESS_TAGS:
            self.suppress+=1; return
        if self.suppress or tag not in ALLOWED_TAGS:
            return
        kept=[]
        if tag=='a':
            amap=dict(attrs)
            href=_safe_href(amap.get('href',''), self.site_url)
            if href:
                kept.append(('href',href))
            if amap.get('title'):
                kept.append(('title',amap['title']))
            if href.startswith('https://'):
                kept.extend([('target','_blank'),('rel','noopener noreferrer')])
        attr_text=''.join(f' {name}="{escape(str(value), quote=True)}"' for name,value in kept)
        self.out.append(f'<{tag}{attr_text}>')
    def handle_startendtag(self,tag,attrs):
        tag=tag.lower()
        if not self.suppress and tag in VOID_TAGS:
            self.out.append(f'<{tag}>')
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag in SUPPRESS_TAGS:
            if self.suppress: self.suppress-=1
            return
        if self.suppress or tag not in ALLOWED_TAGS or tag in VOID_TAGS:
            return
        self.out.append(f'</{tag}>')
    def handle_data(self,data):
        if not self.suppress:
            self.out.append(escape(data))


def render_rich_text(value:str|None, site_url:str="")->Markup:
    text=str(value or '').strip()
    if not text:
        return Markup('')
    # Older/plain content remains useful without requiring HTML from the editor.
    if '<' not in text:
        paras=[f'<p>{escape(part.strip()).replace(chr(10), "<br>")}</p>' for part in text.split('\n\n') if part.strip()]
        return Markup(''.join(paras))
    parser=_Sanitizer(site_url); parser.feed(text); parser.close()
    return Markup(''.join(parser.out))
