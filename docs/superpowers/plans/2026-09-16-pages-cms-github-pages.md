# Pages CMS + GitHub Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the existing static academic website into a GitHub Pages-ready, JSON-driven site editable through Pages CMS without exposing sensitive identity data.

**Architecture:** Keep the current static HTML/CSS deployment model, but move academic content into focused JSON documents under `content/`. A shared `assets/site.js` module fetches and renders those documents into declarative page containers, while `.pages.yml` exposes matching structured forms in Pages CMS. Validation and smoke-test scripts verify content integrity, privacy constraints, internal links, CMS configuration, and local `fetch()` behavior.

**Tech Stack:** Static HTML5, CSS3, vanilla JavaScript, JSON, YAML, Python 3 standard library, GitHub Pages, Pages CMS.

**Spec:** `docs/superpowers/specs/2026-09-16-pages-cms-github-pages-design.md`

## Global Constraints

- GitHub repository is the source of truth.
- GitHub Pages publishes from the `main` branch repository root.
- `.nojekyll` remains in the root.
- Pages CMS reads `.pages.yml` from the repository root.
- Public site and repository must not contain national identification number, date of birth, marital status, or private phone number.
- No paid hosting, CMS, database, server-side runtime, or automatic CV generation in phase 1.
- Missing bibliographic metadata must remain empty rather than be invented.
- Existing public page URLs must remain stable.

---

### Task 1: Structured academic content and validation

**Files:**
- Create: `content/profile.json`
- Create: `content/education.json`
- Create: `content/research.json`
- Create: `content/publications.json`
- Create: `content/projects.json`
- Create: `content/experience.json`
- Create: `content/awards.json`
- Create: `content/skills.json`
- Create: `content/site.json`
- Create: `scripts/validate_content.py`
- Test: `tests/test_content.py`

**Interfaces:**
- Consumes: current public-site copy and the user-supplied CV-backed content already present in the project.
- Produces: JSON documents with stable `id` fields for list records; `scripts.validate_content.validate_site(root: Path) -> list[str]` returning validation errors.

- [x] **Step 1: Write the failing content-validation tests**

```python
from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_content import validate_site


class ContentTests(unittest.TestCase):
    def test_content_files_parse_and_validate(self):
        self.assertEqual(validate_site(ROOT), [])

    def test_no_sensitive_identity_keys_or_long_id_numbers(self):
        banned_keys = {"national_id", "nationalId", "marital_status", "maritalStatus", "date_of_birth", "dateOfBirth", "phone"}
        for path in (ROOT / "content").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            text = json.dumps(data, ensure_ascii=False)
            self.assertFalse(any(f'"{key}"' in text for key in banned_keys))
            self.assertIsNone(re.search(r"(?<!\d)\d{10,12}(?!\d)", text))
```

- [x] **Step 2: Run the tests to verify they fail**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Expected: FAIL because `validate_content` and `content/` do not exist yet.

- [x] **Step 3: Create the JSON content and validator**

Implement `validate_site(root)` to parse every required JSON file, verify stable unique IDs in list records, require the profile name/email/headline fields, and scan repository text files for prohibited sensitive fields/known ID values.

