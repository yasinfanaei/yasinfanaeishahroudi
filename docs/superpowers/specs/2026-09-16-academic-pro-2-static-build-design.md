# Academic Pro 2 — Static Build + Full CMS Design Spec

**Date:** 2026-09-16  
**Status:** Approved by user; implemented and verified  
**Repository:** `yasinfanaei/yasinfanaei.github.io`  
**Primary goal:** Turn the existing bilingual academic site into a durable no-code publishing system where routine content, pages, navigation, contacts, themes, SEO, and layout are managed from Pages CMS while the public site is generated as fast, semantic, static HTML with clean URLs.

## 1. Goals

Academic Pro 2 must satisfy these goals:

1. Keep the public site bilingual: English at `/` and Persian under `/fa/`.
2. Replace client-side page composition with a build step that emits complete HTML for every public page.
3. Use clean, directory-style URLs such as `/research/` and `/fa/research/`.
4. Let the user create, delete, rename, publish, unpublish, reorder, and edit pages from Pages CMS without editing HTML/CSS/JS.
5. Let the user create and reorder navigation items and one-level submenus from Pages CMS.
6. Let the user add unlimited public contact methods such as multiple emails, phone numbers, WhatsApp, Telegram, websites, office addresses, and custom contact items.
7. Add professionally designed theme presets with paired light/dark palettes plus a Custom theme mode.
8. Fix the current dark-mode contrast problem and prevent equivalent regressions through automated contrast tests.
9. Preserve structured academic datasets such as publications, research, education, projects, awards, skills, and news.
10. Preserve current academic-profile links and verified bibliographic behavior: missing DOI/URL/volume/issue/pages/data/code/replication values must remain absent rather than inferred.
11. Make SEO metadata, canonical URLs, `hreflang`, Open Graph, structured data, sitemap, robots policy, breadcrumbs, and indexing behavior build-time outputs rather than runtime patches.
12. Keep validation automatic on every CMS save / Git push.
13. Minimize future maintenance by keeping dependencies small and interfaces explicit.

## 2. Non-goals and platform limits

Academic Pro 2 is not a free-form drag-anything-anywhere visual builder like Webflow. It is a structured page builder: the user composes pages from supported blocks, chooses layout options, changes themes, and manages navigation/content from Pages CMS.

GitHub Pages is a static host. It cannot provide arbitrary origin-level HTTP 301 redirects for changed slugs. Academic Pro 2 will therefore:

- strongly discourage unnecessary slug changes;
- preserve legacy URLs where practical;
- generate static redirect/alias pages with canonical metadata for known previous URLs;
- keep a `redirect_from` list per page;
- support later migration to true HTTP redirects if the site is placed behind a custom-domain CDN/proxy.

This constraint does not affect canonical URLs, clean URLs, sitemap quality, structured data, or normal page indexing.

## 3. Architecture

The repository becomes a small static-site generator with Pages CMS as the content/admin layer.

```text
Pages CMS
   ↓ commits JSON/media/config to main
GitHub Actions
   ↓ validate
Python static builder
   ↓ renders templates + SEO + sitemap + redirects
_site/
   ↓ upload-pages-artifact
GitHub Pages
```

The public site must not depend on JavaScript to obtain its primary text content. JavaScript is enhancement-only: theme switching, search interaction, citation copy/download helpers, menu behavior, and progressive UI features.

### Technology choices

- **Content/admin:** Pages CMS + JSON files
- **Build language:** Python 3.13
- **Templating:** Jinja2 with autoescaping enabled
- **Configuration parsing:** Python JSON + PyYAML for `.pages.yml` validation
- **CSS:** generated semantic CSS variables + authored component CSS
- **JavaScript:** dependency-free ES2022 enhancement layer
- **Deployment:** GitHub Actions + official GitHub Pages artifact/deploy actions
- **Output directory:** `_site/`

Jinja2 is introduced because page-builder rendering, layouts, reusable components, and HTML escaping are clearer and safer in templates than in large Python string literals.

