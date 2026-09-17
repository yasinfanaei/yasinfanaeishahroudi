from __future__ import annotations
from markupsafe import Markup

SUPPORTED_BLOCKS = {
 'profile_hero','heading','rich_text','image','callout','buttons','cards','contact_methods','academic_links',
 'research_themes','education_timeline','publication_index','news_list','experience_list','projects_list','awards_list',
 'skills_list','downloads','accordion','divider','search'
}

def render_blocks(env, page: dict, context: dict) -> Markup:
    rendered=[]
    for block in page.get('blocks',[]):
        if not block.get('enabled', True):
            continue
        btype=block.get('type')
        if btype not in SUPPORTED_BLOCKS:
            raise ValueError(f'unknown block type: {btype}')
        template=env.get_template(f'blocks/{btype}.html')
        rendered.append(template.render(block=block, **context))
    return Markup('\n'.join(rendered))
