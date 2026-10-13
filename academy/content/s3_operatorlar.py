from dsl import SECTION, TOPIC, P, Q, PR, L

SECTION(3, "Operatorlar", "Hisoblash, taqqoslash va mantiq amallari", "➗")

# ---------------------------------------------------------------- 3.1
TOPIC("arifmetik", "Arifmetik operatorlar", "+  -  *  /  //  %  ** va ularning amaliy qoʻllanishi", 20, r'''
Arifmetik operatorlar — sonlar ustidagi amallar. Ular dasturlashning "kalkulyatori".

| Operator | Amal | Misol | Natija |
|---|---|---|---|
| `+` | qoʻshish | `7 + 2` | `9` |
| `-` | ayirish | `7 - 2` | `5` |
| `*` | koʻpaytirish | `7 * 2` | `14` |
| `/` | boʻlish | `7 / 2` | `3.5` |
| `//` | butun boʻlish | `7 // 2` | `3` |
| `%` | qoldiq | `7 % 2` | `1` |
| `**` | daraja | `7 ** 2` | `49` |

```py
a, b = 17, 5
print(a + b, a - b, a * b)
print(a / b, a // b, a % b)
print(a ** 2)
```

## // va % — juftlik
`//` va `%` doim birga ishlaydi: `a = (a // b) * b + a % b`.

```py
konfet, bola = 23, 5
print("Har biriga:", konfet // bola)
print("Ortib qoldi:", konfet % bola)
```

## % ning qoʻllanishlari
- Juft/toq: `n % 2 == 0`
- Boʻlinish: `n % 3 == 0`
- Oxirgi raqam: `n % 10`
- Aylanma sanoq: soat `(soat + 5) % 24`

```py
soat = 22
print("5 soatdan keyin:", (soat + 5) % 24)
```

## Raqamlarga ajratish
```py
n = 4729
print(n // 1000, n // 100 % 10, n // 10 % 10, n % 10)
```

## ** — daraja va ildiz
```py
print(2 ** 10)
print(81 ** 0.5)
print(27 ** (1 / 3))
```

## Amaliy misol: oylik toʻlov
```py input=12000000|12|20
narx = int(input())
oy = int(input())
foiz = int(input())
jami = narx + narx * foiz // 100
print("Jami:", jami)
print("Oyiga:", jami // oy)
```

## Esda tuting
- `/` → doim float; `//` → butun qism; `%` → qoldiq.
- `n % 10` — oxirgi raqam, `n // 10` — undan oldingi qism.
- `x ** 0.5` — kvadrat ildiz.
''', [
    P('print(7 // 2, 7 % 2)', "3.5 1", "3 0", "4 1"),
    P('print(2 ** 5)', "10", "25", "7"),
    P('print(20 / 4)', "5", "5.00", "4"),
    P('print(9 ** 0.5)', "3", "4.5", "81"),
    P('n = 384\nprint(n // 10 % 10)', "3", "4", "38"),
    P('print((22 + 5) % 24)', "27", "1", "5"),
    P('print(10 - 2 * 3)', "24", "-24", "6"),
    Q("23 ta olmani 5 kishiga teng boʻlsa, har biriga nechta tegadi?", "23 // 5", "23 / 5", "23 % 5", "23 ** 5"),
    Q("Son 3 ga boʻlinishini qaysi ifoda tekshiradi?", "n % 3 == 0", "n / 3 == 0", "n // 3 == 0", "n ** 3 == 0"),
    PR("Kalkulyator", "Kirishda bir qatorda ikki son `a b`. Ularning yigʻindisi, ayirmasi va koʻpaytmasini bitta qatorda chiqaring.", "a, b = map(int, input().split())\nprint(a + b, a - b, a * b)", "7 2", "0 5", "-3 -4"),
    PR("Boʻlinma va qoldiq", "Kirishda `a b`. `a // b` va `a % b` ni bir qatorda chiqaring.", "a, b = map(int, input().split())\nprint(a // b, a % b)", "17 5", "10 2", "3 7"),
    PR("Raqamlar", "Kirishda 3 xonali son. Raqamlarini boʻsh joy bilan chiqaring (faqat `//` va `%` bilan).", "n = int(input())\nprint(n // 100, n // 10 % 10, n % 10)", "472", "100", "999"),
    PR("Soat", "Kirishda hozirgi soat (0–23) va qancha soat oʻtishi (bir qatorda). Natija soatni chiqaring.", "h, k = map(int, input().split())\nprint((h + k) % 24)", "22 5", "0 24", "13 100"),
    PR("Konfetlar", "Kirishda konfetlar va bolalar soni (bir qatorda). Har bir bolaga tegadigan va ortib qoladigan konfetlarni alohida qatorlarda chiqaring.", "k, b = map(int, input().split())\nprint(k // b)\nprint(k % b)", "23 5", "10 10", "3 4"),
    PR("Teskari son", "Kirishda 3 xonali son. Uning raqamlarini teskari tartibda son sifatida chiqaring (masalan `123` → `321`). `//` va `%` dan foydalaning.", "n = int(input())\nprint(n % 10 * 100 + n // 10 % 10 * 10 + n // 100)", "123", "500", "909"),
    PR("Kredit", "Kirishda narx, oylar soni va foiz (uch qator). Jami summa: `narx + narx * foiz // 100`. Oylik toʻlovni (butun boʻlish) chiqaring.", "narx = int(input())\noy = int(input())\nf = int(input())\nprint((narx + narx * f // 100) // oy)", "12000000\n12\n20", "1000000\n10\n0", "500000\n3\n10"),
    L("exercism", "grains"),
    L("lc", "subtract-the-product-and-sum-of-digits-of-an-integer"),
    L("acmp", 3),
    L("acmp", 106),
])

