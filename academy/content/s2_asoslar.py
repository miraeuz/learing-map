from dsl import SECTION, TOPIC, P, Q, PR, F, L

SECTION(2, "Python asoslari", "Sintaksis, oʻzgaruvchilar, maʼlumot turlari va satrlar", "🧱")

# ---------------------------------------------------------------- 2.1
TOPIC("sintaksis", "Sintaksis va chekinish", "Python kodi qanday yoziladi va nima uchun boʻsh joylar muhim", 15, r'''
Har bir tilda grammatika bor. Dasturlash tilidagi grammatika **sintaksis** deyiladi. Python sintaksisi juda sodda — shuning uchun u birinchi til sifatida eng koʻp tanlanadi.

## Ifoda va buyruq
Python kodi qatorma-qator, yuqoridan pastga bajariladi. Har bir qator — bitta **buyruq** (statement).

```py
print("Birinchi qator")
print("Ikkinchi qator")
print(2 + 3)
```

> Qator oxirida nuqtali vergul `;` shart emas. Pythonda yangi qator — yangi buyruq.

## Chekinish (indentation)
Boshqa tillarda kod bloklari `{ }` qavslar bilan ajratiladi. Pythonda esa **chekinish** — qator boshidagi boʻsh joylar — blokni belgilaydi. Odatda 4 ta boʻsh joy ishlatiladi.

```py
yosh = 18
if yosh >= 18:
    print("Siz kattasiz")
    print("Ovoz berishingiz mumkin")
print("Bu qator har doim chiqadi")
```

`if` dan keyingi ikki qator 4 ta boʻsh joy bilan yozilgan — ular `if` blokiga tegishli. Oxirgi qator chekinishsiz — u blokdan tashqarida.

!> Chekinish notoʻgʻri boʻlsa, Python `IndentationError` xatosini beradi. Bir blok ichida hamma qatorlar bir xil chekinishda boʻlishi shart.

```py xato
if True:
print("Chekinish yoʻq")
```

## Katta-kichik harf
Python katta va kichik harflarni farqlaydi: `ism`, `Ism` va `ISM` — uchta turli nom. `print` toʻgʻri, `Print` esa xato.

## Bir qatorda bir nechta buyruq
Kamdan-kam hollarda bir qatorga bir nechta buyruq yozish uchun `;` ishlatiladi. Lekin oʻqish qiyinlashadi — tavsiya etilmaydi.

```py
a = 5; b = 7; print(a + b)
```

## Uzun qatorni boʻlish
Qavs ichidagi ifodani bir necha qatorga boʻlish mumkin:

```py
jami = (1200 + 3500 +
        800 + 4500)
print(jami)
```

## Esda tuting
- Kod yuqoridan pastga, qatorma-qator bajariladi.
- Blok chekinish bilan belgilanadi — odatda 4 ta boʻsh joy.
- `print` va `Print` — turli narsalar: katta-kichik harf muhim.
- Qator oxirida `;` kerak emas.
''', [
    P('print("Salom")\nprint("Dunyo")', "Salom Dunyo", "SalomDunyo", "Dunyo\nSalom"),
    P('print(10 + 5)\nprint("10 + 5")', "15\n15", "10 + 5\n10 + 5", "15\n10+5", why="Qoʻshtirnoqsiz `10 + 5` hisoblanadi, qoʻshtirnoq ichida esa matn sifatida chiqadi."),
    P('x = 3\nif x > 1:\n    print("katta")\nprint("tamom")', "katta", "tamom", "tamom\nkatta"),
    P('x = 0\nif x > 1:\n    print("katta")\n    print("ha")\nprint("tamom")', "katta\nha\ntamom", "ha\ntamom", "katta\ntamom", why="`x > 1` yolgʻon, shuning uchun blok ichidagi ikkala qator ham bajarilmaydi."),
    P('a = 2; b = 3; print(a * b)', "23", "5", "a * b"),
    P('jami = (10 +\n        20 +\n        30)\nprint(jami)', "10\n20\n30", "102030", "Xato"),
    P('if True:\nprint("ha")', "ha", "True", "Hech narsa chiqmaydi", why="`if` dan keyingi qator chekinishsiz yozilgan — bu `IndentationError` (u `SyntaxError` turiga kiradi)."),
    Q("Python kod blokini nima bilan belgilaydi?", "Qator boshidagi chekinish (boʻsh joylar)", "Figurali qavslar { }", "begin va end soʻzlari", "Nuqtali vergul ;"),
    Q("Qaysi qator xatoga olib keladi?", "Print(\"Salom\")", "print(\"Salom\")", "print('Salom')", "print( \"Salom\" )", why="Python katta-kichik harfni farqlaydi: funksiya nomi `print`, `Print` emas."),
    PR("Birinchi dastur", "Ekranga aynan `Salom, Mirae Academy!` matnini chiqaring.", 'print("Salom, Mirae Academy!")'),
    PR("Uch qator", "Ekranga uchta qator chiqaring: `Python`, `oson`, `va qiziqarli`.", 'print("Python")\nprint("oson")\nprint("va qiziqarli")'),
    PR("Hisoblash", "Ekranga `125 * 8` ning natijasini chiqaring (faqat son).", "print(125 * 8)"),
    PR("Xatoni tuzating", "Quyidagi kodda chekinish xatosi bor. Uni tuzating: agar son musbat boʻlsa `musbat` deb chiqarsin, oxirida esa har doim `tekshirildi` chiqsin.",
       'son = 7\nif son > 0:\n    print("musbat")\nprint("tekshirildi")',
       starter='son = 7\nif son > 0:\nprint("musbat")\n    print("tekshirildi")\n'),
    PR("Narxlar yigʻindisi", "Doʻkonda uchta mahsulot: 12500, 8300 va 4200 soʻm. Ularning jami narxini bitta `print` bilan chiqaring.", "print(12500 + 8300 + 4200)"),
    PR("Chiroyli chegara", "Ekranga 3 qator chiqaring: `==========`, `  MENYU`, `==========` (ikkinchi qatorda 2 ta boʻsh joy bor).", 'print("==========")\nprint("  MENYU")\nprint("==========")'),
    PR("Ikki son", "Kirishda ikki qator: ikki butun son. Ularning yigʻindisini chiqaring.", "a = int(input())\nb = int(input())\nprint(a + b)", "3\n4", "100\n-25", "0\n0", hint="`int(input())` bilan sonni oʻqing.", starter="a = int(input())\nb = int(input())\n# yigʻindini chiqaring\n"),
    L("exercism", "hello-world"),
    L("acmp", 1, note="Birinchi olimpiada masalasi: ikki sonni qoʻshish."),
    L("exercism", "guidos-gorgeous-lasagna"),
    L("cses", 1068, note="Weird Algorithm — klassik birinchi masala."),
])

# ---------------------------------------------------------------- 2.2
TOPIC("print", "print() — matn va sonlarni chiqarish", "Ekranga maʼlumot chiqarishning barcha usullari", 20, r'''
`print()` — Python'dagi eng koʻp ishlatiladigan funksiya. U qavs ichidagi qiymatni ekranga chiqaradi.

## Matn va sonlar
Matn qoʻshtirnoq ichida yoziladi: `"..."` yoki `'...'` — ikkalasi ham bir xil ishlaydi. Sonlar qoʻshtirnoqsiz yoziladi.

```py
print("Salom!")
print('Bu ham matn')
print(42)
print(3.14)
```

## Bir nechta qiymat
Vergul bilan bir nechta qiymat berish mumkin — ular orasiga avtomatik **boʻsh joy** qoʻyiladi.

```py
print("Yosh:", 17)
print("Narx:", 25000, "soʻm")
print(1, 2, 3)
```

## sep — ajratuvchi
`sep` parametri qiymatlar orasiga nima qoʻyilishini belgilaydi.

```py
print(2026, 10, 13, sep="-")
print("a", "b", "c", sep="")
print("olma", "nok", "uzum", sep=" | ")
```

## end — qator oxiri
Odatda `print` oxirida yangi qatorga oʻtadi. `end` bilan buni oʻzgartirish mumkin.

```py
print("Yuklanmoqda", end="")
print("...", end="")
print(" tayyor!")
```

## Boʻsh print
`print()` — boʻsh qator chiqaradi. Natijani chiroyli koʻrsatish uchun qulay.

```py
print("1-qism")
print()
print("2-qism")
```

## Amaliy misol: chek
```py
print("===== CHEK =====")
print("Non      ", 4000, "soʻm")
print("Sut      ", 12000, "soʻm")
print("Jami:    ", 4000 + 12000, "soʻm")
print("=" * 16)
```

> `"=" * 16` — satrni 16 marta takrorlaydi. Bu haqida satrlar mavzusida batafsil gaplashamiz.

## Esda tuting
- Vergul qoʻyilsa — qiymatlar orasiga boʻsh joy qoʻyiladi.
- `sep` — qiymatlar orasidagi belgi, `end` — oxiridagi belgi.
- `print()` — boʻsh qator.
''', [
    P('print("A", "B", "C")', "ABC", "A,B,C", "A\nB\nC"),
    P('print("A", "B", "C", sep="")', "A B C", "A,B,C", "A\nB\nC"),
    P('print(1, 2, 3, sep="-")', "1 2 3", "-1-2-3-", "123"),
    P('print("Salom", end=" ")\nprint("dunyo")', "Salom\ndunyo", "Salomdunyo", "Salom  dunyo"),
    P('print("a", end="")\nprint("b", end="")\nprint("c")', "a\nb\nc", "a b c", "a b\nc"),
    P('print("Narx:", 5 * 2000)', "Narx: 5 * 2000", "Narx:10000", "Narx: 5 2000"),
    P('print()\nprint("x")', "x", "()\nx", "None\nx"),
    Q("`print(\"a\", \"b\")` nima chiqaradi?", "a b", "ab", "a,b", "a\\nb"),
    Q("Qaysi parametr `print` oxiridagi yangi qatorni oʻzgartiradi?", "end", "sep", "line", "stop"),
    PR("Sana", "`print` va `sep` yordamida ekranga `13.10.2026` chiqaring. Sonlarni alohida qiymat sifatida bering: `13`, `10`, `2026`.", 'print(13, 10, 2026, sep=".")', hint='`sep="."` dan foydalaning.'),
    PR("Bir qatorda", "Ikki xil `print` bilan bitta qatorga `Mirae Academy` chiqaring: birinchisi `Mirae`, ikkinchisi `Academy`.", 'print("Mirae", end=" ")\nprint("Academy")', hint='Birinchi `print` da `end=" "`.'),
    PR("Vergul bilan", "`1`, `2`, `3`, `4`, `5` sonlarini bitta `print` bilan `1, 2, 3, 4, 5` koʻrinishida chiqaring.", 'print(1, 2, 3, 4, 5, sep=", ")'),
    PR("Vizitka", "Ekranga uch qator chiqaring:\n`Ism: Ali`, `Yosh: 17`, `Shahar: Toshkent`. Har bir qatorda vergul bilan ikki qiymat bering (masalan `print(\"Ism:\", \"Ali\")`).", 'print("Ism:", "Ali")\nprint("Yosh:", 17)\nprint("Shahar:", "Toshkent")'),
    PR("Salomlashish", "Kirishda ism beriladi. `Salom, ISM!` koʻrinishida chiqaring (masalan `Salom, Ali!`).", 'ism = input()\nprint("Salom, ", ism, "!", sep="")', "Ali", "Malika", "Bobur", hint='`sep=""` bilan boʻsh joylarni olib tashlang.', starter="ism = input()\n"),
    PR("Jadval qatori", "Kirishda uchta soʻz (har biri alohida qatorda). Ularni bitta qatorda ` | ` bilan ajratib chiqaring.", 'a = input()\nb = input()\nc = input()\nprint(a, b, c, sep=" | ")', "olma\nnok\nuzum", "Toshkent\nSamarqand\nBuxoro", "1\n2\n3", starter="a = input()\nb = input()\nc = input()\n"),
    PR("Hisob-kitob", "Kirishda mahsulot narxi va soni (ikki qator). `Jami: X soʻm` deb chiqaring.", 'narx = int(input())\nson = int(input())\nprint("Jami:", narx * son, "soʻm")', "4000\n3", "12500\n2", "100\n0"),
    L("exercism", "two-fer"),
    L("acmp", 8),
    L("acmp", 21),
    L("cses", 1083),
])

