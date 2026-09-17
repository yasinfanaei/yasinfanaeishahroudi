# No-Code Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make routine content, media, appearance, layout, navigation, branding, and SEO manageable from Pages CMS without editing code.

**Architecture:** Add one shared `content/settings/design.json` settings source, expose it and locale site settings through `.pages.yml`, and make `site.js` translate safe settings into CSS variables/classes and runtime metadata. Keep bilingual academic content in the existing `content/en` and `content/fa` trees.

**Tech Stack:** Static HTML5, CSS custom properties, vanilla JavaScript, JSON, Pages CMS YAML, Python unittest validation, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-16-no-code-dashboard-design.md`

## Global Constraints
- English remains the default root locale; Persian remains under `/fa/`.
- Site must remain deployable as static files on GitHub Pages.
- No database, build tool, paid service, or server-side runtime.
- Existing academic-publication fields must not invent missing bibliographic metadata.
- Sensitive identity/private fields must not be added to public JSON or CMS.
- Existing media path remains `assets/uploads/`.

---

### Task 1: Add failing tests for design settings and CMS controls

**Files:**
- Create: `tests/test_design_settings.py`
- Modify: `tests/test_pages_config.py`

**Interfaces:**
- Consumes: existing repository paths and YAML/JSON files.
- Produces: tests requiring `content/settings/design.json`, CSS variable hooks, JavaScript settings application, and Pages CMS design controls.

- [ ] Write tests asserting the new settings file, required setting keys, home-section IDs, CSS variables, JS loader/application hooks, locale navigation enabled fields, and Design & Branding CMS entry.
- [ ] Run targeted tests and confirm failure because feature files/hooks do not yet exist.

### Task 2: Add shared settings model and CMS schema

**Files:**
- Create: `content/settings/design.json`
- Modify: `.pages.yml`
- Modify: `content/en/site.json`
- Modify: `content/fa/site.json`

**Interfaces:**
- Produces: JSON shape consumed by `site.js`: `branding`, `colors`, `typography`, `layout`, `controls`, `home_sections`.

- [ ] Add safe defaults matching current visual design.
- [ ] Add `enabled` to each navigation item in both locales.
- [ ] Add locale SEO fields and announcement enable flag.
- [ ] Add Pages CMS structured editors for design, branding, SEO/navigation, image/CV/media fields, and guarded operations.
- [ ] Run targeted settings/config tests.

### Task 3: Make CSS design-token driven

**Files:**
- Modify: `assets/style.css`

**Interfaces:**
- Consumes: CSS custom properties set by JS.
- Produces: dashboard-controllable colors, fonts, widths, radii, shadows, spacing, image size, and header behavior.

- [ ] Add failing/assertion tests for new CSS variables where necessary.
- [ ] Replace hard-coded dashboard-managed values with CSS variables and add classes for portrait side, header stickiness, shadow toggle, and section visibility.
- [ ] Run typography/design tests.

### Task 4: Load and apply design settings in JavaScript

**Files:**
- Modify: `assets/site.js`

**Interfaces:**
- Consumes: `content/settings/design.json` plus locale `site.json`.
- Produces: `applyDesignSettings(settings)`, runtime CSS variables/classes, metadata updates, home ordering, navigation filtering.

- [ ] Add/confirm failing tests for required hooks.
- [ ] Load shared settings for every page.
- [ ] Clamp numeric values and set CSS variables safely.
- [ ] Apply branding/favicon/OG image and locale SEO metadata.
- [ ] Respect navigation `enabled`, announcement enabled, language-switch/footer controls.
- [ ] Reorder/hide homepage sections using stable IDs.
- [ ] Run targeted JS/repository tests.

### Task 5: Mark homepage sections and metadata hooks

**Files:**
- Modify: `index.html`
- Modify: `fa/index.html`
- Modify: English/Farsi public HTML heads as needed for metadata placeholders.

**Interfaces:**
- Consumes: JS section-order logic and metadata logic.
- Produces: `data-home-section` hooks and metadata nodes.

- [ ] Add stable homepage section IDs/hooks to both locales.
- [ ] Add Open Graph/Twitter/keywords metadata placeholders consistently to public pages.
- [ ] Run bilingual/site-structure tests.

### Task 6: Update documentation and verify end-to-end

**Files:**
- Modify: `README.md`
- Modify: `CONTENT_CHECKLIST.md`
- Modify: `scripts/check_site.py` if validation needs new required settings.

**Interfaces:**
- Produces: user-facing CMS workflow and validation coverage.

- [ ] Document which settings are no-code editable and the limits of the system.
- [ ] Run `python -m unittest discover -s tests -p 'test_*.py' -v`.
- [ ] Run `python scripts/check_site.py`.
- [ ] Run `node --check assets/site.js`.
- [ ] Serve locally and verify HTTP 200 for `/`, `/fa/`, design JSON and representative content files.
- [ ] Package full upload-ready ZIP plus the minimum changed-file bundle.
