from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(5, "Funksiyalar", "Kodni qayta ishlatiladigan boʻlaklarga ajratish", "🧩")

# ---------------------------------------------------------------- 5.1
TOPIC("def", "Funksiya yaratish", "def, chaqirish va return", 20, r'''
**Funksiya** — nomlangan kod boʻlagi. Uni bir marta yozib, istalgancha chaqirish mumkin. Funksiyalar kodni qisqa, tartibli va qayta ishlatiladigan qiladi.

## def bilan yaratish
```py
def salomlash():
    print("Assalomu alaykum!")
    print("Mirae Academy ga xush kelibsiz")

salomlash()
salomlash()
```

`def` — funksiya yaratadi. Funksiya **chaqirilmaguncha** ishlamaydi.

## Parametr
Funksiyaga qiymat uzatish uchun qavs ichida **parametr** yoziladi:

```py
def salom(ism):
    print(f"Salom, {ism}!")

salom("Ali")
salom("Madina")
```

## return — natija qaytarish
`print` faqat ekranga chiqaradi. `return` esa natijani **qaytaradi** — uni oʻzgaruvchiga saqlash yoki boshqa hisobda ishlatish mumkin.

```py
def kvadrat(x):
    return x * x

natija = kvadrat(7)
print(natija)
print(kvadrat(3) + kvadrat(4))
```

!> `return` dan keyingi qatorlar bajarilmaydi — funksiya shu zahoti tugaydi.

```py
def tekshir(n):
    if n < 0:
        return "manfiy"
    return "musbat yoki nol"

print(tekshir(-5))
print(tekshir(10))
```

## print va return farqi
```py
def a(x):
    print(x * 2)

def b(x):
    return x * 2

natija1 = a(5)
natija2 = b(5)
print(natija1, natija2)
```

`a` hech narsa qaytarmagani uchun `natija1` — `None`.

## Docstring
Funksiya nima qilishini birinchi qatorda uch qoʻshtirnoq bilan yozish yaxshi odat:

```py
def yuza(a, b):
    """Toʻrtburchak yuzini qaytaradi."""
    return a * b

print(yuza(3, 4))
```

## Esda tuting
- `def nom(parametrlar):` — yaratish, `nom(qiymatlar)` — chaqirish.
- `return` natijani qaytaradi va funksiyani tugatadi.
- `return` boʻlmasa funksiya `None` qaytaradi.
''', [
    P('def f():\n    print("A")\nprint("B")', "A\nB", "A", "B\nA"),
    P('def f(x):\n    return x + 1\nprint(f(4))', "4", "x + 1", "None"),
    P('def f(x):\n    print(x)\ny = f(3)\nprint(y)', "3\n3", "3", "None"),
    P('def f(n):\n    return n * 2\n    print("salom")\nprint(f(5))', "10\nsalom", "salom\n10", "5"),
    P('def f(a, b):\n    return a - b\nprint(f(2, 10))', "8", "2 10", "Xato"),
    P('def kv(x):\n    return x * x\nprint(kv(kv(2)))', "4", "8", "Xato"),
    P('def f(n):\n    if n > 0:\n        return "+"\n    return "-"\nprint(f(0))', "+", "None", "0"),
    Q("`print` va `return` ning asosiy farqi?", "return qiymatni chaqiruvchiga qaytaradi, print faqat ekranga chiqaradi", "Ular bir xil", "print qiymatni saqlaydi", "return ekranga chiqaradi"),
    Q("`return` yozilmagan funksiya nima qaytaradi?", "None", "0", "\"\"", "Xato beradi"),
    F("Kvadrat", "`kvadrat(x)` funksiyasini yozing — x ning kvadratini qaytarsin.", "def kvadrat(x):\n    return x * x", "kvadrat(3)", "kvadrat(-4)", "kvadrat(0)", "kvadrat(1000)", lv=1),
    F("Yigʻindi", "`yigindi(a, b)` — ikki son yigʻindisini qaytaring.", "def yigindi(a, b):\n    return a + b", "yigindi(2, 3)", "yigindi(-1, 1)", "yigindi(100, 250)", lv=1),
    F("Juftmi", "`juftmi(n)` — n juft boʻlsa `True`, aks holda `False` qaytarsin.", "def juftmi(n):\n    return n % 2 == 0", "juftmi(4)", "juftmi(7)", "juftmi(0)", "juftmi(-2)", lv=1),
    F("Kattasi", "`kattasi(a, b)` — ikki sonning kattasini qaytaring (`max` ishlatmang).", "def kattasi(a, b):\n    if a > b:\n        return a\n    return b", "kattasi(3, 8)", "kattasi(10, 2)", "kattasi(5, 5)", "kattasi(-1, -7)"),
    F("Salomlashish", "`salom(ism)` — `\"Salom, ISM!\"` satrini qaytarsin (chiqarmasin!).", 'def salom(ism):\n    return f"Salom, {ism}!"', 'salom("Ali")', 'salom("Mirae")', 'salom("")'),
    F("Baho", "`baho(ball)` — 86+ → 5, 71+ → 4, 56+ → 3, aks holda 2 qaytarsin.", "def baho(ball):\n    if ball >= 86:\n        return 5\n    if ball >= 71:\n        return 4\n    if ball >= 56:\n        return 3\n    return 2", "baho(95)", "baho(71)", "baho(60)", "baho(10)"),
    F("Selsiy → Farengeyt", "`farengeyt(c)` — `c * 9 / 5 + 32` ni qaytarsin.", "def farengeyt(c):\n    return c * 9 / 5 + 32", "farengeyt(0)", "farengeyt(100)", "farengeyt(-40)", "farengeyt(36.6)"),
    L("exercism", "guidos-gorgeous-lasagna"),
    L("exercism", "two-fer"),
    L("lc", "convert-the-temperature"),
    L("exercism", "leap"),
])

