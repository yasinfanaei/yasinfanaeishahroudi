# نصب Academic Pro 2 در سایت مستقل پروژه

این بسته مخصوص repository زیر است:

`yasinfanaei/yasinfanaeishahroudi`

آدرس عمومی هدف:

`https://yasinfanaei.github.io/yasinfanaeishahroudi/`

فایل `content/settings/design.json` از قبل با همین `site_url` تنظیم شده است. Build، لینک‌های داخلی، assetها، Search، canonical، hreflang، Open Graph، JSON-LD و sitemap همگی base path `/yasinfanaeishahroudi/` را رعایت می‌کنند.

## نصب

1. ZIP را Extract کن.
2. محتویات داخل پوشه را در root repository آپلود کن؛ خود ZIP یا پوشه مادر را آپلود نکن.
3. مطمئن شو `.pages.yml` و `.github/workflows/validate.yml` و `.github/workflows/deploy-pages.yml` هم وجود دارند.
4. Commit کن.
5. در Settings -> Pages، Source را روی **GitHub Actions** بگذار.
6. در Actions منتظر سبز شدن **Validate Academic Site** و **Build and Deploy Academic Site** بمان.
7. سپس آدرس `https://yasinfanaei.github.io/yasinfanaeishahroudi/` را باز کن.

از این به بعد مدیریت روزمره از Pages CMS انجام می‌شود.