# ---------------------------------------------------------------- 3.2
TOPIC("qiymat-berish", "Qiymat berish operatorlari", "=  +=  -=  *=  /=  //=  %=  **=", 15, r'''
Oʻzgaruvchini oʻz qiymati asosida yangilash juda koʻp uchraydi: ballga qoʻshish, balansdan ayirish, narxni ikki baravar qilish. Buning uchun qisqa operatorlar bor.

| Operator | Uzun yozuvi | Misol |
|---|---|---|
| `+=` | `x = x + 5` | `x += 5` |
| `-=` | `x = x - 5` | `x -= 5` |
| `*=` | `x = x * 5` | `x *= 5` |
| `/=` | `x = x / 5` | `x /= 5` |
| `//=` | `x = x // 5` | `x //= 5` |
| `%=` | `x = x % 5` | `x %= 5` |
| `**=` | `x = x ** 5` | `x **= 5` |

```py
ball = 100
ball += 20
print(ball)
ball -= 50
print(ball)
ball *= 2
print(ball)
ball //= 3
print(ball)
```

## Satrlar va roʻyxatlarda ham ishlaydi
```py
xabar = "Salom"
xabar += ", dunyo"
print(xabar)
chiziq = "-"
chiziq *= 10
print(chiziq)
```

## Yigʻindini toʻplash
Sikl ichida `+=` — eng koʻp ishlatiladigan andoza:

```py
jami = 0
for narx in [12000, 4500, 8000]:
    jami += narx
print("Jami:", jami)
```

## Hisoblagich
```py
gap = "olma nok olma uzum olma"
olma = 0
for soz in gap.split():
    if soz == "olma":
        olma += 1
print("olma:", olma)
```

!> Pythonda `x++` yoki `x--` yoʻq! Faqat `x += 1`.

## Amaliy misol: hamyon
```py
balans = 200000
balans -= 45000   # tushlik
balans -= 30000   # taksi
balans += 150000  # maosh
print("Qoldiq:", balans)
```

## Esda tuting
- `x += 1` — `x = x + 1` ning qisqasi.
- Yigʻindi uchun `jami = 0`, keyin `jami += ...`.
- `x++` Pythonda ishlamaydi.
''', [
    P('x = 10\nx += 5\nx *= 2\nprint(x)', "20", "25", "15"),
    P('x = 17\nx //= 5\nprint(x)', "3.4", "2", "17"),
    P('x = 17\nx %= 5\nprint(x)', "3", "3.4", "5"),
    P('s = "ab"\ns *= 3\nprint(s)', "ab3", "ab ab ab", "Xato"),
    P('x = 2\nx **= 3\nprint(x)', "6", "9", "5"),
    P('x = 10\nx /= 4\nprint(x)', "2", "2.0", "2.25"),
    P('n = 0\nfor i in range(5):\n    n += i\nprint(n)', "5", "15", "4"),
    Q("`x = x * 3` ning qisqa yozuvi qaysi?", "x *= 3", "x =* 3", "x ** 3", "x * = 3"),
    Q("Pythonda `x` ni 1 ga oshirishning toʻgʻri usuli?", "x += 1", "x++", "++x", "x =+ 1", why="`x =+ 1` xato bermaydi, lekin x ga +1 ni (yaʼni 1 ni) beradi — bu oshirish emas."),
    PR("Balans", "Boshlangʻich balans 100000. Kirishda bir qatorda xarajatlar (boʻsh joy bilan). Har birini `-=` bilan ayirib, qoldiqni chiqaring.", "b = 100000\nfor x in input().split():\n    b -= int(x)\nprint(b)", "20000 15000", "100000", "1 2 3"),
    PR("Yigʻindi", "Kirishda bir qatorda sonlar. `jami += ...` bilan ularning yigʻindisini chiqaring.", "jami = 0\nfor x in input().split():\n    jami += int(x)\nprint(jami)", "1 2 3 4", "100", "-5 5"),
    PR("Koʻpaytma", "Kirishda bir qatorda sonlar. `*=` bilan ularning koʻpaytmasini chiqaring.", "p = 1\nfor x in input().split():\n    p *= int(x)\nprint(p)", "1 2 3 4", "7", "5 0 9"),
    PR("Ikki baravar", "Kirishda n. 1 dan boshlab har qadamda `*= 2` qiling; n qadamdan keyingi qiymatni chiqaring.", "x = 1\nfor _ in range(int(input())):\n    x *= 2\nprint(x)", "10", "0", "20"),
    PR("Soʻz sanagich", "Kirishda gap va soʻz (ikki qator). Soʻz gapda necha marta (alohida soʻz sifatida) uchrashini `+= 1` bilan sanang.", "gap = input().split()\nsoz = input()\nn = 0\nfor s in gap:\n    if s == soz:\n        n += 1\nprint(n)", "olma nok olma uzum\nolma", "a b c\nd", "x x x\nx"),
    PR("Satr yigʻish", "Kirishda n. `s = \"\"` dan boshlab 1 dan n gacha sonlarni `s += str(i)` bilan qoʻshib chiqaring.", 's = ""\nfor i in range(1, int(input()) + 1):\n    s += str(i)\nprint(s)', "5", "1", "12"),
    PR("Raqamlar yigʻindisi", "Kirishda natural son. `while` va `//=` yordamida raqamlari yigʻindisini chiqaring.", "n = int(input())\ns = 0\nwhile n > 0:\n    s += n % 10\n    n //= 10\nprint(s)", "1234", "9", "1000"),
    L("exercism", "making-the-grade"),
    L("lc", "final-value-of-variable-after-performing-operations"),
    L("lc", "number-of-steps-to-reduce-a-number-to-zero"),
    L("acmp", 43),
])