## 4. Repository structure

The target structure is:

```text
.github/
  workflows/
    validate.yml
    deploy-pages.yml
.pages.yml
.nojekyll
assets/
  uploads/
    images/
    documents/
    publications/
content/
  en/
    profile.json
    education.json
    research.json
    publications.json
    projects.json
    experience.json
    awards.json
    skills.json
    news.json
    site.json
  fa/
    ...same datasets...
  pages/
    en/
      home.json
      research.json
      publications.json
      experience.json
      news.json
      cv.json
      contact.json
      search.json
      teaching.json
      <custom-page>.json
    fa/
      ...translated/mirrored pages...
  settings/
    design.json
    redirects.json
src/
  build_site.py
  content_loader.py
  routes.py
  seo.py
  themes.py
  blocks.py
  validation.py
  templates/
    base.html
    page.html
    redirect.html
    404.html
    partials/
      header.html
      footer.html
      breadcrumbs.html
      contact_item.html
    blocks/
      hero_profile.html
      rich_text.html
      heading.html
      image.html
      callout.html
      buttons.html
      cards.html
      contact_methods.html
      academic_links.html
      research_themes.html
      education_timeline.html
      publication_index.html
      news_list.html
      experience_list.html
      projects_list.html
      awards_list.html
      skills_list.html
      downloads.html
      accordion.html
      divider.html
  static/
    style.css
    site.js
    favicon.svg
scripts/
  check_site.py
  validate_content.py
  validate_pages_config.py
tests/
  ...existing tests...
  test_build.py
  test_routes.py
  test_pages_model.py
  test_blocks.py
  test_navigation.py
  test_contacts.py
  test_themes.py
  test_seo_build.py
  test_redirects.py
  test_accessibility.py
```

Generated `_site/` files are build artifacts and must not be edited by the user or Pages CMS.

## 5. Page model

Every routable English or Persian page is a JSON file in a Pages CMS collection.

Example conceptual model:

```json
{
  "id": "working-papers",
  "slug": "working-papers",
  "translation_key": "working-papers",
  "title": "Working Papers",
  "menu_label": "Working Papers",
  "status": "published",
  "layout": "standard",
  "show_breadcrumbs": true,
  "show_in_sitemap": true,
  "redirect_from": ["papers.html"],
  "seo": {
    "title": "Working Papers | Yasin Fanaei Shahroudi",
    "description": "Working papers and ongoing research.",
    "image": "",
    "noindex": false
  },
  "blocks": []
}
```

### Required page behavior

- `id` is stable and must not silently change after creation.
- `slug` is lowercase ASCII kebab-case for public routes.
- English `home.json` uses an empty public slug and emits `/index.html`.
- Persian `home.json` emits `/fa/index.html`.
- A normal English page `slug: research` emits `_site/research/index.html`.
- Persian emits `_site/fa/research/index.html`.
- Draft pages are built only for validation/preview metadata when needed but are not included in public navigation or sitemap and must carry `noindex` if emitted.
- Published pages with `show_in_sitemap: true` appear in sitemap.
- A page can exist without being shown in navigation.

Pages CMS will expose English and Persian `collection` entries for these page files. Collection filenames are based on the page slug/primary field and creation/rename/delete operations are enabled for custom pages.

## 6. Block-based page builder

The page `blocks` field uses Pages CMS `type: block`, allowing different block schemas in one ordered list.

### Initial supported blocks

