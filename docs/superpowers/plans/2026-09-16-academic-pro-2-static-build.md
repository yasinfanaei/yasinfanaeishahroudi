# Academic Pro 2 Static Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Convert the bilingual academic site into a Pages-CMS-managed static-site generator with clean URLs, build-time SEO, block-based pages, unlimited navigation/contacts, preset themes, and GitHub Actions deployment.

**Architecture:** Pages CMS remains the authoring layer for JSON/media/config. Python 3.13 reads validated content and page definitions, Jinja2 renders semantic HTML into `_site/`, and GitHub Actions deploys `_site/` to GitHub Pages. JavaScript is enhancement-only for theme switching, search interaction, citations, and menu behavior.

**Tech Stack:** Python 3.13, Jinja2, PyYAML, JSON, HTML5, CSS semantic tokens, dependency-free ES2022 JavaScript, GitHub Actions, GitHub Pages, Pages CMS.

**Spec:** `docs/superpowers/specs/2026-09-16-academic-pro-2-static-build-design.md`

## Global Constraints

- English lives at `/`; Persian lives under `/fa/` and uses RTL.
- Public primary text must be present in generated HTML, not fetched at runtime.
- Clean directory routes are canonical; legacy `.html` routes are aliases only.
- Missing bibliographic metadata must never be fabricated or inferred.
- Site-wide public URL is centralized in `content/settings/design.json`.
- Public repository privacy scanning remains enabled.
- Built-in theme normal text contrast must be >= 4.5:1; large text/UI boundaries >= 3:1 where applicable.
- Draft/noindex pages are excluded from sitemap and search index.
- Generated `_site/` is disposable build output and never the CMS source of truth.

---

### Task 1: Static Builder Foundation and Route Model

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `src/content_loader.py`
- Create: `src/routes.py`
- Create: `src/validation.py`
- Create: `src/build_site.py`
- Create: `tests/test_routes.py`
- Create: `tests/test_build.py`

**Interfaces:**
- `src.routes.validate_slug(slug: str, home: bool=False) -> None`
- `src.routes.output_path(locale: str, slug: str, output_root: Path) -> Path`
- `src.routes.public_path(locale: str, slug: str) -> str`
- `src.content_loader.load_json(path: Path) -> object`
- `src.build_site.build_site(root: Path, output: Path) -> None`

- [x] Write failing route/output tests covering `/`, `/research/`, `/fa/`, `/fa/research/` and invalid slugs.
- [x] Run `python -m unittest tests.test_routes tests.test_build -v` and verify failure because builder modules do not exist.
- [x] Implement route helpers, JSON loader, validation primitives, minimal builder skeleton, and pinned `Jinja2`/`PyYAML` dependencies.
- [x] Run the focused tests and verify pass.

### Task 2: Page Model, Migration, Translation Pairing, and Contacts

**Files:**
- Create: `content/pages/en/*.json`
- Create: `content/pages/fa/*.json`
- Modify: `content/en/profile.json`
- Modify: `content/fa/profile.json`
- Create: `content/settings/redirects.json`
- Create: `src/models.py`
- Create: `tests/test_pages_model.py`
- Create: `tests/test_contacts.py`

**Interfaces:**
- `src.models.load_pages(root, locale) -> list[dict]`
- `src.models.page_by_id(pages) -> dict[str, dict]`
- `src.models.translation_pairs(en_pages, fa_pages) -> dict[str, dict]`
- `src.models.normalize_contacts(profile) -> list[dict]`

- [x] Write failing tests for unique page id/slug/translation keys, translation pairing, duplicate contact IDs, contact visibility, and migration from legacy email.
- [x] Run focused tests and verify failures.
- [x] Migrate current core pages into page JSON definitions and profile email into ordered `contacts` while preserving existing public email fields for compatibility during migration.
- [x] Implement page/contact model validation and pairing.
- [x] Re-run focused tests and verify pass.

### Task 3: Theme Presets, Dark-Mode Regression, and Layout Presets

**Files:**
- Create: `src/themes.py`
- Modify: `content/settings/design.json`
- Create: `src/static/style.css`
- Create: `tests/test_themes.py`
- Create: `tests/test_accessibility.py`

**Interfaces:**
- `src.themes.get_theme(name: str, design: dict) -> dict`
- `src.themes.contrast_ratio(fg: str, bg: str) -> float`
- `src.themes.css_variables(theme: dict) -> str`

- [x] Write failing tests for all eight preset names, semantic token completeness, light/dark contrast, and secondary-button dark-mode contrast.
- [x] Run theme tests and verify failure.
- [x] Implement curated presets, custom mode fallback, semantic tokens, layout preset tokens, and CSS variable generation.
- [x] Run theme/accessibility tests and verify pass.

### Task 4: Templates, Blocks, Navigation, and Static HTML Rendering

**Files:**
- Create: `src/blocks.py`
- Create: `src/templates/base.html`
- Create: `src/templates/page.html`
- Create: `src/templates/redirect.html`
- Create: `src/templates/404.html`
- Create: `src/templates/partials/*.html`
- Create: `src/templates/blocks/*.html`
- Create: `src/static/site.js`
- Create: `tests/test_blocks.py`
- Create: `tests/test_navigation.py`

**Interfaces:**
- `src.blocks.render_blocks(env, page, context) -> str`
- `src.build_site.render_page(...) -> str`
- navigation objects resolve `destination` values `page|section|external|file`.

