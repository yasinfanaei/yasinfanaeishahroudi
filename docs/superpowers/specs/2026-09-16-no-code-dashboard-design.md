# No-Code Managed Academic Website — Design

## Goal
Convert the existing bilingual GitHub Pages academic site into a CMS-managed design system so routine content, media, branding, typography, colors, layout, navigation, homepage sections, and SEO can be changed in Pages CMS without editing HTML/CSS/JavaScript.

## Scope
The public site remains static HTML/CSS/JavaScript hosted on GitHub Pages. Pages CMS edits structured JSON and media files in the repository. A shared site-wide settings file controls visual design and layout, while each locale retains its own profile/content/site metadata.

## Content architecture
- `content/en/*` and `content/fa/*` remain the language-specific academic content trees.
- `content/settings/design.json` stores shared appearance, typography, layout, branding, homepage section visibility/order, and site controls.
- `content/en/site.json` and `content/fa/site.json` retain locale-specific navigation labels, site title/description, footer copy, announcement copy, and SEO text.
- Existing profile files remain responsible for profile image, CV PDF/DOCX, public contact data, and academic profile links.

## Dashboard architecture
Pages CMS exposes:
1. **English content**: Profile, Education, Research, Publications, Projects, Experience, Awards, Skills, Site Settings.
2. **فارسی**: equivalent Persian content editors.
3. **Design & Branding**: theme colors, typography, sizing, spacing, image treatment, header behavior, homepage section order/visibility, language switch, footer visibility, favicon and social preview image.
4. **Media**: upload/replace public images and documents under `assets/uploads/`.

Critical file entries are editable but not creatable, renamable, or deletable from the CMS.

## Runtime behavior
`assets/site.js` loads the shared design settings before rendering page-specific content. It applies validated values to CSS custom properties and HTML classes, updates shared branding/SEO metadata, and then renders normal content.

CSS uses variables rather than hard-coded theme values for all dashboard-controlled properties. English and Persian font families are separate variables. Layout settings are clamped to reasonable ranges in JavaScript to prevent accidental extreme values from breaking the site.

## Homepage controls
Home sections receive stable IDs (`hero`, `about`, `research`, `education`). Pages CMS exposes an ordered list of objects with `id` and `enabled`. JavaScript reorders these existing sections and hides disabled sections. Unknown IDs are ignored, and any omitted known section remains after the configured sections so a malformed list does not destroy content.

## Navigation controls
Locale `site.json` navigation entries gain an `enabled` boolean. Rendering preserves list order and omits disabled entries. Href remains editable for internal/external navigation.

## SEO and branding
Locale site settings control title, description, keywords, footer label, announcement, and navigation. Shared settings control favicon and Open Graph image. JavaScript updates document title, standard description/keywords, Open Graph/Twitter metadata, and favicon at runtime.

## Safety and resilience
- Identity numbers, birth date, marital status and private phone remain excluded.
- Missing or malformed design settings fall back to CSS defaults.
- Numeric settings are range-clamped.
- URLs and text continue to use escaping/attribute escaping in renderers.
- Content schema remains JSON and backward-compatible where possible.
- No database, paid service, or server-side runtime is introduced.

## Limits
This is a configurable design system, not a free-form visual page builder. Existing content types and layout primitives can be controlled from the dashboard. A completely new component type, application feature, or arbitrary page-builder layout would still require a one-time code change to add that primitive to the system.