1. **Profile Hero** — name, academic headline, short bio, research tags, portrait, primary/secondary CTA, academic links.
2. **Heading** — eyebrow, H2/H3 title, optional lead.
3. **Rich Text** — CMS rich-text content rendered to semantic HTML.
4. **Image** — image, alt text, caption, width/alignment preset.
5. **Callout** — title, body, tone, optional link.
6. **Buttons** — ordered list of buttons/links with primary/secondary/text style.
7. **Cards** — repeated cards with title, text, optional image/link.
8. **Contact Methods** — renders selected public contact items.
9. **Academic Links** — ORCID, Scholar, ResearchGate, LinkedIn, GitHub, institutional profile and future supported links.
10. **Research Themes** — structured data from the locale research dataset.
11. **Education Timeline** — structured education dataset.
12. **Publication Index** — full searchable/filterable publication list.
13. **News List** — configurable latest/all/featured news.
14. **Experience List** — experience/service data.
15. **Projects List** — research projects.
16. **Awards List** — honors/awards.
17. **Skills List** — skills/certificates.
18. **Downloads** — CV/files with labels and download links.
19. **Accordion** — FAQ or expandable structured items.
20. **Divider/Spacer** — controlled visual separation; no arbitrary pixel placement.

Blocks are reorderable in Pages CMS. Each block has an `enabled` toggle so it can be temporarily hidden without deletion.

### Security/rendering rule

Rich text is rendered only through the builder's controlled renderer. Arbitrary JavaScript or raw executable HTML is not exposed as a normal CMS block.

## 7. Navigation model

Each locale's `site.json` contains a `navigation` ordered list. The model becomes:

```json
{
  "label": "Research",
  "enabled": true,
  "destination": "page",
  "page": "research",
  "url": "",
  "new_tab": false,
  "children": []
}
```

### Navigation destination types

- `page` — internal page reference
- `section` — anchor on the current/home page
- `external` — external HTTPS URL
- `file` — public downloadable file such as CV PDF

### Navigation requirements

- unlimited top-level items within practical CMS limits;
- one submenu level;
- reorder by CMS list ordering;
- enable/disable without deleting;
- separate English/Persian labels and order;
- internal links are generated from page IDs, not manually typed paths;
- invalid/missing page references fail validation;
- external links may optionally open in a new tab and must receive safe `rel` attributes.

For page references, Pages CMS should use collection-backed references where practical so the editor selects a page rather than typing a path.

## 8. Contact methods model

The current single `email` field is migrated to an ordered `contacts` list in each locale profile.

```json
{
  "id": "academic-email",
  "type": "email",
  "label": "Academic email",
  "value": "name@example.edu",
  "url": "",
  "enabled": true,
  "show_home": false,
  "show_contact": true,
  "show_footer": false
}
```

### Supported contact types

- email
- phone
- whatsapp
- telegram
- website
- office
- location
- custom

The builder derives `mailto:` and `tel:` links where safe. WhatsApp/Telegram may use either normalized account data or an explicit URL. A custom item requires a label and can optionally include a URL.

The dashboard must allow add/delete/reorder and visibility toggles. No number or email is public unless deliberately entered into this public repository. The CMS helper text must remind the user to enter only contact details intended for publication.

## 9. Theme preset system

`content/settings/design.json` gains:

```json
{
  "theme": {
    "preset": "midnight-teal",
    "default_mode": "system"
  },
  "custom_theme": {
    "light": {},
    "dark": {}
  }
}
```

Only one preset is active at a time. Pages CMS presents a select, not independent checkboxes, to prevent contradictory combinations.

### Built-in presets

The first release contains these curated presets:

1. **Classic Academic** — warm ivory + ink + restrained teal.
2. **Oxford Navy** — white/cream + deep navy + scholarly blue.
3. **Midnight Teal** — modern teal/cyan accents with strong dark mode.
4. **Burgundy & Cream** — restrained burgundy academic palette.
5. **Forest & Ivory** — green/ivory research-oriented palette.
6. **Slate Blue** — cool slate surfaces and blue accents.
7. **Monochrome Editorial** — black/white/gray with minimal accent.
8. **Custom** — user-controlled semantic tokens.

### Semantic color tokens

Themes must define semantic tokens, not only raw colors:

- background
- surface
- surface_alt
- text
- text_muted
- border
- accent
- accent_hover
- accent_text
- link
- link_hover
- button_primary_bg
- button_primary_text
- button_secondary_bg
- button_secondary_text
- tag_bg
- tag_text
- focus_ring
- success
- warning
- danger

