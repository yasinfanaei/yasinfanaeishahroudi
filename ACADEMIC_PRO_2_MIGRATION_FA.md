# نصب یک‌باره Academic Pro 2 — راهنمای خیلی ساده

این راهنما برای نصب Academic Pro 2 در repository مستقل `yasinfanaei/yasinfanaeishahroudi` است. بعد از این مهاجرت، مدیریت روزمره از Pages CMS انجام می‌شود.

## مرحله ۱ — فایل نهایی را Upload کن

بسته کامل Academic Pro 2 را Extract کن و **محتویات داخل پوشه** را روی root repository جدید `yasinfanaei/yasinfanaeishahroudi` آپلود کن.

حتماً این فایل‌ها/پوشه‌ها باید وارد repository شوند:

```text
.pages.yml
.nojekyll
.github/
  workflows/
    validate.yml
    deploy-pages.yml
requirements.txt
src/
content/
assets/
scripts/
tests/
```

اگر GitHub Web فایل‌های مخفی را نگرفت، از github.dev یا Create new file برای مسیرهای مخفی استفاده کن. فایل `.github/workflows/deploy-pages.yml` برای AP2 ضروری است.

Commit پیشنهادی:

```text
Install Academic Pro 2 static build
```

## مرحله ۲ — GitHub Actions را بررسی کن

به تب **Actions** برو. باید workflowهای زیر را ببینی:

- Validate Academic Site
- Build and Deploy Academic Site

اولین Push ممکن است هر دو را اجرا کند. اگر قرمز شدند، Deploy را تنظیم نکن تا خطا بررسی شود.

## مرحله ۳ — فقط یک‌بار Source گیت‌هاب پیجز را عوض کن

در GitHub repository برو به:

**Settings -> Pages**

در قسمت **Build and deployment**، Source را از **Deploy from a branch** به **GitHub Actions** تغییر بده.

از این لحظه دیگر `main / (root)` روش انتشار Academic Pro 2 نیست. GitHub Actions پوشه `_site` تولیدشده را deploy می‌کند.

## مرحله ۴ — Deploy را اجرا/بررسی کن

به **Actions -> Build and Deploy Academic Site** برو. آخرین run باید سبز شود.

بعد سایت را باز کن:

- `https://yasinfanaei.github.io/yasinfanaeishahroudi/`
- `https://yasinfanaei.github.io/yasinfanaeishahroudi/fa/`
- `https://yasinfanaei.github.io/yasinfanaeishahroudi/research/`
- `https://yasinfanaei.github.io/yasinfanaeishahroudi/fa/research/`

مسیرهای clean URL باید بدون `.html` باز شوند.

## مرحله ۵ — Pages CMS را Refresh کن

به Pages CMS برو و repository را Refresh/Reopen کن. باید این امکانات را ببینی:

- English -> Pages
- فارسی -> صفحات
- Profile Contacts با Add item
- Site & Navigation با Add item و Children
- Design & Branding -> Theme preset
- Custom theme colors
- Layout presets
- Actions -> Validate site

## مرحله ۶ — تست ساده بدون ریسک

اول فقط Theme preset را مثلاً از Classic Academic به Oxford Navy تغییر بده و Save کن. بعد از سبز شدن Actions، سایت را Hard Refresh کن. سپس دوباره به تم دلخواه برگردان.

برای تست Contacts، یک مورد عمومی واقعی را فقط اگر می‌خواهی منتشر شود اضافه کن و Visibility موردنظر را انتخاب کن.

## مرحله ۷ — از این به بعد

برای کار روزمره GitHub code را باز نکن. از Pages CMS استفاده کن. GitHub Actions خودش Validate -> Build -> Deploy را انجام می‌دهد.

اگر یک Save باعث run قرمز شد، نسخه قبلی سالم سایت باقی می‌ماند و deploy جدید متوقف می‌شود.

## Rollback

اگر در مهاجرت اولیه مشکلی جدی پیش آمد، در GitHub از History/Commits به commit قبل از AP2 برگرد. قبل از rollback، screenshot خطای Actions را نگه دار تا علت دقیق اصلاح شود.
