import re
from pathlib import Path

_SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

def validate_slug(slug: str, home: bool = False) -> None:
    if slug == '' and home:
        return
    if not slug or not _SLUG_RE.fullmatch(slug):
        raise ValueError(f'invalid slug: {slug!r}')

def public_path(locale: str, slug: str) -> str:
    if locale not in {'en', 'fa'}:
        raise ValueError(f'unsupported locale: {locale}')
    if slug:
        validate_slug(slug)
    prefix = '/fa/' if locale == 'fa' else '/'
    return prefix if not slug else f'{prefix}{slug}/'

def output_path(locale: str, slug: str, output_root: Path) -> Path:
    output_root = Path(output_root)
    if locale == 'en':
        return output_root / ('index.html' if not slug else f'{slug}/index.html')
    if locale == 'fa':
        return output_root / 'fa' / ('index.html' if not slug else f'{slug}/index.html')
    raise ValueError(f'unsupported locale: {locale}')
