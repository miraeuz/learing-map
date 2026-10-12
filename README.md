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

## Kompyuter versiyasi (`desktop/`)

Windows, macOS va Linux uchun. TypeScript + Svelte, Electron bilan oʻralgan.
Chapda bosqichlar, oʻrtada orollar xaritasi, oʻngda daraja paneli: har bir masala uchun katakcha,
eslatmalar, klaviatura tugmalari (← → Y N C, Ctrl K), zaxira nusxa (JSON) va tiklash.

Oʻrnatuvchilar har bir push dan keyin **Actions → Build desktop → Artifacts** da paydo boʻladi.

Ishlab chiqish: `cd desktop && npm install && npm run dev`.
Maʼlumotlar mobil ilova bilan bir xil: `python3 tool/export_json.py` → `desktop/src/data/roadmap.json`.