# ---------------------------------------------------------------- 3.3
TOPIC("taqqoslash", "Taqqoslash operatorlari", "==  !=  <  >  <=  >= — sonlar va satrlarni solishtirish", 15, r'''
Taqqoslash operatorlari ikki qiymatni solishtiradi va `True` yoki `False` qaytaradi.

| Operator | Maʼnosi | `5 ? 3` |
|---|---|---|
| `==` | teng | `False` |
| `!=` | teng emas | `True` |
| `>` | katta | `True` |
| `<` | kichik | `False` |
| `>=` | katta yoki teng | `True` |
| `<=` | kichik yoki teng | `False` |

```py
ball = 85
print(ball >= 60)
print(ball == 100)
print(ball != 0)
```

!> `=` — qiymat berish, `==` — taqqoslash. Ularni adashtirish — yangi boshlovchilarning eng koʻp xatosi.

## Satrlarni solishtirish
Satrlar alifbo (aniqrogʻi Unicode) tartibida solishtiriladi. Katta harflar kichiklardan "oldin" keladi.

```py
print("olma" < "uzum")
print("Ali" == "ali")
print("Z" < "a")
print("10" < "9")
```

> `"10" < "9"` — `True`, chunki birinchi belgi `"1"` < `"9"`. Sonlarni solishtirishdan oldin `int()` qiling!

## Har xil turlar
```py
print(1 == 1.0)
print(1 == "1")
```

## Amaliy misol: parol tekshiruvi
```py input=mirae2026|mirae2026
parol = input()
takror = input()
print("Mos:", parol == takror)
print("Uzunligi yetarli:", len(parol) >= 8)
```

## Esda tuting
- Taqqoslash natijasi — `bool`.
- `==` taqqoslaydi, `=` qiymat beradi.
- Matn koʻrinishidagi sonlarni avval `int()` qiling.
''', [
    P('print(5 == 5.0)', "False", "Xato", "5"),
    P('print("abc" == "ABC")', "True", "Xato", "abc"),
    P('print("10" < "9")', "False", "Xato", "10"),
    P('print(10 < 9)', "True", "Xato", "9"),
    P('x = 7\nprint(x != 7, x >= 7)', "True True", "False False", "True False"),
    P('print("a" < "b" < "c")', "False", "a", "Xato"),
    P('print(1 == "1")', "True", "Xato", "1"),
    Q("Qaysi biri taqqoslash operatori?", "==", "=", "+=", "=>"),
    Q("`\"Olma\" < \"olma\"` nima qaytaradi?", "True", "False", "Xato", "None", why="Katta harflarning kodi kichiklardan kichik: `'O'` (79) < `'o'` (111)."),
    PR("Kattasi", "Kirishda ikki son (bir qatorda). Birinchisi katta boʻlsa `True`, aks holda `False`.", "a, b = map(int, input().split())\nprint(a > b)", "5 3", "3 5", "4 4"),
    PR("Tengmi", "Kirishda ikki soʻz (ikki qator). Katta-kichik harfga qaramay tengmi — `True`/`False`.", "print(input().lower() == input().lower())", "Olma\nolma", "nok\nnon", "ABC\nabc"),
    PR("Imtihon", "Kirishda ball. 60 va undan yuqori boʻlsa `True` chiqaring.", "print(int(input()) >= 60)", "60", "59", "100"),
    PR("Alifbo tartibi", "Kirishda ikki soʻz. Alifbo boʻyicha oldin keladiganini chiqaring.", "a = input()\nb = input()\nprint(min(a, b))", "uzum\nolma", "nok\nnon", "a\nb"),
    PR("Sonlarni toʻgʻri solishtirish", "Kirishda ikki son (matn sifatida, ikki qator). Ularni son sifatida solishtirib, birinchisi kichik boʻlsa `True`.", "print(int(input()) < int(input()))", "10\n9", "9\n10", "5\n5"),
    PR("Parol", "Kirishda parol va takrori (ikki qator). Ular teng va uzunligi kamida 8 boʻlsa `True`, aks holda `False`.", "p = input()\nq = input()\nprint(p == q and len(p) >= 8)", "mirae2026\nmirae2026", "abc\nabc", "parol1234\nparol1235"),
    PR("Uchala teng", "Kirishda uch son (bir qatorda). Uchalasi teng boʻlsa `True`.", "a, b, c = map(int, input().split())\nprint(a == b == c)", "5 5 5", "1 1 2", "0 0 0"),
    L("exercism", "black-jack"),
    L("lc", "kids-with-the-greatest-number-of-candies"),
    L("acmp", 25),
    L("acmp", 286),
])

# ---------------------------------------------------------------- 3.4
TOPIC("mantiqiy", "Mantiqiy operatorlar", "and, or, not — shartlarni birlashtirish", 20, r'''
Hayotda qarorlar koʻpincha bir nechta shartga bogʻliq: "agar yomgʻir yogʻmasa **va** vaqtim boʻlsa — sayr qilaman". Pythonda buning uchun `and`, `or`, `not` bor.

| Operator | Qachon `True` |
|---|---|
| `a and b` | ikkalasi ham rost boʻlsa |
| `a or b` | hech boʻlmasa bittasi rost boʻlsa |
| `not a` | `a` yolgʻon boʻlsa |

```py
yosh = 20
guvohnoma = True
print(yosh >= 18 and guvohnoma)
print(yosh < 12 or yosh > 65)
print(not guvohnoma)
```

## Haqiqat jadvali
| a | b | a and b | a or b |
|---|---|---|---|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

## Bir nechta shart
```py
harorat = 24
yomgir = False
dam_olish = True
if harorat > 18 and not yomgir and dam_olish:
    print("Sayrga chiqamiz!")
```

## Ustuvorlik: not → and → or
```py
print(True or False and False)
print((True or False) and False)
```

> Shubha boʻlsa — qavs qoʻying. Qavslar kodni oʻqishni ham osonlashtiradi.

## Amaliy misol: chegirma
```py input=17|True
yosh = int(input())
talaba = input() == "True"
chegirma = yosh < 18 or talaba
print("Chegirma bor:", chegirma)
```

## Esda tuting
- `and` — hammasi rost; `or` — bittasi yetarli; `not` — teskarisi.
- Tartib: `not`, keyin `and`, keyin `or`.
- Murakkab shartlarda qavs ishlating.
''', [
    P('print(True and False)', "True", "None", "TrueFalse"),
    P('print(True or False)', "False", "None", "TrueFalse"),
    P('print(not 5 > 3)', "True", "5", "Xato"),
    P('x = 15\nprint(x > 10 and x < 20)', "False", "15", "Xato"),
    P('print(True or False and False)', "False", "None", "Xato", why="`and` avval bajariladi: `False and False = False`, keyin `True or False = True`."),
    P('a, b = 0, 7\nprint(a > 0 or b > 0)', "False", "7", "0"),
    P('print(not (True and not False))', "True", "None", "Xato"),
    Q("Son 1 dan 10 gacha oraliqda ekanini qaysi ifoda tekshiradi?", "n >= 1 and n <= 10", "n >= 1 or n <= 10", "not n >= 1 and n <= 10", "n >= 1 and or n <= 10"),
    Q("`and`, `or`, `not` dan qaysi biri birinchi bajariladi?", "not", "and", "or", "Chapdan oʻngga tartibda"),
    PR("Oraliq", "Kirishda son. 10 va 20 orasida (ikkalasi kiradi) boʻlsa `True`.", "n = int(input())\nprint(n >= 10 and n <= 20)", "15", "9", "20"),
    PR("Dam olish", "Kirishda hafta kuni raqami (1–7). 6 yoki 7 boʻlsa `True`.", "d = int(input())\nprint(d == 6 or d == 7)", "6", "3", "7"),
    PR("Chegirma", "Kirishda yosh. 7 dan kichik yoki 65 dan katta boʻlsa chegirma bor — `True`.", "y = int(input())\nprint(y < 7 or y > 65)", "5", "30", "70"),
    PR("Kirish ruxsati", "Kirishda login va parol (ikki qator). Login `admin` va parol `1234` boʻlsa `True`.", 'print(input() == "admin" and input() == "1234")', "admin\n1234", "admin\n0000", "user\n1234"),
    PR("Uchburchak", "Kirishda uch tomon (bir qatorda). Har ikki tomon yigʻindisi uchinchisidan katta boʻlsa — uchburchak mavjud: `True`.", "a, b, c = map(int, input().split())\nprint(a + b > c and a + c > b and b + c > a)", "3 4 5", "1 2 3", "5 5 5"),
    PR("Kabisa yili", "Kirishda yil. Kabisa boʻlsa `True`: (4 ga boʻlinadi **va** 100 ga boʻlinmaydi) **yoki** 400 ga boʻlinadi.", "y = int(input())\nprint((y % 4 == 0 and y % 100 != 0) or y % 400 == 0)", "2024", "2100", "2000"),
    PR("Bitta musbat", "Kirishda ikki son. Aynan bittasi musbat boʻlsa `True` (`!=` dan foydalanib koʻring).", "a, b = map(int, input().split())\nprint((a > 0) != (b > 0))", "5 -3", "5 3", "-1 -1"),
    L("exercism", "ghost-gobble-arcade-game"),
    L("exercism", "leap"),
    L("lc", "check-if-the-sentence-is-pangram"),
    L("acmp", 4),
])