This directly fixes the current dark-mode bug: secondary buttons can no longer inherit an inappropriate generic text color.

### Contrast requirements

Automated tests calculate WCAG contrast ratios for every built-in preset in both light and dark modes. Minimums:

- normal body/button text: 4.5:1
- large display text: 3:1
- essential UI boundaries/focus indicators: 3:1 where applicable

A built-in preset cannot ship if required combinations fail.

## 10. Layout controls

The existing layout controls remain and are extended with safe presets:

- content width: narrow / standard / wide / custom
- hero style: split / centered / compact
- portrait: left / right / automatic / hidden
- section density: compact / standard / spacious
- card style: flat / border / elevated
- header style: standard / compact
- corner style: square / subtle / rounded

Fine-grained numeric controls can remain under an Advanced section, but normal users should be able to achieve a coherent layout using presets.

## 11. Static build and clean URLs

The builder reads JSON content, page definitions, theme settings, and uploaded media; validates them; then renders `_site/`.

Representative output:

```text
_site/
  index.html
  research/index.html
  publications/index.html
  contact/index.html
  working-papers/index.html
  fa/index.html
  fa/research/index.html
  fa/working-papers/index.html
  assets/style.css
  assets/site.js
  assets/uploads/...
  sitemap.xml
  robots.txt
  404.html
```

All internal navigation uses `/research/` style URLs, not `.html` URLs or query-string routers.

## 12. SEO model

Every page build computes SEO at build time.

### Per-page fields

- SEO title
- meta description
- canonical override only when explicitly needed
- Open Graph/Twitter image
- noindex toggle
- sitemap toggle
- structured-data type where applicable

### Generated SEO output

Every indexable page receives:

- `<title>`
- meta description
- absolute canonical URL
- reciprocal English/Persian `hreflang` when a translation pair exists
- `x-default` on the appropriate English/default page
- Open Graph title/description/type/url/image
- Twitter card metadata
- robots meta based on status/noindex
- JSON-LD
- breadcrumbs in markup and `BreadcrumbList` JSON-LD for non-home routes

### Structured data

- home/profile: `ProfilePage` + `Person`
- article-like news detail pages, if later introduced: `Article`/`NewsArticle` only when source data supports it
- breadcrumbs: `BreadcrumbList`
- website-level search schema will not claim unsupported server-side search functionality

No structured-data field is fabricated from missing content.

## 13. Sitemap and robots

`sitemap.xml` is generated on every build from published, indexable pages. It includes both language versions and clean absolute URLs. Draft/noindex pages are excluded.

`robots.txt` is generated from site settings and always points to the current absolute sitemap URL when indexing is enabled.

Changing `seo.site_url` in the dashboard must update canonical URLs, structured data, sitemap, robots, and share metadata on the next build.

## 14. Translation pairing

Each page has a stable `translation_key`. The builder pairs English and Persian pages by that key.

Rules:

- paired pages get reciprocal `hreflang`;
- missing translations do not produce broken `hreflang` links;
- the language switch points to the translated counterpart when present;
- otherwise it points to the locale homepage or is disabled according to site setting;
- validation fails on duplicate translation keys within a locale.

## 15. Redirect and legacy URL strategy

`content/settings/redirects.json` plus each page's `redirect_from` field define known old paths.

During migration, legacy routes such as `/research.html` and `/fa/research.html` are retained as static alias documents that:

- declare the new clean route as canonical;
- provide an immediate HTML meta refresh;
- provide a normal clickable fallback link;
- may use a tiny enhancement script to preserve fragments/query parameters where safe.

The builder rejects redirect loops, duplicate aliases, aliases colliding with real routes, and external redirect destinations.

After clean URLs become established, old alias pages remain unless the user intentionally removes them.

## 16. Search

Search remains client-side and dependency-free, but the search index becomes a build artifact rather than being assembled from raw JSON on every visit.

