# ICPC yoʻli ⛵

ICPC tayyorgarlik yoʻl xaritasi — orollar boʻylab daraja xaritasi koʻrinishida.
117 ta daraja, 11 ta bosqich: Asoslar → Maʼlumotlar tuzilmalari → Graflar → Daraxtlar →
Dinamik dasturlash → Matematika → Satrlar → Geometriya → Elita darajasi → Jamoa koʻnikmalari.

- Darajani bosing — karta shu nuqtadan ochiladi: **Oʻrganish** (nimani bilish kerak) va **Masalalar** (15 ta havola).
- Havolalar: Codeforces, LeetCode, CSES, acmp.ru, RoboContest, AtCoder, Library Checker, SPOJ, cp-algorithms va boshqalar.
- **Ha, bilaman** — daraja oʻzlashtirildi (3 yulduz). **Hali yoʻq** — mashq roʻyxatiga tushadi.
- Har qanday javob keyingi darajani ochadi. Natijalar va ochilgan havolalar telefonda saqlanadi.

## APK ni olish

Har bir `push` dan keyin GitHub **Actions** APK ni avtomatik yigʻadi:
Actions → oxirgi "Build APK" → **Artifacts** → `icpc-yoli-apk`.

Oʻz kompyuteringizda: `./build_apk.sh` (Flutter va Android SDK kerak).

## Tuzilishi

- Mavzular va tavsiflar: `lib/data/topics.dart`
- Mashq havolalari: `lib/data/links.dart` — `tool/build_links.py` yaratadi
- Xarita chizmasi: `lib/map/map_painter.dart`
- Daraja kartasi: `lib/widgets/level_sheet.dart`

Shrift: Nunito (SIL Open Font License, `assets/fonts/OFL.txt`).

## Mirae Academy (`academy/`)

Python'ni noldan oʻrgatuvchi kompyuter ilovasi (Windows, macOS, Linux). Svelte + Electron,
Python kodi ilova ichida **internetsiz** ishlaydi (Pyodide, Python 3.14).

- 12 boʻlim (2–13): Python asoslari, operatorlar, boshqaruv oqimi, funksiyalar,
  maʼlumotlar tuzilmalari, istisnolar, OOP, modullar va paketlar, standart kutubxona,
  PyPI va virtual muhitlar, mashhur paketlar (API, scraping, PDF, Excel, NumPy) va Django —
  **123 mavzu, 2 460 mashq**.
- Har bir mavzu: qisqa dars + jonli kod misollari (oʻzgartirib ishga tushirish mumkin) + 20 mashq:
  natijani topish, savollar, funksiya/dastur yozish (avtomatik testlar bilan) va online masalalar
  (Exercism, LeetCode, CSES, acmp.ru) hamda rasmiy hujjatlar (Python, Django, pip...).
- Koʻp faylli topshiriqlar: yordamchi modullar va maʼlumot fayllari alohida tablarda.
- Boʻlim imtihonlari (taymer, 70% oʻtish bali), XP va darajalar, faollik xaritasi, kod maydoni,
  qidiruv (Ctrl K, mavzular va mashqlar), har mavzu uchun shaxsiy qaydlar, yigʻiladigan yon panel
  (Ctrl B), tungi/kunduzgi mavzu, zaxira nusxa.
- Telegram orqali bir martalik faollashtirish (ICPC yoʻli bilan bir xil, `TELEGRAM_BOT_TOKEN` secret).
- Faollashtirish **1 yil** amal qiladi (faollashtirilgan kundan). Muddat tugashiga 30 kun qolganda
  eslatma chiqadi; tugagach ilova xuddi shu Telegram kodi bilan yana 1 yilga yangilanadi —
  natijalar, XP va qaydlar saqlanib qoladi. Kompyuter sanasini orqaga surish muddatni uzaytirmaydi.

Oʻrnatuvchilar: **Actions → Build Mirae Academy → Artifacts**.
Ishlab chiqish: `cd academy && npm install && npm run dev`.
Yangi mavzu qoʻshish: [`academy/content/README.md`](academy/content/README.md).

## Kompyuter versiyasi (`desktop/`)

Windows, macOS va Linux uchun. TypeScript + Svelte, Electron bilan oʻralgan.
Chapda bosqichlar, oʻrtada orollar xaritasi, oʻngda daraja paneli: har bir masala uchun katakcha,
eslatmalar, klaviatura tugmalari (← → Y N C, Ctrl K), zaxira nusxa (JSON) va tiklash.

Oʻrnatuvchilar har bir push dan keyin **Actions → Build desktop → Artifacts** da paydo boʻladi.

Ishlab chiqish: `cd desktop && npm install && npm run dev`.
Maʼlumotlar mobil ilova bilan bir xil: `python3 tool/export_json.py` → `desktop/src/data/roadmap.json`.

### Faollashtirish (Telegram)

Birinchi ishga tushirishda foydalanuvchi ismini kiritadi, ilova bir martalik 6 xonali kodni
Telegram botga yuboradi, kod kiritilgach ilova shu kompyuterda faollashadi.
Kod 10 daqiqa amal qiladi, 5 ta notoʻgʻri urinishdan keyin bekor boʻladi.

Bot tokeni kodda saqlanmaydi. GitHub repository → **Settings → Secrets and variables → Actions** da
`TELEGRAM_BOT_TOKEN` (va ixtiyoriy `TELEGRAM_CHAT_ID`) secretini qoʻshing — oʻrnatuvchilar shundan yigʻiladi.

### Imzolash ("Nomaʼlum nashriyotchi" ogohlantirishi)

Windows imzosiz dasturlar uchun SmartScreen ogohlantirishini koʻrsatadi. Uni faqat
kod imzolash sertifikati olib tashlaydi. Workflow tayyor — quyidagilardan birini tanlang:

1. **OV sertifikat** (~$150–300/yil): `.pfx` faylni base64 qilib `WIN_CSC_LINK` secretiga,
   parolini `WIN_CSC_KEY_PASSWORD` secretiga qoʻshing. Keyingi yigʻishlar avtomatik imzolanadi.
2. **SignPath Foundation** (ochiq kodli loyihalar uchun bepul): https://signpath.org/ — ariza bering;
   talablar: OSI litsenziya (`LICENSE`), maxfiylik siyosati (`PRIVACY.md`), imzolash siyosati (`CODE_SIGNING.md`).
3. **Microsoft Store** (sertifikat kerak emas, Store oʻzi imzolaydi): Partner Center da ilova yarating,
   **Product identity** qiymatlarini repository **Variables** ga qoʻshing
   (`MS_STORE_IDENTITY_NAME`, `MS_STORE_PUBLISHER`, `MS_STORE_PUBLISHER_DISPLAY_NAME`),
   soʻng **Run workflow** da "Microsoft Store paketi" belgisini yoqing.

Maxfiylik siyosati: [PRIVACY.md](PRIVACY.md). Litsenziya: [LICENSE](LICENSE) (MIT).