# ---------------------------------------------------------------- 2.3
TOPIC("izohlar", "Izohlar", "Kod ichida tushuntirish yozish", 10, r'''
**Izoh** (comment) — Python bajarmaydigan matn. U kodni oʻqiydigan odam uchun yoziladi: siz uchun, jamoadoshingiz uchun yoki bir oydan keyingi oʻzingiz uchun.

## Bir qatorli izoh
`#` belgisidan keyingi hamma narsa izoh hisoblanadi.

```py
# Bu dastur foydalanuvchini kutib oladi
print("Xush kelibsiz!")  # ekranga salom chiqaramiz
```

## Kodni vaqtincha oʻchirish
Izoh yordamida kod qatorini oʻchirmasdan "oʻchirib qoʻyish" mumkin — xatoni qidirishda juda qulay.

```py
print("1-qadam")
# print("2-qadam")
print("3-qadam")
```

## Koʻp qatorli izoh
Pythonda alohida koʻp qatorli izoh yoʻq. Har qatorga `#` qoʻyiladi. Baʼzan uchta qoʻshtirnoq `"""..."""` ham ishlatiladi — u aslida satr, lekin hech qayerga yozilmagani uchun eʼtiborga olinmaydi.

```py
"""
Muallif: Mirae Academy
Vazifa: chegirmani hisoblash
"""
narx = 100000
chegirma = 15  # foizda
print(narx - narx * chegirma // 100)
```

## Yaxshi izoh qanday boʻladi
- **Nima uchun**ni tushuntiring, **nima**ni emas: `x = x + 1  # x ga 1 qoʻshamiz` — foydasiz izoh.
- Qisqa va aniq yozing.
- Kod oʻzgarsa — izohni ham yangilang.

```py
# Yomon:
soat = 8  # soat 8 ga teng

# Yaxshi:
soat = 8  # ish kuni 8 soat (mehnat kodeksi boʻyicha)
print(soat * 5)
```

## Esda tuting
- `#` dan keyingi matn bajarilmaydi.
- Izoh — kodni tushunarli qilish uchun.
- Qator oʻrtasidagi `#` ham izoh boshlanishi (agar u satr ichida boʻlmasa).
''', [
    P('# print("A")\nprint("B")', "A\nB", "A", "# print(\"A\")\nB"),
    P('print("A")  # print("B")', "A\nB", "A  # print(\"B\")", "B"),
    P('print("Narx # 5000")', "Narx", "Narx # 5000\n5000", "Hech narsa"),
    P('x = 10\n# x = 20\nprint(x)', "20", "x", "Xato"),
    P('"""\nprint(1)\n"""\nprint(2)', "1\n2", "1", "Xato"),
    P('a = 5  # beshta\nb = 3  # uchta\nprint(a - b)', "5 - 3", "a - b", "-2"),
    P('#print("bir")\n#print("ikki")\nprint("uch")', "bir\nikki\nuch", "uch\nikki\nbir", "Hech narsa"),
    Q("Pythonda bir qatorli izoh qaysi belgi bilan boshlanadi?", "#", "//", "--", "/*"),
    Q("Qaysi izoh eng foydali?", "`chegirma = 0.15  # yangi yil aksiyasi, 31-dekabrgacha`", "`chegirma = 0.15  # chegirma`", "`chegirma = 0.15  # 0.15 ga teng`", "`chegirma = 0.15  # oʻzgaruvchi`", why="Yaxshi izoh nima uchun ekanini tushuntiradi."),
    PR("Izohni olib tashlang", "Kodda ikkinchi qator izohga aylantirilgan. Uni qayta yoqing, natijada 3 qator chiqsin: `bir`, `ikki`, `uch`.", 'print("bir")\nprint("ikki")\nprint("uch")', starter='print("bir")\n# print("ikki")\nprint("uch")\n'),
    PR("Ortiqchasini oʻchiring", "Kod 3 qator chiqaradi. Izoh yordamida `XATO` qatorini oʻchirib qoʻying, faqat `Salom` va `Xayr` qolsin.", 'print("Salom")\n# print("XATO")\nprint("Xayr")', starter='print("Salom")\nprint("XATO")\nprint("Xayr")\n'),
    PR("Izohli hisob", "Toʻrtburchakning boʻyi 12, eni 5. Yuzini chiqaring. Har qatorga izoh yozib koʻring (tekshiruvchi faqat natijaga qaraydi).", "boy = 12  # santimetr\neni = 5\nprint(boy * eni)  # yuz"),
    PR("Yashirin matn", "Ekranga aynan `# bu izoh emas` matnini chiqaring.", 'print("# bu izoh emas")', hint="Qoʻshtirnoq ichidagi `#` izoh boshlamaydi."),
    PR("Soatlar", "Kirishda kunlar soni. Shuncha kundagi soatlar sonini chiqaring (1 kun = 24 soat).", "kun = int(input())\nprint(kun * 24)  # 1 kunda 24 soat", "1", "7", "30"),
    PR("Daqiqalar", "Kirishda soat soni. Uni daqiqaga aylantirib chiqaring.", "soat = int(input())\nprint(soat * 60)", "1", "3", "24"),
    PR("Haftalik maosh", "Kirishda kunlik maosh (soʻm). Haftalik (5 ish kuni) maoshni chiqaring.", "kunlik = int(input())\nprint(kunlik * 5)", "150000", "200000", "0"),
    L("exercism", "guidos-gorgeous-lasagna", note="Bu topshiriqda har bir funksiyaga izoh (docstring) yozish ham talab qilinadi."),
    L("acmp", 25),
    L("acmp", 33),
    L("acmp", 61),
])

# ---------------------------------------------------------------- 2.4
TOPIC("ozgaruvchilar", "Oʻzgaruvchilar va nomlash", "Qiymatlarni saqlash, nomlash qoidalari va input()", 20, r'''
**Oʻzgaruvchi** — qiymatga berilgan nom. Uni yorliqli quti deb tasavvur qiling: qutiga qiymat solasiz, keyin nomi orqali undan foydalanasiz.

## Oʻzgaruvchi yaratish
Pythonda oʻzgaruvchini eʼlon qilish shart emas — `=` bilan qiymat berilganda u paydo boʻladi.

```py
ism = "Dilnoza"
yosh = 16
boy = 1.65
print(ism, yosh, boy)
```

> `=` — tenglik emas, **qiymat berish**. `yosh = 16` degani: "yosh nomli qutiga 16 ni sol".

## Qiymatni oʻzgartirish
Oʻzgaruvchi yangi qiymat olishi mumkin — eski qiymat yoʻqoladi.

```py
ball = 70
print(ball)
ball = 85
print(ball)
ball = ball + 10
print(ball)
```

## Nomlash qoidalari
- Harf yoki `_` bilan boshlanadi: `ism`, `_ism`.
- Raqam bilan boshlanmaydi: `2ism` — xato.
- Faqat harf, raqam va `_`: `ism_2` toʻgʻri, `ism-2` xato.
- Katta-kichik harf farqlanadi: `Yosh` va `yosh` — boshqa-boshqa.
- Python soʻzlari (`if`, `for`, `class`...) nom boʻla olmaydi.

## Yaxshi nom tanlash
Pythonda **snake_case** uslubi qabul qilingan: kichik harflar va pastki chiziq.

```py
talaba_ismi = "Bekzod"
oylik_maosh = 4500000
yillik_maosh = oylik_maosh * 12
print(yillik_maosh)
```

!> `a`, `x1`, `qqq` kabi nomlar kodni tushunarsiz qiladi. Nom qiymatning maʼnosini aytsin.

## Foydalanuvchidan maʼlumot olish: input()
`input()` foydalanuvchi yozgan matnni qaytaradi. Uni oʻzgaruvchiga saqlaymiz.

```py input=Sardor
ism = input()
print("Salom,", ism)
```

`input()` har doim **matn** qaytaradi. Son kerak boʻlsa — `int()` bilan aylantiring:

```py input=2009
tugilgan_yil = int(input())
print("Yoshingiz:", 2026 - tugilgan_yil)
```

## Amaliy misol: taksi narxi
```py input=12
masofa = int(input())        # km
boshlangich = 6000           # oʻtirish narxi
km_narxi = 2500
jami = boshlangich + masofa * km_narxi
print("Toʻlov:", jami, "soʻm")
```

## Esda tuting
- `=` — qiymat berish. Oʻng tomon avval hisoblanadi, keyin chap tomonga yoziladi.
- Nom harf yoki `_` bilan boshlanadi, raqam bilan emas.
- `input()` matn qaytaradi; son uchun `int(input())`.
''', [
    P('x = 5\nx = 8\nprint(x)', "5", "5\n8", "13"),
    P('a = 3\nb = a\na = 10\nprint(b)', "10", "13", "a"),
    P('ball = 50\nball = ball + 25\nprint(ball)', "50", "ball + 25", "5025"),
    P('Ism = "Ali"\nism = "Vali"\nprint(Ism)', "Vali", "Ali Vali", "Xato"),
    P('narx = 1500\nson = 4\njami = narx * son\nprint("Jami:", jami)', "Jami: narx * son", "Jami: 15004", "Jami:6000"),
    P('x = 2\ny = x * 3\nx = 100\nprint(y)', "300", "100", "2"),
    P('ism = "Ali"\nprint("ism")', "Ali", "ism Ali", "Xato"),
    Q("Qaysi oʻzgaruvchi nomi notoʻgʻri?", "2-oʻrin", "ikkinchi_orin", "_ikki", "orin2"),
    Q("`input()` qanday turdagi qiymat qaytaradi?", "Har doim satr (str)", "Har doim butun son (int)", "Foydalanuvchi nima yozsa, oʻsha tur", "Mantiqiy qiymat (bool)"),
    PR("Almashtirish", "Kirishda ism. Uni `ism` oʻzgaruvchisiga saqlang va `Salom, ISM` chiqaring (vergul va boʻsh joy bilan).", 'ism = input()\nprint("Salom,", ism)', "Ali", "Madina", "Sherzod"),
    PR("Yosh", "Kirishda tugʻilgan yil. 2026-yildagi yoshni chiqaring.", "yil = int(input())\nprint(2026 - yil)", "2009", "1990", "2026"),
    PR("Doiraning uzunligi", "Kirishda radius (butun son). Aylana uzunligini `2 * 3.14 * r` formula bilan chiqaring.", "r = int(input())\nprint(2 * 3.14 * r)", "1", "5", "10"),
    PR("Chegirma", "Kirishda narx (soʻm). 20% chegirmadan keyingi narxni butun son qilib chiqaring: `narx - narx * 20 // 100`.", "narx = int(input())\nprint(narx - narx * 20 // 100)", "100000", "35000", "999"),
    PR("Oylik toʻlov", "Kirishda telefon narxi va oylar soni (ikki qator). Oylik toʻlovni chiqaring: narx / oylar.", "narx = int(input())\noy = int(input())\nprint(narx / oy)", "3600000\n12", "1000000\n4", "500000\n3"),
    PR("Taksi", "Kirishda masofa (km). Narx: 6000 soʻm oʻtirish + har km uchun 2500 soʻm. Jami narxni chiqaring.", "km = int(input())\nprint(6000 + km * 2500)", "0", "4", "15"),
    PR("Toʻrtburchak", "Kirishda boʻy va en (ikki qator). Avval yuzini, keyin perimetrini alohida qatorlarda chiqaring.", "a = int(input())\nb = int(input())\nprint(a * b)\nprint(2 * (a + b))", "3\n4", "10\n10", "1\n100"),
    L("exercism", "guidos-gorgeous-lasagna"),
    L("acmp", 2),
    L("acmp", 68),
    L("acmp", 106),
])