- [x] Write failing tests for block dispatch, enabled flag, one-level submenu, internal page references, safe external rel attributes, semantic landmarks, one H1, skip link, and no runtime content fetch.
- [x] Run focused tests and verify failure.
- [x] Implement templates and block renderers for all initial block types, static header/footer/navigation/contact rendering, and enhancement-only JS.
- [x] Run focused tests and verify pass.

### Task 5: Build-Time SEO, Sitemap, Robots, Search Index, and Redirect Aliases

**Files:**
- Create: `src/seo.py`
- Modify: `src/build_site.py`
- Create: `tests/test_seo_build.py`
- Create: `tests/test_redirects.py`

**Interfaces:**
- `src.seo.page_seo_context(...) -> dict`
- `src.seo.jsonld_for_page(...) -> list[dict]`
- `src.seo.build_sitemap(...) -> str`
- `src.seo.build_robots(...) -> str`

- [x] Write failing tests for canonical URLs, hreflang/x-default, OG/Twitter tags, ProfilePage/Person, BreadcrumbList, sitemap exclusions, robots sitemap URL, site-url migration, search-index exclusions, aliases, collision/loop rejection.
- [x] Run focused tests and verify failure.
- [x] Implement build-time SEO/search/redirect generation and wire it into the builder.
- [x] Run focused tests and verify pass.

### Task 6: Pages CMS Full No-Code Schema

**Files:**
- Rewrite: `.pages.yml`
- Create: `tests/test_pages_cms_v2.py`

**Interfaces:**
- English/Persian page collections under `content/pages/<locale>`.
- Profile contacts list exposes add/delete/reorder/visibility fields.
- Site navigation exposes destination/page/url/children controls.
- Design editor exposes theme preset and layout presets.
- Page blocks use Pages CMS block editor schemas.

- [x] Write failing tests proving `.pages.yml` contains page collections, contacts list, navigation/submenus, theme preset select, block schemas, media sources, and Validate Site action.
- [x] Run focused test and verify failure.
- [x] Rewrite CMS config with reusable components and protected core settings.
- [x] Run focused test and existing CMS tests; update legacy tests only where the spec intentionally supersedes the old client-rendered model.

### Task 7: Validation Scripts and Repository Rules

**Files:**
- Modify: `scripts/check_site.py`
- Modify: `scripts/validate_content.py`
- Modify: `scripts/validate_pages_config.py`
- Create: `scripts/check_build.py`
- Create: `tests/test_validation_v2.py`

**Interfaces:**
- `python scripts/check_site.py` validates source data/config/privacy/routes/themes.
- `python scripts/check_build.py _site` validates generated HTML, links, sitemap/canonical consistency, and required assets.

- [x] Write failing tests for invalid page refs, redirect collisions, missing alt text, unsafe URL schemes, duplicate contacts, contrast failure, and post-build broken links.
- [x] Run focused tests and verify failure.
- [x] Implement actionable validation errors and build checker.
- [x] Run validation tests and source checker.

### Task 8: GitHub Actions Static Build/Deploy and Legacy Compatibility

**Files:**
- Modify: `.github/workflows/validate.yml`
- Create: `.github/workflows/deploy-pages.yml`
- Modify: `tests/test_academic_pro_ci.py`
- Create: `tests/test_deploy_pages.py`

**Interfaces:**
- Validate workflow remains manual-dispatchable from Pages CMS.
- Deploy workflow runs tests -> source validation -> build -> build validation -> configure/upload/deploy Pages artifact.

- [x] Write failing tests for official Pages actions, `_site` build before upload, no branch-deploy assumptions, pinned Python/Node setup, and validation before deploy.
- [x] Run CI tests and verify failure.
- [x] Implement workflows and legacy route alias generation.
- [x] Run CI tests and verify pass.

### Task 9: Documentation, Full Migration Verification, and Release Package

**Files:**
- Modify: `README.md`
- Modify: `DASHBOARD_GUIDE_FA.md`
- Modify: `CONTENT_CHECKLIST.md`
- Create: `ACADEMIC_PRO_2_MIGRATION_FA.md`

**Interfaces:**
- User changes GitHub Pages source once to GitHub Actions after upload.
- Routine management thereafter happens in Pages CMS.

- [x] Update docs for themes, custom pages, contacts, navigation, static build, URL rules, SEO, validation, deployment switch, and rollback.
- [x] Run `python -m unittest discover -s tests -p 'test_*.py' -v`.
- [x] Run `python scripts/check_site.py`.
- [x] Run `python src/build_site.py --output _site`.
- [x] Run `python scripts/check_build.py _site`.
- [x] Run `node --check src/static/site.js` and `node --check _site/assets/site.js`.
- [x] Serve `_site` locally and verify representative English/Persian clean routes, legacy aliases, search indexes, sitemap, robots, and 404 return expected content.
- [x] Package a full repository ZIP and a migration guide; verify ZIP extraction reproduces the tested source tree.

## Self-Review

- Spec coverage: all 26 spec sections map to Tasks 1–9, including contacts, navigation, blocks, presets, SEO, clean routes, redirects, search, CMS, validation, deployment, accessibility, migration, and future-proofing.
- Placeholder scan: no TBD/TODO/deferred implementation placeholders remain in this plan.
- Interface consistency: page references use stable IDs; routes use locale+slug; themes expose semantic tokens; build output is `_site`; validation scripts operate on source and generated output separately.
