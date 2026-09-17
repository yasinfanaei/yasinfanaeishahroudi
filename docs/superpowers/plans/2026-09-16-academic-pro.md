# Academic Pro Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add the approved Academic Pro search, publications, news, theme, SEO, accessibility, media, and automated-validation capabilities while keeping the bilingual site fully manageable through Pages CMS.

**Architecture:** Extend the existing static HTML + shared `assets/site.js` renderer and JSON content model. New features remain client-side and dependency-free. Pages CMS continues to edit structured JSON and design settings; GitHub Pages serves static assets and GitHub Actions validates changes.

**Tech Stack:** HTML5, CSS custom properties, vanilla JavaScript, JSON, Pages CMS `.pages.yml`, Python `unittest` validators, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-16-academic-pro-design.md`

## Global Constraints
- Preserve English root and Persian `/fa/` URL structure.
- Preserve the privacy rule excluding government IDs, birth date, marital status, and private phone numbers.
- Do not invent missing bibliographic metadata or official titles.
- Keep core site functionality dependency-free and static.
- New routine content/design controls must be available from Pages CMS.
- Analytics is optional and disabled by default.

---

### Task 1: Extend data model and CMS schema

**Files:**
- Modify: `content/settings/design.json`
- Modify: `content/en/site.json`, `content/fa/site.json`
- Modify: `content/en/publications.json`, `content/fa/publications.json`
- Create: `content/en/news.json`, `content/fa/news.json`
- Modify: `.pages.yml`
- Modify: `scripts/validate_content.py`, `scripts/validate_pages_config.py`
- Test: `tests/test_academic_pro_content.py`

**Interfaces:**
- Produces `news.json`, extended publication fields, `design.theme`, `design.analytics`, and CMS editors consumed by later renderer tasks.

- [x] Write failing tests asserting the new JSON keys, news files, publication resource fields, named media sources, CMS action, and new content paths.
- [x] Run the targeted tests and confirm they fail because the Academic Pro model is absent.
- [x] Add the minimal JSON/schema/validator changes needed for the tests to pass.
- [x] Run targeted and existing content/CMS tests.

### Task 2: Add theme and global header controls

**Files:**
- Modify: `assets/site.js`, `assets/style.css`
- Modify: all English/Persian page templates as needed
- Test: `tests/test_academic_pro_theme.py`

**Interfaces:**
- Consumes `design.theme` and `design.controls`.
- Produces `applyThemeSettings`, theme persistence, header search link, and theme switcher.

- [x] Write failing tests for dark tokens, system/light/dark mode, localStorage persistence hooks, and header controls.
- [x] Verify red state.
- [x] Implement minimal CSS/JS theme behavior and accessible controls.
- [x] Re-run targeted tests and JavaScript syntax check.

### Task 3: Add Search and News pages

**Files:**
- Create: `search.html`, `news.html`, `fa/search.html`, `fa/news.html`
- Modify: `index.html`, `fa/index.html`, `assets/site.js`, `assets/style.css`
- Modify: locale `site.json` navigation/UI text
- Test: `tests/test_academic_pro_pages.py`

**Interfaces:**
- Search reads all locale JSON files and renders local result links.
- News reads locale `news.json`; home renders latest featured/published entries.

- [x] Write failing tests for mirrored pages, RTL, search/news slots, home news section, and renderer functions.
- [x] Verify failures.
- [x] Implement page templates, search index/rendering, news rendering, and homepage news block.
- [x] Re-run tests and syntax check.

### Task 4: Upgrade Publications

**Files:**
- Modify: `publications.html`, `fa/publications.html`, `assets/site.js`, `assets/style.css`
- Modify: publication JSON/CMS fields from Task 1 as needed
- Test: `tests/test_academic_pro_publications.py`

**Interfaces:**
- Produces publication filter controls and citation/resource utilities from verified fields only.

- [x] Write failing tests for filter controls, resource fields, and citation/BibTeX/RIS functions.
- [x] Verify failures.
- [x] Implement filtering, resource links, abstract/keyword rendering, and clipboard citation helpers.
- [x] Re-run tests and syntax check.

### Task 5: Add SEO, 404, accessibility, and analytics opt-in

**Files:**
- Create: `robots.txt`, `sitemap.xml`, `404.html`
- Modify: all page templates, `assets/site.js`, `assets/style.css`, locale site JSON/CMS schema
- Test: `tests/test_academic_pro_seo.py`

**Interfaces:**
- `updateMetadata` sets canonical/page SEO/social metadata and ProfilePage/Person JSON-LD.
- Optional analytics injects only when enabled with a valid measurement ID.

- [x] Write failing tests for canonical/hreflang, structured data function, robots/sitemap/404, focus-visible, reduced-motion, and disabled-by-default analytics.
- [x] Verify failures.
- [x] Implement metadata, JSON-LD, optional analytics, accessibility/performance styles/attributes, and static SEO files.
- [x] Re-run tests and syntax check.

### Task 6: Add automated validation and CMS action

**Files:**
- Create: `.github/workflows/validate.yml`
- Modify: `.pages.yml`, `scripts/check_site.py`, documentation
- Test: `tests/test_academic_pro_ci.py`

**Interfaces:**
- Pages CMS `Validate site` action dispatches `validate.yml` on the current branch.
- Workflow runs Python tests, repository validation, and `node --check assets/site.js`.

- [x] Write failing tests for workflow triggers/steps and Pages CMS action.
- [x] Verify failures.
- [x] Implement workflow and checker coverage for new pages/assets.
- [x] Re-run full test suite.

### Task 7: Release verification and packaging

**Files:**
- Modify: `README.md`, `DASHBOARD_GUIDE_FA.md`, `CONTENT_CHECKLIST.md`
- Output: `/mnt/data/academic-website-academic-pro-upgrade.zip`, `/mnt/data/academic-website-academic-pro-full.zip`

**Interfaces:**
- Upgrade ZIP contains changed/new files needed to overlay the current GitHub repository.
- Full ZIP is a clean backup of the complete site.

- [x] Run `python -m unittest discover -s tests -p 'test_*.py' -v`.
- [x] Run `python scripts/check_site.py` and `node --check assets/site.js`.
- [x] Run a local HTTP server and verify representative English/Persian/Search/News/404 resources return HTTP 200.
- [x] Update docs with CMS workflows and feature boundaries.
- [x] Build both ZIP artifacts and inspect their root paths to ensure files are directly uploadable.
