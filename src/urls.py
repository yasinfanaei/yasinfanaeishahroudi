from urllib.parse import urlparse
SAFE_SCHEMES={'https','mailto','tel'}

def validate_external_url(url:str)->None:
    if not url:return
    parsed=urlparse(url)
    if parsed.scheme not in SAFE_SCHEMES:
        raise ValueError(f'unsafe URL scheme: {parsed.scheme or "missing"}')

def site_base_path(site_url: str) -> str:
    parsed=urlparse(str(site_url or '').strip())
    path=(parsed.path or '').rstrip('/')
    return path if path and path != '/' else ''

def site_href(site_url: str, href: str) -> str:
    value=str(href or '').strip()
    if not value:
        return ''
    if value.startswith('#'):
        return value
    parsed=urlparse(value)
    if parsed.scheme:
        return value if parsed.scheme in SAFE_SCHEMES else ''
    if value.startswith('//'):
        return ''
    base=site_base_path(site_url)
    if value.startswith('/'):
        if base and (value == base or value.startswith(base + '/')):
            return value
        return (base + value) if base else value
    local='/' + value.lstrip('/')
    return (base + local) if base else local