- [x] **Step 4: Run the tests to verify they pass**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add content scripts/validate_content.py tests/test_content.py
git commit -m "feat: add structured academic content"
```

### Task 2: JSON-driven front-end rendering

**Files:**
- Modify: `assets/site.js`
- Modify: `index.html`
- Modify: `research.html`
- Modify: `publications.html`
- Modify: `experience.html`
- Modify: `cv.html`
- Modify: `contact.html`
- Modify: `teaching.html`
- Modify: `assets/style.css`
- Test: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: `content/*.json` from Task 1.
- Produces: `window.AcademicSite` with `loadJson(path)`, `escapeHtml(value)`, and `init()`; public pages expose `data-page` and page-specific render containers.

- [x] **Step 1: Write failing structure tests**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "research.html", "publications.html", "experience.html", "cv.html", "contact.html", "teaching.html"]


class SiteStructureTests(unittest.TestCase):
    def test_pages_load_shared_renderer_and_declarative_page_name(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('src="assets/site.js"', text)
            self.assertIn('data-page="', text)

    def test_static_academic_records_are_removed_from_page_markup(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("GPA 18.89/20", index)
        pubs = (ROOT / "publications.html").read_text(encoding="utf-8")
        self.assertNotIn("Money Laundering", pubs)
```

- [x] **Step 2: Run tests to verify failure**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Expected: FAIL because current pages hard-code records and do not expose `data-page`.

- [x] **Step 3: Implement renderer and page shells**

Replace duplicated academic copy with semantic containers such as `data-slot="profile-hero"`, `data-slot="education-list"`, and `data-slot="publication-list"`. Implement fetch/render helpers in `assets/site.js`, graceful failure states, safe HTML escaping, current-year footer rendering, and page-specific render functions. Add CSS for loading/error states, structured lists, links, featured markers, and empty optional fields.

- [x] **Step 4: Run tests and a local static-server smoke check**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Run: `python -m http.server 8765 --directory .` from repository root, then request `http://127.0.0.1:8765/content/profile.json` and `http://127.0.0.1:8765/index.html`.
Expected: tests PASS and both requests return HTTP 200.

- [x] **Step 5: Commit**

```bash
git add assets/site.js assets/style.css *.html tests/test_site_structure.py
git commit -m "feat: render academic pages from JSON"
```

### Task 3: Pages CMS dashboard configuration

**Files:**
- Create: `.pages.yml`
- Create: `assets/uploads/.gitkeep`
- Create: `scripts/validate_pages_config.py`
- Test: `tests/test_pages_config.py`

**Interfaces:**
- Consumes: JSON schemas from Task 1 and public assets paths.
- Produces: Pages CMS collections/forms for profile, education, research, publications, projects, experience, awards, skills, site settings, profile image, and CV documents.

- [x] **Step 1: Write failing CMS configuration tests**

```python
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_pages_config import validate_pages_config


class PagesConfigTests(unittest.TestCase):
    def test_pages_cms_configuration_matches_content_model(self):
        self.assertEqual(validate_pages_config(ROOT), [])
```

- [x] **Step 2: Run tests to verify failure**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Expected: FAIL because `.pages.yml` and validator do not exist.

- [x] **Step 3: Implement `.pages.yml` and validator**

Configure media under `assets/uploads/`, expose one structured editor per JSON content file, use object/list/select/image/file fields, and include the supported publication status choices. Implement a lightweight validator that checks required top-level Pages CMS keys, required content filenames, and absence of prohibited identity field names.

- [x] **Step 4: Run tests to verify pass**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add .pages.yml assets/uploads/.gitkeep scripts/validate_pages_config.py tests/test_pages_config.py
git commit -m "feat: add Pages CMS dashboard schema"
```

### Task 4: Repository readiness, documentation, and end-to-end verification

**Files:**
- Modify: `README.md`
- Modify: `CONTENT_CHECKLIST.md`
- Create: `scripts/check_site.py`
- Test: `tests/test_repository.py`

**Interfaces:**
- Consumes: all outputs from Tasks 1–3.
- Produces: `scripts/check_site.py` one-command acceptance check and repository instructions for GitHub Pages + Pages CMS connection.

- [x] **Step 1: Write failing repository acceptance tests**

```python
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_site import check_site


class RepositoryTests(unittest.TestCase):
    def test_repository_is_release_ready(self):
        self.assertEqual(check_site(ROOT), [])
```

- [x] **Step 2: Run tests to verify failure**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Expected: FAIL until the aggregate checker and final documentation exist.

- [x] **Step 3: Implement aggregate checks and documentation**

`check_site(root)` must call content/CMS validators, verify all internal local links resolve, confirm profile image and CV PDF/DOCX exist, confirm `.nojekyll` exists, and scan public text files for prohibited sensitive information. Update README with exact GitHub repository creation/push steps, Pages settings (`main`, `/ (root)`), and Pages CMS GitHub App authorization workflow. Update the content checklist with the editable dashboard sections and safe-publication guidance.

- [x] **Step 4: Run full verification**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`
Run: `python scripts/check_site.py`
Run: local HTTP server smoke test for every HTML page and every JSON content file.
Expected: all tests PASS, checker exits 0, all requested URLs return HTTP 200.

- [x] **Step 5: Commit**

```bash
git add README.md CONTENT_CHECKLIST.md scripts/check_site.py tests/test_repository.py
git commit -m "docs: finalize GitHub Pages and CMS workflow"
```