# ---------------------------------------------------------------- 5.2
TOPIC("argumentlar", "Argumentlar va funksiya turlari", "Parametr va argument, bir nechta qiymat qaytarish, sof funksiyalar", 20, r'''
**Parametr** — funksiya taʼrifidagi nom. **Argument** — chaqirishda beriladigan qiymat.

```py
def toliq_ism(ism, familiya):     # ism, familiya — parametrlar
    return ism + " " + familiya

print(toliq_ism("Aziz", "Karimov"))  # "Aziz", "Karimov" — argumentlar
```

## Pozitsion argumentlar
Argumentlar tartib boʻyicha parametrlarga beriladi. Tartib muhim:

```py
def bolish(a, b):
    return a / b

print(bolish(10, 2))
print(bolish(2, 10))
```

!> Argumentlar soni parametrlar soniga mos kelmasa — `TypeError`.

## Bir nechta qiymat qaytarish
Python bir nechta qiymatni **kortej** sifatida qaytaradi:

```py
def statistika(sonlar):
    return min(sonlar), max(sonlar), sum(sonlar) / len(sonlar)

kichik, katta, ortacha = statistika([4, 9, 2, 7])
print(kichik, katta, ortacha)
```

## Funksiya turlari
- **Oʻrnatilgan** (built-in): `print`, `len`, `max`, `sorted` — tayyor.
- **Foydalanuvchi** funksiyalari — `def` bilan oʻzimiz yozganlar.
- **Sof funksiya** — faqat argumentlarga bogʻliq, tashqi narsani oʻzgartirmaydi. Ularni tekshirish oson.
- **Yon taʼsirli** funksiya — ekranga chiqaradi, faylga yozadi yoki global holatni oʻzgartiradi.

## Funksiya funksiyani chaqiradi
Katta masalani kichik funksiyalarga boʻlish — yaxshi dasturlashning asosi:

```py
def kvadrat(x):
    return x * x

def masofa(x1, y1, x2, y2):
    return (kvadrat(x2 - x1) + kvadrat(y2 - y1)) ** 0.5

print(masofa(0, 0, 3, 4))
```

## Roʻyxat argument sifatida
Roʻyxat funksiyaga uzatilsa, funksiya **oʻsha roʻyxat** bilan ishlaydi — uni oʻzgartirsa, tashqarida ham oʻzgaradi:

```py
def qosh(royxat):
    royxat.append(99)

a = [1, 2]
qosh(a)
print(a)
```

## Esda tuting
- Parametr — taʼrifdagi nom, argument — berilgan qiymat.
- `return a, b` — kortej qaytaradi; `x, y = f()` bilan ochiladi.
- Katta masalani kichik funksiyalarga boʻling.
''', [
    P('def f(a, b):\n    return a * 10 + b\nprint(f(1, 2), f(2, 1))', "12 12", "21 12", "3 3"),
    P('def f():\n    return 1, 2\nx = f()\nprint(x)', "1 2", "[1, 2]", "1"),
    P('def f():\n    return 3, 4\na, b = f()\nprint(b)', "3", "(3, 4)", "Xato"),
    P('def f(a, b):\n    return a + b\nprint(f(1))', "1", "None", "1 + b"),
    P('def g(x):\n    return x + 1\ndef f(x):\n    return g(x) * 2\nprint(f(3))', "7", "6", "4"),
    P('def f(r):\n    r.append(0)\na = [5]\nf(a)\nprint(a)', "[5]", "[0]", "[0, 5]"),
    P('print(len("salom"), max(3, 7), abs(-2))', "salom 7 2", "5 3 2", "5 7 -2"),
    Q("`def f(x, y):` dagi `x` va `y` nima deyiladi?", "Parametrlar", "Argumentlar", "Qaytariladigan qiymatlar", "Global oʻzgaruvchilar"),
    Q("`return a, b` qanday turdagi qiymat qaytaradi?", "tuple (kortej)", "list (roʻyxat)", "Faqat a ni", "Xato beradi"),
    F("Min va max", "`min_max(sonlar)` — roʻyxatning eng kichik va eng katta elementini kortej `(min, max)` qilib qaytarsin.", "def min_max(sonlar):\n    return min(sonlar), max(sonlar)", "min_max([3, 1, 4])", "min_max([7])", "min_max([-5, 0, 5])"),
    F("Oʻrtacha", "`ortacha(sonlar)` — roʻyxat elementlarining oʻrtachasini qaytaring.", "def ortacha(sonlar):\n    return sum(sonlar) / len(sonlar)", "ortacha([2, 4, 6])", "ortacha([5])", "ortacha([1, 2])"),
    F("Masofa", "`masofa(x1, y1, x2, y2)` — ikki nuqta orasidagi masofani qaytaring.", "def masofa(x1, y1, x2, y2):\n    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5", "masofa(0, 0, 3, 4)", "masofa(1, 1, 1, 1)", "masofa(-1, -1, 2, 3)"),
    F("Butun boʻlish", "`bolish(a, b)` — `(a // b, a % b)` kortejini qaytarsin.", "def bolish(a, b):\n    return a // b, a % b", "bolish(17, 5)", "bolish(10, 2)", "bolish(3, 7)"),
    F("Raqamlar yigʻindisi", "`raqamlar_yigindisi(n)` — natural son raqamlari yigʻindisini qaytarsin.", "def raqamlar_yigindisi(n):\n    s = 0\n    while n > 0:\n        s += n % 10\n        n //= 10\n    return s", "raqamlar_yigindisi(1234)", "raqamlar_yigindisi(9)", "raqamlar_yigindisi(1000)"),
    F("Uchburchak", "`uchburchakmi(a, b, c)` — shunday tomonli uchburchak mavjud boʻlsa `True`.", "def uchburchakmi(a, b, c):\n    return a + b > c and a + c > b and b + c > a", "uchburchakmi(3, 4, 5)", "uchburchakmi(1, 2, 3)", "uchburchakmi(5, 5, 5)"),
    F("Ikki funksiya", "`kub(x)` va `kublar_yigindisi(a, b)` yozing. Ikkinchisi birinchisidan foydalanib `a³ + b³` qaytarsin. Tekshiruv `kublar_yigindisi` ni chaqiradi.", "def kub(x):\n    return x ** 3\n\ndef kublar_yigindisi(a, b):\n    return kub(a) + kub(b)", "kublar_yigindisi(1, 2)", "kublar_yigindisi(0, 0)", "kublar_yigindisi(-2, 3)", starter="def kub(x):\n    pass\n\ndef kublar_yigindisi(a, b):\n    pass\n"),
    L("exercism", "card-games"),
    L("exercism", "high-scores"),
    L("lc", "richest-customer-wealth"),
    L("lc", "average-salary-excluding-the-minimum-and-maximum-salary"),
])

# ---------------------------------------------------------------- 5.3
TOPIC("kalitli", "Kalitli argumentlar", "nom=qiymat koʻrinishida argument berish", 15, r'''
Argumentni **nomi bilan** berish mumkin: `funksiya(parametr=qiymat)`. Bunda tartib muhim emas va kod oʻqilishi osonlashadi.

```py
def kredit(summa, oylar, foiz):
    jami = summa + summa * foiz / 100
    return round(jami / oylar)

print(kredit(12_000_000, 12, 20))
print(kredit(foiz=20, summa=12_000_000, oylar=12))
```

Ikkinchi chaqiruvda nima qaysi parametrga ketayotgani aniq koʻrinadi.

## Aralash berish
Pozitsion argumentlar **avval**, kalitli argumentlar **keyin** keladi:

```py
def tanishtir(ism, yosh, shahar):
    return f"{ism}, {yosh} yosh, {shahar}"

print(tanishtir("Laylo", shahar="Fargʻona", yosh=16))
```

```py xato
print(tanishtir(ism="Laylo", 16, "Fargʻona"))
```

!> Kalitli argumentdan keyin pozitsion argument yozib boʻlmaydi — `SyntaxError`.

## Oʻrnatilgan funksiyalarda
Siz allaqachon kalitli argument ishlatgansiz:

```py
print("a", "b", sep="-", end="!\n")
print(sorted([3, 1, 2], reverse=True))
print(round(3.14159, ndigits=2))
```

## Faqat kalit bilan (*)
`*` dan keyingi parametrlar faqat nomi bilan berilishi mumkin:

```py
def ulanish(server, *, port, xavfsiz):
    return f"{server}:{port} (xavfsiz={xavfsiz})"

print(ulanish("mirae.uz", port=443, xavfsiz=True))
```

Bu xatolarning oldini oladi: `ulanish("mirae.uz", 443, True)` — `True` nima ekani tushunarsiz.

## Esda tuting
- `f(x=1, y=2)` — nomi bilan, tartib muhim emas.
- Avval pozitsion, keyin kalitli.
- `*` dan keyingi parametrlar faqat kalit bilan.
''', [
    P('def f(a, b):\n    return a - b\nprint(f(b=1, a=10))', "-9", "Xato", "1 10"),
    P('def f(x, y, z):\n    return x + y * z\nprint(f(1, z=3, y=2))', "9", "5", "Xato"),
    P('print(sorted([3, 1, 2], reverse=True))', "[1, 2, 3]", "[2, 1, 3]", "Xato"),
    P('print("a", "b", sep="", end="!")', "a b!", "ab", "a b\n!"),
    P('def f(a, *, b):\n    return a * b\nprint(f(2, b=5))', "Xato", "7", "25"),
    P('def f(a, *, b):\n    return a * b\nprint(f(2, 5))', "10", "7", "2"),
    P('def f(ism, salom="Salom"):\n    return salom + ", " + ism\nprint(f(salom="Hey", ism="Ali"))', "Salom, Ali", "Ali, Hey", "Xato"),
    Q("Qaysi chaqiruv xato?", "f(a=1, 2)", "f(1, b=2)", "f(a=1, b=2)", "f(b=2, a=1)"),
    Q("Kalitli argumentlarning asosiy afzalligi?", "Kod oʻqilishi osonlashadi va tartib muhim boʻlmaydi", "Kod tezroq ishlaydi", "Xotira tejaladi", "Funksiya qisqaroq yoziladi"),
    F("Toʻliq ism", "`toliq_ism(ism, familiya)` — `\"Familiya Ism\"` qaytarsin. Tekshiruv kalitli argumentlar bilan chaqiradi.", 'def toliq_ism(ism, familiya):\n    return familiya + " " + ism', 'toliq_ism(familiya="Karimov", ism="Aziz")', 'toliq_ism(ism="Laylo", familiya="Rahimova")', 'toliq_ism("A", "B")', lv=1),
    F("Kredit", "`oylik(summa, oylar, foiz)` — `(summa + summa * foiz / 100) / oylar` ni `round` qilib qaytaring.", "def oylik(summa, oylar, foiz):\n    return round((summa + summa * foiz / 100) / oylar)", "oylik(12000000, 12, 20)", "oylik(foiz=0, oylar=10, summa=1000)", "oylik(summa=500000, foiz=10, oylar=3)"),
    F("Toʻrtburchak", "`yuza(eni, boyi)` — yuzani qaytarsin.", "def yuza(eni, boyi):\n    return eni * boyi", "yuza(eni=3, boyi=4)", "yuza(boyi=10, eni=2)", "yuza(5, 5)", lv=1),
    F("Faqat kalit bilan", "`narx(miqdor, *, dona_narxi)` — `miqdor * dona_narxi` qaytarsin. `dona_narxi` faqat nomi bilan berilsin.", "def narx(miqdor, *, dona_narxi):\n    return miqdor * dona_narxi", "narx(3, dona_narxi=4000)", "narx(0, dona_narxi=10)", "narx(3, 4000)"),
    F("Formatlash", "`kartochka(ism, yosh, shahar)` — `\"ISM (YOSH), SHAHAR\"` qaytarsin.", 'def kartochka(ism, yosh, shahar):\n    return f"{ism} ({yosh}), {shahar}"', 'kartochka("Ali", shahar="Xiva", yosh=17)', 'kartochka(yosh=9, ism="Sevara", shahar="Termiz")', 'kartochka("X", 1, "Y")'),
    F("Daraja", "`daraja(asos, korsatkich)` — `asos ** korsatkich` qaytarsin.", "def daraja(asos, korsatkich):\n    return asos ** korsatkich", "daraja(korsatkich=3, asos=2)", "daraja(asos=10, korsatkich=0)", "daraja(5, 2)", lv=1),
    F("Chegara", "`chegarala(x, *, past, yuqori)` — x ni `[past, yuqori]` oraligʻiga siqib qaytarsin.", "def chegarala(x, *, past, yuqori):\n    return max(past, min(x, yuqori))", "chegarala(15, past=0, yuqori=10)", "chegarala(-5, past=0, yuqori=10)", "chegarala(7, yuqori=10, past=0)"),
    L("exercism", "two-fer"),
    L("exercism", "lasagna" if False else "guidos-gorgeous-lasagna"),
    L("lc", "kids-with-the-greatest-number-of-candies"),
    L("lc", "shuffle-the-array"),
])

