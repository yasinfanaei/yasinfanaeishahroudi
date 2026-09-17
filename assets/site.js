(function () {
  'use strict';

  const pageRequirements = {
    home: ['profile', 'education', 'research', 'news', 'site'],
    research: ['profile', 'research', 'projects', 'site'],
    publications: ['profile', 'publications', 'site'],
    experience: ['profile', 'experience', 'awards', 'skills', 'site'],
    cv: ['profile', 'education', 'research', 'publications', 'projects', 'experience', 'awards', 'site'],
    contact: ['profile', 'site'],
    teaching: ['profile', 'experience', 'site'],
    news: ['profile', 'news', 'site'],
    search: ['profile', 'education', 'research', 'publications', 'projects', 'experience', 'awards', 'news', 'site']
  };

  const I18N = {
    en: {
      viewResearch: 'View research', downloadCv: 'Download CV', publicOnly: 'Public academic information only; sensitive personal identifiers are not stored in this website repository.',
      gpa: 'GPA', supervisor: 'Supervisor', grade: 'Grade', projectLead: 'Project lead', projectLink: 'Project link →',
      statuses: { accepted: 'Accepted', published: 'Published', published_or_accepted: 'Published/accepted', working_paper: 'Working paper', under_review: 'Under review', conference: 'Conference paper' },
      groups: { journal: 'Journal research', conference: 'Conference papers & presentations' },
      featured: 'Featured', venue: 'Venue:', corresponding: 'Corresponding author reported in source:', publicationLink: 'Publication link', missingBib: 'Empty DOI, URL, volume, issue, page range, or official-English-title fields are intentionally suppressed until verified information is supplied.',
      exp: { research: 'Research', professional: 'Professional', service: 'Academic service', other: 'Other experience' },
      curriculum: 'Curriculum vitae', downloadPdf: 'Download PDF', downloadDocx: 'Download DOCX', print: 'Print this page', degreeListed: 'Degree listed in CV', with: 'With', seeAll: 'See the complete publication and conference-paper list →',
      email: 'Email', institution: 'Institution', location: 'Location', openProfile: 'Open profile →', noLinks: 'No public academic-profile links have been supplied yet. You can add them later from the CMS dashboard.', noTeaching: 'No teaching entries are currently listed.', loadError: 'This section could not be loaded. Please refresh the page or check the content files.',
      links: { google_scholar: 'Google Scholar', orcid: 'ORCID', researchgate: 'ResearchGate', linkedin: 'LinkedIn', github: 'GitHub' },
      langLabel: 'فارسی', portraitAlt: 'Portrait of'
    },
    fa: {
      viewResearch: 'مشاهده پژوهش‌ها', downloadCv: 'دانلود رزومه', publicOnly: 'این وب‌سایت فقط شامل اطلاعات دانشگاهیِ انتخاب‌شده برای انتشار عمومی است و شناسه‌های شخصی حساس در مخزن آن ذخیره نمی‌شوند.',
      gpa: 'معدل', supervisor: 'استاد راهنما', grade: 'نمره', projectLead: 'مسئول طرح', projectLink: 'پیوند طرح ←',
      statuses: { accepted: 'پذیرفته‌شده', published: 'منتشرشده', published_or_accepted: 'منتشرشده/پذیرفته‌شده', working_paper: 'مقاله در دست کار', under_review: 'در حال داوری', conference: 'مقاله کنفرانسی' },
      groups: { journal: 'مقالات علمی', conference: 'مقالات و ارائه‌های کنفرانسی' },
      featured: 'منتخب', venue: 'محل انتشار:', corresponding: 'نویسنده مسئول طبق منبع:', publicationLink: 'پیوند انتشار', missingBib: 'اطلاعات تأییدنشده مانند DOI، پیوند، جلد، شماره، صفحات یا عنوان رسمی انگلیسی تا زمان راستی‌آزمایی نمایش داده نمی‌شوند.',
      exp: { research: 'پژوهشی', professional: 'حرفه‌ای', service: 'خدمات و فعالیت دانشگاهی', other: 'سایر سوابق' },
      curriculum: 'رزومه علمی', downloadPdf: 'دانلود PDF', downloadDocx: 'دانلود Word', print: 'چاپ این صفحه', degreeListed: 'مدرک درج‌شده در رزومه', with: 'با همکاری', seeAll: 'مشاهده فهرست کامل مقالات و ارائه‌ها ←',
      email: 'ایمیل', institution: 'دانشگاه', location: 'محل', openProfile: 'مشاهده پروفایل ←', noLinks: 'هنوز پیوند پروفایل دانشگاهی عمومی ثبت نشده است.', noTeaching: 'در حال حاضر سابقه آموزشی دیگری ثبت نشده است.', loadError: 'بارگذاری این بخش با خطا روبه‌رو شد. صفحه را دوباره بارگذاری کنید یا فایل‌های محتوا را بررسی کنید.',
      links: { google_scholar: 'Google Scholar', orcid: 'ORCID', researchgate: 'ResearchGate', linkedin: 'LinkedIn', github: 'GitHub' },
      langLabel: 'EN', portraitAlt: 'تصویر'
    }
  };

  const locale = document.body.dataset.locale === 'fa' ? 'fa' : 'en';
  const rootPrefix = locale === 'fa' ? '../' : '';
  const t = I18N[locale];
  const designPath = `${rootPrefix}content/settings/design.json`;
  let activeDesign = {};
  let activeSite = {};


  function escapeHtml(value) { return String(value == null ? '' : value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;'); }
  function attr(value) { return escapeHtml(value); }
  function slot(name) { return document.querySelector(`[data-slot="${name}"]`); }
  function setHtml(name, html) { const el = slot(name); if (el) el.innerHTML = html; }
  function setText(name, text) { const el = slot(name); if (el) el.textContent = text || ''; }
  function uiLabel(key, fallback) { return (activeSite.ui && activeSite.ui[key]) || fallback; }
  function joinParts(parts, separator) { return parts.filter(Boolean).join(separator || ' · '); }
  function localAsset(path) { if (!path || /^(https?:|mailto:|tel:|#|data:)/i.test(path) || path.startsWith('/')) return path; return rootPrefix + path.replace(/^\.\//, ''); }
  function sharedAsset(profile, key) {
    const branding = activeDesign.branding || {};
    return branding[key] || (profile && profile[key]) || '';
  }
  function contentPath(key) { return `${rootPrefix}content/${locale}/${key}.json`; }
  async function loadJson(path) { const response = await fetch(path, { cache: 'no-store' }); if (!response.ok) throw new Error(`Unable to load ${path} (${response.status})`); return response.json(); }

  function clampNumber(value, min, max, fallback) {
    const n = Number(value);
    return Number.isFinite(n) ? Math.min(max, Math.max(min, n)) : fallback;
  }

  function fontStack(name, language) {
    const english = {
      'Times New Roman': '"Times New Roman",Times,serif',
      Georgia: 'Georgia,serif', Arial: 'Arial,sans-serif', Helvetica: 'Helvetica,Arial,sans-serif',
      Verdana: 'Verdana,sans-serif', Tahoma: 'Tahoma,sans-serif'
    };
    const persian = {
      'B Nazanin': '"B Nazanin","Nazanin",Tahoma,serif', Nazanin: '"Nazanin",Tahoma,serif',
      Tahoma: 'Tahoma,Arial,sans-serif', Arial: 'Arial,Tahoma,sans-serif', 'Times New Roman': '"Times New Roman",Times,serif'
    };
    const map = language === 'fa' ? persian : english;
    return map[name] || (language === 'fa' ? persian['B Nazanin'] : english['Times New Roman']);
  }

  const THEME_STORAGE_KEY = 'academic-theme';
  const COLOR_VARS = { background: '--bg', surface: '--surface', text: '--text', muted: '--muted', line: '--line', accent: '--accent', accent_secondary: '--accent-2', soft: '--soft' };

  function storedThemePreference() {
    try {
      const value = window.localStorage.getItem(THEME_STORAGE_KEY);
      return ['system', 'light', 'dark'].includes(value) ? value : '';
    } catch (_) { return ''; }
  }

  function resolveThemeMode(preference) {
    if (preference === 'light' || preference === 'dark') return preference;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyPalette(palette) {
    const style = document.documentElement.style;
    Object.entries(COLOR_VARS).forEach(([key, variable]) => {
      if (palette && palette[key]) style.setProperty(variable, palette[key]);
    });
  }

  function applyThemeSettings(settings) {
    const theme = (settings && settings.theme) || {};
    const preference = storedThemePreference() || theme.default_mode || 'system';
    const resolved = resolveThemeMode(preference);
    document.documentElement.setAttribute('data-theme', resolved);
    document.documentElement.setAttribute('data-theme-preference', preference);
    applyPalette(resolved === 'dark' ? ((settings && settings.dark_colors) || {}) : ((settings && settings.colors) || {}));
    return preference;
  }

  function setThemePreference(mode) {
    const preference = ['system', 'light', 'dark'].includes(mode) ? mode : 'system';
    try { window.localStorage.setItem(THEME_STORAGE_KEY, preference); } catch (_) { /* storage may be disabled */ }
    applyThemeSettings(activeDesign);
    const select = document.querySelector('[data-theme-select]');
    if (select) select.value = preference;
  }

  function watchSystemTheme() {
    if (!window.matchMedia) return;
    const query = window.matchMedia('(prefers-color-scheme: dark)');
    const refresh = () => {
      const preference = storedThemePreference() || ((activeDesign.theme || {}).default_mode || 'system');
      if (preference === 'system') applyThemeSettings(activeDesign);
    };
    if (query.addEventListener) query.addEventListener('change', refresh);
    else if (query.addListener) query.addListener(refresh);
  }

  function ensureMeta(selector, attrs) {
    let el = document.head.querySelector(selector);
    if (!el) {
      el = document.createElement('meta');
      Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
      document.head.appendChild(el);
    }
    return el;
  }

  function ensureLink(selector, attrs) {
    let el = document.head.querySelector(selector);
    if (!el) { el = document.createElement('link'); document.head.appendChild(el); }
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  }

  function canonicalUrl(page, language) {
    const base = String(((activeDesign.seo || {}).site_url) || 'https://yasinfanaei.github.io').replace(/\/$/, '');
    const filename = pageFilename(page);
    const path = filename === 'index.html' ? '' : filename;
    return language === 'fa' ? `${base}/fa/${path}` : `${base}/${path}`;
  }

  function updateStructuredData(profile, site, page) {
    const enabled = (activeDesign.seo || {}).structured_data_enabled !== false;
    let script = document.head.querySelector('script[data-academic-structured-data]');
    if (!enabled || !profile || page !== 'home') { if (script) script.remove(); return; }
    if (!script) { script = document.createElement('script'); script.type = 'application/ld+json'; script.setAttribute('data-academic-structured-data', ''); document.head.appendChild(script); }
    const person = { '@type': 'Person', name: profile.name, url: canonicalUrl('home', locale) };
    if (profile.headline) person.jobTitle = profile.headline;
    if (profile.email) person.email = `mailto:${profile.email}`;
    if (profile.affiliation) person.affiliation = { '@type': 'EducationalOrganization', name: profile.affiliation };
    const sameAs = Object.values(profile.links || {}).filter(Boolean); if (sameAs.length) person.sameAs = sameAs;
    const image = sharedAsset(profile, 'profile_image'); if (image) person.image = new URL(localAsset(image), window.location.href).href;
    script.textContent = JSON.stringify({ '@context': 'https://schema.org', '@type': 'ProfilePage', url: canonicalUrl('home', locale), mainEntity: person });
  }

  function initAnalytics(settings) {
    const analytics = (settings && settings.analytics) || {};
    if (!analytics.enabled || analytics.provider !== 'google_analytics' || !/^G-[A-Z0-9]+$/i.test(analytics.measurement_id || '')) return;
    if (document.querySelector('script[data-academic-analytics]')) return;
    const id = analytics.measurement_id.toUpperCase();
    const script = document.createElement('script'); script.async = true; script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(id)}`; script.setAttribute('data-academic-analytics',''); document.head.appendChild(script);
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){ window.dataLayer.push(arguments); };
    window.gtag('js', new Date()); window.gtag('config', id, { anonymize_ip: true });
  }

  function updateMetadata(site, design, page) {
    if (!site) return;
    const current = Array.isArray(site.navigation) ? site.navigation.find((item) => item.id === page) : null;
    const pageSeo = Array.isArray(site.page_seo) ? site.page_seo.find((item) => item.id === page) : null;
    const title = (pageSeo && pageSeo.title) || (page === 'home' ? site.site_title : joinParts([current && current.label, site.site_title], ' | '));
    const pageDescription = (pageSeo && pageSeo.description) || site.default_description || '';
    if (title) document.title = title;
    const description = ensureMeta('meta[name="description"]', { name: 'description' });
    if (pageDescription) description.setAttribute('content', pageDescription);
    const keywords = ensureMeta('meta[name="keywords"]', { name: 'keywords' });
    keywords.setAttribute('content', Array.isArray(site.keywords) ? site.keywords.join(', ') : (site.keywords || ''));
    const indexingEnabled = !activeDesign.seo || activeDesign.seo.indexing_enabled !== false;
    ensureMeta('meta[name="robots"]', { name: 'robots' }).setAttribute('content', indexingEnabled ? 'index,follow' : 'noindex,nofollow');
    ensureMeta('meta[property="og:title"]', { property: 'og:title' }).setAttribute('content', title || '');
    ensureMeta('meta[property="og:description"]', { property: 'og:description' }).setAttribute('content', pageDescription);
    ensureMeta('meta[name="twitter:card"]', { name: 'twitter:card' }).setAttribute('content', 'summary_large_image');
    ensureMeta('meta[name="twitter:title"]', { name: 'twitter:title' }).setAttribute('content', title || '');
    ensureMeta('meta[name="twitter:description"]', { name: 'twitter:description' }).setAttribute('content', pageDescription);
    ensureLink('link[rel="canonical"]', { rel: 'canonical', href: canonicalUrl(page, locale) });
    ensureLink('link[rel="alternate"][hreflang="en"]', { rel: 'alternate', hreflang: 'en', href: canonicalUrl(page, 'en') });
    ensureLink('link[rel="alternate"][hreflang="fa"]', { rel: 'alternate', hreflang: 'fa', href: canonicalUrl(page, 'fa') });
    ensureLink('link[rel="alternate"][hreflang="x-default"]', { rel: 'alternate', hreflang: 'x-default', href: canonicalUrl(page, 'en') });
    const ogImage = design && design.branding && design.branding.open_graph_image;
    if (ogImage) {
      const resolved = new URL(localAsset(ogImage), window.location.href).href;
      ensureMeta('meta[property="og:image"]', { property: 'og:image' }).setAttribute('content', resolved);
      ensureMeta('meta[name="twitter:image"]', { name: 'twitter:image' }).setAttribute('content', resolved);
    }
    const favicon = design && design.branding && design.branding.favicon;
    if (favicon) {
      let link = document.head.querySelector('link[rel="icon"]');
      if (!link) { link = document.createElement('link'); link.rel = 'icon'; document.head.appendChild(link); }
      link.removeAttribute('type');
      link.href = localAsset(favicon);
    }
  }

  function applyDesignSettings(settings) {
    activeDesign = settings || {};
    const root = document.documentElement;
    const style = root.style;
    applyThemeSettings(activeDesign);
    const type = activeDesign.typography || {};
    style.setProperty('--font-en', fontStack(type.english_font, 'en'));
    style.setProperty('--font-fa', fontStack(type.persian_font, 'fa'));
    const baseFont = clampNumber(type.base_font_size, 13, 24, 16);
    const titleScale = clampNumber(type.hero_title_scale, 0.7, 1.35, 1);
    style.setProperty('--base-font-size', `${baseFont}px`);
    style.setProperty('--font-size-fa', `${baseFont * 1.05}px`);
    style.setProperty('--line-height-en', String(clampNumber(type.english_line_height, 1.2, 2.2, 1.68)));
    style.setProperty('--line-height-fa', String(clampNumber(type.persian_line_height, 1.4, 2.5, 1.9)));
    const titleBase = locale === 'fa' ? { min: 3, fluid: 6.2, max: 4.8 } : { min: 2.7, fluid: 7, max: 5.2 };
    style.setProperty('--hero-title-min', `${titleBase.min * titleScale}rem`);
    style.setProperty('--hero-title-fluid', `${titleBase.fluid * titleScale}vw`);
    style.setProperty('--hero-title-max', `${titleBase.max * titleScale}rem`);
    const layout = activeDesign.layout || {};
    style.setProperty('--max', `${clampNumber(layout.max_width, 760, 1600, 1100)}px`);
    style.setProperty('--section-space', `${clampNumber(layout.section_spacing, 24, 140, 62)}px`);
    style.setProperty('--hero-space-top', `${clampNumber(layout.hero_space_top, 24, 180, locale === 'fa' ? 72 : 88)}px`);
    style.setProperty('--hero-space-bottom', `${clampNumber(layout.hero_space_bottom, 20, 160, locale === 'fa' ? 58 : 66)}px`);
    style.setProperty('--hero-gap', `${clampNumber(layout.hero_gap, 12, 120, locale === 'fa' ? 52 : 64)}px`);
    style.setProperty('--portrait-size', `${clampNumber(layout.portrait_size, 45, 100, 100)}%`);
    style.setProperty('--portrait-radius', `${clampNumber(layout.portrait_radius, 0, 80, 18)}px`);
    style.setProperty('--button-radius', `${clampNumber(layout.button_radius, 0, 40, 8)}px`);
    style.setProperty('--card-radius', `${clampNumber(layout.card_radius, 0, 50, 14)}px`);
    style.setProperty('--nav-gap', `${clampNumber(layout.nav_gap, 6, 48, 20)}px`);
    root.classList.toggle('design-header-static', (activeDesign.controls || {}).sticky_header === false);
    root.classList.toggle('design-no-shadow', (activeDesign.controls || {}).show_shadows === false);
    root.classList.toggle('design-hide-footer', (activeDesign.controls || {}).show_footer === false);
    root.classList.toggle('design-hide-language-switch', (activeDesign.controls || {}).show_language_switch === false);
    root.classList.remove('design-portrait-left', 'design-portrait-right');
    if (layout.portrait_side === 'left') root.classList.add('design-portrait-left');
    if (layout.portrait_side === 'right') root.classList.add('design-portrait-right');
  }

  function applyHomeSections(settings) {
    const main = document.querySelector('main');
    if (!main || !settings || !Array.isArray(settings.home_sections)) return;
    const sections = new Map(Array.from(main.querySelectorAll('[data-home-section]')).map((el) => [el.dataset.homeSection, el]));
    const used = new Set();
    settings.home_sections.forEach((item) => {
      const el = sections.get(item.id); if (!el) return;
      el.hidden = item.enabled === false;
      main.appendChild(el); used.add(item.id);
    });
    sections.forEach((el, id) => { if (!used.has(id)) { el.hidden = false; main.appendChild(el); } });
  }
  function pageFilename(page) { return page === 'home' ? 'index.html' : `${page}.html`; }

  function renderLanguageSwitch(page) {
    const el = slot('language-switch'); if (!el) return;
    if ((activeDesign.controls || {}).show_language_switch === false) { el.innerHTML = ''; return; }
    const file = pageFilename(page);
    const href = locale === 'fa' ? `../${file}` : `fa/${file}`;
    el.innerHTML = `<a class="language-switch" href="${attr(href)}" hreflang="${locale === 'fa' ? 'en' : 'fa'}">${t.langLabel}</a>`;
  }

  function renderHeaderControls(page) {
    const navTools = document.querySelector('.nav-tools');
    if (!navTools) return;
    let actions = navTools.querySelector('.header-actions');
    if (!actions) {
      actions = document.createElement('div');
      actions.className = 'header-actions';
      navTools.appendChild(actions);
    }
    const controls = activeDesign.controls || {};
    const searchHref = locale === 'fa' ? 'search.html' : 'search.html';
    const searchLabel = uiLabel('search_button', locale === 'fa' ? 'جستجو' : 'Search');
    const search = controls.show_search === false ? '' : `<a class="search-link" href="${attr(searchHref)}" aria-label="${attr(searchLabel)}">⌕ <span>${escapeHtml(searchLabel)}</span></a>`;
    const theme = activeDesign.theme || {};
    const preference = storedThemePreference() || theme.default_mode || 'system';
    const themeControl = controls.show_theme_switch === false ? '' : `<label class="theme-switch"><span class="visually-hidden">Theme</span><select data-theme-select aria-label="Theme"><option value="system">${escapeHtml(uiLabel('theme_system', locale === 'fa' ? 'سیستم' : 'System'))}</option><option value="light">${escapeHtml(uiLabel('theme_light', locale === 'fa' ? 'روشن' : 'Light'))}</option><option value="dark">${escapeHtml(uiLabel('theme_dark', locale === 'fa' ? 'تیره' : 'Dark'))}</option></select></label>`;
    actions.innerHTML = `${search}${themeControl}`;
    const select = actions.querySelector('[data-theme-select]');
    if (select) {
      select.value = preference;
      select.addEventListener('change', (event) => setThemePreference(event.target.value));
    }
  }

  function renderGlobal(data, page) {
    const { profile, site } = data;
    activeSite = site || {};
    document.querySelectorAll('[data-ui]').forEach((el) => { const value = activeSite.ui && activeSite.ui[el.dataset.ui]; if (value) el.textContent = value; });
    if (profile) {
      document.querySelectorAll('[data-profile-name]').forEach((el) => { el.textContent = profile.name; });
      const brand = slot('brand');
      if (brand) {
        const logo = (activeDesign.branding || {}).logo;
        const showName = (activeDesign.controls || {}).show_brand_name !== false;
        brand.innerHTML = `${logo ? `<img class="brand-logo" src="${attr(localAsset(logo))}" alt="" decoding="async">` : ''}${showName ? `<span>${escapeHtml(profile.name)}</span>` : ''}` || escapeHtml(profile.name);
      }
    }
    if (site && Array.isArray(site.navigation)) {
      const nav = slot('nav');
      if (nav) nav.innerHTML = site.navigation.filter((item) => item.enabled !== false).map((item) => `<a href="${attr(item.href)}"${item.id === page ? ' aria-current="page"' : ''}>${escapeHtml(item.label)}</a>`).join('');
      const footerLabel = slot('footer-label'); if (footerLabel) footerLabel.textContent = site.footer_label || '';
      if (site.site_title && page === 'home') document.title = site.site_title;
      const description = document.querySelector('meta[name="description"]'); if (description && site.default_description && page === 'home') description.setAttribute('content', site.default_description);
      const announcement = slot('announcement'); if (announcement) { announcement.hidden = !(site.announcement_enabled && site.announcement); announcement.textContent = site.announcement || ''; }
    }
    updateMetadata(site, activeDesign, page);
    updateStructuredData(profile, site, page);
    renderLanguageSwitch(page);
    renderHeaderControls(page);
    document.querySelectorAll('[data-current-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
  }

  function socialLinks(profile, compact) {
    const links = Object.entries(profile.links || {}).filter(([, url]) => url);
    if (!links.length) return '';
    return `<div class="${compact ? 'academic-links compact' : 'academic-links'}">${links.map(([key, url]) => `<a href="${attr(url)}" target="_blank" rel="me noopener">${escapeHtml(t.links[key] || key)}</a>`).join('')}</div>`;
  }

  function renderHome(data) {
    const { profile, research, education } = data;
    if (profile && research) {
      setHtml('profile-hero', `<div><p class="eyebrow">${escapeHtml(profile.eyebrow)}</p><h1>${escapeHtml(profile.name)}</h1><p class="lede">${escapeHtml(profile.short_bio)}</p><div class="hero-meta">${research.interests.map((x) => `<span class="tag">${escapeHtml(x)}</span>`).join('')}</div><div class="actions"><a class="button" href="research.html">${uiLabel('view_research', t.viewResearch)}</a>${sharedAsset(profile, 'cv_pdf') ? `<a class="button secondary" href="${attr(localAsset(sharedAsset(profile, 'cv_pdf')))}">${uiLabel('download_cv', t.downloadCv)}</a>` : ''}</div>${(activeDesign.controls || {}).show_social_links_on_home === false ? '' : socialLinks(profile, true)}</div>${sharedAsset(profile, 'profile_image') ? `<img class="portrait" src="${attr(localAsset(sharedAsset(profile, 'profile_image')))}" alt="${t.portraitAlt} ${attr(profile.name)}" decoding="async" fetchpriority="high">` : ''}`);
      setHtml('about', `<p>${escapeHtml(profile.bio)}</p><p class="muted small">${t.publicOnly}</p>`);
      setHtml('research-themes', research.themes.map((theme) => `<article class="card"><h3>${escapeHtml(theme.title)}</h3><p>${escapeHtml(theme.description)}</p></article>`).join(''));
    }
    renderHomeNews(data);
    if (education) setHtml('education-list', `<ul class="list-clean">${education.items.map((item) => { const details = joinParts([item.institution, item.period, item.gpa ? `${t.gpa} ${item.gpa}` : '']); return `<li><strong>${escapeHtml(item.degree)}</strong><br><span class="muted">${escapeHtml(details)}</span>${item.note ? `<br><span class="small muted">${escapeHtml(item.note)}</span>` : ''}</li>`; }).join('')}</ul>`);
  }

  function renderResearch(data) {
    const { research, projects } = data;
    if (research) {
      setText('research-intro', research.intro);
      setHtml('research-themes', research.themes.map((x) => `<article class="entry"><h2 class="entry-title">${escapeHtml(x.title)}</h2><p>${escapeHtml(x.description)}</p></article>`).join(''));
      const x = research.thesis || {};
      setHtml('thesis', `<article class="entry"><h2 class="entry-title">${escapeHtml(x.title)}</h2><p class="entry-meta">${escapeHtml(joinParts([x.degree, x.institution, x.supervisor ? `${t.supervisor}: ${x.supervisor}` : '', x.grade ? `${t.grade}: ${x.grade}` : '']))}</p>${x.note ? `<p>${escapeHtml(x.note)}</p>` : ''}</article>`);
    }
    if (projects) setHtml('projects', projects.items.map((x) => `<article class="entry"><h2 class="entry-title">${escapeHtml(x.title)}</h2><p class="entry-meta">${escapeHtml(joinParts([x.role, x.lead ? `${t.projectLead}: ${x.lead}` : '']))}</p><p>${escapeHtml(x.description)}</p>${x.url ? `<p><a href="${attr(x.url)}">${t.projectLink}</a></p>` : ''}</article>`).join(''));
  }

  function publishedNewsItems(news) {
    return ((news && news.items) || []).filter((item) => item.published !== false).slice().sort((a, b) => String(b.date || '').localeCompare(String(a.date || '')));
  }

  function renderNewsEntry(item, compact) {
    const linkOpen = item.url ? `<a href="${attr(item.url)}"${/^https?:/i.test(item.url) ? ' target="_blank" rel="noopener"' : ''}>` : '';
    const linkClose = item.url ? '</a>' : '';
    return `<article class="${compact ? 'card news-card' : 'entry news-entry'}" id="${attr(item.id || '')}"><div class="entry-heading-row"><h2 class="${compact ? 'news-card-title' : 'entry-title'}">${linkOpen}${escapeHtml(item.title || '')}${linkClose}</h2>${item.featured ? `<span class="status-pill">${t.featured}</span>` : ''}</div><p class="entry-meta">${escapeHtml(joinParts([item.date, item.category]))}</p>${item.summary ? `<p>${escapeHtml(item.summary)}</p>` : ''}</article>`;
  }

  function renderHomeNews(data) {
    const items = publishedNewsItems(data.news);
    const featured = items.filter((item) => item.featured);
    const selected = (featured.length ? featured : items).slice(0, 3);
    setHtml('home-news-list', selected.length ? selected.map((item) => renderNewsEntry(item, true)).join('') : `<p class="muted">${escapeHtml(uiLabel('news_empty', locale === 'fa' ? 'هنوز خبر عمومی ثبت نشده است.' : 'No public updates have been added yet.'))}</p>`);
  }

  function renderNews(data) {
    const news = data.news;
    if (!news) return;
    setText('news-intro', news.intro || '');
    const items = publishedNewsItems(news);
    setHtml('news-list', items.length ? items.map((item) => renderNewsEntry(item, false)).join('') : `<p class="muted">${escapeHtml(uiLabel('news_empty', locale === 'fa' ? 'هنوز خبر عمومی ثبت نشده است.' : 'No public updates have been added yet.'))}</p>`);
  }

  function normalizeSearchText(value) {
    return String(value == null ? '' : value).toLocaleLowerCase(locale === 'fa' ? 'fa' : 'en').replace(/\s+/g, ' ').trim();
  }

  function buildSearchIndex(data) {
    const results = [];
    const add = (type, title, text, href, keywords) => {
      if (!title) return;
      results.push({ type, title, text: text || '', href, haystack: normalizeSearchText([title, text, ...(keywords || [])].filter(Boolean).join(' ')) });
    };
    const p = data.profile || {};
    add('profile', p.name, [p.headline, p.affiliation, p.bio, p.short_bio].filter(Boolean).join(' '), 'index.html');
    ((data.education && data.education.items) || []).forEach((x) => add('education', x.degree, [x.institution, x.period, x.note].filter(Boolean).join(' '), 'cv.html'));
    ((data.research && data.research.themes) || []).forEach((x) => add('research', x.title, x.description, 'research.html'));
    const thesis = data.research && data.research.thesis; if (thesis) add('research', thesis.title, [thesis.degree, thesis.institution, thesis.note].filter(Boolean).join(' '), 'research.html');
    ((data.publications && data.publications.items) || []).forEach((x) => add('publication', x.official_english_title || x.title, [x.title_fa, (x.authors || []).join(' '), x.venue, x.venue_english_rendering, x.year, x.abstract].filter(Boolean).join(' '), `publications.html#${x.id}`, x.keywords || []));
    ((data.projects && data.projects.items) || []).forEach((x) => add('project', x.title, [x.description, x.role, x.lead].filter(Boolean).join(' '), 'research.html'));
    ((data.experience && data.experience.items) || []).forEach((x) => add('experience', x.title, [x.organization, x.period, x.description].filter(Boolean).join(' '), 'experience.html'));
    ((data.awards && data.awards.items) || []).forEach((x) => add('award', x.title, [x.issuer, x.year, x.description].filter(Boolean).join(' '), 'experience.html'));
    publishedNewsItems(data.news).forEach((x) => add('news', x.title, [x.summary, x.category, x.date].filter(Boolean).join(' '), `news.html#${x.id}`));
    return results;
  }

  function renderSearch(data) {
    const input = slot('search-input');
    const output = slot('search-results');
    if (!input || !output) return;
    const index = buildSearchIndex(data);
    const params = new URLSearchParams(window.location.search);
    input.placeholder = uiLabel('search_placeholder', locale === 'fa' ? 'جستجو…' : 'Search…');
    input.value = params.get('q') || '';
    const draw = () => {
      const query = normalizeSearchText(input.value);
      if (!query) { output.innerHTML = ''; return; }
      const terms = query.split(' ').filter(Boolean);
      const matches = index.filter((item) => terms.every((term) => item.haystack.includes(term)));
      output.innerHTML = matches.length ? matches.map((item) => `<article class="search-result"><p class="eyebrow">${escapeHtml(item.type)}</p><h2 class="entry-title"><a href="${attr(item.href)}">${escapeHtml(item.title)}</a></h2>${item.text ? `<p>${escapeHtml(item.text)}</p>` : ''}</article>`).join('') : `<p class="muted">${escapeHtml(uiLabel('search_no_results', locale === 'fa' ? 'نتیجه‌ای یافت نشد.' : 'No matching results.'))}</p>`;
    };
    input.addEventListener('input', draw);
    draw();
    requestAnimationFrame(() => input.focus({ preventScroll: true }));
  }

  function statusLabel(status) { return t.statuses[status] || status || ''; }

  function publicationTypeLabel(type) {
    const en = { journal: 'Journal article', conference: 'Conference paper', working_paper: 'Working paper', book_chapter: 'Book chapter', report: 'Research report' };
    const fa = { journal: 'مقاله مجله', conference: 'مقاله کنفرانسی', working_paper: 'مقاله در دست کار', book_chapter: 'فصل کتاب', report: 'گزارش پژوهشی' };
    return (locale === 'fa' ? fa : en)[type] || type || '';
  }

  function publicationCitation(item) {
    const authors = (item.authors || []).join(locale === 'fa' ? '، ' : ', ');
    const title = item.official_english_title || item.title || '';
    const venue = item.venue_english_rendering || item.venue || '';
    const bibliographic = [item.volume ? `vol. ${item.volume}` : '', item.issue ? `no. ${item.issue}` : '', item.pages ? `pp. ${item.pages}` : ''].filter(Boolean).join(', ');
    const doi = item.doi ? `https://doi.org/${item.doi}` : '';
    return [authors, title, venue, bibliographic, item.year, doi].filter(Boolean).join('. ').replace(/\.\s*\./g, '.');
  }

  function bibtexEscape(value) { return String(value || '').replace(/[{}]/g, ''); }
  function publicationBibtex(item) {
    const type = item.type === 'journal' ? 'article' : (item.type === 'book_chapter' ? 'incollection' : 'misc');
    const firstAuthor = (item.authors && item.authors[0]) || 'Fanaei';
    const surname = firstAuthor.trim().split(/\s+/).slice(-1)[0].replace(/[^A-Za-z0-9]/g, '') || 'Fanaei';
    const yearDigits = String(item.year || '').match(/\d{4}/);
    const titleWord = String(item.official_english_title || item.title || 'work').split(/\s+/)[0].replace(/[^A-Za-z0-9]/g, '') || 'work';
    const key = `${surname}${yearDigits ? yearDigits[0] : ''}${titleWord}`;
    const fields = [
      ['title', item.official_english_title || item.title],
      ['author', (item.authors || []).join(' and ')],
      ['year', item.year],
      [type === 'article' ? 'journal' : 'howpublished', item.venue_english_rendering || item.venue],
      ['volume', item.volume], ['number', item.issue], ['pages', item.pages], ['doi', item.doi], ['url', item.url || item.pdf]
    ].filter(([, value]) => value);
    return `@${type}{${key},\n${fields.map(([name, value]) => `  ${name} = {${bibtexEscape(value)}}`).join(',\n')}\n}`;
  }

  function publicationRis(item) {
    const type = item.type === 'journal' ? 'JOUR' : (item.type === 'conference' ? 'CPAPER' : 'GEN');
    const lines = [`TY  - ${type}`, `TI  - ${item.official_english_title || item.title || ''}`];
    (item.authors || []).forEach((author) => lines.push(`AU  - ${author}`));
    if (item.year) lines.push(`PY  - ${item.year}`);
    if (item.venue_english_rendering || item.venue) lines.push(`T2  - ${item.venue_english_rendering || item.venue}`);
    if (item.volume) lines.push(`VL  - ${item.volume}`);
    if (item.issue) lines.push(`IS  - ${item.issue}`);
    if (item.pages) lines.push(`SP  - ${item.pages}`);
    if (item.doi) lines.push(`DO  - ${item.doi}`);
    if (item.url) lines.push(`UR  - ${item.url}`);
    lines.push('ER  -');
    return lines.join('\n');
  }

  async function copyText(text, button) {
    let copied = false;
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); copied = true; }
    } catch (_) { copied = false; }
    if (!copied) {
      const area = document.createElement('textarea'); area.value = text; area.setAttribute('readonly', ''); area.style.position = 'fixed'; area.style.opacity = '0'; document.body.appendChild(area); area.select();
      try { copied = document.execCommand('copy'); } catch (_) { copied = false; }
      area.remove();
    }
    if (button && copied) {
      const before = button.textContent; button.textContent = uiLabel('citation_copied', locale === 'fa' ? 'کپی شد' : 'Copied');
      window.setTimeout(() => { button.textContent = before; }, 1200);
    }
    return copied;
  }

  function filterPublications(items, state) {
    const query = normalizeSearchText(state.query || '');
    const terms = query.split(' ').filter(Boolean);
    return (items || []).filter((item) => {
      const haystack = normalizeSearchText([item.title, item.official_english_title, item.title_fa, (item.authors || []).join(' '), item.venue, item.venue_english_rendering, item.year, item.abstract, (item.keywords || []).join(' ')].filter(Boolean).join(' '));
      return (!terms.length || terms.every((term) => haystack.includes(term))) && (!state.type || item.type === state.type) && (!state.status || item.status === state.status) && (!state.year || item.year === state.year);
    });
  }

  function publicationResources(item) {
    const links = [];
    if (item.doi) links.push(`<a href="https://doi.org/${attr(item.doi)}" target="_blank" rel="noopener">DOI</a>`);
    if (item.url) links.push(`<a href="${attr(item.url)}" target="_blank" rel="noopener">${escapeHtml(t.publicationLink)}</a>`);
    if (item.pdf) links.push(`<a href="${attr(localAsset(item.pdf))}">${escapeHtml(uiLabel('pdf_label', 'PDF'))}</a>`);
    if (item.data_url) links.push(`<a href="${attr(item.data_url)}" target="_blank" rel="noopener">${escapeHtml(uiLabel('data_label', locale === 'fa' ? 'داده' : 'Data'))}</a>`);
    if (item.code_url) links.push(`<a href="${attr(item.code_url)}" target="_blank" rel="noopener">${escapeHtml(uiLabel('code_label', locale === 'fa' ? 'کد' : 'Code'))}</a>`);
    if (item.replication_url) links.push(`<a href="${attr(item.replication_url)}" target="_blank" rel="noopener">${escapeHtml(uiLabel('replication_label', locale === 'fa' ? 'بسته بازتولید' : 'Replication'))}</a>`);
    return links.length ? `<p class="entry-links publication-resource-links">${links.join('')}</p>` : '';
  }

  function renderPublicationItem(item) {
    const citation = encodeURIComponent(publicationCitation(item));
    const bibtex = encodeURIComponent(publicationBibtex(item));
    const ris = encodeURIComponent(publicationRis(item));
    const keywords = (item.keywords || []).length ? `<p class="publication-keywords"><strong>${escapeHtml(uiLabel('keywords_label', locale === 'fa' ? 'کلیدواژه‌ها' : 'Keywords'))}:</strong> ${item.keywords.map(escapeHtml).join(locale === 'fa' ? '، ' : ', ')}</p>` : '';
    const abstract = item.abstract ? `<details class="publication-abstract"><summary>${escapeHtml(uiLabel('abstract_label', locale === 'fa' ? 'چکیده' : 'Abstract'))}</summary><p>${escapeHtml(item.abstract)}</p></details>` : '';
    return `<article class="entry publication-entry" id="${attr(item.id || '')}"><div class="entry-heading-row"><h2 class="entry-title">${escapeHtml(item.official_english_title || item.title)}</h2>${item.featured ? `<span class="status-pill">${t.featured}</span>` : ''}</div><p class="entry-meta">${escapeHtml(joinParts([(item.authors || []).join(locale === 'fa' ? '، ' : '; '), item.year, statusLabel(item.status)]))}</p>${item.venue_english_rendering || item.venue ? `<p><strong>${t.venue}</strong> ${escapeHtml(item.venue_english_rendering || item.venue)}</p>` : ''}${item.corresponding_author ? `<p class="small muted">${t.corresponding} ${escapeHtml(item.corresponding_author)}</p>` : ''}${abstract}${keywords}${publicationResources(item)}<div class="citation-actions"><button type="button" class="citation-button" data-copy-text="${attr(citation)}">${escapeHtml(uiLabel('citation_copy', locale === 'fa' ? 'کپی ارجاع' : 'Copy citation'))}</button><button type="button" class="citation-button" data-copy-text="${attr(bibtex)}">${escapeHtml(uiLabel('citation_bibtex', 'BibTeX'))}</button><button type="button" class="citation-button" data-copy-text="${attr(ris)}">${escapeHtml(uiLabel('citation_ris', 'RIS'))}</button></div>${item.note ? `<p class="small muted">${escapeHtml(item.note)}</p>` : ''}</article>`;
  }

  function wirePublicationCopyButtons(container) {
    container.querySelectorAll('[data-copy-text]').forEach((button) => button.addEventListener('click', () => copyText(decodeURIComponent(button.dataset.copyText || ''), button)));
  }

  function renderPublicationList(publications, state) {
    const container = slot('publication-list'); if (!container) return;
    const items = filterPublications(publications.items || [], state);
    const types = [...new Set(items.map((x) => x.type))];
    const body = types.map((type) => {
      const group = items.filter((x) => x.type === type);
      return `<section class="publication-group"><p class="eyebrow">${escapeHtml(publicationTypeLabel(type))}</p>${group.map(renderPublicationItem).join('')}</section>`;
    }).join('');
    container.innerHTML = (body || `<p class="muted">${escapeHtml(uiLabel('search_no_results', locale === 'fa' ? 'نتیجه‌ای یافت نشد.' : 'No matching results.'))}</p>`) + `<div class="note small">${t.missingBib}</div>`;
    wirePublicationCopyButtons(container);
  }

  function renderPublicationTools(publications) {
    const tools = slot('publication-tools'); if (!tools) return;
    const types = [...new Set((publications.items || []).map((x) => x.type).filter(Boolean))];
    const statuses = [...new Set((publications.items || []).map((x) => x.status).filter(Boolean))];
    const years = [...new Set((publications.items || []).map((x) => x.year).filter(Boolean))].sort().reverse();
    const state = { query: '', type: '', status: '', year: '' };
    tools.innerHTML = `<div class="publication-tools"><label class="filter-search"><span class="visually-hidden">${escapeHtml(uiLabel('publication_search_placeholder', 'Search publications'))}</span><input type="search" data-pub-filter="query" placeholder="${attr(uiLabel('publication_search_placeholder', locale === 'fa' ? 'جستجو در انتشارات…' : 'Search publications…'))}"></label><select data-pub-filter="type" aria-label="Type"><option value="">${escapeHtml(uiLabel('publication_all_types', locale === 'fa' ? 'همه انواع' : 'All types'))}</option>${types.map((x) => `<option value="${attr(x)}">${escapeHtml(publicationTypeLabel(x))}</option>`).join('')}</select><select data-pub-filter="status" aria-label="Status"><option value="">${escapeHtml(uiLabel('publication_all_statuses', locale === 'fa' ? 'همه وضعیت‌ها' : 'All statuses'))}</option>${statuses.map((x) => `<option value="${attr(x)}">${escapeHtml(statusLabel(x))}</option>`).join('')}</select><select data-pub-filter="year" aria-label="Year"><option value="">${escapeHtml(uiLabel('publication_all_years', locale === 'fa' ? 'همه سال‌ها' : 'All years'))}</option>${years.map((x) => `<option value="${attr(x)}">${escapeHtml(x)}</option>`).join('')}</select><button type="button" class="filter-clear">${escapeHtml(uiLabel('publication_clear_filters', locale === 'fa' ? 'پاک‌کردن فیلترها' : 'Clear filters'))}</button></div>`;
    const redraw = () => renderPublicationList(publications, state);
    tools.querySelectorAll('[data-pub-filter]').forEach((control) => control.addEventListener('input', () => { state[control.dataset.pubFilter] = control.value; redraw(); }));
    const clear = tools.querySelector('.filter-clear'); if (clear) clear.addEventListener('click', () => { Object.keys(state).forEach((key) => { state[key] = ''; }); tools.querySelectorAll('[data-pub-filter]').forEach((control) => { control.value = ''; }); redraw(); });
    redraw();
  }

  function renderPublications(data) {
    const p = data.publications; if (!p) return;
    setText('publications-intro', p.intro);
    renderPublicationTools(p);
  }

  function renderExperience(data) {
    const e=data.experience,a=data.awards,s=data.skills;
    if(e){const cats=['research','professional','service','other'];setHtml('experience-list',cats.map((c)=>{const items=e.items.filter((x)=>x.category===c);if(!items.length)return '';return `<section class="experience-group"><p class="eyebrow">${t.exp[c]}</p>${items.map((x)=>`<article class="entry"><h2 class="entry-title">${escapeHtml(x.title)}</h2><p class="entry-meta">${escapeHtml(joinParts([x.organization,x.period]))}</p>${x.description?`<p>${escapeHtml(x.description)}</p>`:''}</article>`).join('')}</section>`;}).join(''));}
    if(a)setHtml('awards-list',a.items.map((x)=>`<article class="entry"><h2 class="entry-title">${escapeHtml(x.title)}</h2><p class="entry-meta">${escapeHtml(joinParts([x.issuer,x.year]))}</p><p>${escapeHtml(x.description)}</p></article>`).join(''));
    if(s)setHtml('skills-groups',`${s.groups.map((g)=>`<article class="card"><h3>${escapeHtml(g.title)}</h3><p>${g.items.map(escapeHtml).join(' · ')}</p></article>`).join('')}<p class="muted small full-span">${escapeHtml(s.note)}</p>`);
  }

  function renderCv(data) {
    const {profile,education,research,publications,projects,experience,awards}=data;
    if(profile)setHtml('cv-header',`<p class="eyebrow">${t.curriculum}</p><h1>${escapeHtml(profile.name)}</h1><p class="lede">${escapeHtml(profile.headline)} · ${escapeHtml(profile.affiliation)}</p><div class="actions">${sharedAsset(profile,'cv_pdf')?`<a class="button" href="${attr(localAsset(sharedAsset(profile,'cv_pdf')))}">${uiLabel('download_pdf', t.downloadPdf)}</a>`:''}${sharedAsset(profile,'cv_docx')?`<a class="button secondary" href="${attr(localAsset(sharedAsset(profile,'cv_docx')))}">${uiLabel('download_docx', t.downloadDocx)}</a>`:''}<button class="button secondary" type="button" onclick="window.print()">${uiLabel('print', t.print)}</button></div>${socialLinks(profile,true)}`);
    if(education)setHtml('cv-education',education.items.map((x)=>`<div class="cv-row"><div class="cv-year">${escapeHtml(x.period||t.degreeListed)}</div><div><strong>${escapeHtml(x.degree)}</strong><br>${escapeHtml(x.institution)}${x.gpa?` · ${t.gpa} ${escapeHtml(x.gpa)}`:''}${x.note?`<br><span class="muted small">${escapeHtml(x.note)}</span>`:''}</div></div>`).join(''));
    if(research)setHtml('cv-interests',`<p>${research.interests.map(escapeHtml).join(locale==='fa'?'؛ ':'; ')}.</p>`);
    if(publications){const featured=publications.items.filter((x)=>x.featured);setHtml('cv-publications',featured.map((x)=>`<p><strong>${escapeHtml(x.official_english_title||x.title)}.</strong> ${escapeHtml(joinParts([`${t.with} ${x.authors.filter((a)=>a!==profile.name).join(', ')}`,statusLabel(x.status),x.year],'. '))}</p>`).join('')+`<p><a href="publications.html">${t.seeAll}</a></p>`);}
    if(projects)setHtml('cv-projects',projects.items.map((x)=>`<p><strong>${escapeHtml(x.title)}.</strong> ${escapeHtml(x.description)}</p>`).join(''));
    if(experience||awards){const service=(experience?experience.items.filter((x)=>x.category==='service'):[]).slice(0,4);setHtml('cv-service',`${service.map((x)=>`<p><strong>${escapeHtml(x.title)}</strong> — ${escapeHtml(joinParts([x.organization,x.period]))}</p>`).join('')}${awards?awards.items.map((x)=>`<p><strong>${escapeHtml(x.title)}</strong> — ${escapeHtml(joinParts([x.issuer,x.year]))}. ${escapeHtml(x.description)}</p>`).join(''):''}`);}
  }

  function renderContact(data) {
    const p=data.profile;if(!p)return;
    setHtml('contact-grid',`<div class="contact-item"><strong>${t.email}</strong><a href="mailto:${attr(p.email)}">${escapeHtml(p.email)}</a></div><div class="contact-item"><strong>${t.institution}</strong><span>${escapeHtml(p.affiliation)}</span><br><span class="muted">${escapeHtml(p.headline)}</span></div>${p.location?`<div class="contact-item"><strong>${t.location}</strong><span>${escapeHtml(p.location)}</span></div>`:''}`);
    const links=Object.entries(p.links||{}).filter(([,u])=>u);setHtml('profile-links',links.length?links.map(([k,u])=>`<a class="contact-item link-card" href="${attr(u)}" target="_blank" rel="me noopener"><strong>${escapeHtml(t.links[k]||k)}</strong><span>${t.openProfile}</span></a>`).join(''):`<p class="muted">${t.noLinks}</p>`);
  }

  function renderTeaching(data){const items=data.experience?data.experience.items.filter((x)=>/instruction|آموزش/i.test(x.title)):[];setHtml('teaching-list',items.length?items.map((x)=>`<article class="entry"><h2 class="entry-title">${escapeHtml(x.title)}</h2><p class="entry-meta">${escapeHtml(joinParts([x.organization,x.period]))}</p></article>`).join(''):`<p class="muted">${t.noTeaching}</p>`);}
  function showLoadError(error){console.error(error);document.querySelectorAll('[data-slot]').forEach((el)=>{if(!el.innerHTML.trim()&&!['nav','brand','language-switch'].includes(el.dataset.slot))el.innerHTML=`<p class="load-error">${t.loadError}</p>`;});}

  async function init(){
    const page=document.body.dataset.page||'home';
    const keys=pageRequirements[page]||['profile','site'];
    try{
      const [design, values] = await Promise.all([
        loadJson(designPath).catch(() => ({})),
        Promise.all(keys.map(async(key)=>[key,await loadJson(contentPath(key))]))
      ]);
      applyDesignSettings(design);
      initAnalytics(design);
      watchSystemTheme();
      const data=Object.fromEntries(values);
      renderGlobal(data,page);
      if(page==='home')renderHome(data);
      if(page==='research')renderResearch(data);
      if(page==='publications')renderPublications(data);
      if(page==='experience')renderExperience(data);
      if(page==='cv')renderCv(data);
      if(page==='contact')renderContact(data);
      if(page==='teaching')renderTeaching(data);
      if(page==='news')renderNews(data);
      if(page==='search')renderSearch(data);
      if(page==='home')applyHomeSections(design);
      document.documentElement.classList.add('content-ready');
    }catch(error){showLoadError(error);}
  }

  window.AcademicSite={loadJson,escapeHtml,applyDesignSettings,applyHomeSections,applyThemeSettings,resolveThemeMode,setThemePreference,renderHeaderControls,buildSearchIndex,renderSearch,renderNews,renderHomeNews,renderPublicationTools,filterPublications,publicationCitation,publicationBibtex,publicationRis,copyText,updateMetadata,updateStructuredData,initAnalytics,init};document.addEventListener('DOMContentLoaded',init);
}());