# ---------------------------------------------------------------- 2.5
TOPIC("kop-qiymat", "Bir nechta qiymat berish", "Bir qatorda bir nechta oʻzgaruvchi va ularni chiqarish", 15, r'''
Python bir qatorda bir nechta oʻzgaruvchiga qiymat berishga imkon beradi. Bu kodni qisqa va tushunarli qiladi.

## Har biriga oʻz qiymati
```py
ism, yosh, shahar = "Laylo", 17, "Namangan"
print(ism)
print(yosh)
print(shahar)
```

!> Chap va oʻng tomondagi elementlar soni teng boʻlishi shart, aks holda `ValueError`.

## Hammasiga bir xil qiymat
```py
a = b = c = 0
print(a, b, c)
```

## Oʻzgaruvchilarni almashtirish
Boshqa tillarda uchinchi oʻzgaruvchi kerak boʻladi. Pythonda — bir qator:

```py
chap, ong = "olma", "nok"
chap, ong = ong, chap
print(chap, ong)
```

## Bir qatorda bir nechta son oʻqish
Olimpiada masalalarida sonlar koʻpincha bitta qatorda boʻsh joy bilan beriladi: `3 7`. Ularni shunday oʻqiymiz:

```py input=3 7
a, b = map(int, input().split())
print(a + b)
```

`input().split()` — satrni boʻsh joylardan boʻladi, `map(int, ...)` — har birini songa aylantiradi. Buni hozircha "andoza" sifatida yodlang, keyinroq har bir qismini oʻrganamiz.

## Oʻzgaruvchilarni chiqarish
```py
mahsulot, narx = "Kitob", 45000
print(mahsulot, "-", narx, "soʻm")
print(mahsulot + " narxi: " + str(narx))
```

> `+` bilan satrga son qoʻshib boʻlmaydi — avval `str()` bilan matnga aylantiring. Vergul bilan esa istalgan turdagi qiymatlarni chiqarish mumkin.

## Amaliy misol: vaqt
```py input=125
daqiqa = int(input())
soat, qoldiq = daqiqa // 60, daqiqa % 60
print(soat, "soat", qoldiq, "daqiqa")
```

## Esda tuting
- `a, b = 1, 2` — har biriga oʻz qiymati; `a = b = 0` — hammasiga bitta.
- `a, b = b, a` — almashtirishning Python usuli.
- `a, b = map(int, input().split())` — bir qatordan ikki son.
''', [
    P('a, b, c = 1, 2, 3\nprint(b)', "1", "3", "1 2 3"),
    P('x = y = 7\ny = 1\nprint(x, y)', "1 1", "7 7", "x y"),
    P('a, b = 5, 9\na, b = b, a\nprint(a, b)', "5 9", "9 9", "5 5"),
    P('a, b = 1, 2\na = b\nb = a\nprint(a, b)', "2 1", "1 2", "1 1", why="`a = b` dan keyin `a` ham 2 boʻladi, eski qiymati yoʻqoladi. Shuning uchun `a, b = b, a` ishlatiladi."),
    P('ism, yosh = "Ali", 20\nprint(ism + " " + str(yosh))', "Ali 20 ", "Ali20", "Xato"),
    P('a, b = "12", "3"\nprint(a + b)', "15", "12 3", "Xato"),
    P('x, y = 1, 2, 3', "1 2", "Hech narsa", "1 2 3", why="Uchta qiymatni ikkita oʻzgaruvchiga berib boʻlmaydi."),
    Q("Ikki oʻzgaruvchini almashtirishning Python usuli qaysi?", "a, b = b, a", "a = b; b = a", "swap(a, b)", "a <-> b"),
    Q("Bir qatordagi `5 8` sonlarini oʻqishning toʻgʻri usuli qaysi?", "a, b = map(int, input().split())", "a, b = int(input())", "a = b = int(input())", "a, b = input(int)"),
    PR("Ikki son yigʻindisi", "Kirishda bitta qatorda ikki son (masalan `3 4`). Yigʻindisini chiqaring.", "a, b = map(int, input().split())\nprint(a + b)", "3 4", "100 -1", "0 0"),
    PR("Almashtiring", "Kirishda bir qatorda ikki soʻz. Ularni almashtirib, teskari tartibda bir qatorda chiqaring.", "a, b = input().split()\na, b = b, a\nprint(a, b)", "olma nok", "salom dunyo", "1 2"),
    PR("Uch son", "Kirishda bir qatorda uch son. Ularning yigʻindisi va koʻpaytmasini alohida qatorlarda chiqaring.", "a, b, c = map(int, input().split())\nprint(a + b + c)\nprint(a * b * c)", "1 2 3", "10 0 5", "-1 -1 -1"),
    PR("Soat va daqiqa", "Kirishda daqiqalar soni. `S soat D daqiqa` koʻrinishida chiqaring.", 'm = int(input())\nprint(m // 60, "soat", m % 60, "daqiqa")', "125", "60", "59"),
    PR("Oʻrtacha ball", "Kirishda bir qatorda 3 ta baho. Oʻrtacha bahoni chiqaring.", "a, b, c = map(int, input().split())\nprint((a + b + c) / 3)", "5 4 3", "5 5 5", "2 3 5"),
    PR("Nol bilan boshlash", "Uchta hisoblagich `qizil`, `sariq`, `yashil` ni bitta qatorda 0 ga tenglashtiring, keyin `sariq` ga kirishdagi sonni qoʻshing va uchalasini bir qatorda chiqaring.", "qizil = sariq = yashil = 0\nsariq = sariq + int(input())\nprint(qizil, sariq, yashil)", "5", "12", "0"),
    PR("Kvadrat", "Kirishda bir qatorda ikki son `a b`. Avval `a` ning kvadratini, keyin `b` ning kvadratini bir qatorda chiqaring.", "a, b = map(int, input().split())\nprint(a * a, b * b)", "2 3", "10 -4", "0 1"),
    L("acmp", 1),
    L("exercism", "locomotive-engineer"),
    L("acmp", 4),
    L("acmp", 81),
])