# ---------------------------------------------------------------- 5.4
TOPIC("standart", "Standart qiymatli argumentlar", "Berilmasa ishlatiladigan qiymatlar", 15, r'''
Parametrga **standart qiymat** berish mumkin. Chaqirishda argument berilmasa — shu qiymat ishlatiladi.

```py
def salom(ism, xabar="Xush kelibsiz"):
    return f"{xabar}, {ism}!"

print(salom("Ali"))
print(salom("Ali", "Qaytganingizdan xursandmiz"))
```

## Qoida: standartlilar oxirida
Standart qiymatli parametrlar oddiylaridan **keyin** yoziladi:

```py
def chegirma(narx, foiz=10, minimum=0):
    yangi = narx - narx * foiz // 100
    return max(yangi, minimum)

print(chegirma(50000))
print(chegirma(50000, 30))
print(chegirma(50000, foiz=90, minimum=20000))
```

## Siz bilgan misollar
`print(sep=" ", end="\n")`, `round(x, ndigits=None)`, `sorted(reverse=False)` — hammasida standart qiymatlar bor.

## Diqqat: oʻzgaruvchan standart qiymat
Standart qiymat funksiya yaratilganda **bir marta** hisoblanadi. Roʻyxat kabi oʻzgaruvchan qiymat ishlatilsa — kutilmagan natija:

```py
def qosh(element, royxat=[]):
    royxat.append(element)
    return royxat

print(qosh(1))
print(qosh(2))
```

Ikkinchi chaqiruvda yangi roʻyxat kutgan edik, lekin eski roʻyxat davom etdi! Toʻgʻri usul — `None`:

```py
def qosh(element, royxat=None):
    if royxat is None:
        royxat = []
    royxat.append(element)
    return royxat

print(qosh(1))
print(qosh(2))
```

!> Hech qachon `def f(x=[])` yoki `def f(x={})` yozmang — `None` dan foydalaning.

## Esda tuting
- `def f(a, b=5):` — `b` berilmasa 5.
- Standart qiymatli parametrlar oxirida turadi.
- Oʻzgaruvchan standart qiymat (`[]`, `{}`) oʻrniga `None`.
''', [
    P('def f(a, b=2):\n    return a * b\nprint(f(5))', "Xato", "5", "7"),
    P('def f(a, b=2):\n    return a * b\nprint(f(5, 3))', "10", "Xato", "8"),
    P('def f(x, y=1, z=1):\n    return x + y + z\nprint(f(1, z=5))', "6", "3", "Xato"),
    P('def f(x=[]):\n    x.append(1)\n    return x\nf()\nprint(f())', "[1]", "[]", "Xato"),
    P('def f(x=None):\n    if x is None:\n        x = []\n    x.append(1)\n    return x\nf()\nprint(f())', "[1, 1]", "[]", "None"),
    P('def f(ism="Mehmon"):\n    return "Salom, " + ism\nprint(f(""))', "Salom, Mehmon", "Salom,", "Xato"),
    P('print(round(2.567), round(2.567, 1))', "2 2.5", "2.567 2.6", "3 3"),
    Q("Qaysi taʼrif xato?", "def f(a=1, b):", "def f(a, b=1):", "def f(a=1, b=2):", "def f(a, b, c=0):"),
    Q("Nima uchun `def f(x=[])` xavfli?", "Roʻyxat bir marta yaratiladi va chaqiruvlar orasida saqlanib qoladi", "Roʻyxat standart qiymat boʻla olmaydi", "Sintaksis xatosi", "Funksiya sekinlashadi"),
    F("Salomlashish", "`salom(ism, xabar=\"Salom\")` — `\"XABAR, ISM!\"` qaytarsin.", 'def salom(ism, xabar="Salom"):\n    return f"{xabar}, {ism}!"', 'salom("Ali")', 'salom("Ali", "Xayr")', 'salom(xabar="Hey", ism="Vali")', lv=1),
    F("Daraja", "`daraja(x, n=2)` — `x ** n` qaytarsin (n berilmasa kvadrat).", "def daraja(x, n=2):\n    return x ** n", "daraja(5)", "daraja(2, 10)", "daraja(3, n=3)", lv=1),
    F("Chegirma", "`chegirma(narx, foiz=10)` — `narx - narx * foiz // 100` qaytarsin.", "def chegirma(narx, foiz=10):\n    return narx - narx * foiz // 100", "chegirma(50000)", "chegirma(50000, 30)", "chegirma(999, 0)"),
    F("Ajratuvchi", "`birlashtir(sozlar, ajratuvchi=\", \")` — roʻyxatdagi soʻzlarni ajratuvchi bilan bitta satrga yigʻsin.", 'def birlashtir(sozlar, ajratuvchi=", "):\n    return ajratuvchi.join(sozlar)', 'birlashtir(["a", "b", "c"])', 'birlashtir(["x", "y"], "-")', 'birlashtir([])'),
    F("Yaxlitlash", "`yaxlit(x, xona=0)` — `round(x, xona)` qaytarsin; xona 0 boʻlsa butun son (int) qaytsin.", "def yaxlit(x, xona=0):\n    if xona == 0:\n        return round(x)\n    return round(x, xona)", "yaxlit(3.7)", "yaxlit(3.14159, 2)", "yaxlit(2.5)"),
    F("Xavfsiz qoʻshish", "`qosh(element, royxat=None)` — royxat berilmasa yangi roʻyxat yaratib, elementni qoʻshib qaytarsin. Har bir chaqiruv mustaqil boʻlsin.", "def qosh(element, royxat=None):\n    if royxat is None:\n        royxat = []\n    royxat.append(element)\n    return royxat", "qosh(1)", "qosh(2)", "qosh(3, [1, 2])"),
    F("Oraliq yigʻindisi", "`oraliq(oxiri, boshi=1, qadam=1)` — `range(boshi, oxiri + 1, qadam)` yigʻindisini qaytarsin.", "def oraliq(oxiri, boshi=1, qadam=1):\n    return sum(range(boshi, oxiri + 1, qadam))", "oraliq(10)", "oraliq(10, 5)", "oraliq(10, qadam=2)"),
    L("exercism", "two-fer"),
    L("exercism", "high-scores"),
    L("lc", "number-of-good-pairs"),
    L("acmp", 59),
])

