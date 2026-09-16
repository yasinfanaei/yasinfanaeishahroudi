# راهنمای داشبورد Academic Pro 2

بعد از نصب و تغییر GitHub Pages به **GitHub Actions**، کار روزمره سایت را از Pages CMS انجام بده. برای تغییرات عادی لازم نیست HTML، CSS، JavaScript یا Python را باز کنی.

## ۱. اطلاعات شخصی و راه‌های ارتباطی

از **English -> Profile & Contact** یا **فارسی -> مشخصات و ارتباط** استفاده کن.

در بخش Contacts می‌توانی با Add item هر تعداد مورد اضافه کنی:

- Email
- Phone
- WhatsApp
- Telegram
- Website
- Office
- Location
- Custom

برای هر مورد Label، Value، URL اختیاری و سه محل نمایش وجود دارد:

- Show on Home
- Show on Contact
- Show in Footer

ترتیب آیتم‌ها همان ترتیب نمایش است. هر مورد را می‌توانی Disable کنی بدون اینکه حذف شود.

**حریم خصوصی:** فقط ایمیل/شماره/آدرسی را وارد کن که واقعاً می‌خواهی عمومی باشد.

## ۲. عکس، رزومه و برندینگ

از **Design & Branding — ظاهر و تنظیمات اصلی**:

- Profile Image: عکس پروفایل مشترک هر دو زبان
- CV PDF / DOCX: فایل رزومه
- Logo
- Favicon
- Open Graph Image: تصویر هنگام Share شدن سایت

فایل‌های آپلودشده در Media ذخیره می‌شوند.

## ۳. انتخاب تم آماده

در Design & Branding -> Theme preset فقط **یک** تم انتخاب کن:

1. Classic Academic
2. Oxford Navy
3. Midnight Teal
4. Burgundy & Cream
5. Forest & Ivory
6. Slate Blue
7. Monochrome Editorial
8. Custom

هر preset هم Light و هم Dark دارد. Dark Mode با رنگ متن/دکمه/کارت/لینک هماهنگ ساخته می‌شود.

اگر **Custom** را انتخاب کنی، بخش Custom theme colors فعال معنایی پیدا می‌کند. همه رنگ‌های لازم از قبل مقدار امن دارند؛ می‌توانی آن‌ها را تغییر بدهی، ولی اگر contrast نامناسب شود validation ممکن است جلوی انتشار را بگیرد.

## ۴. چیدمان آماده

در Layout presets می‌توانی بدون عددگذاری پیچیده انتخاب کنی:

- Content width: narrow / standard / wide / custom
- Hero style: split / centered / compact
- Section density: compact / standard / spacious
- Card style: flat / border / elevated
- Header style: standard / compact
- Corner style: square / subtle / rounded

Advanced numeric controls همچنان برای تنظیم دقیق‌تر وجود دارند.

## ۵. ساخت صفحه جدید بدون کدنویسی

به **English -> Pages** یا **فارسی -> صفحات** برو و Add entry را بزن.

مقادیر مهم:

- ID: شناسه پایدار؛ انگلیسی کوچک و خط تیره، مثل `working-papers`
- Slug: آدرس URL، مثل `working-papers`
- Translation key: برای وصل کردن نسخه فارسی/انگلیسی؛ در دو زبان یکسان باشد
- Title: عنوان صفحه
- Menu label: عنوانی که می‌خواهی برای منو استفاده کنی
- Status: `draft` یا `published`
- Show breadcrumbs
- Show in sitemap
- SEO title / description / image / noindex
- Blocks: محتوای صفحه

مثال: slug برابر `working-papers` در انگلیسی URL `/working-papers/` می‌سازد. نسخه فارسی با همین translation key و slug مناسب خودش زیر `/fa/.../` ساخته می‌شود.

تا وقتی صفحه Draft باشد در sitemap/search منتشر نمی‌شود.

## ۶. بلوک‌های صفحه

در Blocks با Add block نوع بخش را انتخاب و سپس Drag/Reorder کن. گزینه‌های اصلی:

- Profile Hero
- Heading
- Rich Text
- Image
- Callout
- Buttons
- Cards
- Contact Methods
- Academic Links
- Research Themes
- Education Timeline
- Publication Index
- News List
- Experience List
- Projects List
- Awards List
- Skills List
- Downloads
- Accordion
- Divider
- Search

هر Block یک Enabled دارد. برای مخفی‌کردن موقت، Disable کن و حذف نکن.

Rich Text از ویرایشگر قالب‌بندی‌شده استفاده می‌کند؛ JavaScript خام در آن منتشر نمی‌شود.

## ۷. اضافه‌کردن صفحه به منو

ساختن Page به‌تنهایی آن را وارد منو نمی‌کند. بعد به **Site & Navigation / سایت و منو** برو.

در Navigation با Add item:

- Label
- Enabled
- Destination
- Page / URL / Section
- New tab
- Children

Destinationها:

- `page`: یکی از صفحات سایت را انتخاب کن
- `section`: لینک به یک بخش Home
- `external`: URL خارجی HTTPS
- `file`: فایل عمومی مثل PDF

برای Submenu، آیتم‌های فرزند را در Children اضافه کن. یک سطح زیرمنو پشتیبانی می‌شود.

می‌توانی منوها را هر تعداد لازم اضافه، حذف و مرتب کنی.

## ۸. Publications

از بخش Publications داده‌ها را وارد کن. فقط اطلاعاتی را وارد کن که تأیید شده‌اند. DOI، volume، issue، pages، official English title، PDF/Data/Code/Replication URL را حدس نزن.

صفحه عمومی Publications به‌طور خودکار فیلتر Text / Type / Status / Year و Copy Citation / BibTeX / RIS دارد.

## ۹. SEO

برای هر Page:

- SEO Title
- Description
- Share image
- Noindex
- Show in sitemap

در Design & Branding، `site_url` آدرس اصلی عمومی کل سایت است. اگر بعداً دامنه اختصاصی گرفتی، با تغییر همین مقدار canonical، sitemap، robots، structured data و share URLs در build بعدی تغییر می‌کنند.

Slug صفحات منتشرشده را بدون دلیل تغییر نده. اگر تغییر لازم شد، URL قبلی را در `redirect_from` نگه دار.

## ۱۰. Analytics

Analytics به‌صورت پیش‌فرض خاموش است. اگر GA4 می‌خواهی:

- Enabled = true
- Provider = google_analytics
- Measurement ID = مقدار `G-...`

اگر خاموش باشد هیچ Google Analytics script در HTML قرار نمی‌گیرد.

## ۱۱. Save و انتشار

بعد از Save در Pages CMS:

1. تغییر در GitHub ذخیره می‌شود.
2. Validation اجرا می‌شود.
3. Static Build اجرا می‌شود.
4. SEO / sitemap / search index تولید می‌شود.
5. اگر همه بررسی‌ها موفق باشند GitHub Pages deploy می‌شود.

اگر validation قرمز شود، نسخه خراب منتشر نمی‌شود. در این حالت از Actions یا Pages CMS -> Actions -> Validate site جزئیات خطا را ببین.

## ۱۲. چیزهایی که دیگر نباید برای کار روزمره انجام بدهی

- ویرایش مستقیم HTML
- تغییر CSS برای انتخاب رنگ عادی
- ساخت دستی فایل صفحه
- نوشتن لینک داخلی صفحه با URL دستی وقتی Destination = page داری
- آپلود مستقیم CV/عکس از GitHub وقتی Media/CMS در دسترس است
- تغییر workflowها مگر برای ارتقای فنی آینده