# ---------------------------------------------------------------- 2.6
TOPIC("global", "Global oʻzgaruvchilar", "Funksiya ichidan va tashqarisidan koʻrinadigan qiymatlar", 15, r'''
Bu mavzuda bizga **funksiya** kerak boʻladi. Funksiyalarni 5-boʻlimda chuqur oʻrganamiz, hozircha shuni bilish yetarli: `def nom():` — kod blokiga nom beradi, `nom()` — uni ishga tushiradi.

```py
def salom():
    print("Salom!")

salom()
salom()
```

## Global oʻzgaruvchi
Funksiyadan **tashqarida** yaratilgan oʻzgaruvchi — **global**. Uni hamma joyda oʻqish mumkin.

```py
maktab = "Mirae Academy"

def tanishtir():
    print("Men", maktab, "talabasiman")

tanishtir()
```

## Lokal oʻzgaruvchi
Funksiya **ichida** yaratilgan oʻzgaruvchi — **lokal**. U faqat funksiya ichida mavjud.

```py
rang = "koʻk"

def boya():
    rang = "qizil"   # bu yangi, lokal oʻzgaruvchi
    print("Ichkarida:", rang)

boya()
print("Tashqarida:", rang)
```

Funksiya ichidagi `rang` — butunlay boshqa oʻzgaruvchi. Global `rang` oʻzgarmadi.

## global kalit soʻzi
Funksiya ichidan global oʻzgaruvchini **oʻzgartirish** uchun `global` deb eʼlon qilinadi:

```py
hisob = 0

def bosish():
    global hisob
    hisob = hisob + 1

bosish()
bosish()
bosish()
print("Tugma bosildi:", hisob, "marta")
```

!> `global` ni koʻp ishlatish kodni chalkashtiradi: qiymatni kim oʻzgartirgani nomaʼlum boʻlib qoladi. Funksiya natijani `return` bilan qaytargani yaxshiroq (5-boʻlimda).

## Esda tuting
- Funksiyadan tashqaridagi — global, ichidagi — lokal.
- Global oʻzgaruvchini oʻqish mumkin, oʻzgartirish uchun `global` kerak.
- Lokal oʻzgaruvchi funksiyadan tashqarida koʻrinmaydi.
''', [
    P('x = 5\ndef f():\n    print(x)\nf()', "Xato", "0", "x"),
    P('x = 5\ndef f():\n    x = 9\nf()\nprint(x)', "9", "5\n9", "Xato"),
    P('x = 5\ndef f():\n    global x\n    x = 9\nf()\nprint(x)', "5", "5\n9", "Xato"),
    P('n = 0\ndef qosh():\n    global n\n    n = n + 2\nqosh()\nqosh()\nprint(n)', "2", "0", "Xato"),
    P('def f():\n    y = 3\nf()\nprint(y)', "3", "None", "0", why="`y` faqat funksiya ichida mavjud — tashqarida `NameError`."),
    P('a = 1\ndef f():\n    a = 2\n    print(a)\nf()\nprint(a)', "2\n2", "1\n1", "1\n2"),
    P('ism = "Ali"\ndef salom():\n    print("Salom,", ism)\nism = "Vali"\nsalom()', "Salom, Ali", "Salom, ism", "Xato", why="Funksiya chaqirilgan paytdagi qiymat ishlatiladi — u paytda `ism` allaqachon `Vali`."),
    Q("Funksiya ichida global oʻzgaruvchini oʻzgartirish uchun nima yoziladi?", "global nom", "nonlocal nom", "public nom", "extern nom"),
    Q("Funksiya ichida yaratilgan oʻzgaruvchi qayerda koʻrinadi?", "Faqat shu funksiya ichida", "Hamma joyda", "Faqat funksiyadan keyin", "Faqat boshqa funksiyalarda"),
    PR("Salomlashuvchi funksiya", "`salom()` funksiyasini yozing: u `Assalomu alaykum!` chiqarsin. Uni 2 marta chaqiring.", 'def salom():\n    print("Assalomu alaykum!")\n\nsalom()\nsalom()', starter="def salom():\n    pass\n\n# funksiyani 2 marta chaqiring\n"),
    PR("Global sanagich", "`sanoq = 0` global oʻzgaruvchisi bor. `oshir()` funksiyasi uni 1 ga oshirsin. Kirishda son n — funksiyani n marta chaqiring (`for` bilan) va oxirida `sanoq` ni chiqaring.", "sanoq = 0\n\ndef oshir():\n    global sanoq\n    sanoq = sanoq + 1\n\nn = int(input())\nfor _ in range(n):\n    oshir()\nprint(sanoq)", "3", "0", "10", starter="sanoq = 0\n\ndef oshir():\n    pass\n\nn = int(input())\nfor _ in range(n):\n    oshir()\nprint(sanoq)\n", hint="Funksiya ichida `global sanoq` yozing."),
    PR("Lokalni tekshiring", "Kod `100` chiqarishi kerak, lekin hozir `0` chiqaryapti. Faqat bitta qator qoʻshib tuzating.", "ball = 0\n\ndef yangila():\n    global ball\n    ball = 100\n\nyangila()\nprint(ball)", starter="ball = 0\n\ndef yangila():\n    ball = 100\n\nyangila()\nprint(ball)\n"),
    PR("Hisob raqam", "`balans = 50000`. `toldir()` funksiyasi balansga 25000 qoʻshadi. Uni uch marta chaqirib, balansni chiqaring.", "balans = 50000\n\ndef toldir():\n    global balans\n    balans = balans + 25000\n\ntoldir()\ntoldir()\ntoldir()\nprint(balans)", starter="balans = 50000\n\ndef toldir():\n    pass\n\ntoldir()\ntoldir()\ntoldir()\nprint(balans)\n"),
    PR("Sozlama", "Global `til = \"uz\"`. `ingliz()` funksiyasi tilni `\"en\"` ga oʻzgartirsin. Avval tilni chiqaring, keyin funksiyani chaqirib, yana chiqaring.", 'til = "uz"\n\ndef ingliz():\n    global til\n    til = "en"\n\nprint(til)\ningliz()\nprint(til)', starter='til = "uz"\n\ndef ingliz():\n    pass\n\nprint(til)\ningliz()\nprint(til)\n'),
    PR("Ikki sanagich", "`a = 0`, `b = 0`. Kirishda son n. `qadam()` funksiyasi `a` ni 1 ga, `b` ni 2 ga oshirsin. Uni n marta chaqirib, `a b` ni chiqaring.", "a = 0\nb = 0\n\ndef qadam():\n    global a, b\n    a = a + 1\n    b = b + 2\n\nn = int(input())\nfor _ in range(n):\n    qadam()\nprint(a, b)", "1", "5", "0", starter="a = 0\nb = 0\n\ndef qadam():\n    pass\n\nn = int(input())\nfor _ in range(n):\n    qadam()\nprint(a, b)\n", hint="`global a, b` — bir nechtasini birga eʼlon qilish mumkin."),
    PR("Narx funksiyasi", "Global `kurs = 12800` (1 dollar soʻmda). Kirishda dollar miqdori. `hisobla()` funksiyasi ichida `kurs` ni oʻqib, soʻmdagi summani chiqarsin.", "kurs = 12800\n\ndef hisobla(d):\n    print(d * kurs)\n\nhisobla(int(input()))", "1", "10", "250", starter="kurs = 12800\n\ndef hisobla(d):\n    pass\n\nhisobla(int(input()))\n"),
    L("exercism", "two-fer"),
    L("exercism", "guidos-gorgeous-lasagna"),
    L("acmp", 293),
    L("acmp", 336),
])

# ---------------------------------------------------------------- 2.7
TOPIC("turlar", "Maʼlumot turlari", "int, float, str, bool, list, dict… va type()", 20, r'''
Har bir qiymatning **turi** bor. Tur qiymat bilan qanday amallar qilish mumkinligini belgilaydi: sonlarni qoʻshish mumkin, satrlarni esa katta harfga aylantirish mumkin.

## Asosiy turlar
| Tur | Nomi | Misol |
|---|---|---|
| `int` | butun son | `42`, `-7` |
| `float` | kasr son | `3.14`, `-0.5` |
| `str` | satr (matn) | `"salom"` |
| `bool` | mantiqiy | `True`, `False` |
| `list` | roʻyxat | `[1, 2, 3]` |
| `tuple` | kortej | `(1, 2)` |
| `dict` | lugʻat | `{"ism": "Ali"}` |
| `set` | toʻplam | `{1, 2, 3}` |
| `NoneType` | "hech narsa" | `None` |

## type() — turni bilish
```py
print(type(42))
print(type(3.14))
print(type("salom"))
print(type(True))
print(type([1, 2]))
print(type(None))
```

## Tur avtomatik aniqlanadi
Pythonda turni yozish shart emas — u qiymatdan aniqlanadi. Bitta oʻzgaruvchi turli vaqtda turli turdagi qiymat saqlashi mumkin.

```py
x = 10
print(type(x))
x = "oʻn"
print(type(x))
```

## Tur nima uchun muhim
```py
print(5 + 5)
print("5" + "5")
print("5" * 3)
```

Bir xil `+` belgisi sonlarda qoʻshadi, satrlarda esa yopishtiradi. Turni bilmasangiz — natija kutilmagan boʻladi.

!> Soni va satrni `+` bilan qoʻshib boʻlmaydi: `"Yosh: " + 17` — `TypeError`.

## isinstance() — tekshirish
```py
yosh = 17
print(isinstance(yosh, int))
print(isinstance(yosh, str))
```

## Esda tuting
- `type(x)` — turini koʻrsatadi.
- `5` — int, `5.0` — float, `"5"` — str: uchtasi uch xil narsa.
- Amallar turga bogʻliq: `"5" * 3` → `555`.
''', [
    P('print(type(7))', "<class 'float'>", "int", "<class 'str'>"),
    P('print(type(7.0))', "<class 'int'>", "float", "<class 'str'>"),
    P('print(type("7"))', "<class 'int'>", "str", "<class 'float'>"),
    P('print("3" * 4)', "12", "3 3 3 3", "Xato"),
    P('print(5 + 5, "5" + "5")', "10 10", "55 55", "10 5 5"),
    P('x = True\nprint(type(x))', "<class 'str'>", "<class 'int'>", "True"),
    P('print("Yosh: " + 17)', "Yosh: 17", "Yosh: + 17", "Yosh:17"),
    Q("`[1, 2, 3]` qaysi turga kiradi?", "list", "tuple", "set", "dict"),
    Q("Qaysi qiymat `float` turida?", "2.5", "\"2.5\"", "25", "True"),
    PR("Tur nomi", "Kirishda matn beriladi. `type()` yordamida uning turini chiqaring.", "s = input()\nprint(type(s))", "salom", "123", "3.5", hint="`input()` har doim satr qaytaradi."),
    PR("Butun sonmi?", "Kirishda butun son. `int()` bilan aylantirib, natija turini chiqaring.", "x = int(input())\nprint(type(x))", "5", "-12", "0"),
    PR("Uch tur", "Uch qator chiqaring: `42` ning turi, `4.2` ning turi va `\"42\"` ning turi.", 'print(type(42))\nprint(type(4.2))\nprint(type("42"))'),
    PR("Yopishtirish yoki qoʻshish", "Kirishda ikki qator — ikki son. Avval ularni satr sifatida yopishtirib chiqaring, keyin son sifatida qoʻshib chiqaring.", "a = input()\nb = input()\nprint(a + b)\nprint(int(a) + int(b))", "2\n3", "10\n20", "7\n0"),
    PR("Takrorlash", "Kirishda belgi va son (ikki qator). Belgini shuncha marta takrorlab chiqaring.", "s = input()\nn = int(input())\nprint(s * n)", "*\n5", "ab\n3", "-\n10"),
    PR("isinstance", "Kirishda son. Uni `float` ga aylantiring va `isinstance(x, float)` natijasini chiqaring.", "x = float(input())\nprint(isinstance(x, float))", "3", "2.5", "-1"),
    PR("Yosh xabari", "Kirishda yosh (son). `Siz X yoshdasiz` deb chiqaring — faqat `+` bilan yopishtirib (`str()` dan foydalaning).", 'y = int(input())\nprint("Siz " + str(y) + " yoshdasiz")', "17", "5", "60"),
    L("exercism", "ghost-gobble-arcade-game"),
    L("exercism", "currency-exchange"),
    L("acmp", 46),
    L("acmp", 103, note="Python cheksiz katta sonlar bilan ishlaydi — bu masala buni koʻrsatadi."),
])