# ---------------------------------------------------------------- 3.5
TOPIC("is-in", "is va in operatorlari", "Bir xil obyektmi? Ichida bormi?", 15, r'''
## in — aʼzolik operatori
`in` qiymat satrda, roʻyxatda yoki boshqa toʻplamda borligini tekshiradi. `not in` — yoʻqligini.

```py
print("a" in "salom")
print(3 in [1, 2, 3])
print("Ali" not in ["Vali", "Gani"])
```

Lugʻatda `in` **kalitlarni** tekshiradi:

```py
narxlar = {"non": 4000, "sut": 12000}
print("non" in narxlar)
print(4000 in narxlar)
```

## Amaliy: unli harf yoki taqiqlangan soʻz
```py
xabar = "bu juda yomon soʻz"
taqiq = ["yomon", "ahmoq"]
for soz in xabar.split():
    if soz in taqiq:
        print("Taqiqlangan soʻz topildi:", soz)
```

## is — bir xil obyektmi
`==` qiymatlar tengligini, `is` esa **bitta obyekt** ekanini tekshiradi.

```py
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b)
print(a is b)
print(a is c)
```

`a` va `b` — teng, lekin ikki xil roʻyxat. `c` esa `a` ning oʻzi (bitta roʻyxatga ikki nom). Shuning uchun `c` ni oʻzgartirsak, `a` ham oʻzgaradi:

```py
a = [1, 2, 3]
c = a
c.append(4)
print(a)
```

## Qachon is ishlatiladi
Asosan `None` bilan: `x is None`, `x is not None`.

```py
natija = None
if natija is None:
    print("Hali natija yoʻq")
```

!> Sonlar va satrlarni `is` bilan solishtirmang — `==` ishlating. `is` faqat "aynan oʻsha obyekt"ni tekshiradi.

## Esda tuting
- `in` / `not in` — ichida bormi.
- Lugʻatda `in` faqat kalitlarni koʻradi.
- `is` — bitta obyektmi; asosan `is None` uchun.
''', [
    P('print("lo" in "salom")', "False", "lo", "Xato"),
    P('print(5 in [1, 2, 3])', "True", "None", "Xato"),
    P('d = {"a": 1}\nprint(1 in d)', "True", "1", "Xato"),
    P('a = [1]\nb = [1]\nprint(a == b, a is b)', "True True", "False False", "False True"),
    P('a = [1, 2]\nb = a\nb.append(3)\nprint(a)', "[1, 2]", "[3]", "[1, 2, [3]]"),
    P('print("A" not in "abc")', "False", "A", "Xato"),
    P('x = None\nprint(x is None, x == 0)', "True True", "False True", "None False"),
    Q("`x` qiymati `None` ekanini tekshirishning tavsiya etilgan usuli?", "x is None", "x == None", "x in None", "None(x)"),
    Q("`{\"ism\": \"Ali\"}` lugʻatida `\"Ali\" in d` nima qaytaradi?", "False", "True", "Xato", "\"ism\"", why="`in` lugʻatda kalitlarni tekshiradi, qiymatlarni emas."),
    PR("Unli harfmi", "Kirishda bitta kichik harf. Agar u `aeiou` dan biri boʻlsa `unli`, aks holda `undosh`.", 'h = input()\nprint("unli" if h in "aeiou" else "undosh")', "a", "b", "u"),
    PR("Roʻyxatda bormi", "Kirishda sonlar (bir qatorda) va izlanayotgan son (ikkinchi qatorda). Bor boʻlsa `True`.", "a = input().split()\nprint(input() in a)", "1 2 3\n2", "5 6\n7", "10\n10"),
    PR("Taqiqlangan soʻz", "Taqiqlangan soʻzlar: `yomon`, `ahmoq`. Kirishda gap. Gapda ulardan biri alohida soʻz sifatida boʻlsa `BLOK`, aks holda `OK`.", 'taqiq = ["yomon", "ahmoq"]\nok = True\nfor s in input().split():\n    if s in taqiq:\n        ok = False\nprint("OK" if ok else "BLOK")', "bu yomon fikr", "bu yaxshi fikr", "ahmoq"),
    PR("Email", "Kirishda matn. Unda `@` boʻlsa va boʻsh joy boʻlmasa `True`.", 's = input()\nprint("@" in s and " " not in s)', "ali@mirae.uz", "ali mirae.uz", "a@b c"),
    PR("Kalit bormi", "Lugʻat: `{\"non\": 4000, \"sut\": 12000, \"tuxum\": 1500}`. Kirishda mahsulot nomi. Bor boʻlsa narxini, yoʻq boʻlsa `yoq` chiqaring.", 'd = {"non": 4000, "sut": 12000, "tuxum": 1500}\ns = input()\nprint(d[s] if s in d else "yoq")', "non", "choy", "tuxum"),
    PR("Takrorsiz", "Kirishda soʻzlar (bir qatorda). Har bir soʻzni faqat birinchi uchraganda, kelish tartibida bir qatorda chiqaring (`not in` dan foydalaning).", "natija = []\nfor s in input().split():\n    if s not in natija:\n        natija.append(s)\nprint(*natija)", "a b a c b", "x x x", "bir ikki uch"),
    PR("Ruxsat etilgan foydalanuvchi", "Ruxsat etilganlar: `ali`, `vali`, `gani`. Kirishda login. Roʻyxatda boʻlsa `xush kelibsiz`, aks holda `ruxsat yoq`.", 'ruxsat = ["ali", "vali", "gani"]\nprint("xush kelibsiz" if input() in ruxsat else "ruxsat yoq")', "vali", "hasan", "ali"),
    L("lc", "jewels-and-stones"),
    L("lc", "contains-duplicate"),
    L("exercism", "pangram"),
    L("acmp", 82),
])