# ---------------------------------------------------------------- 5.5
TOPIC("args-kwargs", "*args va **kwargs", "Istalgancha argument qabul qiluvchi funksiyalar", 20, r'''
Baʼzan funksiya nechta argument olishi oldindan nomaʼlum. `print` ga 1 ta ham, 10 ta ham qiymat berish mumkin. Oʻzimiz ham shunday funksiya yoza olamiz.

## *args — istalgancha pozitsion argument
`*args` barcha qoʻshimcha argumentlarni **kortej** qilib yigʻadi:

```py
def yigindi(*sonlar):
    print("Kelganlar:", sonlar)
    return sum(sonlar)

print(yigindi(1, 2))
print(yigindi(5, 10, 15, 20))
print(yigindi())
```

> `args` — shunchaki odatiy nom. Muhimi — `*` belgisi.

## **kwargs — istalgancha kalitli argument
`**kwargs` kalitli argumentlarni **lugʻat** qilib yigʻadi:

```py
def profil(**maʼlumot):
    for kalit, qiymat in maʼlumot.items():
        print(f"{kalit}: {qiymat}")

profil(ism="Dilshod", yosh=18, shahar="Andijon")
```

## Hammasi birga
Tartib: oddiy parametrlar → `*args` → kalit-faqat → `**kwargs`.

```py
def buyurtma(mijoz, *mahsulotlar, yetkazish=False, **qoshimcha):
    print("Mijoz:", mijoz)
    print("Mahsulotlar:", ", ".join(mahsulotlar))
    print("Yetkazish:", yetkazish)
    print("Qoʻshimcha:", qoshimcha)

buyurtma("Aziza", "non", "sut", yetkazish=True, izoh="tez", qavat=3)
```

## Ochib berish (* va ** chaqirishda)
Roʻyxatni alohida argumentlarga, lugʻatni kalitli argumentlarga "ochish" mumkin:

```py
def toliq(ism, familiya):
    return ism + " " + familiya

qismlar = ["Rustam", "Qodirov"]
print(toliq(*qismlar))
d = {"familiya": "Saidova", "ism": "Nilufar"}
print(toliq(**d))
print(*[1, 2, 3], sep=" | ")
```

## Esda tuting
- `*args` → kortej, `**kwargs` → lugʻat.
- Chaqirishda `*roʻyxat` — elementlarga, `**lugʻat` — kalitli argumentlarga ochadi.
- Tartib: `a, *args, b=1, **kwargs`.
''', [
    P('def f(*a):\n    return len(a)\nprint(f(1, 2, 3))', "1", "6", "(1, 2, 3)"),
    P('def f(*a):\n    return a\nprint(f(1, 2))', "[1, 2]", "1 2", "3"),
    P('def f(**k):\n    return k\nprint(f(x=1, y=2))', "(1, 2)", "['x', 'y']", "x=1, y=2"),
    P('def f(a, *b):\n    return b\nprint(f(1, 2, 3))', "(1, 2, 3)", "1", "[2, 3]"),
    P('def f(a, b, c):\n    return a + b + c\nprint(f(*[1, 2, 3]))', "[1, 2, 3]", "Xato", "123"),
    P('def f(x, y):\n    return x - y\nprint(f(**{"y": 1, "x": 5}))', "-4", "Xato", "1 5"),
    P('print(*"abc")', "abc", "['a', 'b', 'c']", "*abc"),
    Q("`*args` qanday turda keladi?", "tuple", "list", "dict", "set"),
    Q("`**kwargs` qanday turda keladi?", "dict", "tuple", "list", "str"),
    F("Yigʻindi", "`yigindi(*sonlar)` — istalgancha sonning yigʻindisini qaytarsin.", "def yigindi(*sonlar):\n    return sum(sonlar)", "yigindi(1, 2, 3)", "yigindi()", "yigindi(10)", "yigindi(-1, 1, 5, 5)", lv=1),
    F("Eng uzun soʻz", "`eng_uzun(*sozlar)` — eng uzun soʻzni qaytarsin (teng boʻlsa birinchisini).", "def eng_uzun(*sozlar):\n    return max(sozlar, key=len)", 'eng_uzun("olma", "anor", "shaftoli")', 'eng_uzun("a")', 'eng_uzun("ab", "cd")'),
    F("Oʻrtacha", "`ortacha(*sonlar)` — oʻrtachani qaytarsin; son berilmasa `0`.", "def ortacha(*sonlar):\n    if not sonlar:\n        return 0\n    return sum(sonlar) / len(sonlar)", "ortacha(2, 4)", "ortacha()", "ortacha(1, 2, 3, 4)"),
    F("Kalitlar soni", "`necha(**k)` — nechta kalitli argument berilganini qaytarsin.", "def necha(**k):\n    return len(k)", "necha(a=1, b=2)", "necha()", "necha(x=0)", lv=1),
    F("Profil", "`profil(**m)` — kalitlarni alifbo tartibida saralab, `\"kalit=qiymat\"` larni `\"; \"` bilan birlashtirgan satr qaytarsin.", 'def profil(**m):\n    return "; ".join(f"{k}={m[k]}" for k in sorted(m))', 'profil(ism="Ali", yosh=17)', "profil()", 'profil(b=2, a=1, c=3)'),
    F("Koʻpaytuvchi", "`kopaytir(k, *sonlar)` — har bir sonni k ga koʻpaytirib, roʻyxat qaytarsin.", "def kopaytir(k, *sonlar):\n    return [k * x for x in sonlar]", "kopaytir(2, 1, 2, 3)", "kopaytir(10)", "kopaytir(-1, 5, 0)"),
    F("Ochib berish", "`uchburchak_perimetri(a, b, c)` yozing. Tekshiruv uni `*` bilan roʻyxatdan ochib chaqiradi.", "def uchburchak_perimetri(a, b, c):\n    return a + b + c", "uchburchak_perimetri(*[3, 4, 5])", "uchburchak_perimetri(*(1, 1, 1))", "uchburchak_perimetri(**{'a': 2, 'b': 2, 'c': 3})", lv=1),
    L("exercism", "locomotive-engineer"),
    L("lc", "running-sum-of-1d-array"),
    L("lc", "maximum-number-of-words-found-in-sentences"),
    L("acmp", 272),
])

