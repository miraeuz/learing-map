# Mirae Academy — kurs mazmuni

Kurs Python fayllarida yoziladi va `build.py` orqali **tekshirilib** `src/data/course.json` ga aylantiriladi.

```bash
cd academy
python3 content/build.py      # hammasini ishga tushiradi va tekshiradi
npm run dev                   # ilovada koʻrish
```

`build.py` har safar:

- dars ichidagi har bir kod misolini ishga tushiradi va natijasini darsga yozadi;
- "Bu kod nima chiqaradi?" savollarining toʻgʻri javobini kodni bajarib topadi
  (notoʻgʻri variantlardan biri haqiqiy natijaga teng boʻlsa — xato beradi);
- funksiya/dastur topshiriqlarining kutilgan natijalarini namunaviy yechimdan hisoblaydi,
  boshlangʻich kod testlardan **oʻtmasligini** tekshiradi;
- online masala havolalarini tasdiqlangan roʻyxatlar bilan solishtiradi (`sources/`);
- har bir mavzuda aynan **20 ta** mashq borligini tekshiradi.

Biror muammo boʻlsa, `course.json` yozilmaydi va xatolar roʻyxati chiqadi.

## Fayllar

| Fayl | Boʻlim |
|---|---|
| `s2_asoslar.py` | 2. Python asoslari |
| `s3_operatorlar.py` | 3. Operatorlar |
| `s4_oqim.py` | 4. Boshqaruv oqimi |
| `s5_funksiyalar.py` | 5. Funksiyalar |
| `s6_tuzilmalar.py`, `s6b_tuzilmalar.py` | 6. Maʼlumotlar tuzilmalari |
| `s7_istisnolar.py` | 7. Istisnolar |
| `s8_oop.py` | 8. Obyektga yoʻnaltirilgan dasturlash |
| `s9_modullar.py` | 9. Modullar va paketlar |
| `s10_stdlib.py`, `s10b_stdlib.py` | 10. Standart kutubxona |
| `s11_paketlar.py` | 11. PyPI va virtual muhitlar |
| `s12_paketlar.py` | 12. Mashhur paketlar (amaliy) |
| `s13_django.py` | 13. Django bilan veb-ilovalar |

Yangi boʻlim qoʻshish: `s14_....py` yarating va nomini `build.py` dagi `COURSE_FILES` ga qoʻshing.
Yangi boʻlimga `src/lib/course.ts` dagi `BANDS` ga daraja yorligʻini ham qoʻshing (qoʻshilmasa — «Yangi»).

## Mavzu yozish

```python
from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(8, "Boʻlim nomi", "Qisqa tavsif", "📦")

TOPIC("slug", "Mavzu nomi", "Bir qatorli tavsif", 20, r'''
Kirish paragrafi — **qalin** va `kod` ishlaydi.

## Sarlavha
- roʻyxat elementi
> maslahat (yashil quti)
!> ogohlantirish (sariq quti)

| Jadval | ustunlari |
|---|---|
| a | b |

```py
print("bu kod build vaqtida ishga tushadi")
```
''', [ ...20 ta mashq... ])
```

Kod bloklari variantlari: ` ```py norun ` (ishga tushirilmaydi), ` ```py xato ` (xato berishi kutiladi),
` ```py input=Ali|25 ` (`input()` uchun qiymatlar, `|` — yangi qator).
Python boʻlmagan bloklar (` ```bash `, ` ```text `, ` ```html `, ` ```toml `) faqat koʻrsatiladi.
` ```py file=geometriya.py ` — yordamchi fayl: keyingi ishlaydigan blok yonida yoziladi va
ilovada alohida tab boʻlib koʻrinadi.

Topshiriqqa yordamchi fayllar: `F(..., files={"baza.py": "KITOBLAR = [...]"})` — fayllar
oʻquvchi kodi yonida yaratiladi (har ishga tushirishda toza vaqtinchalik papkada), ilovada
«🔒 faqat oʻqish» tablari sifatida koʻrinadi.

## Mashq turlari (har mavzuda 20 ta)

| Yordamchi | Nima | Misol |
|---|---|---|
| `P(kod, *notoʻgʻri)` | Kod natijasini topish; toʻgʻri javob avtomatik | `P('print(2 ** 3)', "6", "9", "23")` |
| `Q(savol, toʻgʻri, *notoʻgʻri)` | Nazariy savol | `Q("...", "A", "B", "C")` |
| `F(nom, shart, yechim, *chaqiruvlar)` | Funksiya yozish | `F("Kvadrat", "...", "def kv(x):\n    return x*x", "kv(3)", "kv(-1)", "kv(0)")` |
| `PR(nom, shart, yechim, *kirishlar)` | Toʻliq dastur (input/print) | `PR("Yigʻindi", "...", "a=int(input())...", "2\n3", "10\n-4")` |
| `L(sayt, id)` | Online masala: `exercism`, `lc`, `cses`, `acmp`, `docs` | `L("lc", "two-sum")`, `L("docs", "dj-queries")` |

Tavsiya etilgan tarkib: 7 `P` + 2 `Q` + 7 `F`/`PR` + 4 `L`. Qiyinlik: `lv=1..3`.
Xato chiqishi kutilgan natija `⚠ TypeError` koʻrinishida yoziladi.

`docs` havolalari `sources/docs_candidates.py` da yoziladi va `sources/verify_docs.py`
bilan repozitoriy fayl daraxtlariga solishtirib tekshiriladi → `sources/docs.json`.
