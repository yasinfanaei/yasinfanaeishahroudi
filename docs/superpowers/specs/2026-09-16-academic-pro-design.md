# Academic Pro Design

## Goal
Upgrade the existing bilingual GitHub Pages academic website into a low-maintenance, modern academic profile that remains editable from Pages CMS and does not require routine code changes.

## Scope

### 1. Global academic search
- Add a bilingual Search page (`search.html`, `fa/search.html`).
- Search across profile, education, research themes, publications, projects, experience, awards, and news.
- Add a search control to the header; visibility is controlled from the shared design dashboard.
- Search remains fully client-side and has no external dependency.

### 2. Professional publications workflow
- Keep the existing verified/unknown bibliographic-data policy.
- Extend publication records with optional abstract, keywords, volume, issue, pages, PDF, data, code, replication package, and external URL fields.
- Support more output types while preserving existing journal/conference records.
- Add publication-page filters for free-text query, type, status, and year.
- Add client-side citation utilities for plain citation, BibTeX, and RIS without inventing missing metadata.
- Featured publications remain controllable from the CMS.

### 3. News & Updates
- Add bilingual structured news data (`content/en/news.json`, `content/fa/news.json`).
- Add bilingual News pages and an optional/reorderable Home News section.
- Entries support date, title, summary, category, URL, featured, and published toggles.

### 4. Theme system
- Support Light, Dark, and System modes.
- Keep the current light palette as the default light theme and add a dashboard-controlled dark palette.
- Add a theme switcher in the header with user preference stored in localStorage.
- Dashboard controls default mode and whether the switcher is visible.

### 5. Academic SEO
- Add canonical URLs and absolute reciprocal hreflang URLs for all fixed pages.
- Add localized page-level SEO title/description overrides in CMS while retaining safe fallbacks.
- Add Person/ProfilePage JSON-LD using only public profile data.
- Add `robots.txt`, `sitemap.xml`, and a custom bilingual `404.html`.
- Keep social-preview image dashboard-controlled.

### 6. Accessibility and performance
- Preserve skip links and semantic landmarks.
- Add visible keyboard focus styles and reduced-motion handling.
- Add image decoding/loading hints where appropriate.
- Keep the site dependency-free and static.

### 7. Media management
- Split Pages CMS media into named sources for Images, Documents/CV, and Publication Files.
- Migrate current profile and CV assets into the matching managed folders.
- Configure image/file fields to use the appropriate source.

### 8. Validation automation
- Add a GitHub Actions workflow that runs the test suite, repository checker, and JavaScript syntax check on push, pull request, and manual dispatch.
- Add a Pages CMS repository action named “Validate site” that dispatches the same workflow.
- Validation must continue scanning public content and DOCX files for sensitive-number patterns.

### 9. CMS management
- All new content models, feature toggles, theme settings, SEO labels, search labels, news labels, and publication resource fields must be exposed in `.pages.yml`.
- Critical JSON settings files remain non-deletable/non-renamable from CMS.
- Day-to-day content/design management remains no-code; genuinely new application capabilities remain outside the CMS contract.

## Non-goals
- No chatbot, authentication, comments, database, server-side backend, citation scraping, live citation counts, or PWA/service worker.
- No unverified DOI, official English title, volume, issue, page range, or publication URL will be fabricated.
- Analytics remains optional and disabled by default; the core site must work without it.

## Public URL structure
- English default: `https://yasinfanaei.github.io/`
- Persian: `https://yasinfanaei.github.io/fa/`
- New fixed pages: `/news.html`, `/search.html`, `/fa/news.html`, `/fa/search.html`.