# ---------------------------------------------------------------- 2.8
TOPIC("casting", "Turlarni oʻzgartirish", "int(), float(), str() va bool() bilan aylantirish", 20, r'''
Koʻpincha bir turdagi qiymatni boshqasiga aylantirish kerak boʻladi: `input()` dan kelgan matnni songa, sonni matnga. Bu **casting** (tur almashtirish) deyiladi.

## int() — butun songa
```py
print(int("42"))
print(int(3.99))
print(int(-2.7))
print(int(True))
```

!> `int(3.99)` — `3`. U yaxlitlamaydi, kasr qismini **tashlab yuboradi**.

## float() — kasr songa
```py
print(float("3.5"))
print(float(7))
print(float("1e3"))
```

## str() — satrga
```py
narx = 25000
xabar = "Narx: " + str(narx) + " soʻm"
print(xabar)
```

## bool() — mantiqiy qiymatga
"Boʻsh" qiymatlar `False`, qolganlari `True`:

```py
print(bool(0), bool(""), bool(None))
print(bool(5), bool("a"), bool(-1))
```

## Xato aylantirish
Hamma narsani aylantirib boʻlmaydi:

```py xato
print(int("salom"))
```

```py xato
print(int("3.5"))
```

`int("3.5")` ham xato beradi — avval `float`, keyin `int`: `int(float("3.5"))`.

## round() — yaxlitlash
```py
print(round(3.7))
print(round(2.345, 2))
print(round(1234.5678, -2))
```

## Amaliy misol: oʻrtacha baho
```py input=5|4|5
a = int(input())
b = int(input())
c = int(input())
ortacha = (a + b + c) / 3
print("Oʻrtacha:", round(ortacha, 2))
```

## Esda tuting
- `int()` kasrni tashlaydi, `round()` yaxlitlaydi.
- `int("3.5")` — xato; `int(float("3.5"))` — 3.
- `0`, `""`, `None` → `False`; qolganlari → `True`.
''', [
    P('print(int(7.9))', "8", "7.9", "Xato"),
    P('print(round(7.9))', "7", "7.9", "7.0"),
    P('print(float(5))', "5", "5.00", "Xato"),
    P('print(int("12") + 3)', "123", "12 3", "Xato"),
    P('print(str(12) + "3")', "15", "12 3", "Xato"),
    P('print(bool(""), bool(" "))', "False False", "True True", "True False"),
    P('print(int(float("2.75")))', "3", "2.75", "Xato"),
    Q("`int(\"3.5\")` nima qaytaradi?", "ValueError xatosi", "3", "4", "3.5"),
    Q("Qaysi qiymat `bool()` da `False` beradi?", "0", "-1", "\"0\"", "[0]", why="`\"0\"` — boʻsh boʻlmagan satr, `[0]` — boʻsh boʻlmagan roʻyxat; ular `True`."),
    PR("Kasr qismini tashlash", "Kirishda kasr son. Uning butun qismini `int()` bilan chiqaring.", "x = float(input())\nprint(int(x))", "3.75", "10.01", "-2.5"),
    PR("Yaxlitlash", "Kirishda kasr son. Uni 2 xonagacha yaxlitlab chiqaring.", "x = float(input())\nprint(round(x, 2))", "3.14159", "2.005", "10"),
    PR("Kilogramm", "Kirishda gramm (butun son). Kilogrammni kasr son sifatida chiqaring.", "g = int(input())\nprint(g / 1000)", "1500", "250", "1000"),
    PR("Narx matni", "Kirishda narx. Faqat `+` bilan `Narxi: X soʻm` satrini yasab chiqaring.", 'n = int(input())\nprint("Narxi: " + str(n) + " soʻm")', "5000", "123456", "0"),
    PR("Boʻshmi?", "Kirishda bir qator. Agar u boʻsh boʻlmasa `True`, boʻsh boʻlsa `False` chiqaring (`bool()` bilan).", "s = input()\nprint(bool(s))", "salom", "", " "),
    PR("Harorat", "Kirishda Selsiy harorati (kasr boʻlishi mumkin). Farengeytga aylantiring (`C * 9 / 5 + 32`) va 1 xonagacha yaxlitlab chiqaring.", "c = float(input())\nprint(round(c * 9 / 5 + 32, 1))", "36.6", "0", "-40"),
    PR("Raqamlar yigʻindisi", "Kirishda uch xonali son. Uning raqamlari yigʻindisini chiqaring. Maslahat: sonni satr deb oʻqing va har bir belgini `int()` qiling.", "s = input()\nprint(int(s[0]) + int(s[1]) + int(s[2]))", "123", "999", "105"),
    L("exercism", "currency-exchange"),
    L("lc", "convert-the-temperature"),
    L("acmp", 45),
    L("acmp", 109),
])

# ---------------------------------------------------------------- 2.9
TOPIC("sonlar", "Sonlar: int, float, complex", "Butun, kasr va kompleks sonlar bilan ishlash", 20, r'''
Pythonda uch xil son turi bor: **int** (butun), **float** (kasr) va **complex** (kompleks).

## int — cheksiz katta butun sonlar
Pythonda butun sonlar chegaralanmagan. Bu olimpiadada katta qulaylik.

```py
print(2 ** 100)
print(12345678901234567890 * 98765432109876543210)
```

Katta sonlarni oʻqish oson boʻlishi uchun `_` qoʻyish mumkin:

```py
aholi = 37_000_000
print(aholi)
```

## float — kasr sonlar
```py
print(7 / 2)
print(0.1 + 0.2)
print(1.5e6)
```

!> `0.1 + 0.2` aniq `0.3` emas! Kompyuter kasrlarni ikkilik tizimda saqlaydi — kichik xatolik boʻladi. Pulni hisoblashda kasr oʻrniga tiyin/soʻmda butun son ishlating.

## Boʻlish turlari
| Amal | Maʼnosi | `17` va `5` |
|---|---|---|
| `/` | oddiy boʻlish | `3.4` |
| `//` | butun boʻlish | `3` |
| `%` | qoldiq | `2` |
| `**` | daraja | `1419857` |

```py
print(17 / 5, 17 // 5, 17 % 5)
print(-7 // 2, -7 % 2)
```

## Foydali funksiyalar
```py
print(abs(-12))
print(max(3, 9, 4), min(3, 9, 4))
print(pow(2, 10))
print(divmod(17, 5))
```

## math moduli
```py
import math
print(math.sqrt(144))
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))
print(math.gcd(12, 18))
```

## complex — kompleks sonlar
Kompleks son: haqiqiy va mavhum qism. Mavhum qism `j` bilan yoziladi.

```py
z = 3 + 4j
print(z.real, z.imag)
print(abs(z))
```

## Amaliy misol: oxirgi raqam va raqamlar soni
```py input=2026
n = int(input())
print("Oxirgi raqam:", n % 10)
print("Raqamlar soni:", len(str(n)))
print("Juftmi:", n % 2 == 0)
```

## Esda tuting
- `/` har doim float qaytaradi, `//` — butun boʻlish, `%` — qoldiq.
- `n % 10` — oxirgi raqam, `n // 10` — oxirgi raqamsiz son.
- `0.1 + 0.2 != 0.3` — kasrlarni `==` bilan solishtirmang.
''', [
    P('print(17 // 5)', "3.4", "2", "4"),
    P('print(17 % 5)', "3", "3.4", "0"),
    P('print(10 / 2)', "5", "5.00", "2"),
    P('print(2 ** 3 ** 2)', "64", "36", "12", why="`**` oʻngdan chapga hisoblanadi: `3 ** 2 = 9`, keyin `2 ** 9 = 512`."),
    P('print(-7 // 2)', "-3", "-3.5", "3"),
    P('print(abs(-5) + abs(3))', "-2", "2", "-8"),
    P('print(1234 % 10, 1234 // 10)', "4 1234", "123 4", "1 234"),
    Q("`0.1 + 0.2 == 0.3` natijasi qanday?", "False", "True", "Xato", "0.3"),
    Q("Sonning oxirgi raqamini qanday olish mumkin?", "n % 10", "n // 10", "n / 10", "n ** 10"),
    PR("Oxirgi raqam", "Kirishda natural son. Uning oxirgi raqamini chiqaring.", "n = int(input())\nprint(n % 10)", "2026", "7", "1000"),
    PR("Juft yoki toq", "Kirishda butun son. Agar juft boʻlsa `0`, toq boʻlsa `1` chiqaring (faqat `%` bilan).", "n = int(input())\nprint(n % 2)", "4", "7", "0"),
    PR("Katta daraja", "Kirishda n. `2` ning `n`-darajasini chiqaring.", "n = int(input())\nprint(2 ** n)", "10", "64", "100"),
    PR("Gipotenuza", "Kirishda katetlar `a` va `b` (bir qatorda). Gipotenuzani `math.sqrt` bilan hisoblab chiqaring.", "import math\na, b = map(int, input().split())\nprint(math.sqrt(a * a + b * b))", "3 4", "5 12", "1 1"),
    PR("Avtobuslar", "Kirishda yoʻlovchilar soni va bitta avtobus sigʻimi (bir qatorda). Nechta avtobus kerakligini chiqaring.", "n, k = map(int, input().split())\nprint((n + k - 1) // k)", "100 30", "60 30", "1 50", hint="Butun boʻlishni yuqoriga yaxlitlash: `(n + k - 1) // k`."),
    PR("Daqiqa va soniya", "Kirishda soniyalar. `M daqiqa S soniya` deb chiqaring (`divmod` dan foydalanib koʻring).", 'm, s = divmod(int(input()), 60)\nprint(m, "daqiqa", s, "soniya")', "125", "59", "3600"),
    PR("EKUB", "Kirishda ikki son (bir qatorda). Ularning eng katta umumiy boʻluvchisini chiqaring.", "import math\na, b = map(int, input().split())\nprint(math.gcd(a, b))", "12 18", "7 13", "100 75"),
    L("exercism", "grains"),
    L("lc", "add-digits"),
    L("acmp", 14),
    L("acmp", 79),
])

# ---------------------------------------------------------------- 2.10
TOPIC("bool-none", "Mantiqiy qiymatlar va None", "True, False va “hech narsa” qiymati", 15, r'''
**bool** turida faqat ikki qiymat bor: `True` (rost) va `False` (yolgʻon). Ular har bir qarorning asosi: "parol toʻgʻrimi?", "yosh 18 dan kattami?".

## Taqqoslash natijasi — bool
```py
yosh = 17
print(yosh >= 18)
print(yosh == 17)
print(type(yosh > 5))
```

## True va False — aslida sonlar
`True` — 1 ga, `False` — 0 ga teng. Shuning uchun ularni qoʻshish mumkin:

```py
print(True + True + False)
javoblar = [True, False, True, True]
print("Toʻgʻri javoblar:", sum(javoblar))
```

## Rost-yolgʻon qiymatlar (truthy / falsy)
Har qanday qiymat `if` da rost yoki yolgʻon sifatida qaraladi. **Yolgʻon** hisoblanadiganlar: `False`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, `None`. Qolganlari — rost.

```py
ism = ""
if ism:
    print("Salom,", ism)
else:
    print("Ism kiritilmadi")
```

## None — "hech narsa"
`None` — qiymat yoʻqligini bildiradi. U `0` ham, `""` ham emas.

```py
natija = None
print(natija)
print(type(natija))
print(natija is None)
```

> `None` ni tekshirishda `==` emas, `is` ishlatiladi: `x is None`.

Funksiya hech narsa qaytarmasa, u `None` qaytaradi:

```py
def salom():
    print("Salom")

javob = salom()
print(javob)
```

## Amaliy misol
```py input=25
harorat = int(input())
issiq = harorat > 30
sovuq = harorat < 10
print("Issiqmi:", issiq)
print("Sovuqmi:", sovuq)
print("Yoqimli:", not issiq and not sovuq)
```

## Esda tuting
- Taqqoslash har doim `True` yoki `False` qaytaradi.
- `0`, `""`, `[]`, `None` — yolgʻon; qolganlari — rost.
- `None` ni `is None` bilan tekshiring.
''', [
    P('print(5 > 3)', "5 > 3", "1", "true"),
    P('print(True + True)', "TrueTrue", "True", "Xato"),
    P('print(bool([]), bool([0]))', "False False", "True True", "True False"),
    P('x = None\nprint(x is None)', "None", "False", "Xato"),
    P('print(10 == 10.0)', "False", "Xato", "10"),
    P('def f():\n    pass\nprint(f())', "pass", "0", "Hech narsa"),
    P('print(sum([True, True, False, True]))', "True", "4", "TrueTrueFalseTrue"),
    Q("Qaysi qiymat `if` da yolgʻon (False) hisoblanadi?", "\"\"", "\" \"", "\"False\"", "-1"),
    Q("`None` ni tekshirishning eng toʻgʻri usuli qaysi?", "x is None", "x == 0", "x == \"\"", "not x", why="`not x` — 0 va boʻsh satr uchun ham True boʻladi, shuning uchun aniq emas."),
    PR("Kattami?", "Kirishda yosh. `yosh >= 18` natijasini chiqaring.", "y = int(input())\nprint(y >= 18)", "17", "18", "40"),
    PR("Juftmi?", "Kirishda son. Juft boʻlsa `True`, aks holda `False` chiqaring.", "n = int(input())\nprint(n % 2 == 0)", "4", "7", "0"),
    PR("Toʻgʻri javoblar", "Kirishda 5 ta soʻz (bir qatorda): `ha` yoki `yoq`. Nechta `ha` borligini chiqaring. Har birini `== \"ha\"` bilan bool qiling va `sum` dan foydalaning.", 'javob = input().split()\nprint(sum(x == "ha" for x in javob))', "ha yoq ha ha yoq", "yoq yoq yoq yoq yoq", "ha ha ha ha ha", hint='`sum(x == "ha" for x in javob)` — har bir True 1 ga teng.'),
    PR("Ism bormi", "Kirishda bir qator (boʻsh boʻlishi mumkin). Agar boʻsh boʻlmasa `Salom, ISM`, boʻsh boʻlsa `Mehmon` chiqaring.", 'ism = input()\nif ism:\n    print("Salom,", ism)\nelse:\n    print("Mehmon")', "Ali", "", "Zarina"),
    PR("Oraliqda", "Kirishda son. U 1 dan 100 gacha (ikkalasi ham kiradi) boʻlsa `True`, aks holda `False`.", "n = int(input())\nprint(1 <= n <= 100)", "50", "0", "100"),
    PR("Kabisa yili", "Kirishda yil. U kabisa boʻlsa `True` chiqaring: 4 ga boʻlinadi va 100 ga boʻlinmaydi, yoki 400 ga boʻlinadi.", "y = int(input())\nprint(y % 4 == 0 and y % 100 != 0 or y % 400 == 0)", "2024", "1900", "2000"),
    PR("None bilan", "Kirishda soʻz. Agar soʻz `yoq` boʻlsa `natija = None`, aks holda `natija = soʻz`. Keyin `natija is None` ni chiqaring.", 's = input()\nnatija = None if s == "yoq" else s\nprint(natija is None)', "yoq", "bor", "Yoq"),
    L("exercism", "ghost-gobble-arcade-game"),
    L("exercism", "leap"),
    L("lc", "power-of-two"),
    L("acmp", 25),
])