# ---------------------------------------------------------------- 5.6
TOPIC("scope", "Koʻrinish sohasi (scope)", "LEGB qoidasi, global va nonlocal", 20, r'''
**Koʻrinish sohasi** (scope) — oʻzgaruvchi qayerda koʻrinishini belgilaydi. Python nomni qidirganda **LEGB** tartibiga amal qiladi:

| Harf | Soha | Qayerda |
|---|---|---|
| L | Local | joriy funksiya ichida |
| E | Enclosing | tashqi (oʻrab turgan) funksiyada |
| G | Global | modul (fayl) darajasida |
| B | Built-in | Pythonning oʻzida: `len`, `print`… |

```py
x = "global"

def tashqi():
    x = "tashqi"
    def ichki():
        x = "ichki"
        print(x)
    ichki()
    print(x)

tashqi()
print(x)
```

Har bir funksiya oʻzining `x` ini koʻradi.

## Qidiruv tashqariga qarab ketadi
Ichki funksiyada nom topilmasa, Python tashqi sohalarga qaraydi:

```py
narx = 10000

def chek():
    soni = 3
    def jami():
        return narx * soni   # soni — E, narx — G
    return jami()

print(chek())
```

## global va nonlocal
Tashqi oʻzgaruvchini **oʻzgartirish** uchun:
- `global` — global oʻzgaruvchi uchun,
- `nonlocal` — tashqi funksiyadagi oʻzgaruvchi uchun.

```py
def hisoblagich():
    son = 0
    def bosish():
        nonlocal son
        son += 1
        return son
    bosish()
    bosish()
    return bosish()

print(hisoblagich())
```

## Klassik xato: UnboundLocalError
```py xato
balans = 100

def xarid():
    balans -= 30   # balans lokal deb hisoblanadi, lekin hali qiymati yoʻq
    return balans

print(xarid())
```

Funksiya ichida oʻzgaruvchiga qiymat berilsa, Python uni **butun funksiya boʻyicha lokal** deb hisoblaydi.

## Built-in nomlarni "yopib qoʻymang"
```py
sonlar = [3, 1, 2]
list_ = list(sonlar)  # yaxshi
print(sorted(list_))
```

!> `list = [1, 2]`, `sum = 0`, `max = 5` kabi nomlar oʻrnatilgan funksiyalarni yashirib qoʻyadi — keyin `sum(...)` ishlamay qoladi.

## Esda tuting
- Qidiruv tartibi: Local → Enclosing → Global → Built-in.
- Oʻqish — erkin, oʻzgartirish uchun `global` / `nonlocal`.
- Built-in nomlarni oʻzgaruvchi nomi qilmang.
''', [
    P('x = 1\ndef f():\n    x = 2\n    def g():\n        return x\n    return g()\nprint(f())', "1", "None", "Xato"),
    P('x = 1\ndef f():\n    return x + 1\nprint(f(), x)', "2 2", "1 1", "Xato"),
    P('def f():\n    n = 0\n    def g():\n        nonlocal n\n        n += 5\n    g()\n    g()\n    return n\nprint(f())', "5", "0", "Xato"),
    P('n = 10\ndef f():\n    n = n + 1\n    return n\nprint(f())', "11", "10", "1"),
    P('a = 5\ndef f():\n    global a\n    a = 7\nf()\nprint(a)', "5", "None", "Xato"),
    P('def f():\n    y = 1\nf()\nprint(y)', "1", "None", "0"),
    P('sum = 0\nprint(sum([1, 2]))', "3", "0", "[1, 2]"),
    Q("Python oʻzgaruvchini qaysi tartibda qidiradi?", "Local → Enclosing → Global → Built-in", "Global → Local → Built-in → Enclosing", "Built-in → Global → Local", "Faqat Local va Global"),
    Q("Tashqi (oʻrab turgan) funksiyadagi oʻzgaruvchini ichki funksiyada oʻzgartirish uchun nima yoziladi?", "nonlocal", "global", "outer", "extern"),
    F("Hisoblagich yaratuvchi", "`hisoblagich()` funksiyasi `bosish` ichki funksiyasini qaytarsin. Har chaqirilganda `bosish()` 1, 2, 3… qaytarsin (`nonlocal` bilan).", "def hisoblagich():\n    n = 0\n    def bosish():\n        nonlocal n\n        n += 1\n        return n\n    return bosish", "hisoblagich()()", "(lambda b: (b(), b(), b()))(hisoblagich())", "(lambda a, b: (a(), a(), b()))(hisoblagich(), hisoblagich())"),
    F("Koʻpaytiruvchi", "`kopaytiruvchi(k)` — x ni k ga koʻpaytiradigan funksiya qaytarsin.", "def kopaytiruvchi(k):\n    def f(x):\n        return x * k\n    return f", "kopaytiruvchi(3)(5)", "kopaytiruvchi(10)(0)", "kopaytiruvchi(-1)(7)"),
    F("Global hisob", "Global `jami = 0` bor. `qosh(x)` uni x ga oshirsin va yangi `jami` ni qaytarsin. (Tekshiruv bir necha marta ketma-ket chaqiradi.)", "jami = 0\n\ndef qosh(x):\n    global jami\n    jami += x\n    return jami", "qosh(5)", "qosh(10)", "qosh(-3)", starter="jami = 0\n\ndef qosh(x):\n    pass\n"),
    F("Tuzatish", "Bu funksiya `UnboundLocalError` beradi. Uni tuzating: `balans` dan `summa` ni ayirib, yangi balansni qaytarsin.", "balans = 100\n\ndef yech(summa):\n    global balans\n    balans -= summa\n    return balans", "yech(30)", "yech(20)", "yech(0)", starter="balans = 100\n\ndef yech(summa):\n    balans -= summa\n    return balans\n"),
    F("Akkumulyator", "`yigʻuvchi()` — har chaqiruvda berilgan sonni oldingilarga qoʻshib, umumiy yigʻindini qaytaradigan funksiya qaytarsin. Funksiya nomi: `yiguvchi`.", "def yiguvchi():\n    s = 0\n    def f(x):\n        nonlocal s\n        s += x\n        return s\n    return f", "(lambda f: (f(5), f(10), f(-3)))(yiguvchi())", "yiguvchi()(7)", "(lambda f, g: (f(1), g(100), f(1)))(yiguvchi(), yiguvchi())"),
    F("Salomlovchi", "`salomlovchi(til)` — `til == \"uz\"` boʻlsa `Salom, ISM` qaytaradigan, aks holda `Hello, ISM` qaytaradigan funksiya qaytarsin.", 'def salomlovchi(til):\n    soz = "Salom" if til == "uz" else "Hello"\n    def f(ism):\n        return f"{soz}, {ism}"\n    return f', 'salomlovchi("uz")("Ali")', 'salomlovchi("en")("Bob")', 'salomlovchi("ru")("Ivan")'),
    F("Oʻrnatilgan nom", "Kodda `max` nomi oʻzgaruvchi sifatida ishlatilgan va `eng_katta` ishlamayapti. Oʻzgaruvchi nomini oʻzgartirib tuzating: `eng_katta(sonlar)` eng katta sonni qaytarsin.", "chegara = 100\n\ndef eng_katta(sonlar):\n    return max(sonlar)", "eng_katta([3, 9, 2])", "eng_katta([-5])", "eng_katta([1, 100, 50])", starter="max = 100\n\ndef eng_katta(sonlar):\n    return max(sonlar)\n"),
    L("exercism", "plane-tickets"),
    L("lc", "design-hashset"),
    L("exercism", "high-scores"),
    L("acmp", 296),
])