# ---------------------------------------------------------------- 3.6
TOPIC("bitli", "Bitli operatorlar", "&  |  ^  ~  <<  >> — sonlar ichidagi bitlar bilan ishlash", 20, r'''
Kompyuter har bir sonni **ikkilik** koʻrinishda — 0 va 1 lar bilan saqlaydi. Masalan `13 = 1101₂`. Bitli operatorlar aynan shu bitlar ustida ishlaydi.

```py
print(bin(13))
print(int("1101", 2))
print(f"{13:08b}")
```

| Operator | Nomi | Qoida |
|---|---|---|
| `&` | VA | ikkalasi 1 boʻlsa — 1 |
| `\|` | YOKI | bittasi 1 boʻlsa — 1 |
| `^` | XOR | har xil boʻlsa — 1 |
| `~` | inkor | `~x = -x - 1` |
| `<<` | chapga surish | `x << k = x * 2**k` |
| `>>` | oʻngga surish | `x >> k = x // 2**k` |

```py
a, b = 12, 10      # 1100 va 1010
print(a & b)       # 1000
print(a | b)       # 1110
print(a ^ b)       # 0110
print(~a)
print(a << 2, a >> 2)
```

## Amaliy qoʻllanishlar
**Juft-toqlik** — eng kichik bit:

```py
for n in [4, 7]:
    print(n, "toq" if n & 1 else "juft")
```

**2 ning darajasi** — tez koʻpaytirish va boʻlish:

```py
print(1 << 10)
print(1000 >> 1)
```

**XOR bilan almashtirish va takrorsiz sonni topish:**

```py
sonlar = [4, 1, 2, 1, 2]
x = 0
for n in sonlar:
    x ^= n
print("Juftsiz son:", x)
```

**Bitlar soni:**

```py
print(bin(255).count("1"))
```

> Bitli amallar olimpiadada, kriptografiyada va tarmoq dasturlashda koʻp uchraydi. Boshlanishda `&`, `|`, `^`, `<<`, `>>` maʼnosini bilish yetarli.

## Esda tuting
- `bin(x)` — ikkilik koʻrinish; `int(s, 2)` — orqaga.
- `x & 1` — toqmi; `x << k` — `2**k` ga koʻpaytirish.
- `a ^ a = 0` — XOR ning asosiy xossasi.
''', [
    P('print(6 & 3)', "7", "5", "9"),
    P('print(6 | 3)', "2", "5", "9"),
    P('print(6 ^ 3)', "2", "7", "9"),
    P('print(1 << 4)', "4", "5", "8"),
    P('print(100 >> 2)', "50", "400", "98"),
    P('print(bin(10))', "1010", "0x1010", "10"),
    P('print(5 ^ 5, 7 ^ 0)', "10 7", "1 0", "0 0"),
    Q("`x & 1` nimani tekshiradi?", "Son toqligini", "Son musbatligini", "Son 1 ga tengligini", "Son 2 ning darajasi ekanini"),
    Q("`x << 3` nimaga teng?", "x * 8", "x * 3", "x + 3", "x // 8"),
    PR("Ikkilik", "Kirishda son. Uning ikkilik koʻrinishini `0b` siz chiqaring.", "print(bin(int(input()))[2:])", "13", "1", "255"),
    PR("Oʻnlikka", "Kirishda ikkilik satr. Uni oʻnlik songa aylantiring.", "print(int(input(), 2))", "1101", "1", "100000"),
    PR("Birlar soni", "Kirishda son. Ikkilik koʻrinishidagi `1` lar sonini chiqaring.", 'print(bin(int(input())).count("1"))', "7", "8", "1023"),
    PR("Juft yoki toq", "Kirishda son. `& 1` yordamida `juft` yoki `toq` chiqaring.", 'print("toq" if int(input()) & 1 else "juft")', "4", "7", "0"),
    PR("2 ning darajasi", "Kirishda k. `1 << k` ni chiqaring.", "print(1 << int(input()))", "0", "10", "40"),
    PR("Yolgʻiz son", "Kirishda sonlar (bir qatorda): bittasidan tashqari hammasi ikki martadan uchraydi. Yolgʻiz sonni XOR bilan toping.", "x = 0\nfor n in input().split():\n    x ^= int(n)\nprint(x)", "4 1 2 1 2", "7", "9 3 9"),
    PR("Hamming masofasi", "Kirishda ikki son. Ularning ikkilik koʻrinishida nechta bit farq qilishini chiqaring (`^` va `count`).", 'a, b = map(int, input().split())\nprint(bin(a ^ b).count("1"))', "1 4", "7 7", "0 255"),
    L("lc", "number-of-1-bits"),
    L("lc", "single-number"),
    L("lc", "hamming-distance"),
    L("cses", 1146),
])

