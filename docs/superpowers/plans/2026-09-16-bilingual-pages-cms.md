# Bilingual Academic Website + Pages CMS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the existing academic website into an English-first bilingual site with Persian at `/fa/`, add verified academic profile links, and expose both languages through Pages CMS.

**Architecture:** Keep one shared renderer (`assets/site.js`) and stylesheet (`assets/style.css`). Store locale-specific academic content in `content/en/` and `content/fa/`; root HTML pages render English and mirrored `fa/*.html` pages render Persian, with language switching and `hreflang` links. Pages CMS edits the two locale content trees as separate groups while shared media stays in `assets/uploads/`.

**Tech Stack:** Static HTML/CSS/JavaScript, JSON, Pages CMS `.pages.yml`, Python unittest validators, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-16-pages-cms-github-pages-design.md` plus the approved bilingual extension from the current conversation.

## Global Constraints

- English is the default site at `/`; Persian lives at `/fa/`.
- No database or paid service.
- Shared static renderer and media; locale-specific JSON content.
- Preserve privacy: no government ID, birth date, marital status, or private phone number in public content.
- Do not invent DOI, official English article titles, volume, issue, page range, or publication URLs.
- Add only user-supplied academic links: ORCID, ResearchGate, Google Scholar, LinkedIn, plus existing GitHub.
- Persian pages must use `lang="fa"` and RTL layout.

---

### Task 1: Add failing bilingual structure tests

**Files:**
- Modify: `tests/test_site_structure.py`
- Modify: `tests/test_content.py`
- Modify: `tests/test_pages_config.py`

**Interfaces:**
- Produces: test requirements for `content/en`, `content/fa`, `fa/*.html`, language switcher, `hreflang`, and bilingual CMS paths.

- [ ] **Step 1: Write tests that require both locale content trees and mirrored Persian pages.**
- [ ] **Step 2: Run `python -m unittest discover -s tests -p 'test_*.py' -v` and verify the new tests fail because bilingual files/config do not yet exist.**
- [ ] **Step 3: Keep failures as the RED baseline for Tasks 2–5.**

### Task 2: Split content into English and Persian trees

**Files:**
- Create: `content/en/*.json`
- Create: `content/fa/*.json`
- Remove after migration: old root `content/*.json`

**Interfaces:**
- Consumes: current JSON schema.
- Produces: identical schema per locale, with locale-specific labels/descriptions and verified social URLs in both `profile.json` files.

- [ ] **Step 1: Copy existing content to `content/en/` and insert the verified ORCID, ResearchGate, Google Scholar, LinkedIn, and GitHub links.**
- [ ] **Step 2: Create Persian translations in `content/fa/`, preserving IDs, factual values, publication status, authorship, GPA, dates, and unverified bibliographic blanks.**
- [ ] **Step 3: Update validators to validate both locale trees and scan both for sensitive identity information.**
- [ ] **Step 4: Run content tests and confirm they pass while site/config tests may still fail.**

### Task 3: Make shared renderer locale-aware

**Files:**
- Modify: `assets/site.js`
- Modify: `assets/style.css`

**Interfaces:**
- Consumes: `<html lang>`, `<body data-page data-locale>` and locale JSON trees.
- Produces: locale-aware rendering, localized UI/status labels, correct root-relative assets/links, academic profile cards, and EN/FA language switching.

- [ ] **Step 1: Add locale/root path detection before content loading.**
- [ ] **Step 2: Localize fixed renderer strings (status labels, section labels generated in JS, CV labels, profile link labels).**
- [ ] **Step 3: Render language switcher for the same page in the alternate locale.**
- [ ] **Step 4: Add robust RTL CSS for `html[dir="rtl"]`, including typography, notes, layout direction, and nav behavior.**
- [ ] **Step 5: Run `node --check assets/site.js`.**

### Task 4: Create mirrored Persian HTML pages and SEO language metadata

**Files:**
- Modify: root HTML pages
- Create: `fa/index.html`, `fa/research.html`, `fa/publications.html`, `fa/experience.html`, `fa/cv.html`, `fa/contact.html`, `fa/teaching.html`

**Interfaces:**
- Produces: root English pages with `data-locale="en"`; Persian pages with `lang="fa" dir="rtl" data-locale="fa"`; same render slots and page IDs; reciprocal `hreflang="en"` and `hreflang="fa"` links.

- [ ] **Step 1: Add language-switch slot and SEO alternate links to every English page.**
- [ ] **Step 2: Mirror each page under `fa/`, translate only static shell text, and point assets to `../assets/`.**
- [ ] **Step 3: Run site structure tests.**

### Task 5: Rebuild Pages CMS for both languages

**Files:**
- Modify: `.pages.yml`
- Modify: `scripts/validate_pages_config.py`

**Interfaces:**
- Produces: distinct dashboard entries prefixed `English — ...` and `فارسی — ...`, each bound to its locale JSON file, while shared image/CV media remains common.

- [ ] **Step 1: Duplicate the content editor schema for `content/en/*.json` and `content/fa/*.json` with clear locale labels.**
- [ ] **Step 2: Keep profile link fields editable in both locale profile files.**
- [ ] **Step 3: Update CMS validator expected paths and uniqueness checks.**
- [ ] **Step 4: Run Pages CMS tests.**

### Task 6: Documentation, full verification, and release package

**Files:**
- Modify: `README.md`
- Modify: `CONTENT_CHECKLIST.md`
- Modify: `scripts/check_site.py` as needed
- Create: release ZIP outside repository

**Interfaces:**
- Produces: deploy-ready bilingual repository and clear CMS workflow.

- [ ] **Step 1: Document English `/`, Persian `/fa/`, language switcher, and Pages CMS bilingual editing workflow.**
- [ ] **Step 2: Run `python -m unittest discover -s tests -p 'test_*.py' -v`.**
- [ ] **Step 3: Run `python scripts/check_site.py` and `node --check assets/site.js`.**
- [ ] **Step 4: Launch a local HTTP server and verify representative English/Persian pages and JSON return HTTP 200.**
- [ ] **Step 5: Package the verified repository as `/mnt/data/academic-website-bilingual.zip`.**
