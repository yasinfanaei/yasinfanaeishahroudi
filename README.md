# Yasin Fanaei Shahroudi — Academic Pro 2

Bilingual academic website generated as semantic static HTML and managed through Pages CMS.

## Public site model

- English: `https://yasinfanaei.github.io/yasinfanaeishahroudi/`
- Persian: `https://yasinfanaei.github.io/yasinfanaeishahroudi/fa/`
- Canonical content pages use clean directory URLs under the project-site base path, such as `/yasinfanaeishahroudi/research/` and `/yasinfanaeishahroudi/fa/research/`.
- Legacy `.html` URLs are generated as canonicalized alias pages for compatibility.

## Publishing architecture

```text
Pages CMS -> commit JSON/media/config to main
          -> Validate Academic Site workflow
          -> Build and Deploy Academic Site workflow
          -> Python/Jinja2 static build in _site/
          -> GitHub Pages artifact deployment
```

GitHub Pages must use **GitHub Actions** as its deployment source. The old **Deploy from a branch / main / root** mode is not the production path for Academic Pro 2.

## What is editable without coding

Pages CMS manages:

- profile and unlimited public contact methods;
- education, research, publications, projects, experience, awards, skills and news;
- English and Persian page collections;
- block-based custom pages;
- navigation order, page links, external links, file links and one submenu level;
- SEO title/description/indexing/sitemap fields per page;
- shared profile photo, CV files, favicon and social image;
- theme preset, light/dark mode defaults, custom semantic colors and safe layout presets;
- optional GA4 analytics settings.

## Theme presets

Built-in presets are:

- Classic Academic
- Oxford Navy
- Midnight Teal
- Burgundy & Cream
- Forest & Ivory
- Slate Blue
- Monochrome Editorial
- Custom

Every built-in light/dark palette is automatically checked for required contrast. Custom is pre-populated with a safe complete palette so selecting it does not break the build; its semantic tokens can then be edited in Pages CMS.

## Pages and block builder

Pages live under `content/pages/en/` and `content/pages/fa/`. A page contains a stable ID, clean slug, translation key, publication state, SEO settings and an ordered block list.

Supported blocks include Profile Hero, Heading, Rich Text, Image, Callout, Buttons, Cards, Contact Methods, Academic Links, Research Themes, Education Timeline, Publication Index, News, Experience, Projects, Awards, Skills, Downloads, Accordion, Divider and Search.

Primary page text is rendered into HTML at build time. JavaScript is enhancement-only.

## Contacts

Locale profiles contain an ordered `contacts` list. Supported types:

- email
- phone
- WhatsApp
- Telegram
- website
- office
- location
- custom

Each item can independently be enabled and shown on Home, Contact and/or Footer. Only intentionally public information belongs here.

## Publications

The publication renderer supports text/type/status/year filtering, Abstract/Keywords, verified DOI/PDF/Data/Code/Replication links, Copy Citation, BibTeX and RIS. Citation helpers use only populated bibliographic fields; missing DOI, official English title, volume, issue, page range or resource URLs are never inferred.

## SEO and search

The build emits:

- absolute canonical URLs;
- reciprocal `hreflang` and `x-default` where translations exist;
- Open Graph and Twitter metadata;
- `ProfilePage`/`Person` JSON-LD on the profile home page;
- `BreadcrumbList` JSON-LD on interior pages;
- `sitemap.xml` and `robots.txt`;
- locale search indexes containing published/indexable public text only.

This edition is preconfigured for `https://yasinfanaei.github.io/yasinfanaeishahroudi`. Changing the public `site_url` in Design & Branding regenerates absolute SEO URLs and browser base-path links on the next build.

## Validation

Source validation:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/check_site.py
node --check src/static/site.js
```

Static build and post-build validation:

```bash
python -m src.build_site --output _site
python scripts/check_build.py _site
node --check _site/assets/site.js
```

The validation workflow is also exposed as **Actions -> Validate site** in Pages CMS.

## Repository privacy rule

Never put government identification numbers, birth date, marital status, passwords, private telephone numbers, or other non-public identifiers in this public repository. Public email/phone/contact values are appropriate only when deliberately entered as public contact methods.

## Key files

- `.pages.yml` — Pages CMS schema
- `content/settings/design.json` — shared branding/theme/layout/SEO/analytics settings
- `content/settings/redirects.json` — explicit legacy aliases
- `src/build_site.py` — static-site builder
- `src/templates/` — semantic HTML templates
- `src/static/` — production CSS and enhancement JavaScript
- `.github/workflows/validate.yml` — validation
- `.github/workflows/deploy-pages.yml` — static build and GitHub Pages deployment
- `ACADEMIC_PRO_2_MIGRATION_FA.md` — one-time installation guide in Persian
- `DASHBOARD_GUIDE_FA.md` — routine dashboard guide in Persian