The builder emits locale indexes such as:

```text
_site/search-index.en.json
_site/search-index.fa.json
```

The index contains only published/indexable public text and public URLs. It excludes draft pages and hidden/private fields.

## 17. Publications and academic datasets

Existing structured academic datasets remain source-of-truth content. The page builder references them through dynamic blocks.

Publication rules remain strict:

- DOI, official English title, volume, issue, pages, PDF, data, code, replication, and external URLs display only when explicitly populated/verified.
- citation/BibTeX/RIS helpers use only available bibliographic fields.
- a build must not infer missing bibliographic facts.

## 18. Pages CMS dashboard design

The sidebar becomes conceptually:

```text
English
  Profile & Contact
  Education
  Research
  Publications
  Projects
  Experience & Service
  Awards
  Skills & Certificates
  News & Updates
  Pages
  Site & Navigation

فارسی
  مشخصات و ارتباط
  تحصیلات
  پژوهش
  انتشارات
  طرح‌ها
  سوابق و فعالیت‌ها
  جوایز
  مهارت‌ها و گواهی‌ها
  تازه‌ها
  صفحات
  سایت و منو

Design & Branding
Media
Actions
```

Repeated schemas such as SEO, buttons, contact items, and cards should be defined as Pages CMS `components` to avoid configuration drift.

Pages collections are searchable/listed by title, slug, status, and translation key. Custom pages allow create/rename/delete; required core pages receive stronger validation and cannot be accidentally deleted without an explicit migration decision.

## 19. Build and deployment workflow

GitHub Pages changes once from **Deploy from a branch** to **GitHub Actions**.

`deploy-pages.yml` runs on pushes to `main` and manual dispatch:

1. checkout repository;
2. set up Python;
3. install pinned build dependencies;
4. run all unit tests;
5. validate JSON, Pages CMS config, privacy rules, routes, page refs, theme contrast, SEO invariants, and JavaScript syntax;
6. run `python src/build_site.py --output _site`;
7. run post-build HTML/link assertions;
8. configure GitHub Pages;
9. upload `_site` as Pages artifact;
10. deploy with the official Pages deployment action.

Deployment must not occur when validation/build fails.

The existing validation workflow may either be folded into this workflow or retained as a separate fast check; the final implementation should avoid redundant expensive work while keeping a manual **Validate site** Pages CMS action.

## 20. Migration plan

Migration must preserve the currently published information and URLs as much as possible.

1. Copy current content JSON unchanged into the new model where possible.
2. Convert the existing `email` to the first contact item.
3. Convert existing academic links into the existing links object; do not change verified URLs.
4. Convert current fixed navigation to page references.
5. Create page JSON files representing current Home, Research, Publications, Experience, News, CV, Contact, Search, and Teaching pages.
6. Reproduce the current home section order as initial page blocks.
7. Preserve current design settings as the initial **Classic Academic** or equivalent preset/custom settings.
8. Add legacy `.html` paths to redirect aliases.
9. Build both locales and compare visible content against the current site.
10. Switch GitHub Pages deployment source only after the generated site passes all tests.

No public content should be intentionally removed during migration.

## 21. Error handling and validation

Build fails with actionable messages when any of these occur:

- malformed JSON/YAML;
- duplicate page ID/slug/translation key;
- invalid slug;
- internal navigation points to a missing/unpublished page;
- redirect collision or loop;
- missing required image alt text in a public image block;
- duplicate contact IDs;
- unsafe/invalid external URL schemes;
- theme preset missing semantic tokens;
- required theme contrast failure;
- sitemap/canonical URL mismatch;
- English/Persian route collision;
- missing required core datasets;
- sensitive identity-number-like values detected by the existing privacy scanner;
- publication metadata violates existing anti-fabrication rules.

Error output should identify the exact content file and field where possible.

## 22. Accessibility and performance

The generated site must preserve/improve:

