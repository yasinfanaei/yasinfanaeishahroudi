# Design: GitHub Pages + Pages CMS academic website

Date: 2026-09-16
Status: Awaiting final spec approval before implementation

## 1. Objective

Convert the current static academic website into a Git-backed, editable academic site that remains free to host on GitHub Pages while allowing non-technical content updates through Pages CMS.

The public site will remain static HTML/CSS/JavaScript. Pages CMS will be the editing layer only: it will edit structured content and media in the GitHub repository, and GitHub Pages will publish the resulting files.

## 2. Privacy boundary

The public repository and website must not contain sensitive identity information that is unnecessary for an academic profile. In particular, national identification number, date of birth, marital status, and private phone number will not be stored in the site content or Pages CMS schema.

Only public academic/contact information chosen for publication will be represented in CMS-editable files.

## 3. Architecture

### Hosting and source control
- GitHub repository is the source of truth.
- GitHub Pages publishes from the `main` branch repository root.
- `.nojekyll` remains in the root so GitHub Pages serves the static files directly.

### CMS
- Pages CMS reads `.pages.yml` from the repository root.
- Pages CMS edits repository files directly; there is no CMS database.
- Media uploads are stored under `assets/uploads/` or dedicated subfolders.

### Content model
The current hard-coded academic information will move into structured JSON files under `content/`.

Planned files:
- `content/profile.json` — name, headline, affiliation, bio, email, profile image, social/academic links.
- `content/education.json` — degrees and institutions.
- `content/research.json` — research interests and research-theme cards.
- `content/publications.json` — journal papers, conference papers/presentations, status, authors, venue, year, links.
- `content/projects.json` — research projects and descriptions.
- `content/experience.json` — academic/research/professional experience and service.
- `content/awards.json` — awards and honors.
- `content/skills.json` — software, methods, technical skills, certificates if retained publicly.
- `content/site.json` — navigation labels, footer text, SEO defaults, optional announcements.

All list-like records will receive stable IDs so they can be reordered or updated without depending on their array position.

## 4. Front-end data flow

Each public HTML page will keep its existing URL and visual identity but will no longer duplicate academic content in markup.

At page load:
1. `assets/site.js` loads the required JSON files with `fetch()`.
2. Shared rendering helpers create navigation-independent page sections.
3. Page-specific containers receive profile, education, research, publication, experience, and contact data.
4. If a JSON file or optional field is unavailable, the site shows a graceful fallback rather than raw errors.

This design keeps GitHub Pages deployment simple and does not require a build system or server-side runtime.

## 5. Pages CMS dashboard

`.pages.yml` will organize editable data into the following dashboard groups:

- Profile & Contact
- Education
- Research
- Publications
- Projects
- Experience & Service
- Awards
- Skills & Certificates
- Site Settings
- Media / CV

Relevant fields will use structured editors: strings, multiline text, booleans, selects, nested object lists, image fields, and file fields.

For publications, the editor will support:
- title
- official English title, when available
- type
- publication status
- authors
- corresponding-author flag if desired
- venue
- year
- DOI/URL
- short note
- featured toggle

For profile media, Pages CMS will support replacing the profile image. For documents, it will support replacing the public CV PDF/DOCX files.

## 6. Publication status and uncertainty

No missing bibliographic metadata will be invented. Existing publication entries will preserve only information supported by the supplied CV. Fields such as DOI, volume, issue, pages, official English title, or publication URL will remain empty until supplied or independently verified.

The front end will suppress empty fields rather than displaying placeholders.

## 7. CV handling

The current generated English CV files remain downloadable from `assets/`.

Pages CMS will allow replacing the public CV document files. The first version will not automatically regenerate a DOCX/PDF from CMS content because that would require a build workflow and adds unnecessary complexity. A later phase can add automated CV generation through GitHub Actions if desired.

## 8. GitHub Pages deployment

The intended deployment configuration is:
- source: Deploy from a branch
- branch: `main`
- folder: `/ (root)`

Once Pages CMS saves a change to `main`, GitHub Pages will republish the updated static site.

## 9. Repository setup and connection

The local project will be made repository-ready, including `.pages.yml`, structured content, validation scripts/tests, and deployment documentation.

Publishing to the user's GitHub account requires an authenticated GitHub write channel. If direct write access is exposed in the active product, the repository can be created/pushed there. Otherwise, the finished repository package will be ready for a one-time GitHub upload/push, after which Pages CMS can handle normal content edits through its GitHub App.

Pages CMS itself requires the user to sign in with GitHub and authorize its GitHub App for the chosen repository. That authorization cannot be safely pre-authorized without the account holder.

## 10. Testing and validation

Implementation acceptance checks:
- Every existing public page loads without console errors.
- All internal navigation links resolve.
- JSON content parses successfully.
- Missing optional fields do not break rendering.
- Publication/research/education/experience lists render from data rather than hard-coded content.
- Mobile layout remains usable.
- Profile image and CV links work.
- `.pages.yml` is syntactically valid and reflects the JSON schema.
- No prohibited sensitive identity fields appear anywhere in the repository.
- A local static-server smoke test verifies `fetch()` behavior (because opening pages as `file://` does not reliably allow JSON fetches).

## 11. Non-goals for this phase

- No paid hosting or paid CMS.
- No database.
- No login system hosted inside the public site.
- No server-side code.
- No automatic CV PDF/DOCX generation from the CMS in phase 1.
- No storage of national ID, marital status, date of birth, or private phone number.

## 12. Expected editor workflow after launch

1. Open Pages CMS hosted app.
2. Sign in with GitHub.
3. Select the academic-website repository.
4. Open the relevant section, e.g. Publications.
5. Add/edit/delete/reorder content.
6. Save.
7. Pages CMS writes the change to GitHub.
8. GitHub Pages republishes the site.