# ---------------------------------------------------------------- 3.7
TOPIC("ternar", "Ternar operator", "Bir qatorli shart: A if shart else B", 10, r'''
**Ternar operator** — `if/else` ni bitta ifodaga sigʻdiradi. U qiymat qaytaradi, shuning uchun uni oʻzgaruvchiga berish yoki `print` ichida ishlatish mumkin.

```py
yosh = 20
holat = "katta" if yosh >= 18 else "yosh"
print(holat)
```

Oʻqilishi: *"katta", agar yosh >= 18 boʻlsa, aks holda "yosh"*.

## Oddiy if bilan solishtirish
```py
ball = 72

# Oddiy if
if ball >= 60:
    natija = "oʻtdi"
else:
    natija = "yiqildi"
print(natija)

# Ternar
print("oʻtdi" if ball >= 60 else "yiqildi")
```

## f-satr ichida
```py
son = 7
print(f"{son} — {'juft' if son % 2 == 0 else 'toq'}")
```

## Eng katta va mutlaq qiymat
```py
a, b = 15, 22
kattasi = a if a > b else b
print(kattasi)
x = -9
print(x if x >= 0 else -x)
```

## Zanjir (ehtiyot bilan)
```py
harorat = 15
print("issiq" if harorat > 25 else "iliq" if harorat > 10 else "sovuq")
```

!> Ikki darajadan ortiq zanjir oʻqishni qiyinlashtiradi. Bunday hollarda oddiy `if/elif/else` yozing.

## Esda tuting
- `A if shart else B` — shart rost boʻlsa A, aks holda B.
- `else` qismi majburiy.
- Qisqa holatlar uchun qulay; murakkablarida — oddiy `if`.
''', [
    P('x = 5\nprint("musbat" if x > 0 else "manfiy")', "manfiy", "True", "x"),
    P('n = 4\nprint("toq" if n % 2 else "juft")', "toq", "0", "Xato"),
    P('a, b = 3, 8\nprint(a if a > b else b)', "3", "True", "3 8"),
    P('x = -6\nprint(x if x >= 0 else -x)', "-6", "0", "x"),
    P('t = 5\nprint("issiq" if t > 25 else "iliq" if t > 10 else "sovuq")', "iliq", "issiq", "Xato"),
    P('s = ""\nprint(s if s else "boʻsh")', "\"\"", "None", "Xato"),
    P('print(10 if False else 20)', "10", "False", "Xato"),
    Q("Ternar operatorning toʻgʻri yozilishi qaysi?", "x if shart else y", "shart ? x : y", "if shart x else y", "x else y if shart"),
    Q("Ternar operatorda qaysi qism majburiy?", "else qismi ham", "Faqat if qismi", "elif qismi", "Qavslar"),
    PR("Juft-toq", "Kirishda son. Ternar operator bilan `juft` yoki `toq` chiqaring.", 'n = int(input())\nprint("juft" if n % 2 == 0 else "toq")', "4", "7", "0"),
    PR("Kattasi", "Kirishda ikki son. Ternar bilan kattasini chiqaring (`max` ishlatmang).", "a, b = map(int, input().split())\nprint(a if a > b else b)", "3 8", "10 2", "5 5"),
    PR("Modul", "Kirishda son. Ternar bilan uning mutlaq qiymatini chiqaring (`abs` ishlatmang).", "x = int(input())\nprint(x if x >= 0 else -x)", "-6", "9", "0"),
    PR("Imtihon", "Kirishda ball. 60 va undan katta boʻlsa `oʻtdi`, aks holda `yiqildi`.", 'b = int(input())\nprint("oʻtdi" if b >= 60 else "yiqildi")', "60", "45", "100"),
    PR("Belgisi", "Kirishda son. Musbat boʻlsa `+`, manfiy boʻlsa `-`, nol boʻlsa `0`.", 'x = int(input())\nprint("+" if x > 0 else "-" if x < 0 else "0")', "5", "-3", "0"),
    PR("Koʻplik", "Kirishda olmalar soni. `1 ta olma` yoki `N ta olmalar` (1 dan farqli boʻlsa) chiqaring.", 'n = int(input())\nprint(f"{n} ta {\'olma\' if n == 1 else \'olmalar\'}")', "1", "5", "0"),
    PR("Narx", "Kirishda yosh. 12 dan kichiklarga chipta 5000, qolganlarga 10000. Narxni chiqaring.", "y = int(input())\nprint(5000 if y < 12 else 10000)", "8", "12", "40"),
    L("exercism", "black-jack"),
    L("lc", "fizz-buzz"),
    L("acmp", 25),
    L("acmp", 272),
])

# ---------------------------------------------------------------- 3.8
TOPIC("ustuvorlik", "Operatorlar ustuvorligi", "Qaysi amal birinchi bajariladi", 15, r'''
`2 + 3 * 4` — 20 mi yoki 14 mi? Matematikadagi kabi, Pythonda ham amallarning **ustuvorligi** bor.

## Ustuvorlik jadvali (yuqoridan pastga)
| Daraja | Operatorlar |
|---|---|
| 1 | `( )` qavslar |
| 2 | `**` daraja |
| 3 | `+x`, `-x`, `~x` (unar) |
| 4 | `*`, `/`, `//`, `%` |
| 5 | `+`, `-` |
| 6 | `<<`, `>>` |
| 7 | `&` |
| 8 | `^` |
| 9 | `\|` |
| 10 | `==`, `!=`, `<`, `>`, `<=`, `>=`, `is`, `in` |
| 11 | `not` |
| 12 | `and` |
| 13 | `or` |

```py
print(2 + 3 * 4)
print((2 + 3) * 4)
print(10 - 4 - 3)
print(2 ** 3 ** 2)
```

## Chapdan oʻngga va oʻngdan chapga
Koʻp operatorlar chapdan oʻngga bajariladi: `10 - 4 - 3 = (10 - 4) - 3`. Lekin `**` oʻngdan chapga: `2 ** 3 ** 2 = 2 ** 9`.

## Manfiy son va daraja
```py
print(-3 ** 2)
print((-3) ** 2)
```

!> `-3 ** 2` — bu `-(3 ** 2) = -9`. Manfiy sonni darajaga koʻtarishda qavs qoʻying.

## Arifmetika va taqqoslash
Arifmetika avval, taqqoslash keyin, mantiq oxirida:

```py
x = 7
print(x + 1 > 5 and x % 2 == 1)
```

## Oʻrtacha qiymat — klassik xato
```py
a, b = 4, 6
print(a + b / 2)
print((a + b) / 2)
```

> Qoida: ustuvorlikni eslay olmasangiz — qavs qoʻying. Qavslar hech qachon zarar qilmaydi.

## Esda tuting
- `**` → `*` `/` `//` `%` → `+` `-` → taqqoslash → `not` → `and` → `or`.
- `**` oʻngdan chapga hisoblanadi.
- `-3 ** 2 = -9`, `(-3) ** 2 = 9`.
''', [
    P('print(2 + 3 * 4)', "20", "24", "9"),
    P('print(10 - 4 - 3)', "9", "-3", "1 "),
    P('print(-2 ** 2)', "4", "-2", "2"),
    P('print(20 / 4 * 2)', "2.5", "10", "40"),
    P('a, b = 4, 6\nprint(a + b / 2)', "5.0", "5", "10"),
    P('print(2 * 3 ** 2)', "36", "12", "64"),
    P('print(1 + 2 == 3 and 2 * 2 == 5)', "True", "3", "Xato"),
    Q("`(a + b) / 2` va `a + b / 2` farqi nimada?", "Birinchisida avval qoʻshiladi, ikkinchisida avval boʻlinadi", "Farqi yoʻq", "Ikkinchisi xato beradi", "Birinchisi butun son qaytaradi"),
    Q("Quyidagilardan qaysi biri eng yuqori ustuvorlikka ega?", "**", "*", "+", "and"),
    PR("Oʻrtacha", "Kirishda ikki son. Ularning oʻrtachasini chiqaring (qavslarni unutmang!).", "a, b = map(int, input().split())\nprint((a + b) / 2)", "4 6", "1 2", "-5 5"),
    PR("Formula", "Kirishda x. `3x² + 2x + 1` ni hisoblang.", "x = int(input())\nprint(3 * x ** 2 + 2 * x + 1)", "2", "0", "-3"),
    PR("Manfiy kvadrat", "Kirishda son (manfiy boʻlishi mumkin). Uning kvadratini chiqaring (`**` bilan, qavsga ehtiyot boʻling).", "x = int(input())\nprint(x ** 2)", "-3", "4", "0"),
    PR("Diskriminant", "Kirishda `a b c` (bir qatorda). `D = b² - 4ac` ni chiqaring.", "a, b, c = map(int, input().split())\nprint(b ** 2 - 4 * a * c)", "1 -3 2", "1 2 1", "2 1 5"),
    PR("Yuza", "Kirishda trapetsiya asoslari va balandligi `a b h`. Yuzani `(a + b) * h / 2` bilan chiqaring.", "a, b, h = map(int, input().split())\nprint((a + b) * h / 2)", "3 5 4", "1 1 1", "10 0 5"),
    PR("Foizli qoʻshimcha", "Kirishda narx va foiz (bir qatorda). Yangi narx: `narx + narx * foiz / 100` — natijani `int()` qilib chiqaring.", "n, f = map(int, input().split())\nprint(int(n + n * f / 100))", "100000 12", "5000 0", "999 50"),
    PR("Masofa", "Kirishda `x1 y1 x2 y2`. Ikki nuqta orasidagi masofani `((x2-x1)**2 + (y2-y1)**2) ** 0.5` bilan chiqaring.", "x1, y1, x2, y2 = map(int, input().split())\nprint(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)", "0 0 3 4", "1 1 1 1", "-1 -1 2 3"),
    L("lc", "convert-the-temperature"),
    L("acmp", 10),
    L("acmp", 277),
    L("exercism", "currency-exchange"),
])