# ---------------------------------------------------------------- 2.11
TOPIC("satrlar", "Satrlar asoslari", "Matn bilan ishlash: indeks, uzunlik, oʻzgarmaslik", 20, r'''
**Satr** (string, `str`) — belgilar ketma-ketligi. Ism, xabar, parol, fayl nomi — hammasi satr.

## Satr yaratish
```py
a = "Salom"
b = 'Python'
c = """Bir necha
qatorli matn"""
print(a, b)
print(c)
```

## Uzunlik: len()
```py
soz = "Toshkent"
print(len(soz))
print(len(""))
```

## Indekslar
Har bir belgining tartib raqami — **indeksi** bor. Sanash **0** dan boshlanadi. Manfiy indeks oxiridan sanaydi.

```py
s = "PYTHON"
print(s[0], s[1], s[5])
print(s[-1], s[-2])
```

| Belgi | P | Y | T | H | O | N |
|---|---|---|---|---|---|---|
| Indeks | 0 | 1 | 2 | 3 | 4 | 5 |
| Manfiy | -6 | -5 | -4 | -3 | -2 | -1 |

!> Mavjud boʻlmagan indeks — `IndexError`: `"abc"[5]`.

## Satrlar oʻzgarmas
Satrni joyida oʻzgartirib boʻlmaydi. Yangi satr yaratish kerak:

```py xato
s = "salom"
s[0] = "S"
```

```py
s = "salom"
s = "S" + s[1:]
print(s)
```

## in — ichida bormi
```py
xabar = "Bugun dars soat 15:00 da"
print("dars" in xabar)
print("imtihon" in xabar)
```

## Satr boʻylab yurish
```py
for harf in "OLMA":
    print(harf)
```

## Amaliy misol: unli harflarni sanash
```py input=Assalomu alaykum
matn = input().lower()
unlilar = 0
for h in matn:
    if h in "aeiou":
        unlilar += 1
print("Unli harflar:", unlilar)
```

## Esda tuting
- Indeks 0 dan boshlanadi; `s[-1]` — oxirgi belgi.
- `len(s)` — uzunlik; oxirgi indeks `len(s) - 1`.
- Satr oʻzgarmas — `s[0] = ...` ishlamaydi.
''', [
    P('s = "Python"\nprint(s[0], s[-1])', "P N", "y o", "P o"),
    P('print(len("Mirae"))', "4", "6", "Mirae"),
    P('s = "salom"\nprint(s[1] + s[3])', "so", "al", "sl"),
    P('print("o" in "Toshkent")', "False", "1", "o"),
    P('s = "abc"\nprint(s[3])', "c", "Hech narsa", "abc"),
    P('print(len("a b"))', "2", "1", "a b"),
    P('for h in "ABC":\n    print(h, end="-")', "A-B-C", "ABC-", "A\nB\nC"),
    Q("`s = \"KITOB\"` boʻlsa, `s[-2]` nima?", "O", "T", "B", "I"),
    Q("Nima uchun `s[0] = \"X\"` xato beradi?", "Satrlar oʻzgarmas (immutable)", "Indeks 0 mavjud emas", "Satrga faqat son yozish mumkin", "Qoʻshtirnoq notoʻgʻri"),
    PR("Birinchi va oxirgi", "Kirishda soʻz. Birinchi va oxirgi harfini boʻsh joy bilan chiqaring.", "s = input()\nprint(s[0], s[-1])", "Python", "a", "Samarqand"),
    PR("Uzunlik", "Kirishda matn. Uning uzunligini chiqaring.", "print(len(input()))", "salom", "Mirae Academy", "x"),
    PR("Bormi?", "Kirishda ikki qator: matn va soʻz. Soʻz matnda bor boʻlsa `True`, aks holda `False`.", "matn = input()\nsoz = input()\nprint(soz in matn)", "bugun havo issiq\nhavo", "salom dunyo\nxayr", "abc\nabc"),
    PR("Harflab", "Kirishda soʻz. Har bir harfini alohida qatorda chiqaring.", "for h in input():\n    print(h)", "olma", "Py", "x"),
    PR("Bosh harf", "Kirishda kichik harfli soʻz. Birinchi harfini katta qilib, butun soʻzni chiqaring (`upper()` faqat bitta harfga).", "s = input()\nprint(s[0].upper() + s[1:])", "toshkent", "ali", "x"),
    PR("Unli harflar", "Kirishda matn (kichik harflarda). `aeiou` harflari sonini chiqaring.", 's = input()\nn = 0\nfor h in s:\n    if h in "aeiou":\n        n += 1\nprint(n)', "assalomu alaykum", "python", "aeiou"),
    PR("Oʻrtadagi harf", "Kirishda toq uzunlikdagi soʻz. Oʻrtadagi harfini chiqaring.", "s = input()\nprint(s[len(s) // 2])", "salom", "abc", "x"),
    L("exercism", "little-sisters-vocab"),
    L("lc", "length-of-last-word"),
    L("lc", "jewels-and-stones"),
    L("acmp", 50),
])

# ---------------------------------------------------------------- 2.12
TOPIC("kesish", "Kesish (slicing)", "Satrdan istalgan qismni olish: s[boshi:oxiri:qadam]", 20, r'''
**Kesish** (slicing) — satrdan bir boʻlakni olish. Sintaksis: `s[boshi:oxiri:qadam]`.

- `boshi` — qayerdan (shu indeks **kiradi**),
- `oxiri` — qayergacha (shu indeks **kirmaydi**),
- `qadam` — nechtadan sakrab.

## Oddiy kesish
```py
s = "MIRAE ACADEMY"
print(s[0:5])
print(s[6:13])
print(s[2:4])
```

## Boshini yoki oxirini tashlab ketish
```py
s = "PYTHON"
print(s[:3])
print(s[3:])
print(s[:])
```

## Manfiy indekslar bilan
```py
fayl = "hisobot.pdf"
print(fayl[-3:])
print(fayl[:-4])
```

## Qadam
```py
s = "0123456789"
print(s[::2])
print(s[1::2])
print(s[::3])
```

## Teskari aylantirish
Qadam `-1` boʻlsa, satr teskari oʻqiladi — eng mashhur Python "hiylasi":

```py
print("salom"[::-1])
soz = "kiyik"
print(soz == soz[::-1])
```

> Kesish hech qachon `IndexError` bermaydi: `"abc"[1:100]` — shunchaki `"bc"`.

## Amaliy misol: telefon raqami
```py input=+998901234567
tel = input()
kod = tel[4:6]
raqam = tel[6:]
print("Operator kodi:", kod)
print("Yashirin:", tel[:6] + "*****" + tel[-2:])
```

## Esda tuting
- `s[a:b]` — `a` kiradi, `b` kirmaydi; uzunligi `b - a`.
- `s[:n]` — dastlabki n ta, `s[-n:]` — oxirgi n ta.
- `s[::-1]` — teskari satr.
''', [
    P('s = "Python"\nprint(s[1:4])', "Pyth", "ytho", "Pyt"),
    P('s = "Python"\nprint(s[:2] + s[-2:])', "Pyth", "Pyhon", "Pyto"),
    P('print("salom"[::-1])', "salom", "molaS", "s"),
    P('print("0123456789"[::3])', "0123", "369", "036"),
    P('print("abc"[1:100])', "Xato", "abc", "c"),
    P('s = "hisobot.pdf"\nprint(s[-3:])', ".pdf", "hisobot", "pd"),
    P('print("abcdef"[4:1])', "dcb", "edc", "Xato", why="Qadam musbat va boshi oxiridan katta — natija boʻsh satr."),
    Q("`s = \"TOSHKENT\"` dan `TOSH` ni qanday olish mumkin?", "s[:4]", "s[0:3]", "s[1:5]", "s[4:]"),
    Q("Soʻz palindrom ekanini qaysi ifoda tekshiradi?", "s == s[::-1]", "s == s[-1]", "s == s[::2]", "s[0] == s[1]"),
    PR("Teskari", "Kirishda soʻz. Uni teskari tartibda chiqaring.", "print(input()[::-1])", "salom", "Python", "a"),
    PR("Palindrom", "Kirishda soʻz. Palindrom boʻlsa `ha`, aks holda `yoq` chiqaring.", 's = input()\nif s == s[::-1]:\n    print("ha")\nelse:\n    print("yoq")', "kiyik", "olma", "a"),
    PR("Fayl kengaytmasi", "Kirishda fayl nomi (masalan `rasm.png`). Oxirgi 3 belgini chiqaring.", "print(input()[-3:])", "rasm.png", "hisobot.pdf", "kod.py "),
    PR("Juft oʻrinlar", "Kirishda soʻz. Faqat juft indeksdagi (0, 2, 4...) harflarni chiqaring.", "print(input()[::2])", "abcdef", "Python", "x"),
    PR("Yashirin raqam", "Kirishda karta raqami (16 ta raqam). Dastlabki 4 va oxirgi 4 raqamni qoldirib, oʻrtasini 8 ta `*` bilan almashtiring.", 's = input()\nprint(s[:4] + "*" * 8 + s[-4:])', "8600123456789012", "1111222233334444", "9860000000001234"),
    PR("Ikki yarim", "Kirishda juft uzunlikdagi soʻz. Avval ikkinchi yarmini, keyin birinchi yarmini qoʻshib chiqaring.", "s = input()\nh = len(s) // 2\nprint(s[h:] + s[:h])", "abcdef", "olma", "xy"),
    PR("Sana formati", "Kirishda sana `YYYY-MM-DD` koʻrinishida. Uni `DD.MM.YYYY` koʻrinishida chiqaring (faqat kesish bilan).", 's = input()\nprint(s[8:10] + "." + s[5:7] + "." + s[0:4])', "2026-10-13", "1999-01-05", "2000-12-31"),
    L("lc", "reverse-string"),
    L("lc", "valid-palindrome"),
    L("exercism", "reverse-string"),
    L("acmp", 149),
])