- semantic landmarks (`header`, `nav`, `main`, `footer`);
- one H1 per normal page unless a block explicitly follows a documented special layout;
- logical heading hierarchy;
- keyboard-accessible navigation and submenu controls;
- visible focus indicators;
- skip-to-content link;
- correct `lang` and `dir` attributes;
- alt text enforcement for meaningful images;
- `prefers-reduced-motion` support;
- no layout-critical dependence on JavaScript;
- responsive images where possible;
- lazy loading for below-the-fold images;
- small dependency footprint;
- static compressed assets eligible for GitHub Pages/CDN caching.

## 23. Test strategy

The implementation is test-driven. Required coverage includes:

### Content/model tests
- page creation schema and slug validation;
- contact-list add/reorder/render behavior;
- navigation references and submenu behavior;
- translation pairing;
- block schemas and renderer dispatch.

### Build tests
- clean route output paths;
- published vs draft behavior;
- legacy aliases;
- sitemap/robots generation;
- search-index generation;
- generated asset copy.

### SEO tests
- absolute canonical;
- `hreflang` pairing;
- no draft pages in sitemap;
- Open Graph/Twitter fields;
- ProfilePage/Person and BreadcrumbList JSON-LD validity at structural level;
- site URL migration behavior.

### Theme/accessibility tests
- all preset token completeness;
- light and dark required contrast ratios;
- secondary button dark-mode regression test;
- keyboard/focus CSS hooks;
- reduced-motion hooks.

### Repository/deployment tests
- `.pages.yml` parses and exposes page collections, block editor, contacts, theme preset and navigation controls;
- deployment workflow builds `_site` before upload;
- no deploy step after failed validation;
- public repository privacy checks remain active.

## 24. Acceptance criteria

Academic Pro 2 is complete only when all of the following are demonstrated:

1. A new English and Persian custom page can be created entirely in Pages CMS and receives a clean public URL after build.
2. The page can be added to, removed from, and reordered in navigation without code changes.
3. A submenu can be configured from the dashboard.
4. Multiple emails and phone/contact types can be added, reordered, hidden, and shown in selected locations.
5. Switching the theme preset in the dashboard visibly changes both light and dark palettes after build.
6. Every built-in theme passes automated contrast tests; the current invisible dark secondary button bug is covered by a regression test.
7. Existing academic pages and datasets still render their current public information.
8. `/research/` and `/fa/research/` render static HTML with correct canonical/hreflang metadata.
9. Legacy `.html` routes resolve through generated alias pages and do not become duplicate canonical pages.
10. Sitemap contains only intended published/indexable clean URLs.
11. Search results use clean URLs and exclude drafts.
12. Pages CMS save → GitHub push → validate/build → GitHub Pages deploy works without manual coding.
13. A failed validation prevents deployment.
14. The final repository has no requirement for the user to edit source templates for routine site management.

## 25. Future-proofing rules

- Core content schemas use stable IDs rather than display labels as references.
- Themes are semantic-token based so future templates do not depend on raw palette names.
- Pages use block types with explicit versions/interfaces; incompatible block shape changes require migration tests.
- Navigation references stable page IDs rather than copied URLs.
- Site URL is centralized in settings.
- Generated output is disposable; content/config/templates are source of truth.
- Build dependencies are pinned and updated intentionally.
- The public repository must never contain government IDs, birth date, marital status, private phone numbers, passwords, or other non-public personal identifiers.

## 26. Explicit decisions made by this spec

- Use **true static generation**, not `page.html?slug=...`.
- Use **clean directory URLs**.
- Use **Pages CMS collections + block fields** for pages.
- Use **page references** for internal navigation.
- Use **ordered contact lists** for unlimited public contact methods.
- Use **one selected theme preset**, not multiple independent theme checkboxes.
- Use **semantic light/dark tokens and contrast tests**.
- Use **GitHub Actions Pages deployment** after migration.
- Keep **legacy route alias pages** because GitHub Pages cannot supply arbitrary server-side 301 redirects.
- Keep the site's academic data model structured and anti-fabrication rules intact.