# ---------------------------------------------------------------- 5.7
TOPIC("lambda", "Lambda funksiyalar", "Bir qatorli anonim funksiyalar", 15, r'''
**Lambda** — nomsiz, bir qatorli funksiya. U `return` siz, bitta ifoda natijasini qaytaradi.

```py
kvadrat = lambda x: x * x
print(kvadrat(6))

qosh = lambda a, b: a + b
print(qosh(3, 4))
```

Bu quyidagi bilan bir xil:

```py
def kvadrat(x):
    return x * x
print(kvadrat(6))
```

## Qayerda foydali: key=
Lambda koʻpincha boshqa funksiyaga "qoida" sifatida beriladi. Eng koʻp — saralashda:

```py
talabalar = [("Ali", 85), ("Vali", 92), ("Gani", 78)]
print(sorted(talabalar, key=lambda t: t[1]))
print(sorted(talabalar, key=lambda t: t[1], reverse=True)[0])
```

```py
sozlar = ["olma", "anor", "shaftoli", "uzum"]
print(sorted(sozlar, key=len))
print(max(sozlar, key=len))
print(sorted(sozlar, key=lambda s: s[-1]))
```

## map va filter bilan
```py
narxlar = [10000, 25000, 8000]
print(list(map(lambda n: n * 1.12, narxlar)))
print(list(filter(lambda n: n > 9000, narxlar)))
```

## Ternar operator bilan
```py
holat = lambda ball: "oʻtdi" if ball >= 60 else "yiqildi"
print(holat(72), holat(40))
```

!> Lambda ichida `if/for/while` bloklari, bir nechta qator yozib boʻlmaydi. Murakkab mantiq uchun oddiy `def` yozing.

> PEP 8 (Python uslub qoidalari) lambdani oʻzgaruvchiga berishni tavsiya qilmaydi — bu holda `def` yaxshiroq. Lambda — "bir martalik" joylar uchun: `key=`, `map`, `filter`.

## Esda tuting
- `lambda args: ifoda` — natija avtomatik qaytadi.
- Asosiy joyi: `sorted(..., key=lambda ...)`, `max(..., key=...)`, `map`, `filter`.
- Murakkab mantiq — `def`.
''', [
    P('f = lambda x: x + 10\nprint(f(5))', "5", "x + 10", "Xato"),
    P('f = lambda a, b: a * b\nprint(f(3, 4))', "7", "34", "Xato"),
    P('print(sorted([3, -5, 2], key=abs))', "[-5, 2, 3]", "[3, 2, -5]", "[2, 3, 5]"),
    P('print(max(["ab", "abcd", "abc"], key=len))', "ab", "abc", "4"),
    P('print(list(map(lambda x: x * 2, [1, 2, 3])))', "[1, 2, 3, 1, 2, 3]", "[2, 3, 4]", "<map object>"),
    P('print(list(filter(lambda x: x % 2, [1, 2, 3, 4])))', "[2, 4]", "[True, False, True, False]", "[0, 1, 0, 1]"),
    P('print((lambda x: "juft" if x % 2 == 0 else "toq")(7))', "juft", "7", "Xato"),
    Q("Lambda funksiya qanday qiymat qaytaradi?", "Ifodaning natijasini avtomatik", "Faqat return yozilsa", "Har doim None", "Faqat True/False"),
    Q("Lambda eng koʻp qayerda ishlatiladi?", "sorted / max / min dagi key= da", "Katta dasturlarning asosiy funksiyasida", "Sinflar ichida", "Fayllarni ochishda"),
    F("Ball boʻyicha saralash", "`saralash(talabalar)` — `(ism, ball)` juftliklarini ball boʻyicha kamayish tartibida saralab qaytarsin.", "def saralash(talabalar):\n    return sorted(talabalar, key=lambda t: t[1], reverse=True)", 'saralash([("Ali", 85), ("Vali", 92), ("Gani", 78)])', 'saralash([("X", 1)])', 'saralash([])'),
    F("Eng uzun soʻz", "`eng_uzun(sozlar)` — eng uzun soʻzni qaytarsin (`max` va `key`).", "def eng_uzun(sozlar):\n    return max(sozlar, key=len)", 'eng_uzun(["olma", "shaftoli", "nok"])', 'eng_uzun(["a"])', 'eng_uzun(["ab", "cd", "e"])', lv=1),
    F("Oxirgi harf boʻyicha", "`oxirgi_harf(sozlar)` — soʻzlarni oxirgi harfi boʻyicha saralab qaytarsin.", "def oxirgi_harf(sozlar):\n    return sorted(sozlar, key=lambda s: s[-1])", 'oxirgi_harf(["olma", "nok", "uzum"])', 'oxirgi_harf(["b", "a"])', 'oxirgi_harf([])'),
    F("Mutlaq qiymat boʻyicha", "`yaqin_nolga(sonlar)` — nolga eng yaqin sonni qaytarsin.", "def yaqin_nolga(sonlar):\n    return min(sonlar, key=abs)", "yaqin_nolga([5, -2, 8])", "yaqin_nolga([-7])", "yaqin_nolga([10, -10, 3])"),
    F("Funksiya qaytarish", "`qoshuvchi(n)` — x ga n qoʻshadigan lambda qaytarsin.", "def qoshuvchi(n):\n    return lambda x: x + n", "qoshuvchi(5)(10)", "qoshuvchi(0)(7)", "qoshuvchi(-3)(3)"),
    F("Ikki kalit", "`saralash2(sozlar)` — avval uzunlik boʻyicha, teng boʻlsa alifbo boʻyicha saralasin (`key=lambda s: (len(s), s)`).", "def saralash2(sozlar):\n    return sorted(sozlar, key=lambda s: (len(s), s))", 'saralash2(["nok", "olma", "anor", "uzum", "ol"])', 'saralash2(["b", "a"])', 'saralash2([])'),
    F("Narx + QQS", "`qqs(narxlar)` — har bir narxga 12% qoʻshib, `int` qilib roʻyxat qaytarsin (`map` va `lambda`).", "def qqs(narxlar):\n    return list(map(lambda n: int(n * 1.12), narxlar))", "qqs([10000, 25000])", "qqs([])", "qqs([1])"),
    L("lc", "sort-array-by-parity"),
    L("lc", "height-checker"),
    L("exercism", "high-scores"),
    L("lc", "relative-sort-array"),
])

# ---------------------------------------------------------------- 5.8
TOPIC("rekursiya", "Rekursiya", "Oʻzini chaqiradigan funksiyalar", 25, r'''
**Rekursiya** — funksiya oʻzini oʻzi chaqirishi. Katta masala xuddi shunday, lekin kichikroq masalaga keltiriladi.

Har bir rekursiv funksiyada ikki qism boʻladi:
1. **Asos holat** — qachon toʻxtash kerak (aks holda cheksiz chaqiruv).
2. **Rekursiv qadam** — masalani kichraytirib, oʻzini chaqirish.

## Faktorial
`n! = n × (n-1)!`, va `1! = 1`:

```py
def faktorial(n):
    if n <= 1:          # asos holat
        return 1
    return n * faktorial(n - 1)   # rekursiv qadam

print(faktorial(5))
```

Qanday ishlaydi: `faktorial(5) = 5 × faktorial(4) = 5 × 4 × faktorial(3) = … = 120`.

## Teskari sanash
```py
def sana(n):
    if n == 0:
        print("Start!")
        return
    print(n)
    sana(n - 1)

sana(3)
```

## Raqamlar yigʻindisi
```py
def raqam_yigindi(n):
    if n < 10:
        return n
    return n % 10 + raqam_yigindi(n // 10)

print(raqam_yigindi(9875))
```

## Fibonachchi
```py
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
```

!> Bu `fib` juda sekin: `fib(35)` millionlab chaqiruv qiladi. Sababi — bir xil qiymatlar qayta-qayta hisoblanadi.

## Tezlashtirish: eslab qolish (memoization)
```py
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(80))
```

## Rekursiya chuqurligi
Python chuqurlikni cheklaydi (odatda ~1000). Asos holatni unutish — `RecursionError`.

```py
import sys
print(sys.getrecursionlimit())
```

> Koʻp rekursiv masalalarni sikl bilan ham yechish mumkin. Rekursiya daraxtlar, boʻlib-boshqarish (merge sort), kombinatorika uchun ayniqsa qulay.

## Esda tuting
- Asos holat — majburiy!
- Har bir chaqiruvda masala kichrayishi kerak.
- Takroriy hisoblarni `lru_cache` bilan tezlashtiring.
''', [
    P('def f(n):\n    if n == 0:\n        return 0\n    return n + f(n - 1)\nprint(f(4))', "4", "24", "0"),
    P('def f(n):\n    if n <= 1:\n        return 1\n    return n * f(n - 1)\nprint(f(4))', "10", "4", "1"),
    P('def f(n):\n    if n == 0:\n        return\n    print(n, end=" ")\n    f(n - 1)\nf(3)', "1 2 3", "3 2 1 0", "0"),
    P('def f(n):\n    if n == 0:\n        return\n    f(n - 1)\n    print(n, end=" ")\nf(3)', "3 2 1", "0 1 2 3", "3"),
    P('def f(s):\n    if s == "":\n        return ""\n    return f(s[1:]) + s[0]\nprint(f("abc"))', "abc", "a", "bca"),
    P('def f(n):\n    return f(n - 1)\nf(3)', "0", "3", "None"),
    P('def f(n):\n    if n < 2:\n        return n\n    return f(n - 1) + f(n - 2)\nprint(f(7))', "7", "8", "21"),
    Q("Rekursiv funksiyada nima majburiy?", "Asos holat (toʻxtash sharti)", "Global oʻzgaruvchi", "for sikli", "Kamida ikkita parametr"),
    Q("Asos holat boʻlmasa nima boʻladi?", "RecursionError", "Funksiya 0 qaytaradi", "Dastur cheksiz, xatosiz ishlaydi", "SyntaxError"),
    F("Faktorial", "`faktorial(n)` — n! ni rekursiya bilan hisoblang.", "def faktorial(n):\n    if n <= 1:\n        return 1\n    return n * faktorial(n - 1)", "faktorial(5)", "faktorial(0)", "faktorial(1)", "faktorial(20)"),
    F("1 dan n gacha", "`yigindi(n)` — 1 + 2 + … + n ni rekursiya bilan qaytaring.", "def yigindi(n):\n    if n == 0:\n        return 0\n    return n + yigindi(n - 1)", "yigindi(10)", "yigindi(0)", "yigindi(1)", lv=1),
    F("Daraja", "`daraja(a, n)` — `a ** n` ni rekursiya bilan hisoblang (n ≥ 0).", "def daraja(a, n):\n    if n == 0:\n        return 1\n    return a * daraja(a, n - 1)", "daraja(2, 10)", "daraja(5, 0)", "daraja(3, 4)"),
    F("Teskari satr", "`teskari(s)` — satrni rekursiya bilan teskari qaytaring.", 'def teskari(s):\n    if s == "":\n        return ""\n    return teskari(s[1:]) + s[0]', 'teskari("salom")', 'teskari("")', 'teskari("a")'),
    F("Raqamlar yigʻindisi", "`raqam_yigindi(n)` — raqamlar yigʻindisini rekursiya bilan qaytaring.", "def raqam_yigindi(n):\n    if n < 10:\n        return n\n    return n % 10 + raqam_yigindi(n // 10)", "raqam_yigindi(9875)", "raqam_yigindi(5)", "raqam_yigindi(1000)"),
    F("Fibonachchi (tez)", "`fib(n)` — n-Fibonachchi sonini qaytaring (`fib(0)=0, fib(1)=1`). `fib(80)` ham tez ishlashi kerak — `lru_cache` dan foydalaning.", "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)", "fib(10)", "fib(0)", "fib(80)", lv=3, starter="from functools import lru_cache\n\ndef fib(n):\n    pass\n"),
    F("EKUB", "`ekub(a, b)` — Evklid algoritmini rekursiya bilan yozing: `ekub(a, 0) = a`, aks holda `ekub(b, a % b)`.", "def ekub(a, b):\n    if b == 0:\n        return a\n    return ekub(b, a % b)", "ekub(12, 18)", "ekub(17, 5)", "ekub(100, 0)"),
    L("exercism", "pascals-triangle"),
    L("lc", "fibonacci-number"),
    L("lc", "power-of-three"),
    L("cses", 2165, note="Hanoy minorasi — rekursiyaning eng mashhur masalasi."),
])

