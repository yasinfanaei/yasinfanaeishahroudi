from __future__ import annotations


def _clean(value) -> str:
    return str(value or '').strip()


def citation_payload(item: dict) -> dict[str, str]:
    title = _clean(item.get('official_english_title') or item.get('title'))
    authors = [str(a).strip() for a in (item.get('authors') or []) if str(a).strip()]
    venue = _clean(item.get('venue'))
    year = _clean(item.get('year'))
    doi = _clean(item.get('doi'))
    volume = _clean(item.get('volume'))
    issue = _clean(item.get('issue'))
    pages = _clean(item.get('pages'))

    citation_parts = []
    if authors:
        citation_parts.append(', '.join(authors))
    if year:
        citation_parts.append(f'({year})')
    if title:
        citation_parts.append(title)
    if venue:
        citation_parts.append(venue)
    if volume:
        citation_parts.append(f'vol. {volume}')
    if issue:
        citation_parts.append(f'no. {issue}')
    if pages:
        citation_parts.append(f'pp. {pages}')
    if doi:
        citation_parts.append(f'DOI: {doi}')
    citation = '. '.join(part.rstrip('.') for part in citation_parts if part).strip()
    if citation and not citation.endswith('.'):
        citation += '.'

    kind = {'journal': 'article', 'conference': 'inproceedings'}.get(_clean(item.get('type')).lower(), 'misc')
    key = _clean(item.get('id')) or 'publication'
    bib_fields = []
    if authors:
        bib_fields.append(('author', ' and '.join(authors)))
    if title:
        bib_fields.append(('title', title))
    if venue:
        field = 'journal' if kind == 'article' else ('booktitle' if kind == 'inproceedings' else 'howpublished')
        bib_fields.append((field, venue))
    for field, value in (('year', year), ('volume', volume), ('number', issue), ('pages', pages), ('doi', doi)):
        if value:
            bib_fields.append((field, value))
    bib_body = ',\n'.join(f'  {field} = {{{value}}}' for field, value in bib_fields)
    bibtex = f'@{kind}{{{key}' + (',\n' + bib_body if bib_body else '') + '\n}'

    ty = {'journal': 'JOUR', 'conference': 'CONF'}.get(_clean(item.get('type')).lower(), 'GEN')
    ris = [f'TY  - {ty}']
    for author in authors:
        ris.append(f'AU  - {author}')
    if title:
        ris.append(f'TI  - {title}')
    if venue:
        ris.append(f'T2  - {venue}')
    if year:
        ris.append(f'PY  - {year}')
    if volume:
        ris.append(f'VL  - {volume}')
    if issue:
        ris.append(f'IS  - {issue}')
    if pages:
        ris.append(f'SP  - {pages}')
    if doi:
        ris.append(f'DO  - {doi}')
    ris.append('ER  -')
    return {'citation': citation, 'bibtex': bibtex, 'ris': '\n'.join(ris)}