# ---------------------------------------------------------------- 2.13
TOPIC("satr-metodlari", "Satr metodlari", "upper, lower, strip, replace, split, join, find, count…", 25, r'''
**Metod** — muayyan turga tegishli funksiya. U nuqta orqali chaqiriladi: `satr.metod()`. Satr metodlari asl satrni oʻzgartirmaydi — **yangi satr qaytaradi**.

## Harf registri
```py
s = "Mirae Academy"
print(s.upper())
print(s.lower())
print("toshkent shahri".title())
print("python".capitalize())
print("PyThOn".swapcase())
```

## Boʻsh joylarni tozalash
Foydalanuvchi kiritgan matn atrofida koʻpincha ortiqcha boʻsh joy boʻladi:

```py
s = "   salom   "
print("[" + s.strip() + "]")
print("[" + s.lstrip() + "]")
print("[" + s.rstrip() + "]")
```

## Qidirish va sanash
```py
s = "banan va ananas"
print(s.find("an"))
print(s.find("olma"))
print(s.count("an"))
print(s.startswith("ban"), s.endswith("as"))
```

`find` topilmasa `-1` qaytaradi.

## Almashtirish
```py
xabar = "Dars soat 14:00 da"
print(xabar.replace("14:00", "15:30"))
print("a-b-c".replace("-", ""))
```

## split va join
`split()` satrni roʻyxatga boʻladi, `join()` esa roʻyxatni satrga yigʻadi.

```py
gap = "Python dasturlash tili"
sozlar = gap.split()
print(sozlar)
print(len(sozlar))
print("-".join(sozlar))
print("12,45,7".split(","))
```

## Tekshiruvchi metodlar
```py
print("2026".isdigit(), "a1".isdigit())
print("salom".isalpha(), "salom!".isalpha())
print("ABC".isupper(), "abc".islower())
```

## Zanjir qilib chaqirish
```py input="   ALI valiyev"
ism = input().strip().title()
print("Salom,", ism)
```

## Amaliy misol: login tekshiruvi
```py input="  Admin@Mirae.UZ"
email = input().strip().lower()
print("Email:", email)
print("Toʻgʻrimi:", "@" in email and email.endswith(".uz"))
```

## Esda tuting
- Metodlar yangi satr qaytaradi: `s.upper()` dan keyin `s` oʻzgarmaydi.
- `split()` → roʻyxat, `"x".join(roʻyxat)` → satr.
- `find` topilmasa `-1`, `count` — necha marta uchrashi.
''', [
    P('s = "salom"\ns.upper()\nprint(s)', "SALOM", "Salom", "Xato", why="`upper()` yangi satr qaytaradi; natija hech qayerga saqlanmadi."),
    P('print("  a b  ".strip())', "ab", "  a b", "a b  "),
    P('print("banan".count("a"))', "1", "3", "5"),
    P('print("salom".find("x"))', "0", "None", "Xato"),
    P('print("a,b,c".split(","))', "abc", "a b c", "('a', 'b', 'c')"),
    P('print("-".join(["2026", "10", "13"]))', "2026 10 13", "-2026-10-13-", "20261013"),
    P('print("toshkent".title())', "TOSHKENT", "toshkent", "Toshkent Shahri"),
    Q("`\"a b c\".split()` nima qaytaradi?", "['a', 'b', 'c']", "'abc'", "('a', 'b', 'c')", "['a b c']"),
    Q("`\"x\".join([\"1\", \"2\", \"3\"])` natijasi?", "1x2x3", "x1x2x3x", "123x", "['1x', '2x', '3x']"),
    PR("Katta harflar", "Kirishda matn. Uni katta harflar bilan chiqaring.", "print(input().upper())", "salom dunyo", "Mirae", "abc123"),
    PR("Tozalash", "Kirishda atrofida boʻsh joylar bor matn. Boʻsh joylarni olib tashlab, `[` va `]` ichida chiqaring.", 'print("[" + input().strip() + "]")', "   salom   ", "a", "  x y  "),
    PR("Soʻzlar soni", "Kirishda gap. Undagi soʻzlar sonini chiqaring.", "print(len(input().split()))", "Python dasturlash tili", "salom", "bir  ikki   uch"),
    PR("Almashtirish", "Kirishda matn. Undagi barcha `a` harflarini `@` ga almashtiring.", 'print(input().replace("a", "@"))', "banana", "salom", "xyz"),
    PR("Bosh harflar", "Kirishda ism-familiya (kichik harflarda). Har bir soʻzni bosh harf bilan chiqaring.", "print(input().title())", "ali valiyev", "malika", "abdulla qodiriy"),
    PR("Initsiallar", "Kirishda ism va familiya. Initsiallarni `A.V.` koʻrinishida chiqaring (katta harflarda).", 'i, f = input().split()\nprint(i[0].upper() + "." + f[0].upper() + ".")', "ali valiyev", "Zarina Karimova", "x y"),
    PR("Teskari tartib", "Kirishda gap. Soʻzlarni teskari tartibda, boʻsh joy bilan chiqaring.", 'print(" ".join(input().split()[::-1]))', "men python oʻrganaman", "bir ikki uch", "salom"),
    L("exercism", "little-sisters-essay"),
    L("lc", "to-lower-case"),
    L("lc", "reverse-words-in-a-string-iii"),
    L("lc", "detect-capital"),
])

# ---------------------------------------------------------------- 2.14
TOPIC("birlashtirish", "Satrlarni birlashtirish", "+ va * amallari, ko'p qismli matn yig'ish", 15, r'''
Satrlarni bir-biriga ulash — **birlashtirish** (concatenation) deyiladi.

## + bilan ulash
```py
ism = "Aziza"
familiya = "Rahimova"
toliq = ism + " " + familiya
print(toliq)
```

!> `+` faqat satrni satr bilan ulaydi. Son boʻlsa, avval `str()`:

```py
yosh = 16
print("Yoshi: " + str(yosh))
```

## * bilan takrorlash
```py
print("ha" * 3)
print("-" * 20)
print("=" * 5 + " MENYU " + "=" * 5)
```

## += bilan qoʻshib borish
```py
natija = ""
natija += "Py"
natija += "thon"
print(natija)
```

## Koʻp qismni yigʻish: join()
Juda koʻp boʻlakni ulashda `+` sekin ishlaydi. Toʻgʻri usul — roʻyxatga yigʻib, `join` qilish:

```py
qismlar = []
for i in range(1, 6):
    qismlar.append(str(i))
print(" + ".join(qismlar))
```

## Vergul, + yoki f-satr?
```py
narx = 15000
print("Narx:", narx, "soʻm")
print("Narx: " + str(narx) + " soʻm")
print(f"Narx: {narx} soʻm")
```

Uchalasi bir xil natija beradi. Eng qulay va zamonaviy usul — **f-satr** (keyingi mavzu).

## Amaliy misol: uchburchak
```py input=4
n = int(input())
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))
```

## Esda tuting
- `+` — satrlarni ulaydi; son bilan ulash uchun `str()`.
- `"ab" * 3` → `ababab`.
- Koʻp boʻlak uchun `"".join(...)`.
''', [
    P('print("Py" + "thon")', "Py thon", "Py+thon", "Xato"),
    P('print("ab" * 3)', "ab3", "ab ab ab", "Xato"),
    P('s = "a"\ns += "b"\ns += "c"\nprint(s)', "a", "c", "a b c"),
    P('print("5" + "5" * 2)', "105", "15", "555 "),
    P('print("-" * 3 + ">")', "--->>>", "-3>", "Xato"),
    P('print("Yosh: " + str(10 + 5))', "Yosh: 105", "Yosh: 10 + 5", "Xato"),
    P('print("x" * 0 + "y")', "xy", "0y", "Xato"),
    Q("Qaysi ifoda xato beradi?", "\"Ball: \" + 90", "\"Ball: \" + \"90\"", "\"Ball: \" + str(90)", "\"Ball: \" * 2"),
    Q("Juda koʻp satrni ulashning eng samarali usuli qaysi?", "\"\".join(roʻyxat)", "Har birini + bilan qoʻshish", "str(roʻyxat)", "roʻyxat * 1"),
    PR("Toʻliq ism", "Kirishda ism va familiya (ikki qator). Ularni boʻsh joy bilan ulab chiqaring.", 'print(input() + " " + input())', "Aziza\nRahimova", "Ali\nValiyev", "X\nY"),
    PR("Chiziq", "Kirishda n. n ta `=` belgisidan iborat chiziq chiqaring.", 'print("=" * int(input()))', "5", "20", "1"),
    PR("Sarlavha", "Kirishda soʻz. `*** SOʻZ ***` koʻrinishida chiqaring (soʻz katta harflarda).", 'print("*** " + input().upper() + " ***")', "menyu", "Natijalar", "a"),
    PR("Zinapoya", "Kirishda n. 1 dan n gacha qatorlar chiqaring: i-qatorda i ta `#`.", 'n = int(input())\nfor i in range(1, n + 1):\n    print("#" * i)', "3", "5", "1"),
    PR("Archa", "Kirishda n. Markazlashgan archa chiqaring: i-qatorda `n - i` ta boʻsh joy va `2i - 1` ta `*`.", 'n = int(input())\nfor i in range(1, n + 1):\n    print(" " * (n - i) + "*" * (2 * i - 1))', "3", "1", "5"),
    PR("Yigʻindi yozuvi", "Kirishda n. `1+2+...+n=S` koʻrinishida chiqaring (masalan n=3 → `1+2+3=6`).", 'n = int(input())\nprint("+".join(str(i) for i in range(1, n + 1)) + "=" + str(n * (n + 1) // 2))', "3", "1", "10"),
    PR("Takror soʻz", "Kirishda soʻz va son (ikki qator). Soʻzni shuncha marta, orasida vergul va boʻsh joy bilan chiqaring.", 's = input()\nn = int(input())\nprint(", ".join([s] * n))', "ha\n3", "salom\n1", "x\n5"),
    L("exercism", "pretty-leaflet"),
    L("lc", "merge-strings-alternately"),
    L("lc", "defanging-an-ip-address"),
    L("acmp", 70),
])