# ---------------------------------------------------------------- 5.9
TOPIC("generatorlar", "Generatorlar", "yield va generator ifodalar — xotirani tejab qiymat ishlab chiqarish", 20, r'''
**Generator** — qiymatlarni birdaniga emas, **kerak boʻlganda birma-bir** ishlab chiqaradigan funksiya. U `return` oʻrniga `yield` ishlatadi.

```py
def sanoq(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for x in sanoq(4):
    print(x, end=" ")
```

## yield qanday ishlaydi
`yield` qiymatni beradi va funksiyani **pauza** qiladi. Keyingi soʻrovda funksiya toʻxtagan joyidan davom etadi.

```py
def gen():
    print("1-qadam")
    yield "A"
    print("2-qadam")
    yield "B"

g = gen()
print(next(g))
print(next(g))
```

## Nima uchun kerak: xotira
Roʻyxat barcha elementlarni xotirada saqlaydi. Generator esa faqat joriy elementni:

```py
import sys
royxat = [x * x for x in range(100000)]
generator = (x * x for x in range(100000))
print(sys.getsizeof(royxat) > 100000)
print(sys.getsizeof(generator) < 1000)
print(sum(generator))
```

## Generator ifodasi
Roʻyxat yigʻindisi `[...]`, generator ifodasi esa `(...)`:

```py
print(sum(x * x for x in range(1, 11)))
print(max(len(s) for s in ["olma", "shaftoli", "nok"]))
```

## Cheksiz generator
```py
def toq_sonlar():
    n = 1
    while True:
        yield n
        n += 2

g = toq_sonlar()
print([next(g) for _ in range(5)])
```

## Amaliy misol: Fibonachchi oqimi
```py
def fibonachchi():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

for i, f in enumerate(fibonachchi()):
    if f > 100:
        break
    print(f, end=" ")
```

!> Generator bir marta "sarflanadi". Ikkinchi marta aylanib chiqsangiz — boʻsh boʻladi.

## Esda tuting
- `yield` — qiymat berib, pauza qiladi.
- `(x for x in ...)` — generator ifodasi, `[x for x in ...]` — roʻyxat.
- Katta yoki cheksiz ketma-ketliklar uchun generator — xotirani tejaydi.
''', [
    P('def g():\n    yield 1\n    yield 2\nprint(list(g()))', "1 2", "[2]", "(1, 2)"),
    P('def g():\n    yield "a"\n    yield "b"\nx = g()\nnext(x)\nprint(next(x))', "a", "ab", "Xato"),
    P('print(sum(x for x in range(4)))', "4", "10", "Xato"),
    P('g = (x * 2 for x in [1, 2])\nprint(list(g))\nprint(list(g))', "[2, 4]\n[2, 4]", "[2, 4]", "[1, 2]\n[]"),
    P('def g(n):\n    for i in range(n):\n        yield i * i\nprint(list(g(4)))', "[1, 4, 9, 16]", "[0, 1, 2, 3]", "16"),
    P('def g():\n    yield 1\n    return\n    yield 2\nprint(list(g()))', "[1, 2]", "[]", "Xato"),
    P('x = (i for i in range(3))\nprint(type(x).__name__)', "list", "tuple", "range"),
    Q("`yield` ning `return` dan asosiy farqi?", "yield qiymat berib, funksiyani pauza qiladi va keyin davom ettiradi", "yield faqat bir marta ishlaydi", "yield None qaytaradi", "Farqi yoʻq"),
    Q("Million element uchun qaysi biri kamroq xotira oladi?", "(x for x in range(10**6))", "[x for x in range(10**6)]", "list(range(10**6))", "Hammasi bir xil"),
    F("Juft sonlar generatori", "`juftlar(n)` — 0 dan n gacha (n kirmaydi) juft sonlarni `yield` qiluvchi generator. Tekshiruv `list(juftlar(...))` ni chaqiradi.", "def juftlar(n):\n    for i in range(0, n, 2):\n        yield i", "list(juftlar(10))", "list(juftlar(1))", "list(juftlar(0))"),
    F("Kvadratlar yigʻindisi", "`kvadratlar_yigindisi(n)` — 1² + … + n² ni generator ifodasi va `sum` bilan qaytaring.", "def kvadratlar_yigindisi(n):\n    return sum(i * i for i in range(1, n + 1))", "kvadratlar_yigindisi(3)", "kvadratlar_yigindisi(10)", "kvadratlar_yigindisi(0)", lv=1),
    F("Fibonachchi generatori", "`fib_gen(n)` — dastlabki n ta Fibonachchi sonini (0, 1, 1, 2, …) yield qilsin.", "def fib_gen(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b", "list(fib_gen(8))", "list(fib_gen(1))", "list(fib_gen(0))"),
    F("Teskari sanoq", "`teskari(n)` — n dan 1 gacha sonlarni yield qilsin.", "def teskari(n):\n    while n > 0:\n        yield n\n        n -= 1", "list(teskari(5))", "list(teskari(0))", "list(teskari(1))", lv=1),
    F("Boʻlaklarga", "`boʻlaklar` emas, `bolaklar(royxat, k)` — roʻyxatni k tadan boʻlaklarga boʻlib yield qilsin.", "def bolaklar(royxat, k):\n    for i in range(0, len(royxat), k):\n        yield royxat[i:i + k]", "list(bolaklar([1, 2, 3, 4, 5], 2))", "list(bolaklar([], 3))", "list(bolaklar([1, 2, 3], 3))"),
    F("Cheksiz toq", "`toqlar()` — 1, 3, 5, … cheksiz generator. `birinchi_n(n)` — undan foydalanib dastlabki n ta toq sonni roʻyxat qilib qaytarsin.", "def toqlar():\n    n = 1\n    while True:\n        yield n\n        n += 2\n\ndef birinchi_n(n):\n    g = toqlar()\n    return [next(g) for _ in range(n)]", "birinchi_n(5)", "birinchi_n(0)", "birinchi_n(1)", starter="def toqlar():\n    pass\n\ndef birinchi_n(n):\n    pass\n"),
    F("Uzun soʻzlar soni", "`uzunlar(sozlar, k)` — uzunligi k dan katta soʻzlar sonini generator ifodasi va `sum` bilan qaytaring.", "def uzunlar(sozlar, k):\n    return sum(1 for s in sozlar if len(s) > k)", 'uzunlar(["olma", "shaftoli", "nok"], 3)', "uzunlar([], 1)", 'uzunlar(["a", "bb"], 0)'),
    L("exercism", "plane-tickets"),
    L("exercism", "nth-prime"),
    L("lc", "fibonacci-number"),
    L("exercism", "sieve"),
])

