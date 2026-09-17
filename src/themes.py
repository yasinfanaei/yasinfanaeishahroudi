from __future__ import annotations

SEMANTIC_TOKENS = (
    'background','surface','surface_alt','text','text_muted','border','accent','accent_hover','accent_text',
    'link','link_hover','button_primary_bg','button_primary_text','button_secondary_bg','button_secondary_text',
    'tag_bg','tag_text','focus_ring','success','warning','danger'
)

def _hex_to_rgb(value: str):
    value=value.lstrip('#')
    if len(value)==3: value=''.join(ch*2 for ch in value)
    if len(value)!=6: raise ValueError(f'invalid hex color: {value}')
    return tuple(int(value[i:i+2],16)/255 for i in (0,2,4))

def _linear(c: float) -> float:
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4

def contrast_ratio(fg: str, bg: str) -> float:
    def lum(v):
        r,g,b=_hex_to_rgb(v)
        return 0.2126*_linear(r)+0.7152*_linear(g)+0.0722*_linear(b)
    a,b=lum(fg),lum(bg)
    hi,lo=max(a,b),min(a,b)
    return (hi+0.05)/(lo+0.05)

def _light(background, surface, surface_alt, text, muted, border, accent, accent_hover, link, link_hover, focus, tag_bg, tag_text=None):
    tag_text=tag_text or text
    return {
      'background':background,'surface':surface,'surface_alt':surface_alt,'text':text,'text_muted':muted,'border':border,
      'accent':accent,'accent_hover':accent_hover,'accent_text':'#ffffff','link':link,'link_hover':link_hover,
      'button_primary_bg':accent,'button_primary_text':'#ffffff','button_secondary_bg':surface_alt,'button_secondary_text':text,
      'tag_bg':tag_bg,'tag_text':tag_text,'focus_ring':focus,'success':'#176b3a','warning':'#7a4b00','danger':'#a12525'
    }

def _dark(background, surface, surface_alt, text, muted, border, accent, accent_hover, link, link_hover, focus, tag_bg, tag_text=None):
    tag_text=tag_text or text
    return {
      'background':background,'surface':surface,'surface_alt':surface_alt,'text':text,'text_muted':muted,'border':border,
      'accent':accent,'accent_hover':accent_hover,'accent_text':'#0b1112','link':link,'link_hover':link_hover,
      'button_primary_bg':accent,'button_primary_text':'#0b1112','button_secondary_bg':surface_alt,'button_secondary_text':text,
      'tag_bg':tag_bg,'tag_text':tag_text,'focus_ring':focus,'success':'#79d69c','warning':'#f2ca72','danger':'#ff9a9a'
    }

BUILTIN_THEMES = {
 'classic-academic': {
   'light': _light('#fbfbf8','#ffffff','#eef5f3','#171717','#555b55','#d7ddd8','#164e63','#0e3c4d','#164e63','#0e3c4d','#0f766e','#e5f0ed','#173f3a'),
   'dark': _dark('#101311','#181c19','#222a25','#f4f5f2','#b7c0b8','#3a453d','#8fc7d8','#a8d7e4','#9fd6e5','#b9e3ec','#7dd3c7','#26352f','#e7f4ef'),
 },
 'oxford-navy': {
   'light': _light('#faf9f5','#ffffff','#eef1f6','#151b2b','#535d70','#d7dce7','#17365d','#0f2949','#17365d','#0f2949','#245f9e','#e6ebf3','#1a2b45'),
   'dark': _dark('#0d1420','#151e2d','#202c3f','#f5f7fb','#b8c3d4','#35445d','#9fc5f8','#b8d5fa','#a9cdfa','#c2ddff','#8bb7ef','#24334a','#edf4ff'),
 },
 'midnight-teal': {
   'light': _light('#f7fbfa','#ffffff','#e7f4f2','#102522','#4f625e','#cfe0dc','#075e59','#044843','#075e59','#044843','#0c7c73','#dff2ef','#123f3b'),
   'dark': _dark('#071615','#0d201e','#15302d','#f1fbf9','#b2cbc6','#2d504b','#7ee0d3','#98e9df','#8de6da','#b1f0e8','#60d4c6','#183d38','#e2faf6'),
 },
 'burgundy-cream': {
   'light': _light('#fffaf2','#ffffff','#f6eee6','#241719','#66565a','#e3d7d3','#6f1d36','#55152a','#6f1d36','#55152a','#8b2d4b','#f4e5ea','#572033'),
   'dark': _dark('#1a1114','#24181c','#342329','#fff7f1','#d2bdc2','#543a43','#f0a9bd','#f5bfd0','#f2b4c6','#ffd0dd','#de8daa','#402831','#fff1f5'),
 },
 'forest-ivory': {
   'light': _light('#fcfbf2','#ffffff','#edf3e8','#182018','#596158','#d8ded2','#285b35','#1d4528','#285b35','#1d4528','#3f7c4d','#e6f0df','#26452b'),
   'dark': _dark('#10160f','#171f16','#233022','#f5f8f1','#bdc8b8','#3a4d38','#9bd2a4','#b1ddb8','#a8d7af','#c4e7ca','#83c38f','#2b3f29','#eef8ec'),
 },
 'slate-blue': {
   'light': _light('#f8f9fc','#ffffff','#edf0f7','#171b26','#565e70','#d7dce8','#344b7a','#283b61','#344b7a','#283b61','#496da8','#e7ecf6','#263a61'),
   'dark': _dark('#11141b','#191e28','#252d3b','#f4f6fb','#b9c1d0','#3c4658','#a8c4ff','#bfd3ff','#b0c9ff','#cfddff','#91aff0','#2d3850','#f0f4ff'),
 },
 'monochrome-editorial': {
   'light': _light('#fafafa','#ffffff','#ededed','#111111','#555555','#d0d0d0','#242424','#0f0f0f','#242424','#0f0f0f','#555555','#e8e8e8','#202020'),
   'dark': _dark('#0d0d0d','#171717','#252525','#f5f5f5','#bdbdbd','#3d3d3d','#e3e3e3','#f1f1f1','#e5e5e5','#ffffff','#cfcfcf','#2a2a2a','#f5f5f5'),
 },
}

def get_theme(name: str, design: dict) -> dict:
    if name == 'custom':
        custom=design.get('custom_theme',{})
        if not all(mode in custom for mode in ('light','dark')):
            raise ValueError('custom theme requires light and dark palettes')
        for mode in ('light','dark'):
            missing=set(SEMANTIC_TOKENS)-set(custom[mode])
            if missing: raise ValueError(f'custom/{mode} missing tokens: {sorted(missing)}')
        return custom
    if name not in BUILTIN_THEMES:
        raise ValueError(f'unknown theme preset: {name}')
    return BUILTIN_THEMES[name]

def css_variables(tokens: dict) -> str:
    return ';'.join(f'--{key.replace("_","-")}:{value}' for key,value in tokens.items())