# ---------------------------------------------------------------- 3.9
TOPIC("zanjir", "Zanjirli taqqoslash", "1 < x < 10 — Pythonning chiroyli imkoniyati", 10, r'''
Matematikada `1 < x < 10` deb yozamiz. Koʻp tillarda buni `1 < x && x < 10` deb yozish kerak. Python esa matematik yozuvni toʻgʻridan-toʻgʻri tushunadi!

```py
x = 5
print(1 < x < 10)
print(10 < x < 20)
```

## Qanday ishlaydi
`a < b < c` — bu `a < b and b < c` bilan bir xil. Faqat `b` bir marta hisoblanadi.

```py
yosh = 16
print(13 <= yosh <= 19)
```

## Boshqa operatorlar bilan
```py
a = b = c = 7
print(a == b == c)
x, y, z = 1, 5, 3
print(x < y > z)
```

`x < y > z` — `x < y and y > z` degani. Toʻgʻri, lekin chalkash — bunday yozmang.

## Amaliy misollar
```py
def baho(ball):
    if 86 <= ball <= 100:
        return 5
    elif 71 <= ball <= 85:
        return 4
    elif 56 <= ball <= 70:
        return 3
    return 2

print(baho(90), baho(75), baho(40))
```

```py
soat = 14
print("Ish vaqti:", 9 <= soat < 18)
```

!> `1 < x < 10` — toʻgʻri; `x > 1 < 10` ham ishlaydi, lekin maʼnosi chalkash. Doim kichikdan kattaga yozing.

## Esda tuting
- `a < b < c` = `a < b and b < c`.
- Oraliqni tekshirishning eng oʻqiladigan usuli.
- `a == b == c` — uchala qiymat tengligi.
''', [
    P('x = 5\nprint(1 < x < 10)', "False", "1", "Xato"),
    P('x = 15\nprint(1 < x < 10)', "True", "15", "Xato"),
    P('print(3 == 3 == 3.0)', "False", "3", "Xato"),
    P('print(1 < 3 > 2)', "False", "Xato", "3"),
    P('y = 18\nprint(18 <= y < 25)', "False", "18", "Xato"),
    P('print(5 < 5 <= 10)', "True", "5", "Xato"),
    P('a, b, c = 1, 2, 2\nprint(a < b == c)', "False", "2", "Xato"),
    Q("`a < b < c` qaysi ifodaga teng?", "a < b and b < c", "a < b or b < c", "a < c", "(a < b) < c"),
    Q("Yosh 13 dan 19 gacha (ikkalasi ham kiradi) ekanini eng chiroyli tekshirish?", "13 <= yosh <= 19", "yosh >= 13 or yosh <= 19", "yosh in 13..19", "13 < yosh < 19"),
    PR("Oraliq", "Kirishda son. 1 dan 100 gacha (ikkalasi kiradi) boʻlsa `True` — zanjirli taqqoslash bilan.", "x = int(input())\nprint(1 <= x <= 100)", "1", "101", "50"),
    PR("Ish vaqti", "Kirishda soat (0–23). 9 va 18 orasida (9 kiradi, 18 kirmaydi) boʻlsa `ochiq`, aks holda `yopiq`.", 'h = int(input())\nprint("ochiq" if 9 <= h < 18 else "yopiq")', "9", "18", "13"),
    PR("Baho", "Kirishda ball. 86–100 → 5, 71–85 → 4, 56–70 → 3, qolgani → 2.", "b = int(input())\nif 86 <= b <= 100:\n    print(5)\nelif 71 <= b <= 85:\n    print(4)\nelif 56 <= b <= 70:\n    print(3)\nelse:\n    print(2)", "90", "71", "30"),
    PR("Oʻsuvchi", "Kirishda uch son. Ular qatʼiy oʻsuvchi tartibda boʻlsa `True` (`a < b < c`).", "a, b, c = map(int, input().split())\nprint(a < b < c)", "1 2 3", "1 1 2", "3 2 1"),
    PR("Harf", "Kirishda bitta belgi. U kichik lotin harfi boʻlsa (`\"a\" <= ch <= \"z\"`) `True`.", 'ch = input()\nprint("a" <= ch <= "z")', "q", "Q", "5"),
    PR("Teng tomonli", "Kirishda uch tomon. Uchalasi teng boʻlsa `teng tomonli`, aks holda `yoq`.", 'a, b, c = map(int, input().split())\nprint("teng tomonli" if a == b == c else "yoq")', "5 5 5", "5 5 6", "1 1 1"),
    PR("BMI", "Kirishda vazn (kg) va boʻy (sm). BMI = vazn / (boʻy/100)². 18.5 ≤ BMI < 25 boʻlsa `normal`, aks holda `normal emas`.", 'v, b = map(int, input().split())\nbmi = v / (b / 100) ** 2\nprint("normal" if 18.5 <= bmi < 25 else "normal emas")', "70 175", "50 180", "100 170"),
    L("exercism", "darts"),
    L("lc", "count-odd-numbers-in-an-interval-range"),
    L("acmp", 205),
    L("acmp", 336),
])