# ---------------------------------------------------------------- 5.10
TOPIC("debugging", "Xatolarni topish (debugging)", "Xato xabarlarini oʻqish, print bilan tekshirish, VS Code maslahatlari", 25, r'''
Har bir dasturchi xato qiladi. Yaxshi dasturchini yomonidan ajratadigan narsa — xatoni **tez topa olishi**. Bu jarayon **debugging** deyiladi.

## 1. Xato xabarini oxiridan oʻqing
Python xatoning **turi**, **matni** va **qator raqamini** aytadi:

```py xato
narxlar = [12000, 8000, 15000]
print(narxlar[3])
```

`IndexError: list index out of range` — roʻyxatda 3-indeks yoʻq (indekslar 0, 1, 2).

## Eng koʻp uchraydigan xatolar
| Xato | Odatda sababi |
|---|---|
| `SyntaxError` | qavs, `:` yoki qoʻshtirnoq yetishmaydi |
| `IndentationError` | chekinish notoʻgʻri |
| `NameError` | oʻzgaruvchi nomi xato yozilgan yoki yaratilmagan |
| `TypeError` | turlar mos emas: `"5" + 5` |
| `ValueError` | qiymat yaroqsiz: `int("abc")` |
| `IndexError` | roʻyxat chegarasidan chiqish |
| `KeyError` | lugʻatda kalit yoʻq |
| `ZeroDivisionError` | nolga boʻlish |

## 2. Mantiqiy xatolar — eng ayyorlari
Dastur ishlaydi, lekin javob notoʻgʻri. Masalan, oʻrtachani hisoblash:

```py
def ortacha(a, b):
    return a + b / 2      # xato: qavs yoʻq

print(ortacha(4, 6))       # 5 kutgan edik
```

## 3. print bilan tekshirish
Eng oddiy va ishonchli usul — oraliq qiymatlarni chiqarish:

```py
def raqamlar_yigindisi(n):
    s = 0
    while n > 0:
        print(f"[debug] n={n}, s={s}")
        s += n % 10
        n //= 10
    return s

print(raqamlar_yigindisi(123))
```

Xato topilgach `[debug]` qatorlarini oʻchiring.

## 4. assert — kutilgan natijani tekshirish
```py
def kvadrat(x):
    return x * x

assert kvadrat(3) == 9
assert kvadrat(-2) == 4
print("Hamma tekshiruvlar oʻtdi")
```

`assert` sharti yolgʻon boʻlsa — `AssertionError`. Bu — kichik avtomatik testlar.

## 5. Kichik qismga ajrating
- Xatoni **qayta hosil qiling**: qaysi kirishda xato chiqadi?
- Kodning yarmini izohga oling — xato qolsa, u qolgan yarmida.
- Eng kichik misolni toping: 3 ta element bilan ham xato boʻladimi?

## VS Code maslahatlari
- `F5` — debug rejimida ishga tushirish; qator raqami yonini bosib **toʻxtash nuqtasi** (breakpoint) qoʻying.
- `F10` — keyingi qatorga, `F11` — funksiya ichiga kirish.
- `Ctrl + /` (Mac: `Cmd + /`) — tanlangan qatorlarni izohga olish.
- `Alt + ↑/↓` — qatorni yuqori/pastga surish; `Shift + Alt + ↓` — qatorni nusxalash.
- `F2` — oʻzgaruvchi nomini hamma joyda birdan oʻzgartirish.
- `Ctrl + Space` — avto-toʻldirish; `Ctrl + Shift + P` — buyruqlar paneli.

> Mirae Academy ichida: `Ctrl + Enter` — ishga tushirish, `Ctrl + Shift + Enter` — tekshirish. Xato boʻlgan qator qizil rangda belgilanadi.

## Esda tuting
- Xato xabarining oxirgi qatoridan boshlang: tur + matn + qator.
- Mantiqiy xatolar uchun — `print` va `assert`.
- Xatoni kichik misolgacha qisqartiring.
''', [
    P('x = [1, 2, 3]\nprint(x[3])', "3", "None", "[1, 2, 3]"),
    P('print(int("12a"))', "12", "0", "12a"),
    P('d = {"a": 1}\nprint(d["b"])', "None", "0", "1"),
    P('print(ismi)', "ismi", "None", "\"\""),
    P('print("Yosh: " + 5)', "Yosh: 5", "Yosh: + 5", "None"),
    P('assert 2 + 2 == 4\nprint("ok")', "True\nok", "Xato", "4"),
    P('assert len("abc") == 4\nprint("ok")', "ok", "False", "3"),
    Q("`NameError` odatda nimani bildiradi?", "Oʻzgaruvchi yaratilmagan yoki nomi xato yozilgan", "Nolga boʻlish", "Roʻyxat chegarasidan chiqish", "Notoʻgʻri chekinish"),
    Q("Dastur xatosiz ishlaydi, lekin javob notoʻgʻri. Bu qanday xato?", "Mantiqiy xato", "Sintaksis xatosi", "Chekinish xatosi", "Import xatosi"),
    F("Oʻrtachani tuzating", "Funksiya notoʻgʻri hisoblayapti. Tuzating: ikki sonning oʻrtachasini qaytarsin.", "def ortacha(a, b):\n    return (a + b) / 2", "ortacha(4, 6)", "ortacha(1, 2)", "ortacha(-3, 3)", starter="def ortacha(a, b):\n    return a + b / 2\n", lv=1),
    F("Oxirgi elementni tuzating", "Funksiya `IndexError` beradi. Tuzating: roʻyxatning oxirgi elementini qaytarsin.", "def oxirgi(royxat):\n    return royxat[-1]", "oxirgi([1, 2, 3])", "oxirgi([7])", 'oxirgi(["a", "b"])', starter="def oxirgi(royxat):\n    return royxat[len(royxat)]\n", lv=1),
    F("Yigʻindini tuzating", "Funksiya 1 dan n gacha yigʻindini qaytarishi kerak, lekin bitta son kam qoʻshyapti. Tuzating.", "def yigindi(n):\n    s = 0\n    for i in range(1, n + 1):\n        s += i\n    return s", "yigindi(10)", "yigindi(1)", "yigindi(0)", starter="def yigindi(n):\n    s = 0\n    for i in range(1, n):\n        s += i\n    return s\n"),
    F("Juftlarni sanashni tuzating", "Funksiya juft sonlar sonini qaytarishi kerak, lekin hisoblagich notoʻgʻri joyda nolga tushiriladi. Tuzating.", "def juftlar_soni(sonlar):\n    k = 0\n    for x in sonlar:\n        if x % 2 == 0:\n            k += 1\n    return k", "juftlar_soni([1, 2, 3, 4])", "juftlar_soni([])", "juftlar_soni([2, 2, 2])", starter="def juftlar_soni(sonlar):\n    for x in sonlar:\n        k = 0\n        if x % 2 == 0:\n            k += 1\n    return k\n"),
    F("Turni tuzating", "Funksiya `TypeError` beradi. Tuzating: `\"Yosh: N\"` satrini qaytarsin.", 'def yosh_matni(n):\n    return "Yosh: " + str(n)', "yosh_matni(17)", "yosh_matni(0)", "yosh_matni(100)", starter='def yosh_matni(n):\n    return "Yosh: " + n\n', lv=1),
    F("Kattasini tuzating", "Funksiya roʻyxatning eng katta elementini qaytarishi kerak, lekin manfiy sonlarda xato ishlaydi. Tuzating (`max` ishlatmang).", "def eng_katta(sonlar):\n    m = sonlar[0]\n    for x in sonlar:\n        if x > m:\n            m = x\n    return m", "eng_katta([3, 9, 2])", "eng_katta([-5, -2, -9])", "eng_katta([7])", starter="def eng_katta(sonlar):\n    m = 0\n    for x in sonlar:\n        if x > m:\n            m = x\n    return m\n"),
    F("Palindromni tuzating", "Funksiya katta-kichik harfga qaramasdan palindromni tekshirishi kerak. Tuzating.", "def palindrom(s):\n    s = s.lower()\n    return s == s[::-1]", 'palindrom("Kiyik")', 'palindrom("olma")', 'palindrom("Aa")', starter="def palindrom(s):\n    return s == s[::-1]\n"),
    L("exercism", "hello-world"),
    L("lc", "valid-parentheses"),
    L("exercism", "matching-brackets"),
    L("acmp", 249),
])