# ---------------------------------------------------------------- 2.15
TOPIC("f-satrlar", "f-satrlar (formatlangan satrlar)", "Qiymatlarni matnga chiroyli joylashtirish", 20, r'''
**f-satr** — satrga qiymatlarni qulay joylashtirish usuli. Qoʻshtirnoq oldiga `f` harfi qoʻyiladi, qiymatlar esa `{ }` ichida yoziladi.

## Oddiy f-satr
```py
ism = "Bekzod"
yosh = 19
print(f"Mening ismim {ism}, yoshim {yosh}.")
```

## Qavs ichida ifoda
`{ }` ichida istalgan ifoda yozish mumkin:

```py
narx, soni = 12500, 3
print(f"Jami: {narx * soni} soʻm")
print(f"Ism katta harflarda: {'ali'.upper()}")
```

## Kasr sonlarni formatlash
`:.2f` — 2 xona aniqlikda:

```py
pi = 3.14159265
print(f"{pi:.2f}")
print(f"{pi:.0f}")
print(f"{2/3:.3f}")
```

## Katta sonlarni ajratish
```py
summa = 12500000
print(f"{summa:,}")
print(f"{summa:,}".replace(",", " "))
```

## Foiz
```py
ulush = 0.875
print(f"{ulush:.1%}")
```

## Joylashtirish (kenglik)
`:<10` — chapga, `:>10` — oʻngga, `:^10` — markazga, 10 belgi kenglikda:

```py
print(f"[{'chap':<10}]")
print(f"[{'oʻng':>10}]")
print(f"[{'markaz':^10}]")
print(f"[{7:03d}]")
```

## Amaliy misol: jadval
```py
mahsulotlar = [("Non", 4000), ("Sut", 12000), ("Pishloq", 45000)]
print(f"{'Mahsulot':<10}{'Narx':>10}")
for nom, narx in mahsulotlar:
    print(f"{nom:<10}{narx:>10,}")
```

## Debug uchun: {x=}
```py
x = 42
print(f"{x=}")
```

## Esda tuting
- `f"...{qiymat}..."` — qiymat joylashadi.
- `:.2f` — 2 xona, `:,` — minglik ajratuvchi, `:.1%` — foiz.
- `:<10`, `:>10`, `:^10` — kenglik va tekislash.
''', [
    P('x = 5\nprint(f"x = {x}")', "x = {x}", "f\"x = 5\"", "x = x"),
    P('a, b = 2, 3\nprint(f"{a} + {b} = {a + b}")', "2 + 3 = a + b", "{a} + {b} = {a + b}", "2 + 3 = 23"),
    P('print(f"{3.14159:.2f}")', "3.1", "3.141", "3.14159"),
    P('print(f"{1000000:,}")', "1000000", "1.000.000", "1 000 000"),
    P('print(f"[{5:03d}]")', "[5]", "[  5]", "[500]"),
    P('print(f"{0.25:.0%}")', "0.25%", "0%", "25"),
    P('ism = "ali"\nprint(f"{ism.title()}!")', "ali!", "{ism.title()}!", "ALI!"),
    Q("`f\"{2/3:.2f}\"` natijasi?", "0.67", "0.66", "0.6", "0.666"),
    Q("Qaysi format sonni 8 belgi kenglikda oʻngga tekislaydi?", "{x:>8}", "{x:<8}", "{x:^8}", "{x:8<}"),
    PR("Tanishtiruv", "Kirishda ism va yosh (ikki qator). f-satr bilan `ISM X yoshda` deb chiqaring.", 'ism = input()\nyosh = int(input())\nprint(f"{ism} {yosh} yoshda")', "Ali\n17", "Madina\n9", "Bobur\n30"),
    PR("Ikki xona", "Kirishda kasr son. Uni aynan 2 xona bilan chiqaring.", 'print(f"{float(input()):.2f}")', "3.14159", "2", "0.005"),
    PR("Pul formati", "Kirishda summa (butun). Uni minglik ajratuvchi vergul bilan chiqaring va oxiriga ` soʻm` qoʻshing.", 'print(f"{int(input()):,} soʻm")', "12500000", "999", "1000"),
    PR("Foiz", "Kirishda toʻgʻri javoblar soni va jami savollar (bir qatorda). Natijani 1 xonali foizda chiqaring.", 'a, b = map(int, input().split())\nprint(f"{a / b:.1%}")', "17 20", "1 3", "0 5"),
    PR("Nol bilan toʻldirish", "Kirishda son (0–999). Uni 3 xonali qilib, oldidan nollar bilan chiqaring (masalan `7` → `007`).", 'print(f"{int(input()):03d}")', "7", "42", "123"),
    PR("Ko'paytirish jadvali", "Kirishda n. n uchun 1 dan 10 gacha koʻpaytirish jadvalini `n x i = natija` koʻrinishida chiqaring.", 'n = int(input())\nfor i in range(1, 11):\n    print(f"{n} x {i} = {n * i}")', "7", "1", "12"),
    PR("Chek", "Kirishda mahsulot nomi va narxi (ikki qator). `NOM` ni 10 belgi kenglikda chapga, narxni 8 belgi kenglikda oʻngga tekislab, bitta qatorda chiqaring.", 'nom = input()\nnarx = int(input())\nprint(f"{nom:<10}{narx:>8}")', "Non\n4000", "Shokolad\n15000", "Choy\n0"),
    L("exercism", "pretty-leaflet"),
    L("exercism", "line-up"),
    L("lc", "fizz-buzz"),
    L("acmp", 59),
])

# ---------------------------------------------------------------- 2.16
TOPIC("escape", "Maxsus belgilar (escape)", "\\n, \\t, \\\\, qoʻshtirnoq va raw satrlar", 15, r'''
Baʼzi belgilarni satr ichiga oddiy yozib boʻlmaydi: yangi qator, tabulyatsiya yoki qoʻshtirnoqning oʻzi. Buning uchun **teskari chiziq** `\` bilan boshlanadigan maxsus ketma-ketliklar ishlatiladi.

## Asosiy escape belgilar
| Yozuv | Maʼnosi |
|---|---|
| `\n` | yangi qator |
| `\t` | tabulyatsiya (bir nechta boʻsh joy) |
| `\\` | teskari chiziqning oʻzi |
| `\"` | qoʻshtirnoq |
| `\'` | apostrof |

```py
print("Birinchi qator\nIkkinchi qator")
print("Ism:\tAli\nYosh:\t17")
```

## Qoʻshtirnoq ichida qoʻshtirnoq
```py
print("U dedi: \"Salom!\"")
print('Bu \'bitta\' tirnoq')
print("Aralash: 'bunday' ham boʻladi")
```

> Eng oson yoʻl — tashqi va ichki qoʻshtirnoqni har xil tanlash: `"... '...' ..."`.

## Teskari chiziq
```py
print("C:\\Users\\Ali\\Hujjatlar")
```

!> `"C:\new"` yozilsa, `\n` yangi qatorga aylanadi! Fayl yoʻllarida ehtiyot boʻling.

## raw satr — r"..."
Oldiga `r` qoʻyilsa, `\` oddiy belgi sifatida qoladi:

```py
print(r"C:\new\test")
print(len("\n"), len(r"\n"))
```

## Unicode belgilar
```py
print("Yurak: \u2764")
print("Oʻzbekiston \U0001F1FA\U0001F1FF")
```

## Amaliy misol: kvitansiya
```py
print("Kvitansiya\n" + "-" * 20)
print("Xizmat:\tInternet")
print("Summa:\t120 000 soʻm")
print("Holat:\t\"Toʻlangan\"")
```

## Esda tuting
- `\n` — yangi qator, `\t` — tab, `\\` — teskari chiziq.
- Qoʻshtirnoq ichida qoʻshtirnoq: `\"` yoki boshqa turdagi tirnoq.
- `r"..."` — escape ishlamaydigan satr (fayl yoʻllari, regex).
''', [
    P('print("a\\nb")', "a\\nb", "ab", "a b"),
    P('print(len("a\\tb"))', "4", "5", "2"),
    P('print("U: \\"Ha\\"")', "U: \\\"Ha\\\"", "U: Ha", "Xato"),
    P('print(r"a\\nb")', "a\nb", "ab", "a\\\\nb"),
    P('print("C:\\\\Users")', "C:\\\\Users", "C:Users", "C:\nUsers"),
    P("print('It\\'s')", "It\\'s", "Its", "Xato"),
    P('print("1\\n2\\n3".count("\\n"))', "3", "0", "1"),
    Q("Yangi qatorga oʻtish uchun qaysi belgi ishlatiladi?", "\\n", "\\t", "/n", "\\l"),
    Q("`r\"C:\\new\"` nima uchun qulay?", "Teskari chiziqlar maxsus belgiga aylanmaydi", "Satr katta harfga oʻtadi", "Satr teskari yoziladi", "Satr ikki marta chiqadi"),
    PR("Ikki qator", "Bitta `print` va `\\n` bilan ikki qator chiqaring: `Salom` va `Dunyo`.", 'print("Salom\\nDunyo")'),
    PR("Tablitsa", "Bitta `print` bilan chiqaring: `Ism`, tab, `Ball` (ya'ni `Ism\\tBall`).", 'print("Ism\\tBall")'),
    PR("Iqtibos", "Ekranga aynan shuni chiqaring: `Ustoz dedi: \"Mashq qiling!\"`", 'print("Ustoz dedi: \\"Mashq qiling!\\"")'),
    PR("Fayl yoʻli", "Ekranga aynan `C:\\Mirae\\darslar` chiqaring.", 'print("C:\\\\Mirae\\\\darslar")', hint="`\\\\` yoki `r\"...\"` dan foydalaning."),
    PR("Har biri yangi qatorda", "Kirishda vergul bilan ajratilgan soʻzlar. Ularni har birini yangi qatorda chiqaring (bitta `print` va `\"\\n\".join`).", 'print("\\n".join(input().split(",")))', "olma,nok,uzum", "a", "1,2"),
    PR("Tab bilan", "Kirishda ism va ball (ikki qator). `ism<TAB>ball` koʻrinishida chiqaring.", 'print(input() + "\\t" + input())', "Ali\n95", "Malika\n100", "X\n0"),
    PR("Belgilar soni", "Kirishda bir qator. Undagi teskari chiziq `\\` belgilari sonini chiqaring.", 'print(input().count("\\\\"))', "C:\\Users\\Ali", "salom", "\\\\\\"),
    L("exercism", "pretty-leaflet"),
    L("lc", "goal-parser-interpretation"),
    L("acmp", 44),
    L("acmp", 288),
])