# ---------------------------------------------------------------- 3.10
TOPIC("qisqa-tutashuv", "Qisqa tutashuv (short-circuit)", "and / or natijani qanday tez hisoblaydi", 15, r'''
`and` va `or` dangasa: natija aniq boʻlishi bilan qolgan qismni **hisoblamaydi**. Bu **qisqa tutashuv** deyiladi.

- `A and B` — agar `A` yolgʻon boʻlsa, `B` ga qaramaydi (natija baribir yolgʻon).
- `A or B` — agar `A` rost boʻlsa, `B` ga qaramaydi (natija baribir rost).

```py
def tekshir(nom, qiymat):
    print("tekshirildi:", nom)
    return qiymat

print(tekshir("A", False) and tekshir("B", True))
print("---")
print(tekshir("A", True) or tekshir("B", False))
```

## Xatodan himoya
Qisqa tutashuv xavfli amallarni xavfsiz qiladi:

```py
x = 0
print(x != 0 and 10 / x > 1)
```

`x != 0` yolgʻon — shuning uchun `10 / x` umuman bajarilmaydi, nolga boʻlish xatosi yoʻq.

```py
ism = ""
print(len(ism) > 0 and ism[0] == "A")
```

## and va or qiymat qaytaradi
Ular har doim `True`/`False` emas, **oxirgi tekshirilgan qiymatni** qaytaradi:

```py
print(0 or 5)
print("" or "Mehmon")
print(3 and 7)
print(0 and 7)
```

## Standart qiymat berish
```py
kiritilgan = ""
ism = kiritilgan or "Mehmon"
print("Salom,", ism)
```

> `x or "standart"` — juda koʻp ishlatiladigan andoza. Lekin `0` ham yolgʻon: agar `0` toʻgʻri qiymat boʻlishi mumkin boʻlsa, `if x is None` ishlating.

## Esda tuting
- `and` birinchi yolgʻonda, `or` birinchi rostda toʻxtaydi.
- `x != 0 and a / x` — nolga boʻlishdan himoya.
- `a or b` — `a` rost boʻlsa `a`, aks holda `b`.
''', [
    P('print(0 or 7)', "True", "0", "False"),
    P('print(5 and 9)', "True", "5", "14"),
    P('print("" or "Mehmon")', "\"\"", "True", "Xato"),
    P('x = 0\nprint(x != 0 and 10 / x)', "Xato", "0", "10"),
    P('print(None or 0 or "x")', "None", "0", "True"),
    P('print(0 and 1 / 0)', "Xato", "1", "False"),
    P('def f():\n    print("chaqirildi")\n    return True\nprint(True or f())', "chaqirildi\nTrue", "chaqirildi", "False"),
    Q("`A and B` ifodasida B qachon hisoblanmaydi?", "A yolgʻon boʻlsa", "A rost boʻlsa", "Hech qachon", "Doim hisoblanadi"),
    Q("`ism = kiritilgan or \"Mehmon\"` — `kiritilgan = \"\"` boʻlsa, `ism` nima boʻladi?", "Mehmon", "\"\"", "True", "None"),
    PR("Mehmon", "Kirishda ism (boʻsh boʻlishi mumkin). `or` bilan: boʻsh boʻlsa `Mehmon`, aks holda ismning oʻzi. `Salom, X` chiqaring.", 'print("Salom,", input() or "Mehmon")', "Ali", "", "Zarina"),
    PR("Xavfsiz boʻlish", "Kirishda `a b`. `b != 0 and a / b > 1` natijasini chiqaring — nolga boʻlish xatosi chiqmasin.", "a, b = map(int, input().split())\nprint(b != 0 and a / b > 1)", "10 2", "5 0", "1 5"),
    PR("Birinchi harf", "Kirishda soʻz (boʻsh boʻlishi mumkin). Soʻz boʻsh boʻlmasa va `A` bilan boshlansa `True` (qisqa tutashuvdan foydalaning).", 's = input()\nprint(len(s) > 0 and s[0] == "A")', "Ali", "", "Vali"),
    PR("Standart son", "Kirishda bir qator. Agar u boʻsh boʻlsa `10`, aks holda kiritilgan sonni ishlating. Natijaning ikki baravarini chiqaring.", 'print(int(input() or "10") * 2)', "", "7", "0"),
    PR("Birinchi rost", "Kirishda uch soʻz (bir qatorda; boʻsh oʻrin `-` bilan beriladi). `-` ni boʻsh satrga almashtirib, `a or b or c` natijasini chiqaring; hammasi boʻsh boʻlsa `hech narsa`.", 'a, b, c = [x if x != "-" else "" for x in input().split()]\nprint(a or b or c or "hech narsa")', "- olma nok", "- - -", "uzum - -"),
    PR("Shartli narx", "Kirishda narx va chegirma kodi (ikki qator, kod boʻsh boʻlishi mumkin). Kod `MIRAE` boʻlsa 10% chegirma. Yakuniy narxni (butun) chiqaring.", 'n = int(input())\nkod = input()\nprint(n - (kod == "MIRAE" and n // 10 or 0))', "50000\nMIRAE", "50000\n", "100\nXYZ"),
    PR("Qavslarsiz", "Kirishda son x. `x > 0 and x % 2 == 0 or x == -1` ni hisoblab chiqaring.", "x = int(input())\nprint(x > 0 and x % 2 == 0 or x == -1)", "4", "-1", "3"),
    L("exercism", "ghost-gobble-arcade-game"),
    L("lc", "valid-palindrome"),
    L("acmp", 35),
    L("acmp", 264),
])
