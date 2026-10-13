from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(8, "Obyektga yoʻnaltirilgan dasturlash", "Sinflar, obyektlar, vorislik va maxsus metodlar", "🏛️")

# ---------------------------------------------------------------- 8.1
TOPIC("sinf-obyekt", "Sinf va obyekt", "Chizma va undan yasalgan narsalar", 20, r'''
Hozirgacha biz maʼlumotni (son, roʻyxat, lugʻat) va uni qayta ishlaydigan funksiyalarni **alohida** saqladik. **Obyektga yoʻnaltirilgan dasturlash** (OOP) ularni bitta "quti"ga birlashtiradi.

- **Sinf** (`class`) — chizma, andoza. Masalan: "Avtomobil" tushunchasi.
- **Obyekt** (nusxa, instance) — chizmadan yasalgan aniq narsa: "oq Malibu, 01A777AA".

Pythonda **hamma narsa obyekt**: `5`, `"salom"`, `[1, 2]` — har biri qaysidir sinfga tegishli.

```py
print(type(5))
print(type("salom"))
print(type([1, 2]))
print("salom".upper())   # upper — str sinfining metodi
```

## Birinchi sinf
```py
class Mushuk:
    pass

a = Mushuk()
b = Mushuk()
print(type(a).__name__)
print(a is b)              # ikki xil obyekt
print(isinstance(a, Mushuk))
```

> Sinf nomlari **KattaHarfBilan** (CamelCase) yoziladi: `Mushuk`, `BankHisobi`, `TalabaKartasi`.

## Atributlar — obyektning maʼlumotlari
Obyektga nuqta orqali qiymat biriktirish mumkin:

```py
class Mushuk:
    pass

m = Mushuk()
m.ism = "Momiq"
m.yosh = 3
print(m.ism, m.yosh)
```

## Metodlar — obyektning harakatlari
Sinf ichidagi funksiya **metod** deyiladi. Uning birinchi parametri — `self`, yaʼni "shu obyektning oʻzi":

```py
class Mushuk:
    def miyovla(self):
        print(f"{self.ism}: Miyov!")

m = Mushuk()
m.ism = "Momiq"
m.miyovla()        # Python buni Mushuk.miyovla(m) qilib chaqiradi
```

## Nega OOP?
| Muammo | OOP yechimi |
|---|---|
| Maʼlumot va funksiyalar tarqoq | bitta sinfda birga turadi |
| Kod takrorlanadi | vorislik orqali qayta ishlatiladi |
| Katta loyihani tushunish qiyin | real dunyo tushunchalari bilan modellashtiriladi |

## Esda tuting
- `class Nom:` — sinf; `Nom()` — yangi obyekt.
- Atribut — `obyekt.nom`, metod — `obyekt.metod()`.
''', [
    P('class A:\n    pass\nx = A()\ny = A()\nprint(x is y, type(x) is type(y))', "True True", "False False", "True False"),
    P('class Kitob:\n    pass\nk = Kitob()\nk.nom = "Alpomish"\nprint(k.nom)', "nom", "Kitob", "Xato"),
    P('class Kitob:\n    pass\nk = Kitob()\nprint(k.nom)', "None", '""', "⚠ NameError", lv=2),
    P('class It:\n    def ovoz(self):\n        return "Vov"\nprint(It().ovoz() * 2)', "Vov", "Vov Vov", "Xato"),
    P('print(type("salom").__name__, type(3.0).__name__)', "string double", "str int", "salom 3.0"),
    P('class A:\n    pass\na = A()\nprint(isinstance(a, A), isinstance(5, A))', "True True", "False True", "False False"),
    P('class Sanoq:\n    def bir(self):\n        return 1\ns = Sanoq()\nprint(s.bir() + Sanoq().bir())', "1", "11", "Xato"),
    Q("Sinf va obyekt farqi nimada?", "Sinf — chizma, obyekt — undan yasalgan aniq nusxa", "Ular bir xil narsa", "Obyekt — chizma, sinf — nusxa", "Sinf faqat sonlarni saqlaydi"),
    Q("Metodning birinchi parametri `self` nimani bildiradi?", "Metod chaqirilgan obyektning oʻzini", "Sinfning nomini", "Global oʻzgaruvchini", "Hech narsani, uni tashlab ketish mumkin"),
    F("Itcha", "`It` sinfini yozing. Uning `ovoz(self)` metodi `\"Vov!\"` qaytarsin.",
      "class It:\n    def ovoz(self):\n        return 'Vov!'", "It().ovoz()", "It().ovoz() * 2", "isinstance(It(), It)", lv=1),
    F("Salomlashuvchi", "`Robot` sinfi: `salom(self, ism)` metodi `\"Salom, ISM! Men robotman.\"` qaytarsin.",
      "class Robot:\n    def salom(self, ism):\n        return f'Salom, {ism}! Men robotman.'", 'Robot().salom("Ali")', 'Robot().salom("Mirae")', 'Robot().salom("")', lv=1),
    F("Kalkulyator", "`Kalkulyator` sinfi: `qosh(a, b)`, `ayir(a, b)`, `kopaytir(a, b)` metodlari.",
      "class Kalkulyator:\n    def qosh(self, a, b):\n        return a + b\n\n    def ayir(self, a, b):\n        return a - b\n\n    def kopaytir(self, a, b):\n        return a * b",
      "Kalkulyator().qosh(2, 3)", "Kalkulyator().ayir(10, 4)", "Kalkulyator().kopaytir(6, 7)", "(lambda k: k.qosh(k.kopaytir(2, 3), 1))(Kalkulyator())"),
    F("Atributli obyekt", "`yasash(ism, yosh)` funksiyasi `Talaba()` obyektini yaratib, unga `ism` va `yosh` atributlarini biriktirsin va obyektni qaytarsin. `Talaba` sinfini ham yozing (ichi boʻsh boʻlishi mumkin).",
      "class Talaba:\n    pass\n\n\ndef yasash(ism, yosh):\n    t = Talaba()\n    t.ism = ism\n    t.yosh = yosh\n    return t",
      'yasash("Ali", 17).ism', 'yasash("Ali", 17).yosh', 'type(yasash("X", 1)).__name__', lv=2),
    F("Matn vositasi", "`Matn` sinfi: `unlilar(self, s)` — satrdagi `aeiou` harflari sonini, `teskari(self, s)` — teskari satrni qaytarsin.",
      "class Matn:\n    def unlilar(self, s):\n        return sum(h in 'aeiou' for h in s.lower())\n\n    def teskari(self, s):\n        return s[::-1]",
      'Matn().unlilar("Assalomu alaykum")', 'Matn().teskari("salom")', 'Matn().unlilar("")'),
    F("Metod ichida metod", "`Geometriya` sinfi: `kvadrat(self, x)` — `x*x`, `gipotenuza(self, a, b)` — `kvadrat` dan foydalanib `(a² + b²) ** 0.5` qaytarsin.",
      "class Geometriya:\n    def kvadrat(self, x):\n        return x * x\n\n    def gipotenuza(self, a, b):\n        return (self.kvadrat(a) + self.kvadrat(b)) ** 0.5",
      "Geometriya().kvadrat(5)", "Geometriya().gipotenuza(3, 4)", "Geometriya().gipotenuza(5, 12)", lv=2),
    F("Harorat oʻgirgich", "`Harorat` sinfi: `farengeyt(self, c)` → `c * 9 / 5 + 32`, `selsiy(self, f)` → `(f - 32) * 5 / 9`.",
      "class Harorat:\n    def farengeyt(self, c):\n        return c * 9 / 5 + 32\n\n    def selsiy(self, f):\n        return (f - 32) * 5 / 9",
      "Harorat().farengeyt(100)", "Harorat().selsiy(212)", "Harorat().selsiy(Harorat().farengeyt(37))"),
    L("exercism", "ellens-alien-game", note="Sinflar boʻyicha Exercism'ning maxsus mashqi."),
    L("docs", "py-classes"),
    L("lc", "design-parking-system", note="Birinchi \"design\" masalasi — sinf yozish."),
    L("exercism", "space-age"),
])

# ---------------------------------------------------------------- 8.2
TOPIC("init-self", "Konstruktor __init__ va self", "Obyekt yaratilishi bilan uni tayyorlash", 20, r'''
Har safar atributlarni qoʻlda biriktirish noqulay va xavfli (unutib qoʻyish mumkin). **Konstruktor** — `__init__` metodi — obyekt yaratilishi bilan **avtomatik** ishlaydi.

```py
class Talaba:
    def __init__(self, ism, yosh):
        self.ism = ism
        self.yosh = yosh
        self.baholar = []

t = Talaba("Madina", 16)
print(t.ism, t.yosh, t.baholar)
```

`Talaba("Madina", 16)` chaqirilganda Python:
1. yangi boʻsh obyekt yaratadi;
2. `__init__(obyekt, "Madina", 16)` ni chaqiradi;
3. tayyor obyektni qaytaradi.

## self — "men"
`self.ism = ism` — "**mening** ismim — berilgan ism". Har bir obyektning atributlari oʻziniki:

```py
class Hisob:
    def __init__(self, egasi, balans=0):
        self.egasi = egasi
        self.balans = balans

    def toldir(self, summa):
        self.balans += summa

    def yech(self, summa):
        if summa > self.balans:
            print("Mablagʻ yetarli emas")
            return
        self.balans -= summa

a = Hisob("Ali", 100000)
b = Hisob("Vali")
a.toldir(50000)
b.yech(1000)
print(a.egasi, a.balans)
print(b.egasi, b.balans)
```

!> `self` ni yozishni unutish — eng koʻp uchraydigan xato. `balans += summa` emas, `self.balans += summa`!

## Standart qiymatlar
`__init__` ham oddiy funksiya — standart qiymat, `*args`, kalitli argumentlar ishlaydi:

```py
class Mahsulot:
    def __init__(self, nom, narx, soni=1):
        self.nom = nom
        self.narx = narx
        self.soni = soni

    def jami(self):
        return self.narx * self.soni

print(Mahsulot("Non", 4000).jami())
print(Mahsulot("Sut", 12000, soni=3).jami())
```

## Atributlar oʻzgaruvchan
```py
class Nuqta:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Nuqta(1, 2)
p.x = 10
print(p.x, p.y)
print(vars(p))     # obyekt atributlari lugʻat koʻrinishida
```

## Esda tuting
- `__init__` — obyekt "tugʻilganda" bir marta ishlaydi.
- Barcha atributlarni `__init__` ichida yarating — kod tushunarli boʻladi.
''', [
    P('class A:\n    def __init__(self):\n        print("yaratildi")\nA()\nA()', "yaratildi", "", "Xato"),
    P('class T:\n    def __init__(self, n):\n        self.n = n * 2\nprint(T(5).n)', "5", "n", "Xato"),
    P('class H:\n    def __init__(self, b=0):\n        self.b = b\n    def qosh(self, x):\n        self.b += x\nh = H(10)\nh.qosh(5)\nh.qosh(5)\nprint(h.b)', "15", "10", "5"),
    P('class H:\n    def __init__(self):\n        self.b = 0\n    def qosh(self, x):\n        b = x\nh = H()\nh.qosh(5)\nprint(h.b)', "5", "None", "Xato", lv=2,
      why="`b = x` — mahalliy oʻzgaruvchi. Atributni oʻzgartirish uchun `self.b = x` kerak."),
    P('class P:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\nprint(vars(P(1, 2)))', "(1, 2)", "P(1, 2)", "{x: 1, y: 2}"),
    P('class A:\n    def __init__(self, a):\n        self.a = a\nprint(A().a)', "None", "0", "a", lv=2),
    P('class S:\n    def __init__(self):\n        self.r = []\na = S()\nb = S()\na.r.append(1)\nprint(a.r, b.r)', "[1] [1]", "[] []", "[1] None"),
    Q("`__init__` qachon ishlaydi?", "Obyekt yaratilganda avtomatik", "Faqat qoʻlda chaqirilganda", "Dastur tugaganda", "Har bir metod chaqirilganda"),
    Q("Metod ichida obyekt atributini oʻzgartirishning toʻgʻri yozuvi?", "self.balans += 100", "balans += 100", "this.balans += 100", "Hisob.balans += 100"),
    F("Toʻrtburchak", "`Turtburchak(eni, boyi)` sinfi: `yuza()` va `perimetr()` metodlari.",
      "class Turtburchak:\n    def __init__(self, eni, boyi):\n        self.eni = eni\n        self.boyi = boyi\n\n    def yuza(self):\n        return self.eni * self.boyi\n\n    def perimetr(self):\n        return 2 * (self.eni + self.boyi)",
      "Turtburchak(3, 4).yuza()", "Turtburchak(3, 4).perimetr()", "Turtburchak(10, 1).yuza()", lv=1),
    F("Bank hisobi", "`Hisob(egasi, balans=0)`: `toldir(summa)` balansni oshirsin; `yech(summa)` — yetarli boʻlsa ayirib `True`, aks holda `False` qaytarsin (balans oʻzgarmasin).",
      "class Hisob:\n    def __init__(self, egasi, balans=0):\n        self.egasi = egasi\n        self.balans = balans\n\n    def toldir(self, summa):\n        self.balans += summa\n\n    def yech(self, summa):\n        if summa > self.balans:\n            return False\n        self.balans -= summa\n        return True",
      '(h := Hisob("Ali", 100), h.toldir(50), h.balans)[-1]', 'Hisob("Ali", 100).yech(30)', 'Hisob("Ali", 10).yech(30)', '(h := Hisob("V"), h.toldir(20), h.yech(5), h.balans)[-1]', 'Hisob("X").egasi'),
    F("Talaba", "`Talaba(ism)`: `baholar` boʻsh roʻyxat bilan boshlansin. `baho_qosh(b)` — qoʻshsin; `ortacha()` — oʻrtacha, baho boʻlmasa `0`.",
      "class Talaba:\n    def __init__(self, ism):\n        self.ism = ism\n        self.baholar = []\n\n    def baho_qosh(self, b):\n        self.baholar.append(b)\n\n    def ortacha(self):\n        if not self.baholar:\n            return 0\n        return sum(self.baholar) / len(self.baholar)",
      'Talaba("A").ortacha()', '(t := Talaba("A"), t.baho_qosh(5), t.baho_qosh(4), t.ortacha())[-1]', '(t := Talaba("B"), t.baho_qosh(3), t.baholar)[-1]', '(a := Talaba("A"), b := Talaba("B"), a.baho_qosh(5), b.baholar)[-1]'),
    F("Sanagich", "`Sanagich(boshi=0)`: `bos()` qiymatni 1 ga oshirib, yangi qiymatni qaytarsin; `nolla()` — 0 ga qaytarsin.",
      "class Sanagich:\n    def __init__(self, boshi=0):\n        self.qiymat = boshi\n\n    def bos(self):\n        self.qiymat += 1\n        return self.qiymat\n\n    def nolla(self):\n        self.qiymat = 0",
      "Sanagich().bos()", "(s := Sanagich(10), s.bos(), s.bos())[-1]", "(s := Sanagich(5), s.nolla(), s.bos())[-1]"),
    F("Savat", "`Savat()`: `qosh(nom, narx, soni=1)` mahsulot qoʻshsin; `jami()` — umumiy summa; `soni()` — mahsulotlar soni (dona hisobida).",
      "class Savat:\n    def __init__(self):\n        self.narsalar = []\n\n    def qosh(self, nom, narx, soni=1):\n        self.narsalar.append((nom, narx, soni))\n\n    def jami(self):\n        return sum(n * s for _, n, s in self.narsalar)\n\n    def soni(self):\n        return sum(s for _, _, s in self.narsalar)",
      "Savat().jami()", '(s := Savat(), s.qosh("non", 4000, 2), s.qosh("sut", 12000), s.jami())[-1]', '(s := Savat(), s.qosh("non", 4000, 2), s.qosh("sut", 12000), s.soni())[-1]', lv=2),
    F("Vaqt", "`Vaqt(soat, daqiqa)`: `qosh(d)` daqiqa qoʻshsin (24 soatdan keyin 0 dan boshlanadi); `matn()` — `\"SS:DD\"` (ikki xonali).",
      "class Vaqt:\n    def __init__(self, soat, daqiqa):\n        self.jami = (soat * 60 + daqiqa) % 1440\n\n    def qosh(self, d):\n        self.jami = (self.jami + d) % 1440\n\n    def matn(self):\n        return f'{self.jami // 60:02d}:{self.jami % 60:02d}'",
      "Vaqt(9, 5).matn()", "(v := Vaqt(23, 30), v.qosh(45), v.matn())[-1]", "(v := Vaqt(0, 0), v.qosh(-1), v.matn())[-1]", lv=3),
    F("Doira", "`Doira(r)`: `yuza()` — `3.14159 * r * r` ni 2 xonagacha yaxlitlab; `kattalashtir(k)` radiusni k marta oshirsin.",
      "class Doira:\n    def __init__(self, r):\n        self.r = r\n\n    def yuza(self):\n        return round(3.14159 * self.r * self.r, 2)\n\n    def kattalashtir(self, k):\n        self.r *= k",
      "Doira(1).yuza()", "Doira(10).yuza()", "(d := Doira(1), d.kattalashtir(3), d.yuza())[-1]"),
    L("exercism", "bank-account"),
    L("exercism", "clock", note="`Clock` sinfi — vaqtni qoʻshish/ayirish, xuddi Vaqt mashqi kabi."),
    L("lc", "design-browser-history"),
    L("lc", "simple-bank-system"),
])

# ---------------------------------------------------------------- 8.3
TOPIC("sinf-metodlari", "Sinf atributlari va metod turlari", "Umumiy maʼlumot, classmethod va staticmethod", 20, r'''
Baʼzi maʼlumotlar **har bir obyektga** emas, **butun sinfga** tegishli boʻladi: QQS stavkasi, yaratilgan obyektlar soni, standart sozlamalar.

## Sinf atributi
```py
class Mahsulot:
    qqs = 0.12          # sinf atributi — hamma uchun bitta
    soni = 0

    def __init__(self, nom, narx):
        self.nom = nom   # obyekt atributi — har biriniki
        self.narx = narx
        Mahsulot.soni += 1

    def yakuniy(self):
        return self.narx * (1 + self.qqs)

a = Mahsulot("Choy", 10000)
b = Mahsulot("Shakar", 15000)
print(Mahsulot.soni)
print(a.qqs, b.qqs)
print(a.yakuniy())
```

> `self.qqs` avval obyektning oʻzidan, topilmasa sinfdan qidiriladi.

!> `self.soni += 1` deb yozsangiz, Python obyektda **yangi** atribut yaratadi — sinfdagi sanoq oʻzgarmaydi. Sinf atributini oʻzgartirish uchun `Sinf.atribut` yoki `cls.atribut` yozing.

## Uch xil metod
| Turi | Birinchi parametr | Qachon |
|---|---|---|
| oddiy metod | `self` (obyekt) | obyekt maʼlumoti bilan ishlash |
| `@classmethod` | `cls` (sinf) | sinf maʼlumoti, muqobil konstruktorlar |
| `@staticmethod` | yoʻq | sinfga tegishli yordamchi funksiya |

```py
class Sana:
    def __init__(self, kun, oy, yil):
        self.kun, self.oy, self.yil = kun, oy, yil

    @classmethod
    def satrdan(cls, s):              # muqobil konstruktor
        k, o, y = map(int, s.split("."))
        return cls(k, o, y)

    @staticmethod
    def kabisami(yil):                # obyektsiz yordamchi
        return yil % 4 == 0 and yil % 100 != 0 or yil % 400 == 0

    def matn(self):
        return f"{self.kun:02d}.{self.oy:02d}.{self.yil}"

d = Sana.satrdan("13.10.2026")
print(d.matn())
print(Sana.kabisami(2024), Sana.kabisami(2026))
```

## Amaliy misol: ID berish
```py
class Buyurtma:
    _keyingi_id = 1

    def __init__(self, mijoz):
        self.id = Buyurtma._keyingi_id
        Buyurtma._keyingi_id += 1
        self.mijoz = mijoz

for ism in ["Ali", "Vali", "Gani"]:
    b = Buyurtma(ism)
    print(b.id, b.mijoz)
```

## Esda tuting
- Sinf atributi — sinf ichida, metoddan tashqarida yoziladi.
- `@classmethod` → `cls`, `@staticmethod` → hech qanday maxsus parametr.
''', [
    P('class A:\n    x = 5\na = A()\nb = A()\nA.x = 7\nprint(a.x, b.x)', "5 5", "5 7", "7 5"),
    P('class A:\n    x = 5\na = A()\na.x = 9\nprint(a.x, A.x)', "9 9", "5 5", "5 9", lv=2),
    P('class S:\n    n = 0\n    def __init__(self):\n        S.n += 1\nS(); S(); S()\nprint(S.n)', "0", "1", "Xato"),
    P('class S:\n    n = 0\n    def __init__(self):\n        self.n += 1\nS(); S()\nprint(S.n)', "2", "1", "Xato", lv=3,
      why="`self.n += 1` obyektning oʻzida yangi `n` yaratadi; sinfdagi `S.n` 0 ligicha qoladi."),
    P('class M:\n    @staticmethod\n    def ikki(x):\n        return x * 2\nprint(M.ikki(4), M().ikki(5))', "8 8", "Xato", "4 5"),
    P('class N:\n    def __init__(self, v):\n        self.v = v\n    @classmethod\n    def nol(cls):\n        return cls(0)\nprint(N.nol().v)', "None", "cls", "Xato"),
    P('class A:\n    tur = "hayvon"\n    def __init__(self, ism):\n        self.ism = ism\nprint(A("Bars").tur, A.tur)', "Bars hayvon", "hayvon Bars", "Xato"),
    Q("`@classmethod` ning birinchi parametri nima?", "cls — sinfning oʻzi", "self — obyekt", "Hech qanday parametr yoʻq", "super"),
    Q("Muqobil konstruktor (masalan satrdan obyekt yasash) uchun qaysi biri mos?", "@classmethod", "@staticmethod", "@property", "__del__"),
    F("Sanaladigan", "`Foydalanuvchi(ism)` — har bir yangi obyekt yaratilganda sinf atributi `soni` 1 ga oshsin. `Foydalanuvchi.soni` dastlab 0.",
      "class Foydalanuvchi:\n    soni = 0\n\n    def __init__(self, ism):\n        self.ism = ism\n        Foydalanuvchi.soni += 1",
      "Foydalanuvchi.soni", '(Foydalanuvchi("A"), Foydalanuvchi("B"), Foydalanuvchi.soni)[-1]', '(Foydalanuvchi("C"), Foydalanuvchi.soni)[-1]',
      starter="class Foydalanuvchi:\n    soni = 0\n\n    def __init__(self, ism):\n        self.ism = ism\n        # soni ni oshiring\n", lv=1),
    F("QQS", "`Narx(summa)` sinfi: sinf atributi `stavka = 0.12`. `yakuniy()` — `round(summa * (1 + stavka))` qaytarsin. Stavka sinfda oʻzgartirilsa, hamma obyektlarga taʼsir qilsin.",
      "class Narx:\n    stavka = 0.12\n\n    def __init__(self, summa):\n        self.summa = summa\n\n    def yakuniy(self):\n        return round(self.summa * (1 + self.stavka))",
      "Narx(10000).yakuniy()", "Narx(0).yakuniy()", "(setattr(Narx, 'stavka', 0.2), Narx(100).yakuniy(), setattr(Narx, 'stavka', 0.12))[1]"),
    F("Satrdan", "`Odam(ism, yosh)` sinfi va `@classmethod` `satrdan(s)` — `\"Ali,17\"` satridan obyekt yasasin (yosh — int).",
      "class Odam:\n    def __init__(self, ism, yosh):\n        self.ism = ism\n        self.yosh = yosh\n\n    @classmethod\n    def satrdan(cls, s):\n        ism, yosh = s.split(',')\n        return cls(ism, int(yosh))",
      'Odam.satrdan("Ali,17").ism', 'Odam.satrdan("Ali,17").yosh', 'type(Odam.satrdan("Vali,30")).__name__'),
    F("Yordamchi", "`Matematika` sinfi: `@staticmethod` `tubmi(n)` — n tub boʻlsa `True`.",
      "class Matematika:\n    @staticmethod\n    def tubmi(n):\n        if n < 2:\n            return False\n        i = 2\n        while i * i <= n:\n            if n % i == 0:\n                return False\n            i += 1\n        return True",
      "Matematika.tubmi(7)", "Matematika.tubmi(1)", "Matematika.tubmi(91)", "Matematika().tubmi(97)"),
    F("ID raqamlar", "`Chipta()` — har bir yangi chipta 1 dan boshlab ketma-ket `raqam` olsin. `@classmethod` `nolla()` sanoqni qaytadan 1 ga tushirsin.",
      "class Chipta:\n    _keyingi = 1\n\n    def __init__(self):\n        self.raqam = Chipta._keyingi\n        Chipta._keyingi += 1\n\n    @classmethod\n    def nolla(cls):\n        cls._keyingi = 1",
      "(Chipta.nolla(), Chipta().raqam)[-1]", "(Chipta.nolla(), Chipta(), Chipta(), Chipta().raqam)[-1]", "(Chipta.nolla(), [Chipta().raqam for _ in range(4)])[-1]", lv=2),
    F("Valyuta", "`Valyuta(som)` sinfi: sinf atributi `kurslar = {\"USD\": 12800, \"EUR\": 14000}`. `ga(kod)` — soʻmni shu valyutaga oʻgirib 2 xonagacha yaxlitlasin. `@classmethod` `kurs_qosh(kod, qiymat)` — yangi kurs qoʻshsin.",
      "class Valyuta:\n    kurslar = {'USD': 12800, 'EUR': 14000}\n\n    def __init__(self, som):\n        self.som = som\n\n    def ga(self, kod):\n        return round(self.som / self.kurslar[kod], 2)\n\n    @classmethod\n    def kurs_qosh(cls, kod, qiymat):\n        cls.kurslar[kod] = qiymat",
      'Valyuta(128000).ga("USD")', 'Valyuta(7000).ga("EUR")', '(Valyuta.kurs_qosh("RUB", 160), Valyuta(1600).ga("RUB"))[-1]', lv=3),
    F("Harorat zavodi", "`Harorat(selsiy)` va ikki `@classmethod`: `farengeytdan(f)` va `kelvindan(k)` (`k - 273.15`). Obyektda `selsiy` atributi boʻlsin (1 xonagacha yaxlitlangan).",
      "class Harorat:\n    def __init__(self, selsiy):\n        self.selsiy = round(selsiy, 1)\n\n    @classmethod\n    def farengeytdan(cls, f):\n        return cls((f - 32) * 5 / 9)\n\n    @classmethod\n    def kelvindan(cls, k):\n        return cls(k - 273.15)",
      "Harorat.farengeytdan(212).selsiy", "Harorat.kelvindan(300).selsiy", "Harorat(36.66).selsiy"),
    L("lc", "design-an-ordered-stream"),
    L("exercism", "robot-name", note="Sinf atributida ishlatilgan nomlarni saqlash gʻoyasi."),
    L("lc", "seat-reservation-manager"),
    L("docs", "py-descriptor", title="Descriptor HowTo — classmethod/staticmethod qanday ishlaydi"),
])

# ---------------------------------------------------------------- 8.4
TOPIC("magic-str", "Maxsus metodlar: __str__, __repr__, taqqoslash", "Obyektni chiroyli chiqarish va solishtirish", 20, r'''
`print(obyekt)` qilsak, odatda tushunarsiz `<__main__.Nuqta object at 0x...>` chiqadi. **Maxsus (magic, dunder) metodlar** — ikki pastki chiziq bilan oʻralgan metodlar — obyektga Python'ning oʻrnatilgan amallarini "oʻrgatadi".

## __str__ va __repr__
```py
class Nuqta:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):                 # odamlar uchun: print, str()
        return f"({self.x}; {self.y})"

    def __repr__(self):                # dasturchilar uchun: konsol, roʻyxat ichida
        return f"Nuqta({self.x}, {self.y})"

p = Nuqta(3, 4)
print(p)
print(str(p))
print(repr(p))
print([p, Nuqta(0, 0)])     # roʻyxat elementlari repr bilan chiqadi
print(f"Nuqta: {p}")
```

> Qoida: `__repr__` ni doim yozing — u disk raskadrovka (debug) uchun juda foydali. `__str__` boʻlmasa, `print` ham `__repr__` dan foydalanadi.

## Tenglik: __eq__
Odatda `==` ikki obyekt **bitta** obyekt ekanini tekshiradi. Qiymat boʻyicha solishtirish uchun:

```py
class Pul:
    def __init__(self, summa, valyuta):
        self.summa, self.valyuta = summa, valyuta

    def __eq__(self, boshqa):
        return self.summa == boshqa.summa and self.valyuta == boshqa.valyuta

print(Pul(100, "USD") == Pul(100, "USD"))
print(Pul(100, "USD") == Pul(100, "EUR"))
print(Pul(100, "USD") != Pul(5, "USD"))   # != avtomatik ishlaydi
```

## Tartib: __lt__ va saralash
`__lt__` (less than, `<`) yozilsa, `sorted`, `min`, `max` ishlaydi:

```py
class Talaba:
    def __init__(self, ism, ball):
        self.ism, self.ball = ism, ball

    def __lt__(self, boshqa):
        return self.ball < boshqa.ball

    def __repr__(self):
        return f"{self.ism}:{self.ball}"

guruh = [Talaba("Ali", 85), Talaba("Vali", 92), Talaba("Gani", 78)]
print(sorted(guruh))
print(max(guruh))
```

| Metod | Amal |
|---|---|
| `__eq__` | `==` |
| `__ne__` | `!=` |
| `__lt__`, `__le__` | `<`, `<=` |
| `__gt__`, `__ge__` | `>`, `>=` |

> `functools.total_ordering` dekoratori bilan faqat `__eq__` va `__lt__` ni yozsangiz, qolgan taqqoslashlar avtomatik yaratiladi.

## Esda tuting
- `__str__` — chiroyli matn, `__repr__` — aniq, texnik matn.
- `__eq__` va `__lt__` — obyektlarni solishtirish va saralash uchun.
''', [
    P('class A:\n    def __str__(self):\n        return "Men A"\nprint(A())', "A", "<A>", "None"),
    P('class A:\n    def __repr__(self):\n        return "A()"\nprint([A(), A()])', "[A, A]", "A() A()", "[<A>, <A>]"),
    P('class A:\n    def __str__(self):\n        return "str"\n    def __repr__(self):\n        return "repr"\nx = A()\nprint(x, repr(x), [x])', "str str str", "repr repr repr", "str repr str", lv=2),
    P('class P:\n    def __init__(self, v):\n        self.v = v\nprint(P(1) == P(1))', "True", "Xato", "None", lv=2,
      why="`__eq__` yozilmagan boʻlsa `==` ikkita **alohida** obyektni solishtiradi — ular har xil."),
    P('class P:\n    def __init__(self, v):\n        self.v = v\n    def __eq__(self, o):\n        return self.v == o.v\nprint(P(1) == P(1), P(1) != P(2))', "False True", "True False", "Xato"),
    P('class T:\n    def __init__(self, n):\n        self.n = n\n    def __lt__(self, o):\n        return self.n < o.n\n    def __repr__(self):\n        return str(self.n)\nprint(sorted([T(3), T(1), T(2)]))', "[3, 1, 2]", "[T(1), T(2), T(3)]", "Xato"),
    P('class T:\n    def __init__(self, n):\n        self.n = n\nprint(sorted([T(2), T(1)]))', "[1, 2]", "[2, 1]", "None", lv=3),
    Q("`print(obyekt)` qaysi metodni chaqiradi?", "__str__ (boʻlmasa __repr__)", "__repr__ (boʻlmasa __str__)", "__print__", "__init__"),
    Q("Obyektlar roʻyxatini `sorted()` bilan saralash uchun eng kamida qaysi metod kerak?", "__lt__", "__eq__", "__str__", "__len__"),
    F("Kitob matni", "`Kitob(nom, muallif)`: `__str__` → `\"NOM — MUALLIF\"`, `__repr__` → `\"Kitob('NOM')\"`.",
      "class Kitob:\n    def __init__(self, nom, muallif):\n        self.nom, self.muallif = nom, muallif\n\n    def __str__(self):\n        return f'{self.nom} — {self.muallif}'\n\n    def __repr__(self):\n        return f\"Kitob('{self.nom}')\"",
      'str(Kitob("Kecha va kunduz", "Choʻlpon"))', 'repr(Kitob("Alpomish", "Xalq"))', 'str([Kitob("A", "B")])', lv=1),
    F("Kasr", "`Kasr(surat, maxraj)`: `__str__` → `\"s/m\"`; `__eq__` — `1/2 == 2/4` boʻlsin (koʻpaytirib solishtiring).",
      "class Kasr:\n    def __init__(self, s, m):\n        self.s, self.m = s, m\n\n    def __str__(self):\n        return f'{self.s}/{self.m}'\n\n    def __eq__(self, o):\n        return self.s * o.m == o.s * self.m",
      "str(Kasr(3, 4))", "Kasr(1, 2) == Kasr(2, 4)", "Kasr(1, 3) == Kasr(1, 2)", "Kasr(2, 3) != Kasr(4, 6)"),
    F("Versiya", "`Versiya(\"1.10.2\")` — `__lt__` va `__eq__` versiyalarni son sifatida solishtirsin (`1.9 < 1.10`). `__repr__` → asl satr.",
      "class Versiya:\n    def __init__(self, s):\n        self.s = s\n        self.q = tuple(int(x) for x in s.split('.'))\n\n    def __lt__(self, o):\n        return self.q < o.q\n\n    def __eq__(self, o):\n        return self.q == o.q\n\n    def __repr__(self):\n        return self.s",
      'Versiya("1.9") < Versiya("1.10")', 'Versiya("2.0.0") == Versiya("2.0.0")', 'str(sorted([Versiya("1.10"), Versiya("1.2"), Versiya("1.9")]))', 'max([Versiya("0.9"), Versiya("0.10")]).s', lv=3),
    F("Talabalar reytingi", "`Talaba(ism, ball)`: `__lt__` — ball boʻyicha; `__repr__` → `\"ISM(BALL)\"`. `top(talabalar, n)` funksiyasi eng yuqori n tasini kamayish tartibida qaytarsin.",
      "class Talaba:\n    def __init__(self, ism, ball):\n        self.ism, self.ball = ism, ball\n\n    def __lt__(self, o):\n        return self.ball < o.ball\n\n    def __repr__(self):\n        return f'{self.ism}({self.ball})'\n\n\ndef top(talabalar, n):\n    return sorted(talabalar, reverse=True)[:n]",
      'str(top([Talaba("A", 70), Talaba("B", 95), Talaba("C", 80)], 2))', 'str(top([Talaba("X", 1)], 3))', 'repr(Talaba("Ali", 100))'),
    F("Pul", "`Pul(summa)`: `__eq__`, `__lt__` va `__str__` (`\"12 500 soʻm\"` — minglik ajratgich boʻsh joy).",
      "class Pul:\n    def __init__(self, summa):\n        self.summa = summa\n\n    def __eq__(self, o):\n        return self.summa == o.summa\n\n    def __lt__(self, o):\n        return self.summa < o.summa\n\n    def __str__(self):\n        return f'{self.summa:,} soʻm'.replace(',', ' ')",
      "str(Pul(12500))", "Pul(5) < Pul(7)", "Pul(100) == Pul(100)", "str(min([Pul(3000), Pul(1500000), Pul(900)]))"),
    F("Total ordering", "`functools.total_ordering` bilan `Bal(n)` sinfi: faqat `__eq__` va `__lt__` yozing — `>=` va `>` ham ishlasin.",
      "from functools import total_ordering\n\n\n@total_ordering\nclass Bal:\n    def __init__(self, n):\n        self.n = n\n\n    def __eq__(self, o):\n        return self.n == o.n\n\n    def __lt__(self, o):\n        return self.n < o.n",
      "Bal(5) >= Bal(5)", "Bal(7) > Bal(3)", "Bal(1) <= Bal(0)", lv=2),
    F("Karta", "`Karta(qiymat, mast)`: `__repr__` → `\"Q♠\"` koʻrinishi (masalan `Karta(\"A\", \"♠\")` → `A♠`), `__eq__` — ikkala maydon boʻyicha.",
      "class Karta:\n    def __init__(self, qiymat, mast):\n        self.qiymat, self.mast = qiymat, mast\n\n    def __repr__(self):\n        return f'{self.qiymat}{self.mast}'\n\n    def __eq__(self, o):\n        return (self.qiymat, self.mast) == (o.qiymat, o.mast)",
      'repr(Karta("A", "♠"))', 'Karta("10", "♥") == Karta("10", "♥")', 'Karta("K", "♦") == Karta("K", "♣")', 'str([Karta("2", "♣"), Karta("J", "♥")])'),
    L("exercism", "rational-numbers", note="Kasrlar uchun barcha maxsus metodlar."),
    L("exercism", "complex-numbers"),
    L("docs", "py-datamodel"),
    L("lc", "kth-largest-element-in-a-stream"),
])

# ---------------------------------------------------------------- 8.5
TOPIC("magic-op", "Maxsus metodlar: operatorlar, len, in, chaqiruv", "__add__, __len__, __contains__, __getitem__, __call__", 25, r'''
Maxsus metodlar bilan oʻz obyektlaringizga `+`, `len()`, `in`, `[]` va hatto `()` ni oʻrgatish mumkin — ular xuddi oʻrnatilgan turlardek ishlaydi.

## Arifmetika: __add__, __sub__, __mul__
```py
class Vektor:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, o):
        return Vektor(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vektor(self.x - o.x, self.y - o.y)

    def __mul__(self, k):            # vektor * son
        return Vektor(self.x * k, self.y * k)

    def __repr__(self):
        return f"Vektor({self.x}, {self.y})"

a = Vektor(1, 2)
b = Vektor(3, 4)
print(a + b)
print(b - a)
print(a * 3)
```

| Metod | Amal | Metod | Amal |
|---|---|---|---|
| `__add__` | `a + b` | `__truediv__` | `a / b` |
| `__sub__` | `a - b` | `__floordiv__` | `a // b` |
| `__mul__` | `a * b` | `__neg__` | `-a` |

## Konteyner kabi: __len__, __contains__, __getitem__, __iter__
```py
class Pleylist:
    def __init__(self, nom):
        self.nom = nom
        self.qoshiqlar = []

    def qosh(self, q):
        self.qoshiqlar.append(q)

    def __len__(self):
        return len(self.qoshiqlar)

    def __contains__(self, q):
        return q in self.qoshiqlar

    def __getitem__(self, i):
        return self.qoshiqlar[i]

    def __iter__(self):
        return iter(self.qoshiqlar)

p = Pleylist("Sevimlilar")
for q in ["Bahor", "Yoshlik", "Vatan"]:
    p.qosh(q)

print(len(p))
print("Yoshlik" in p)
print(p[0], p[-1])
print(p[1:])
for q in p:
    print("♪", q)
```

## Chaqiriladigan obyekt: __call__
```py
class Kopaytiruvchi:
    def __init__(self, k):
        self.k = k

    def __call__(self, x):
        return x * self.k

uch_barobar = Kopaytiruvchi(3)
print(uch_barobar(10))           # obyekt funksiya kabi chaqirildi
print(list(map(uch_barobar, [1, 2, 3])))
```

## bool va obyekt
`__bool__` yoki `__len__` boʻlsa, obyekt `if` da ishlaydi:

```py
class Savat:
    def __init__(self):
        self.narsalar = []
    def __len__(self):
        return len(self.narsalar)

s = Savat()
print("Boʻsh" if not s else "Toʻla")
```

## Esda tuting
- Operator metodlari **yangi** obyekt qaytaradi, eskisini oʻzgartirmaydi.
- `__len__`, `__contains__`, `__getitem__`, `__iter__` — obyekt roʻyxatdek ishlaydi.
''', [
    P('class V:\n    def __init__(self, n):\n        self.n = n\n    def __add__(self, o):\n        return V(self.n + o.n)\nprint((V(2) + V(3)).n)', "23", "V(5)", "Xato"),
    P('class S:\n    def __len__(self):\n        return 42\nprint(len(S()))', "0", "S", "Xato"),
    P('class B:\n    def __contains__(self, x):\n        return x % 2 == 0\nprint(4 in B(), 5 in B())', "False True", "True True", "Xato"),
    P('class R:\n    def __getitem__(self, i):\n        return i * 10\nr = R()\nprint(r[3], r[-1])', "3 -1", "30 10", "Xato"),
    P('class F:\n    def __call__(self, x):\n        return x + 1\nf = F()\nprint(f(1), f(f(1)))', "1 2", "Xato", "F F"),
    P('class V:\n    def __init__(self, n):\n        self.n = n\nprint(V(1) + V(2))', "V(3)", "3", "12", lv=2),
    P('class B:\n    def __len__(self):\n        return 0\nprint(bool(B()), bool([0]))', "True True", "False False", "True False", lv=2),
    Q("Obyekt bilan `a + b` ishlashi uchun qaysi metod kerak?", "__add__", "__plus__", "__sum__", "__concat__"),
    Q("Obyektni funksiya kabi chaqirish (`obj(5)`) uchun qaysi metod yoziladi?", "__call__", "__init__", "__func__", "__run__"),
    F("Vektor", "`Vektor(x, y)`: `+`, `-` va son bilan `*` ishlasin; `__eq__` va `__repr__` → `\"Vektor(x, y)\"`.",
      "class Vektor:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\n    def __add__(self, o):\n        return Vektor(self.x + o.x, self.y + o.y)\n\n    def __sub__(self, o):\n        return Vektor(self.x - o.x, self.y - o.y)\n\n    def __mul__(self, k):\n        return Vektor(self.x * k, self.y * k)\n\n    def __eq__(self, o):\n        return (self.x, self.y) == (o.x, o.y)\n\n    def __repr__(self):\n        return f'Vektor({self.x}, {self.y})'",
      "repr(Vektor(1, 2) + Vektor(3, 4))", "repr(Vektor(5, 5) - Vektor(1, 2))", "repr(Vektor(2, -1) * 3)", "Vektor(1, 1) + Vektor(1, 1) == Vektor(2, 2)"),
    F("Toʻplam", "`Guruh()` sinfi: `qosh(ism)`; `len()` — aʼzolar soni; `in` — aʼzolikni tekshirish; takror qoʻshilmasin.",
      "class Guruh:\n    def __init__(self):\n        self.azolar = []\n\n    def qosh(self, ism):\n        if ism not in self.azolar:\n            self.azolar.append(ism)\n\n    def __len__(self):\n        return len(self.azolar)\n\n    def __contains__(self, ism):\n        return ism in self.azolar",
      'len(Guruh())', '(g := Guruh(), g.qosh("Ali"), g.qosh("Ali"), g.qosh("Vali"), len(g))[-1]', '(g := Guruh(), g.qosh("Ali"), "Ali" in g, "Bek" in g)[2:]'),
    F("Polinom", "`Polinom(koeffs)` — `[1, 2, 3]` → `1 + 2x + 3x²`. `__call__(x)` qiymatni hisoblasin; `__len__` — darajasi + 1.",
      "class Polinom:\n    def __init__(self, koeffs):\n        self.k = koeffs\n\n    def __call__(self, x):\n        return sum(c * x ** i for i, c in enumerate(self.k))\n\n    def __len__(self):\n        return len(self.k)",
      "Polinom([1, 2, 3])(2)", "Polinom([5])(100)", "len(Polinom([0, 0, 1]))", "Polinom([0, 1])(-7)", lv=2),
    F("Jumla", "`Jumla(matn)`: `len()` — soʻzlar soni; `j[i]` — i-soʻz; `for` bilan soʻzlarni aylanish mumkin boʻlsin (`__iter__`).",
      "class Jumla:\n    def __init__(self, matn):\n        self.sozlar = matn.split()\n\n    def __len__(self):\n        return len(self.sozlar)\n\n    def __getitem__(self, i):\n        return self.sozlar[i]\n\n    def __iter__(self):\n        return iter(self.sozlar)",
      'len(Jumla("men python organaman"))', 'Jumla("bir ikki uch")[-1]', '[s.upper() for s in Jumla("a b")]', 'Jumla("x y z")[0:2]'),
    F("Pul qoʻshish", "`Pul(summa, valyuta)`: `+` faqat bir xil valyutada ishlasin, aks holda `ValueError`. `__repr__` → `\"100 USD\"`.",
      "class Pul:\n    def __init__(self, summa, valyuta):\n        self.summa, self.valyuta = summa, valyuta\n\n    def __add__(self, o):\n        if self.valyuta != o.valyuta:\n            raise ValueError('valyuta har xil')\n        return Pul(self.summa + o.summa, self.valyuta)\n\n    def __repr__(self):\n        return f'{self.summa} {self.valyuta}'",
      'repr(Pul(100, "USD") + Pul(50, "USD"))', 'Pul(1, "USD") + Pul(1, "EUR")', 'repr(Pul(0, "UZS") + Pul(5000, "UZS") + Pul(7000, "UZS"))', lv=3),
    F("Hisoblagich obyekt", "`Hisoblagich()`: har `__call__` qilinganda 1 ga oshib, yangi qiymatni qaytarsin; `__int__` joriy qiymatni bersin.",
      "class Hisoblagich:\n    def __init__(self):\n        self.n = 0\n\n    def __call__(self):\n        self.n += 1\n        return self.n\n\n    def __int__(self):\n        return self.n",
      "Hisoblagich()()", "(h := Hisoblagich(), h(), h(), h())[-1]", "(h := Hisoblagich(), h(), int(h))[-1]"),
    F("Matritsa", "`Matritsa(qatorlar)`: `m[i][j]` ishlasin (`__getitem__` qatorni qaytaradi), `+` — elementlar yigʻindisi (yangi `Matritsa`), `qatorlar` atributi saqlansin.",
      "class Matritsa:\n    def __init__(self, qatorlar):\n        self.qatorlar = qatorlar\n\n    def __getitem__(self, i):\n        return self.qatorlar[i]\n\n    def __add__(self, o):\n        return Matritsa([[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(self.qatorlar, o.qatorlar)])",
      "Matritsa([[1, 2], [3, 4]])[1][0]", "(Matritsa([[1, 2], [3, 4]]) + Matritsa([[10, 20], [30, 40]])).qatorlar", "(Matritsa([[1]]) + Matritsa([[-1]]))[0][0]", lv=2),
    L("exercism", "custom-set", note="`__contains__`, `__eq__`, `__add__`… — oʻz toʻplam sinfingiz."),
    L("lc", "range-sum-query-immutable"),
    L("lc", "peeking-iterator"),
    L("exercism", "matrix"),
])

# ---------------------------------------------------------------- 8.6
TOPIC("vorislik", "Vorislik (inheritance)", "Bor sinfni kengaytirish, super() va koʻp vorislik", 25, r'''
**Vorislik** — yangi sinfni mavjud sinf asosida yaratish. Bola sinf ota sinfning barcha atribut va metodlarini oladi, oʻzinikini qoʻshadi yoki oʻzgartiradi.

```py
class Hayvon:
    def __init__(self, ism):
        self.ism = ism

    def tanishtir(self):
        return f"Men {self.ism}"

    def ovoz(self):
        return "..."

class It(Hayvon):                  # It — Hayvon ning bolasi
    def ovoz(self):                # metodni qayta yozish (override)
        return "Vov!"

class Mushuk(Hayvon):
    def ovoz(self):
        return "Miyov!"

for h in [It("Bars"), Mushuk("Momiq"), Hayvon("Nomaʼlum")]:
    print(h.tanishtir(), "—", h.ovoz())
```

## super() — ota metodini chaqirish
```py
class Xodim:
    def __init__(self, ism, maosh):
        self.ism = ism
        self.maosh = maosh

    def malumot(self):
        return f"{self.ism}: {self.maosh:,} soʻm"

class Rahbar(Xodim):
    def __init__(self, ism, maosh, bolim):
        super().__init__(ism, maosh)     # ota konstruktori
        self.bolim = bolim

    def malumot(self):
        return super().malumot() + f" ({self.bolim} boʻlimi rahbari)"

print(Xodim("Ali", 8_000_000).malumot())
print(Rahbar("Madina", 15_000_000, "IT").malumot())
```

## isinstance va issubclass
```py
class Xodim:
    pass

class Rahbar(Xodim):
    pass

r = Rahbar()
print(isinstance(r, Rahbar), isinstance(r, Xodim))
print(issubclass(Rahbar, Xodim), issubclass(Xodim, Rahbar))
```

## Yaxshi vorislik misoli
Vorislik "**... bu ... turi**" (is-a) munosabatida toʻgʻri: *Rahbar — xodim turi*, *Kvadrat — shakl turi*.

```py
class Shakl:
    def yuza(self):
        return 0
    def tavsif(self):
        return f"{type(self).__name__}: yuza = {self.yuza():.2f}"

class Turtburchak(Shakl):
    def __init__(self, a, b):
        self.a, self.b = a, b
    def yuza(self):
        return self.a * self.b

class Kvadrat(Turtburchak):
    def __init__(self, a):
        super().__init__(a, a)

class Doira(Shakl):
    def __init__(self, r):
        self.r = r
    def yuza(self):
        return 3.14159 * self.r ** 2

for s in [Turtburchak(2, 3), Kvadrat(4), Doira(1)]:
    print(s.tavsif())
```

!> "**... da ... bor**" (has-a) munosabatida vorislik emas, **tarkib** ishlating: *Mashinada dvigatel bor* → `self.dvigatel = Dvigatel()`.

## Koʻp vorislik va MRO
Sinf bir nechta otadan meros olishi mumkin. Metod qidirish tartibi — **MRO**:

```py
class Uchuvchi:
    def harakat(self):
        return "uchadi"

class Suzuvchi:
    def harakat(self):
        return "suzadi"
    def sho_ng(self):
        return "shoʻngʻiydi"

class Ordak(Uchuvchi, Suzuvchi):
    pass

o = Ordak()
print(o.harakat(), o.sho_ng())
print([k.__name__ for k in Ordak.__mro__])
```

> Koʻp vorislikdan ehtiyotkorlik bilan foydalaning. Koʻpincha kichik "mixin" sinflar uchun ishlatiladi.

## Esda tuting
- `class Bola(Ota):` — vorislik; `super()` — ota metodiga murojaat.
- Bola metodni qayta yozishi mumkin (override).
''', [
    P('class A:\n    def f(self):\n        return "A"\nclass B(A):\n    pass\nprint(B().f())', "B", "Xato", "None"),
    P('class A:\n    def f(self):\n        return "A"\nclass B(A):\n    def f(self):\n        return "B"\nprint(A().f(), B().f())', "A A", "B B", "B A"),
    P('class A:\n    def f(self):\n        return "A"\nclass B(A):\n    def f(self):\n        return super().f() + "B"\nprint(B().f())', "B", "BA", "A"),
    P('class A:\n    def __init__(self):\n        self.x = 1\nclass B(A):\n    def __init__(self):\n        self.y = 2\nprint(hasattr(B(), "x"), hasattr(B(), "y"))', "True True", "True False", "False False", lv=3,
      why="`B.__init__` ota konstruktorini (`super().__init__()`) chaqirmagan — `x` yaratilmadi."),
    P('class A: pass\nclass B(A): pass\nprint(isinstance(B(), A), isinstance(A(), B))', "True True", "False True", "False False"),
    P('class X:\n    def f(self):\n        return "X"\nclass Y:\n    def f(self):\n        return "Y"\nclass Z(Y, X):\n    pass\nprint(Z().f())', "X", "XY", "Xato", lv=2),
    P('class A:\n    n = 1\nclass B(A):\n    pass\nB.n = 5\nprint(A.n, B.n)', "5 5", "1 1", "5 1"),
    Q("`super().__init__(...)` nima uchun chaqiriladi?", "Ota sinfning konstruktorini ishga tushirish uchun", "Yangi obyekt yaratish uchun", "Sinfni oʻchirish uchun", "Bola sinfni otaga aylantirish uchun"),
    Q("Qaysi holatda vorislik emas, tarkib (composition) mos?", "Mashinada dvigatel bor", "Kvadrat — toʻrtburchak turi", "It — hayvon turi", "Rahbar — xodim turi"),
    F("Hayvonlar", "`Hayvon(ism)` sinfi `ovoz()` → `\"...\"` va `tanishtir()` → `\"ISM: OVOZ\"`. `It` va `Sigir` bolalari mos ravishda `\"Vov\"` va `\"Moo\"` qaytarsin.",
      "class Hayvon:\n    def __init__(self, ism):\n        self.ism = ism\n\n    def ovoz(self):\n        return '...'\n\n    def tanishtir(self):\n        return f'{self.ism}: {self.ovoz()}'\n\n\nclass It(Hayvon):\n    def ovoz(self):\n        return 'Vov'\n\n\nclass Sigir(Hayvon):\n    def ovoz(self):\n        return 'Moo'",
      'It("Bars").tanishtir()', 'Sigir("Malla").tanishtir()', 'Hayvon("X").tanishtir()', 'isinstance(It("a"), Hayvon)', lv=1),
    F("Xodim va rahbar", "`Xodim(ism, maosh)`: `yillik()` → `maosh * 12`. `Rahbar(ism, maosh, bonus)` — `super()` bilan, `yillik()` = ota natijasi + bonus.",
      "class Xodim:\n    def __init__(self, ism, maosh):\n        self.ism, self.maosh = ism, maosh\n\n    def yillik(self):\n        return self.maosh * 12\n\n\nclass Rahbar(Xodim):\n    def __init__(self, ism, maosh, bonus):\n        super().__init__(ism, maosh)\n        self.bonus = bonus\n\n    def yillik(self):\n        return super().yillik() + self.bonus",
      'Xodim("A", 1000).yillik()', 'Rahbar("B", 1000, 500).yillik()', 'Rahbar("C", 0, 7).ism'),
    F("Shakllar", "`Shakl` — `yuza()` 0 qaytaradi. `Turtburchak(a, b)`, undan `Kvadrat(a)` (super bilan) va `Uchburchak(asos, h)` (`asos*h/2`). `jami_yuza(shakllar)` funksiyasi.",
      "class Shakl:\n    def yuza(self):\n        return 0\n\n\nclass Turtburchak(Shakl):\n    def __init__(self, a, b):\n        self.a, self.b = a, b\n\n    def yuza(self):\n        return self.a * self.b\n\n\nclass Kvadrat(Turtburchak):\n    def __init__(self, a):\n        super().__init__(a, a)\n\n\nclass Uchburchak(Shakl):\n    def __init__(self, asos, h):\n        self.asos, self.h = asos, h\n\n    def yuza(self):\n        return self.asos * self.h / 2\n\n\ndef jami_yuza(shakllar):\n    return sum(s.yuza() for s in shakllar)",
      "Kvadrat(5).yuza()", "jami_yuza([Turtburchak(2, 3), Kvadrat(2), Uchburchak(4, 5)])", "isinstance(Kvadrat(1), Turtburchak)", "jami_yuza([])", lv=2),
    F("Jamgʻarma hisobi", "`Hisob(balans)` — `yech(s)` (yetmasa `False`). `Jamgarma(balans, foiz)` — `Hisob` dan meros, `foiz_qosh()` balansga foizni qoʻshsin (int), `yech` esa bir martalik limit 1000 dan oshsa `False`.",
      "class Hisob:\n    def __init__(self, balans):\n        self.balans = balans\n\n    def yech(self, s):\n        if s > self.balans:\n            return False\n        self.balans -= s\n        return True\n\n\nclass Jamgarma(Hisob):\n    def __init__(self, balans, foiz):\n        super().__init__(balans)\n        self.foiz = foiz\n\n    def foiz_qosh(self):\n        self.balans += int(self.balans * self.foiz / 100)\n\n    def yech(self, s):\n        if s > 1000:\n            return False\n        return super().yech(s)",
      "Jamgarma(5000, 10).yech(2000)", "(j := Jamgarma(5000, 10), j.yech(500), j.balans)[-1]", "(j := Jamgarma(1000, 5), j.foiz_qosh(), j.balans)[-1]", "Hisob(5000).yech(2000)", lv=3),
    F("Mixin", "`JSONMixin` sinfi `json()` metodi bilan `self.__dict__` ni `json.dumps(..., ensure_ascii=False)` qilib qaytarsin. `Talaba(ism, ball)` uni meros qilib olsin.",
      "import json\n\n\nclass JSONMixin:\n    def json(self):\n        return json.dumps(self.__dict__, ensure_ascii=False)\n\n\nclass Talaba(JSONMixin):\n    def __init__(self, ism, ball):\n        self.ism, self.ball = ism, ball",
      'Talaba("Oʻktam", 90).json()', 'Talaba("A", 1).json()', "issubclass(Talaba, JSONMixin)"),
    F("MRO", "`A`, `B(A)`, `C(A)`, `D(B, C)` sinflarini yarating; har birida `nom()` sinf nomini qaytarsin, `D` da `nom()` yoʻq. `mro_nomlar()` funksiyasi `D.__mro__` dagi sinf nomlari roʻyxatini (`object` siz) qaytarsin.",
      "class A:\n    def nom(self):\n        return 'A'\n\n\nclass B(A):\n    def nom(self):\n        return 'B'\n\n\nclass C(A):\n    def nom(self):\n        return 'C'\n\n\nclass D(B, C):\n    pass\n\n\ndef mro_nomlar():\n    return [k.__name__ for k in D.__mro__ if k is not object]",
      "D().nom()", "mro_nomlar()", "issubclass(D, C)", lv=2),
    F("Transport", "`Transport(nom, tezlik)` — `vaqt(masofa)` soatda (`masofa / tezlik`, 2 xona). `Avtobus(nom, tezlik, oʻrinlar)` — `super()` bilan; qoʻshimcha `chipta_narxi(masofa)` = `masofa * 500`.",
      "class Transport:\n    def __init__(self, nom, tezlik):\n        self.nom, self.tezlik = nom, tezlik\n\n    def vaqt(self, masofa):\n        return round(masofa / self.tezlik, 2)\n\n\nclass Avtobus(Transport):\n    def __init__(self, nom, tezlik, orinlar):\n        super().__init__(nom, tezlik)\n        self.orinlar = orinlar\n\n    def chipta_narxi(self, masofa):\n        return masofa * 500",
      'Avtobus("Isuzu", 60, 30).vaqt(90)', 'Avtobus("Isuzu", 60, 30).chipta_narxi(120)', 'Avtobus("A", 50, 20).orinlar', 'Transport("Velosiped", 15).vaqt(10)'),
    L("exercism", "dnd-character"),
    L("exercism", "simple-linked-list"),
    L("lc", "design-linked-list"),
    L("docs", "py-classes", title="Inheritance — rasmiy qoʻllanma"),
])

# ---------------------------------------------------------------- 8.7
TOPIC("abstrakt", "Abstrakt sinflar (ABC)", "Bolalar majburiy yozishi kerak boʻlgan metodlar", 20, r'''
Baʼzan ota sinf faqat **shablon** boʻlishi kerak: "har bir toʻlov usulida `tolash()` boʻlishi shart", lekin "toʻlov" ning oʻzidan obyekt yaratish maʼnosiz. Buning uchun **abstrakt sinf** ishlatiladi.

```py
from abc import ABC, abstractmethod

class TolovUsuli(ABC):
    @abstractmethod
    def tolash(self, summa):
        """Har bir bola buni yozishi SHART."""

    def chek(self, summa):              # oddiy metod ham boʻlishi mumkin
        return f"{type(self).__name__}: {summa:,} soʻm — {self.tolash(summa)}"

class Karta(TolovUsuli):
    def tolash(self, summa):
        return "kartadan yechildi"

class Naqd(TolovUsuli):
    def tolash(self, summa):
        return "naqd qabul qilindi"

for usul in [Karta(), Naqd()]:
    print(usul.chek(150000))
```

## Abstrakt sinfdan obyekt yaratib boʻlmaydi
```py
from abc import ABC, abstractmethod

class Shakl(ABC):
    @abstractmethod
    def yuza(self): ...

try:
    Shakl()
except TypeError as e:
    print("TypeError:", e)
```

## Bola metodni yozishni unutsa
```py
from abc import ABC, abstractmethod

class Saqlovchi(ABC):
    @abstractmethod
    def saqla(self, malumot): ...
    @abstractmethod
    def yukla(self): ...

class Yarimta(Saqlovchi):
    def saqla(self, malumot):
        self.m = malumot
    # yukla() yozilmadi!

try:
    Yarimta()
except TypeError:
    print("Yarimta: yukla() yozilmagan — obyekt yaratilmaydi")
```

> ABC xatoni **obyekt yaratilayotganda** darhol koʻrsatadi — dastur ishlab turganda, kutilmagan joyda emas. Bu jamoaviy loyihalarda juda foydali.

## Abstrakt property
```py
from abc import ABC, abstractmethod

class Hayvon(ABC):
    @property
    @abstractmethod
    def oyoqlar(self): ...

class It(Hayvon):
    @property
    def oyoqlar(self):
        return 4

print(It().oyoqlar)
```

## Esda tuting
- `class X(ABC)` + `@abstractmethod` — "shartnoma".
- Abstrakt metodlarning hammasi yozilmaguncha bola sinfdan obyekt yaratilmaydi.
''', [
    P('from abc import ABC, abstractmethod\nclass A(ABC):\n    @abstractmethod\n    def f(self): ...\ntry:\n    A()\n    print("ok")\nexcept TypeError:\n    print("TypeError")', "ok", "None", "⚠ TypeError"),
    P('from abc import ABC, abstractmethod\nclass A(ABC):\n    @abstractmethod\n    def f(self): ...\nclass B(A):\n    def f(self):\n        return 5\nprint(B().f())', "None", "Xato", "f"),
    P('from abc import ABC, abstractmethod\nclass A(ABC):\n    @abstractmethod\n    def f(self): ...\n    def g(self):\n        return self.f() * 2\nclass B(A):\n    def f(self):\n        return 21\nprint(B().g())', "21", "Xato", "None"),
    P('from abc import ABC, abstractmethod\nclass A(ABC):\n    @abstractmethod\n    def f(self): ...\n    @abstractmethod\n    def g(self): ...\nclass B(A):\n    def f(self):\n        return 1\ntry:\n    B()\n    print("yaratildi")\nexcept TypeError:\n    print("yoʻq")', "yaratildi", "1", "⚠ TypeError", lv=2),
    P('from abc import ABC\nclass A(ABC):\n    pass\nprint(type(A()).__name__)', "ABC", "Xato", "None", lv=2,
      why="Abstrakt metodi boʻlmagan ABC sinfidan obyekt yaratish mumkin."),
    P('from abc import ABC, abstractmethod\nclass A(ABC):\n    @abstractmethod\n    def f(self):\n        return "ota"\nclass B(A):\n    def f(self):\n        return super().f() + "+bola"\nprint(B().f())', "bola", "ota", "Xato", lv=3),
    P('from abc import ABC, abstractmethod\nclass A(ABC):\n    @abstractmethod\n    def f(self): ...\nclass B(A):\n    def f(self): ...\nprint(isinstance(B(), A), B().f())', "True ...", "False None", "Xato"),
    Q("Abstrakt sinfning asosiy vazifasi?", "Bolalar majburiy yozishi kerak boʻlgan metodlar shartnomasini belgilash", "Kodni tezlashtirish", "Sinfni yashirish", "Obyektlarni nusxalash"),
    Q("Abstrakt metodi bor sinfdan obyekt yaratilsa nima boʻladi?", "TypeError", "None qaytadi", "Obyekt yaratiladi", "SyntaxError"),
    F("Toʻlov tizimi", "`TolovUsuli(ABC)` — abstrakt `komissiya(summa)`. `Karta` — 1%, `Naqd` — 0, `Onlayn` — 2% (int). `jami(usul, summa)` funksiyasi `summa + komissiya` qaytarsin.",
      "from abc import ABC, abstractmethod\n\n\nclass TolovUsuli(ABC):\n    @abstractmethod\n    def komissiya(self, summa):\n        ...\n\n\nclass Karta(TolovUsuli):\n    def komissiya(self, summa):\n        return int(summa * 0.01)\n\n\nclass Naqd(TolovUsuli):\n    def komissiya(self, summa):\n        return 0\n\n\nclass Onlayn(TolovUsuli):\n    def komissiya(self, summa):\n        return int(summa * 0.02)\n\n\ndef jami(usul, summa):\n    return summa + usul.komissiya(summa)",
      "jami(Karta(), 100000)", "jami(Naqd(), 100000)", "jami(Onlayn(), 50000)", "(lambda: (TolovUsuli(), 'ok'))()", lv=2),
    F("Shakl shartnomasi", "`Shakl(ABC)` — abstrakt `yuza()` va `perimetr()`, oddiy `nisbat()` = yuza/perimetr (2 xona). `Kvadrat(a)` va `Doira(r)` (π = 3.14).",
      "from abc import ABC, abstractmethod\n\n\nclass Shakl(ABC):\n    @abstractmethod\n    def yuza(self):\n        ...\n\n    @abstractmethod\n    def perimetr(self):\n        ...\n\n    def nisbat(self):\n        return round(self.yuza() / self.perimetr(), 2)\n\n\nclass Kvadrat(Shakl):\n    def __init__(self, a):\n        self.a = a\n\n    def yuza(self):\n        return self.a * self.a\n\n    def perimetr(self):\n        return 4 * self.a\n\n\nclass Doira(Shakl):\n    def __init__(self, r):\n        self.r = r\n\n    def yuza(self):\n        return 3.14 * self.r * self.r\n\n    def perimetr(self):\n        return 2 * 3.14 * self.r",
      "Kvadrat(4).nisbat()", "Doira(10).nisbat()", "Kvadrat(3).perimetr()", "round(Doira(1).yuza(), 2)"),
    F("Xabar yuboruvchi", "`Yuboruvchi(ABC)` — abstrakt `yubor(kimga, matn)`. `SMS` → `\"SMS → KIMGA: MATN\"` (matn 20 belgigacha qirqiladi), `Email` → `\"Email → KIMGA: MATN\"`. `tarqat(yuboruvchilar, kimga, matn)` — natijalar roʻyxati.",
      "from abc import ABC, abstractmethod\n\n\nclass Yuboruvchi(ABC):\n    @abstractmethod\n    def yubor(self, kimga, matn):\n        ...\n\n\nclass SMS(Yuboruvchi):\n    def yubor(self, kimga, matn):\n        return f'SMS → {kimga}: {matn[:20]}'\n\n\nclass Email(Yuboruvchi):\n    def yubor(self, kimga, matn):\n        return f'Email → {kimga}: {matn}'\n\n\ndef tarqat(yuboruvchilar, kimga, matn):\n    return [y.yubor(kimga, matn) for y in yuboruvchilar]",
      'tarqat([SMS(), Email()], "Ali", "Ertaga dars soat 9 da boshlanadi")', 'SMS().yubor("+998", "salom")', 'tarqat([], "x", "y")', lv=2),
    F("Toʻliqmi?", "`toliqmi(sinf)` funksiyasi — berilgan sinfdan obyekt yaratish mumkinmi (barcha abstrakt metodlar yozilganmi)? `sinf.__abstractmethods__` dan foydalaning. Tekshiruv uchun `Asos(ABC)` (abstrakt `a`, `b`), `Yarim(Asos)` (faqat `a`) va `Toliq(Yarim)` (`b` ham) yarating.",
      "from abc import ABC, abstractmethod\n\n\nclass Asos(ABC):\n    @abstractmethod\n    def a(self):\n        ...\n\n    @abstractmethod\n    def b(self):\n        ...\n\n\nclass Yarim(Asos):\n    def a(self):\n        return 1\n\n\nclass Toliq(Yarim):\n    def b(self):\n        return 2\n\n\ndef toliqmi(sinf):\n    return not getattr(sinf, '__abstractmethods__', None)",
      "toliqmi(Asos)", "toliqmi(Yarim)", "toliqmi(Toliq)", "sorted(Yarim.__abstractmethods__)", lv=3),
    F("Saqlash", "`Saqlovchi(ABC)` — abstrakt `saqla(k, v)` va `ol(k)`. `XotiraSaqlovchi` lugʻatda saqlasin; `ol` yoʻq kalitga `None` bersin.",
      "from abc import ABC, abstractmethod\n\n\nclass Saqlovchi(ABC):\n    @abstractmethod\n    def saqla(self, k, v):\n        ...\n\n    @abstractmethod\n    def ol(self, k):\n        ...\n\n\nclass XotiraSaqlovchi(Saqlovchi):\n    def __init__(self):\n        self.d = {}\n\n    def saqla(self, k, v):\n        self.d[k] = v\n\n    def ol(self, k):\n        return self.d.get(k)",
      '(s := XotiraSaqlovchi(), s.saqla("a", 1), s.ol("a"))[-1]', 'XotiraSaqlovchi().ol("yoq")', "isinstance(XotiraSaqlovchi(), Saqlovchi)"),
    F("Hayvon oyoqlari", "`Hayvon(ABC)` — abstrakt property `oyoqlar`. `It` → 4, `Tovuq` → 2, `Ilon` → 0. `jami_oyoq(hayvonlar)` funksiyasi.",
      "from abc import ABC, abstractmethod\n\n\nclass Hayvon(ABC):\n    @property\n    @abstractmethod\n    def oyoqlar(self):\n        ...\n\n\nclass It(Hayvon):\n    @property\n    def oyoqlar(self):\n        return 4\n\n\nclass Tovuq(Hayvon):\n    @property\n    def oyoqlar(self):\n        return 2\n\n\nclass Ilon(Hayvon):\n    @property\n    def oyoqlar(self):\n        return 0\n\n\ndef jami_oyoq(hayvonlar):\n    return sum(h.oyoqlar for h in hayvonlar)",
      "jami_oyoq([It(), Tovuq(), Tovuq(), Ilon()])", "It().oyoqlar", "jami_oyoq([])"),
    F("Hisobot shabloni", "`Hisobot(ABC)` — abstrakt `qatorlar()` (roʻyxat qaytaradi) va tayyor `chiqar()` metodi: sarlavha `\"== NOM ==\"` (NOM — sinf nomi) + qatorlar, hammasi `\"\\n\"` bilan. `Savdo` → `[\"Jami: 100\"]`, `Ombor` → `[\"Non: 5\", \"Sut: 2\"]`.",
      "from abc import ABC, abstractmethod\n\n\nclass Hisobot(ABC):\n    @abstractmethod\n    def qatorlar(self):\n        ...\n\n    def chiqar(self):\n        return '\\n'.join([f'== {type(self).__name__} =='] + self.qatorlar())\n\n\nclass Savdo(Hisobot):\n    def qatorlar(self):\n        return ['Jami: 100']\n\n\nclass Ombor(Hisobot):\n    def qatorlar(self):\n        return ['Non: 5', 'Sut: 2']",
      "Savdo().chiqar()", "Ombor().chiqar()", "Hisobot()", lv=2),
    L("docs", "py-abc"),
    L("lc", "design-circular-queue"),
    L("lc", "design-hashmap"),
    L("exercism", "robot-simulator"),
])

# ---------------------------------------------------------------- 8.8
TOPIC("polimorfizm", "Polimorfizm va duck typing", "Bir xil interfeys — har xil xatti-harakat", 20, r'''
**Polimorfizm** ("koʻp shakllilik") — har xil turdagi obyektlarni **bir xil usulda** ishlatish imkoniyati. Siz `len()` ni satr, roʻyxat, lugʻatga ham bir xil chaqirasiz — bu polimorfizm.

```py
print(len("salom"), len([1, 2, 3]), len({"a": 1}))
print(3 + 4, "ab" + "cd", [1] + [2])
```

## Oʻz sinflaringizda
```py
class PDF:
    def eksport(self, matn):
        return f"[PDF] {matn}"

class Word:
    def eksport(self, matn):
        return f"[DOCX] {matn}"

class HTML:
    def eksport(self, matn):
        return f"<p>{matn}</p>"

def saqla(formatlar, matn):
    for f in formatlar:              # f ning turi muhim emas!
        print(f.eksport(matn))

saqla([PDF(), Word(), HTML()], "Hisobot 2026")
```

`saqla` funksiyasi `PDF`, `Word` yoki `HTML` ekanini tekshirmaydi — u faqat `eksport()` metodi borligiga tayanadi.

## Duck typing
> "Agar u oʻrdakdek yursa va oʻrdakdek gʻaqillasa — demak u oʻrdak."

Python obyektning **turiga** emas, **qobiliyatiga** qaraydi. Vorislik ham shart emas:

```py
class Ordak:
    def ovoz(self):
        return "Gʻaq-gʻaq"

class Robot:
    def ovoz(self):
        return "Bip-bip"

class Odam:
    def ovoz(self):
        return "Salom!"

for narsa in [Ordak(), Robot(), Odam()]:
    print(narsa.ovoz())
```

## Hayotiy misol: "fayl kabi" obyekt
`print(..., file=x)` ga `write()` metodi bor **istalgan** obyektni berish mumkin:

```py
class Yozuvchi:
    def __init__(self):
        self.qatorlar = []
    def write(self, s):
        if s.strip():
            self.qatorlar.append(s.strip())

y = Yozuvchi()
print("birinchi", file=y)
print("ikkinchi", file=y)
print(y.qatorlar)
```

## isinstance yoki duck typing?
| Yondashuv | Misol | Qachon |
|---|---|---|
| Duck typing | `obj.eksport()` ni chaqirish | koʻpincha ✅ |
| `hasattr` | `if hasattr(obj, "eksport")` | ixtiyoriy imkoniyat |
| `isinstance` | `if isinstance(obj, PDF)` | haqiqatan tur muhim boʻlsa |

## Esda tuting
- Bir xil nomli metod → bir xil kod har xil obyektlar bilan ishlaydi.
- Python'da "nima ekanligi" emas, "nima qila olishi" muhim.
''', [
    P('class A:\n    def f(self):\n        return 1\nclass B:\n    def f(self):\n        return 2\nprint(sum(x.f() for x in [A(), B(), A()]))', "3", "Xato", "[1, 2, 1]"),
    P('print(len("abc") + len([0, 0]) + len({1: 2}))', "3", "5", "Xato"),
    P('class O:\n    def ovoz(self):\n        return "gʻaq"\nclass R:\n    pass\nfor x in [O(), R()]:\n    print(x.ovoz())', "gʻaq\ngʻaq", "gʻaq\nNone", "gʻaq", lv=2),
    P('class A:\n    def __len__(self):\n        return 3\nprint(len(A()) * 2)', "Xato", "AA", "3"),
    P('class Y:\n    def __init__(self):\n        self.s = ""\n    def write(self, t):\n        self.s += t\ny = Y()\nprint("hi", file=y)\nprint(repr(y.s))', "'hi'", "''", "Xato", lv=3),
    P('print(hasattr("abc", "upper"), hasattr(5, "upper"))', "True True", "False False", "False True"),
    P('def ikki(x):\n    return x + x\nprint(ikki(3), ikki("ab"), ikki([1]))', "6 abab [2]", "Xato", "6 ab2 [1, 1]"),
    Q("Duck typing nimani anglatadi?", "Obyekt turiga emas, qanday metodlari borligiga qarash", "Faqat Ordak sinfidan foydalanish", "Har doim isinstance bilan tekshirish", "Obyektlarni nusxalash"),
    Q("Polimorfizmga eng yaxshi misol qaysi?", "len() ning satr, roʻyxat va lugʻatda ishlashi", "Oʻzgaruvchiga qiymat berish", "for sikli", "import buyrugʻi"),
    F("Eksport", "`PDF`, `Word`, `Matn` sinflari — har birida `eksport(s)`: mos ravishda `\"PDF:s\"`, `\"DOCX:s\"`, `s`. `hammasi(formatlar, s)` — natijalar roʻyxati.",
      "class PDF:\n    def eksport(self, s):\n        return f'PDF:{s}'\n\n\nclass Word:\n    def eksport(self, s):\n        return f'DOCX:{s}'\n\n\nclass Matn:\n    def eksport(self, s):\n        return s\n\n\ndef hammasi(formatlar, s):\n    return [f.eksport(s) for f in formatlar]",
      'hammasi([PDF(), Word(), Matn()], "hisobot")', 'hammasi([], "x")', 'hammasi([Matn(), Matn()], "a")', lv=1),
    F("Gapira oladiganlar", "`gapiradiganlar(narsalar)` — roʻyxatdan faqat `ovoz` metodi borlarining ovozlarini qaytarsin (`hasattr` bilan). Tekshiruv uchun `Ordak` (`\"gʻaq\"`), `Robot` (`\"bip\"`) va `Tosh` (metodsiz) sinflarini yozing.",
      "class Ordak:\n    def ovoz(self):\n        return 'gʻaq'\n\n\nclass Robot:\n    def ovoz(self):\n        return 'bip'\n\n\nclass Tosh:\n    pass\n\n\ndef gapiradiganlar(narsalar):\n    return [n.ovoz() for n in narsalar if hasattr(n, 'ovoz')]",
      "gapiradiganlar([Ordak(), Tosh(), Robot()])", "gapiradiganlar([Tosh()])", "gapiradiganlar([Robot(), Robot()])"),
    F("Uzunlik hisobi", "`jami_uzunlik(narsalar)` — `len()` qoʻllab boʻladigan elementlar uzunliklari yigʻindisi; boshqalarini (`TypeError`) tashlab keting.",
      "def jami_uzunlik(narsalar):\n    s = 0\n    for x in narsalar:\n        try:\n            s += len(x)\n        except TypeError:\n            pass\n    return s",
      'jami_uzunlik(["abc", [1, 2], 5, {"a": 1}, None])', "jami_uzunlik([])", 'jami_uzunlik([3.5, "xy"])', lv=2),
    F("Toʻlovlar", "`Click`, `Payme`, `Naqd` sinflari: `tolov(summa)` mos ravishda komissiya bilan `summa*1.01`, `summa*1.005`, `summa` (int) qaytarsin. `eng_arzon(usullar, summa)` — eng kam toʻlov summasini qaytarsin.",
      "class Click:\n    def tolov(self, summa):\n        return int(summa * 1.01)\n\n\nclass Payme:\n    def tolov(self, summa):\n        return int(summa * 1.005)\n\n\nclass Naqd:\n    def tolov(self, summa):\n        return summa\n\n\ndef eng_arzon(usullar, summa):\n    return min(u.tolov(summa) for u in usullar)",
      "eng_arzon([Click(), Payme()], 100000)", "eng_arzon([Click(), Payme(), Naqd()], 100000)", "Click().tolov(1000)"),
    F("Fayl kabi", "`Jurnal` sinfi — `write(s)` metodi bilan boʻsh boʻlmagan qatorlarni `qatorlar` roʻyxatiga yigʻsin. `yoz(jurnal)` funksiyasi `print(\"A\", file=jurnal)` va `print(\"B\", file=jurnal)` qilib, `jurnal.qatorlar` ni qaytarsin.",
      "class Jurnal:\n    def __init__(self):\n        self.qatorlar = []\n\n    def write(self, s):\n        if s.strip():\n            self.qatorlar.append(s.strip())\n\n\ndef yoz(jurnal):\n    print('A', file=jurnal)\n    print('B', file=jurnal)\n    return jurnal.qatorlar",
      "yoz(Jurnal())", "(j := Jurnal(), j.write('  x  '), j.qatorlar)[-1]", "(j := Jurnal(), j.write('\\n'), j.qatorlar)[-1]", lv=3),
    F("Umumiy maydon", "`Kvadrat(a)`, `Doira(r)` (π=3.14), `Uchburchak(a, h)` — barchasida `yuza()`. `eng_kattasi(shakllar)` — eng katta yuzali shakl sinf nomini qaytarsin.",
      "class Kvadrat:\n    def __init__(self, a):\n        self.a = a\n\n    def yuza(self):\n        return self.a ** 2\n\n\nclass Doira:\n    def __init__(self, r):\n        self.r = r\n\n    def yuza(self):\n        return 3.14 * self.r ** 2\n\n\nclass Uchburchak:\n    def __init__(self, a, h):\n        self.a, self.h = a, h\n\n    def yuza(self):\n        return self.a * self.h / 2\n\n\ndef eng_kattasi(shakllar):\n    return type(max(shakllar, key=lambda s: s.yuza())).__name__",
      "eng_kattasi([Kvadrat(3), Doira(2), Uchburchak(4, 4)])", "eng_kattasi([Uchburchak(10, 10), Kvadrat(7)])", "eng_kattasi([Doira(1)])"),
    F("Universal yigʻindi", "`yigindi(narsalar, boshi)` — `+` amalini qoʻllab ketma-ket qoʻshsin (sonlar, satrlar, roʻyxatlar uchun bir xil kod).",
      "def yigindi(narsalar, boshi):\n    natija = boshi\n    for x in narsalar:\n        natija = natija + x\n    return natija",
      "yigindi([1, 2, 3], 0)", 'yigindi(["a", "b"], "")', "yigindi([[1], [2, 3]], [])", "yigindi([], 10)"),
    L("lc", "design-hashset"),
    L("exercism", "high-scores"),
    L("lc", "implement-stack-using-queues"),
    L("docs", "py-datamodel", title="Data model — protokollar va maxsus metodlar"),
])

# ---------------------------------------------------------------- 8.9
TOPIC("inkapsulyatsiya", "Inkapsulyatsiya va @property", "Maʼlumotni himoyalash: _, __ va getter/setter", 25, r'''
**Inkapsulyatsiya** — obyektning ichki tuzilishini yashirib, tashqariga faqat xavfsiz "eshiklar" (metodlar) qoldirish. Masalan, bank hisobining balansini istalgan kishi `-1000000` qilib qoʻyolmasligi kerak.

## Kelishuv: _ va __
Python'da qatʼiy "private" yoʻq — buning oʻrniga **kelishuvlar** bor:

| Yozuv | Maʼnosi |
|---|---|
| `nom` | ochiq (public) |
| `_nom` | "ichki, tegmang" — kelishuv |
| `__nom` | nom oʻzgartiriladi (name mangling) — tasodifiy foydalanishdan himoya |

```py
class Hisob:
    def __init__(self, balans):
        self._valyuta = "UZS"       # ichki
        self.__balans = balans      # yashirin

    def balans(self):
        return self.__balans

h = Hisob(5000)
print(h.balans())
print(h._valyuta)                    # mumkin, lekin tavsiya etilmaydi
try:
    print(h.__balans)
except AttributeError:
    print("__balans tashqaridan koʻrinmaydi")
print(h._Hisob__balans)              # haqiqiy nomi — Python uni oʻzgartirgan
```

## @property — atribut koʻrinishidagi metod
```py
class Harorat:
    def __init__(self, selsiy):
        self.selsiy = selsiy          # setter orqali tekshiriladi!

    @property
    def selsiy(self):
        return self._selsiy

    @selsiy.setter
    def selsiy(self, qiymat):
        if qiymat < -273.15:
            raise ValueError("Mutlaq noldan past boʻlishi mumkin emas")
        self._selsiy = qiymat

    @property
    def farengeyt(self):              # faqat oʻqish uchun, hisoblanadigan
        return self._selsiy * 9 / 5 + 32

t = Harorat(25)
print(t.selsiy, t.farengeyt)
t.selsiy = 100                       # setter ishladi
print(t.farengeyt)
try:
    t.selsiy = -300
except ValueError as e:
    print("Xato:", e)
```

> Foydalanuvchi uchun `t.selsiy` oddiy atributdek koʻrinadi, lekin ichida tekshiruv ishlaydi. Bu Python'ning eng chiroyli imkoniyatlaridan biri.

## Faqat oʻqiladigan xususiyat
Setter yozilmasa, property'ni oʻzgartirib boʻlmaydi:

```py
class Doira:
    def __init__(self, r):
        self.r = r

    @property
    def diametr(self):
        return 2 * self.r

d = Doira(5)
print(d.diametr)
try:
    d.diametr = 20
except AttributeError:
    print("diametr faqat oʻqiladi")
```

## Esda tuting
- `_nom` — "ichki" degan kelishuv; `__nom` — nomi yashiriladi.
- `@property` + `@x.setter` — tekshiruvli atribut.
''', [
    P('class A:\n    def __init__(self):\n        self._x = 5\nprint(A()._x)', "Xato", "None", "_x"),
    P('class A:\n    def __init__(self):\n        self.__x = 5\ntry:\n    print(A().__x)\nexcept AttributeError:\n    print("yashirin")', "5", "None", "⚠ AttributeError"),
    P('class A:\n    def __init__(self):\n        self.__x = 5\nprint(A()._A__x)', "Xato", "None", "_A__x", lv=2),
    P('class D:\n    def __init__(self, r):\n        self.r = r\n    @property\n    def d(self):\n        return self.r * 2\nprint(D(3).d)', "<bound method>", "3", "Xato"),
    P('class D:\n    def __init__(self, r):\n        self.r = r\n    @property\n    def d(self):\n        return self.r * 2\nx = D(3)\nx.r = 10\nprint(x.d)', "6", "10", "Xato"),
    P('class T:\n    @property\n    def v(self):\n        return 1\nt = T()\ntry:\n    t.v = 5\nexcept AttributeError:\n    print("faqat oʻqish")\nprint(t.v)', "5", "faqat oʻqish\n5", "1", lv=2),
    P('class Y:\n    def __init__(self, y):\n        self.yosh = y\n    @property\n    def yosh(self):\n        return self._y\n    @yosh.setter\n    def yosh(self, v):\n        self._y = max(0, v)\nprint(Y(-5).yosh, Y(20).yosh)', "-5 20", "Xato", "0 0", lv=3,
      why="`__init__` dagi `self.yosh = y` ham setter orqali oʻtadi — manfiy qiymat 0 ga aylandi."),
    Q("`_nom` (bitta pastki chiziq) nimani bildiradi?", "Bu ichki atribut — tashqaridan ishlatmang degan kelishuv", "Atribut butunlay yopiq, unga hech qachon murojaat qilib boʻlmaydi", "Atribut oʻchirilgan", "Bu sinf atributi"),
    Q("`@property` ning asosiy afzalligi?", "Metodni atribut kabi ishlatib, ichida tekshiruv yoki hisob-kitob qilish mumkin", "Kod tezroq ishlaydi", "Atributni oʻchirib qoʻyadi", "Sinfni abstrakt qiladi"),
    F("Xavfsiz hisob", "`Hisob(balans)` — balans `__balans` da saqlansin. `balans` faqat oʻqiladigan property; `toldir(s)` — s musbat boʻlmasa `ValueError`.",
      "class Hisob:\n    def __init__(self, balans):\n        self.__balans = balans\n\n    @property\n    def balans(self):\n        return self.__balans\n\n    def toldir(self, s):\n        if s <= 0:\n            raise ValueError('summa musbat boʻlsin')\n        self.__balans += s",
      "Hisob(100).balans", "(h := Hisob(100), h.toldir(50), h.balans)[-1]", "Hisob(100).toldir(-5)", "(lambda h: (setattr(h, 'balans', 9), h.balans))(Hisob(1))", lv=2),
    F("Yosh", "`Odam(ism, yosh)` — `yosh` property: setter 0..150 oraligʻidan tashqari qiymatga `ValueError` chiqarsin (konstruktorda ham!).",
      "class Odam:\n    def __init__(self, ism, yosh):\n        self.ism = ism\n        self.yosh = yosh\n\n    @property\n    def yosh(self):\n        return self._yosh\n\n    @yosh.setter\n    def yosh(self, v):\n        if not 0 <= v <= 150:\n            raise ValueError('yosh notoʻgʻri')\n        self._yosh = v",
      'Odam("A", 17).yosh', 'Odam("A", 200)', '(o := Odam("B", 5), setattr(o, "yosh", 6), o.yosh)[-1]', '(o := Odam("B", 5), setattr(o, "yosh", -1))'),
    F("Toʻrtburchak", "`Turtburchak(eni, boyi)`: `yuza` va `perimetr` — faqat oʻqiladigan property'lar (eni yoki boyi oʻzgarsa, ular ham avtomatik yangilansin).",
      "class Turtburchak:\n    def __init__(self, eni, boyi):\n        self.eni, self.boyi = eni, boyi\n\n    @property\n    def yuza(self):\n        return self.eni * self.boyi\n\n    @property\n    def perimetr(self):\n        return 2 * (self.eni + self.boyi)",
      "Turtburchak(3, 4).yuza", "(t := Turtburchak(3, 4), setattr(t, 'eni', 10), t.yuza)[-1]", "Turtburchak(1, 1).perimetr", lv=1),
    F("Parol", "`Foydalanuvchi(login, parol)` — parolni ochiq saqlamang: `hashlib.sha256(parol.encode()).hexdigest()` ni `_xesh` da saqlang. `tekshir(p)` — mos kelsa `True`. `parol` property'si oʻqilsa `AttributeError` chiqarsin.",
      "import hashlib\n\n\nclass Foydalanuvchi:\n    def __init__(self, login, parol):\n        self.login = login\n        self._xesh = hashlib.sha256(parol.encode()).hexdigest()\n\n    def tekshir(self, p):\n        return hashlib.sha256(p.encode()).hexdigest() == self._xesh\n\n    @property\n    def parol(self):\n        raise AttributeError('parolni oʻqib boʻlmaydi')",
      'Foydalanuvchi("ali", "mirae2026").tekshir("mirae2026")', 'Foydalanuvchi("ali", "mirae2026").tekshir("xato")', 'Foydalanuvchi("ali", "x").parol', 'len(Foydalanuvchi("a", "b")._xesh)', lv=3),
    F("Mahsulot narxi", "`Mahsulot(nom, narx)` — `narx` property: setter manfiy narxni 0 ga aylantirsin; `chegirma(foiz)` metodi narxni foizga kamaytirsin (int).",
      "class Mahsulot:\n    def __init__(self, nom, narx):\n        self.nom = nom\n        self.narx = narx\n\n    @property\n    def narx(self):\n        return self._narx\n\n    @narx.setter\n    def narx(self, v):\n        self._narx = max(0, v)\n\n    def chegirma(self, foiz):\n        self.narx = int(self.narx * (100 - foiz) / 100)",
      'Mahsulot("a", -100).narx', '(m := Mahsulot("a", 50000), m.chegirma(20), m.narx)[-1]', '(m := Mahsulot("a", 100), m.chegirma(150), m.narx)[-1]'),
    F("Harorat", "`Harorat(selsiy)`: `selsiy` property (−273.15 dan past → `ValueError`), `farengeyt` property — oʻqish va **yozish** mumkin (yozilganda selsiy yangilanadi).",
      "class Harorat:\n    def __init__(self, selsiy):\n        self.selsiy = selsiy\n\n    @property\n    def selsiy(self):\n        return self._c\n\n    @selsiy.setter\n    def selsiy(self, v):\n        if v < -273.15:\n            raise ValueError('juda past')\n        self._c = v\n\n    @property\n    def farengeyt(self):\n        return self._c * 9 / 5 + 32\n\n    @farengeyt.setter\n    def farengeyt(self, f):\n        self.selsiy = (f - 32) * 5 / 9",
      "Harorat(100).farengeyt", "(t := Harorat(0), setattr(t, 'farengeyt', 212), t.selsiy)[-1]", "Harorat(-300)", lv=3),
    F("Hisoblanadigan maydon", "`Talaba(ism)` — baholar `_baholar` ichki roʻyxatida. `baho_qosh(b)` (1..5 dan tashqari → `ValueError`), `ortacha` — faqat oʻqiladigan property (baho yoʻq boʻlsa 0, 2 xona).",
      "class Talaba:\n    def __init__(self, ism):\n        self.ism = ism\n        self._baholar = []\n\n    def baho_qosh(self, b):\n        if not 1 <= b <= 5:\n            raise ValueError('baho 1..5')\n        self._baholar.append(b)\n\n    @property\n    def ortacha(self):\n        if not self._baholar:\n            return 0\n        return round(sum(self._baholar) / len(self._baholar), 2)",
      'Talaba("A").ortacha', '(t := Talaba("A"), t.baho_qosh(5), t.baho_qosh(4), t.baho_qosh(4), t.ortacha)[-1]', 'Talaba("B").baho_qosh(6)', lv=2),
    L("docs", "py-descriptor"),
    L("lc", "design-authentication-manager"),
    L("exercism", "bank-account", title="Bank Account (inkapsulyatsiya bilan)"),
    L("lc", "design-a-number-container-system"),
])

# ---------------------------------------------------------------- 8.10
TOPIC("builtin-kengaytirish", "Oʻrnatilgan turlarni kengaytirish", "list, dict, str va Exception dan meros olish", 20, r'''
`list`, `dict`, `str` ham sinflar! Ulardan meros olib, yangi imkoniyatlar qoʻshish mumkin.

## list ni kengaytirish
```py
class Roʻyxat(list):
    def birinchi(self):
        return self[0] if self else None

    def yigindi(self):
        return sum(self)

r = Roʻyxat([5, 3, 8])
r.append(4)                   # list ning barcha metodlari ishlaydi
print(r, len(r))
print(r.birinchi(), r.yigindi())
print(sorted(r))
```

## dict ni kengaytirish
```py
class Sozlamalar(dict):
    def __missing__(self, kalit):          # yoʻq kalit soʻralganda
        return f"<{kalit} sozlanmagan>"

s = Sozlamalar(til="uz", tema="qorongʻi")
print(s["til"])
print(s["shrift"])
```

## str ni kengaytirish
`str` oʻzgarmas, shuning uchun yangi metodlar yangi satr qaytaradi:

```py
class Matn(str):
    def unlilar(self):
        return sum(h in "aeiouAEIOU" for h in self)

    def bosh_harflar(self):
        return "".join(s[0].upper() for s in self.split())

m = Matn("mirae academy python")
print(m.upper())          # str metodlari ham bor
print(m.unlilar(), m.bosh_harflar())
```

## Oʻz istisnolaringiz — eng koʻp uchraydigan holat
```py
class IlovaXatosi(Exception):
    """Ilovamizdagi barcha xatolarning otasi."""

class TopilmadiXatosi(IlovaXatosi):
    def __init__(self, nom):
        super().__init__(f"'{nom}' topilmadi")
        self.nom = nom

try:
    raise TopilmadiXatosi("talaba #42")
except IlovaXatosi as e:
    print(type(e).__name__, "→", e)
```

## collections.UserDict / UserList
Agar `dict` ning **hamma** metodlarini (`update`, `setdefault`...) oʻzgartirmoqchi boʻlsangiz, `UserDict` qulayroq — u ichki ishlarni bitta joyda (`__setitem__`) boshqaradi:

```py
from collections import UserDict

class KichikHarfli(UserDict):
    def __setitem__(self, kalit, qiymat):
        super().__setitem__(kalit.lower(), qiymat)

d = KichikHarfli()
d["ISM"] = "Ali"
d.update({"Shahar": "Xiva"})
print(dict(d))
```

## Esda tuting
- `class X(list)`, `class X(dict)`, `class X(str)` — oʻrnatilgan imkoniyatlar + sizniki.
- Xatolar ierarxiyasi: `class MeningXatom(Exception)` — eng amaliy misol.
''', [
    P('class R(list):\n    def ikkinchi(self):\n        return self[1]\nr = R([7, 8, 9])\nprint(r.ikkinchi(), len(r))', "7 3", "8 2", "Xato"),
    P('class R(list):\n    pass\nr = R([1])\nr.append(2)\nprint(r, isinstance(r, list))', "R([1, 2]) True", "[1, 2] False", "[1] True"),
    P('class D(dict):\n    def __missing__(self, k):\n        return 0\nd = D(a=5)\nprint(d["a"], d["b"])', "5 None", "⚠ KeyError", "5 b"),
    P('class D(dict):\n    def __missing__(self, k):\n        return 0\nd = D()\nprint(d.get("x"), d["x"])', "0 0", "None None", "⚠ KeyError", lv=3,
      why="`__missing__` faqat `d[k]` uchun ishlaydi; `get()` uni chaqirmaydi."),
    P('class M(str):\n    def baqir(self):\n        return self.upper() + "!"\nprint(M("salom").baqir())', "salom!", "SALOM", "Xato"),
    P('class X(Exception):\n    pass\ntry:\n    raise X("oops")\nexcept Exception as e:\n    print(type(e).__name__, e)', "Exception oops", "X", "⚠ X"),
    P('class A(Exception): pass\nclass B(A): pass\ntry:\n    raise B()\nexcept A:\n    print("A ushladi")', "⚠ B", "B ushladi", "Hech narsa"),
    Q("Yoʻq kalit soʻralganda `dict` bolasi sinfida qaysi metod chaqiriladi?", "__missing__", "__getattr__", "__default__", "__none__"),
    Q("Oʻz istisno sinfi uchun qaysi sinfdan meros olish kerak?", "Exception", "BaseObject", "Error", "object"),
    F("Statistik roʻyxat", "`StatRoyxat(list)`: `ortacha()` (boʻsh boʻlsa 0), `mediana()` (toq uzunlik — oʻrtadagi, juft — ikkitasining oʻrtachasi).",
      "class StatRoyxat(list):\n    def ortacha(self):\n        return sum(self) / len(self) if self else 0\n\n    def mediana(self):\n        b = sorted(self)\n        n = len(b)\n        if n % 2:\n            return b[n // 2]\n        return (b[n // 2 - 1] + b[n // 2]) / 2",
      "StatRoyxat([3, 1, 2]).mediana()", "StatRoyxat([4, 1, 3, 2]).mediana()", "StatRoyxat([2, 4]).ortacha()", "StatRoyxat().ortacha()", lv=2),
    F("Standart lugʻat", "`Standart(dict)` — yoʻq kalit soʻralsa `0` qaytarsin (`__missing__`). `sanash(sozlar)` funksiyasi undan foydalanib soʻzlarni sanab, oddiy `dict` qaytarsin.",
      "class Standart(dict):\n    def __missing__(self, k):\n        return 0\n\n\ndef sanash(sozlar):\n    d = Standart()\n    for s in sozlar:\n        d[s] += 1\n    return dict(d)",
      'sanash(["a", "b", "a"])', "sanash([])", 'Standart()["yoq"]', lv=1),
    F("Bosh harflar", "`Ism(str)` — `qisqa()` metodi: `\"ali valiyev\"` → `\"A. Valiyev\"` (birinchi soʻzning bosh harfi, ikkinchisi bosh harf bilan).",
      "class Ism(str):\n    def qisqa(self):\n        a, b = self.split()\n        return f'{a[0].upper()}. {b.capitalize()}'",
      'Ism("ali valiyev").qisqa()', 'Ism("MADINA karimova").qisqa()', 'Ism("a b").upper()'),
    F("Xatolar oilasi", "`DokonXatosi(Exception)`, undan `TugadiXatosi(nom)` (xabar `\"NOM tugadi\"`) va `NarxXatosi`. `sotish(qoldiq, nom, son)` — qoldiqdan kam boʻlsa `TugadiXatosi` chiqarsin, aks holda yangi qoldiqni. `sinov(...)` — `sotish` ni chaqirib, `DokonXatosi` ni ushlab, xabar matnini qaytarsin.",
      "class DokonXatosi(Exception):\n    pass\n\n\nclass TugadiXatosi(DokonXatosi):\n    def __init__(self, nom):\n        super().__init__(f'{nom} tugadi')\n\n\nclass NarxXatosi(DokonXatosi):\n    pass\n\n\ndef sotish(qoldiq, nom, son):\n    if son > qoldiq:\n        raise TugadiXatosi(nom)\n    return qoldiq - son\n\n\ndef sinov(qoldiq, nom, son):\n    try:\n        return sotish(qoldiq, nom, son)\n    except DokonXatosi as e:\n        return str(e)",
      'sinov(10, "non", 3)', 'sinov(2, "sut", 5)', 'sotish(1, "x", 2)', "issubclass(NarxXatosi, DokonXatosi)", lv=2),
    F("Kichik harfli lugʻat", "`collections.UserDict` dan `KichikLugat` — kalitlar doim kichik harfga oʻtkazilsin (oʻqishda ham!).",
      "from collections import UserDict\n\n\nclass KichikLugat(UserDict):\n    def __setitem__(self, k, v):\n        super().__setitem__(k.lower(), v)\n\n    def __getitem__(self, k):\n        return super().__getitem__(k.lower())",
      '(d := KichikLugat(), d.__setitem__("ISM", "Ali"), d["ism"])[-1]', '(d := KichikLugat({"A": 1, "b": 2}), sorted(d.keys()))[-1]', '(d := KichikLugat(), d.update(X=5), d["x"])[-1]', lv=3),
    F("Chegaralangan roʻyxat", "`Chegarali(list)` — `__init__(self, max_uzunlik)`; `append` max_uzunlikdan oshsa eng eski elementni olib tashlasin.",
      "class Chegarali(list):\n    def __init__(self, max_uzunlik):\n        super().__init__()\n        self.max_uzunlik = max_uzunlik\n\n    def append(self, x):\n        super().append(x)\n        if len(self) > self.max_uzunlik:\n            self.pop(0)",
      "(c := Chegarali(3), [c.append(i) for i in range(5)], list(c))[-1]", "(c := Chegarali(1), c.append('a'), c.append('b'), list(c))[-1]", "len(Chegarali(5))", lv=2),
    F("Takrorsiz roʻyxat", "`Takrorsiz(list)` — `append` element allaqachon boʻlsa qoʻshmasin. `__init__` ham takrorlarni olib tashlasin (tartib saqlansin).",
      "class Takrorsiz(list):\n    def __init__(self, elementlar=()):\n        super().__init__()\n        for x in elementlar:\n            self.append(x)\n\n    def append(self, x):\n        if x not in self:\n            super().append(x)",
      "list(Takrorsiz([3, 1, 3, 2, 1]))", "(t := Takrorsiz(), t.append(5), t.append(5), len(t))[-1]", "isinstance(Takrorsiz(), list)"),
    L("docs", "py-collections"),
    L("lc", "design-front-middle-back-queue"),
    L("exercism", "circular-buffer", note="Oʻz xato sinflari (BufferFullException) bilan."),
    L("lc", "lru-cache", note="Qiyinroq: `OrderedDict` dan meros olib yechish mumkin."),
])

# ---------------------------------------------------------------- 8.11
TOPIC("dataclass", "Data class'lar", "@dataclass — kam kod, koʻp imkoniyat", 20, r'''
Koʻp sinflar asosan **maʼlumot saqlash** uchun: `Talaba`, `Mahsulot`, `Nuqta`. Ular uchun `__init__`, `__repr__`, `__eq__` ni har safar yozish zerikarli. `@dataclass` bularni avtomatik yaratadi.

## Oddiy sinf va dataclass
```py
from dataclasses import dataclass

@dataclass
class Mahsulot:
    nom: str
    narx: int
    soni: int = 1          # standart qiymat

m = Mahsulot("Daftar", 5000, 3)
print(m)                    # chiroyli __repr__ — avtomatik
print(m.narx * m.soni)
print(m == Mahsulot("Daftar", 5000, 3))   # __eq__ — avtomatik
```

> `nom: str` — **tip izohi** (type hint). Python uni tekshirmaydi, lekin `dataclass` maydonlarni aynan shu yozuvdan topadi.

## Metodlar qoʻshish
```py
from dataclasses import dataclass

@dataclass
class Talaba:
    ism: str
    ball: float

    def baho(self):
        if self.ball >= 86:
            return 5
        if self.ball >= 71:
            return 4
        return 3 if self.ball >= 56 else 2

t = Talaba("Madina", 91.5)
print(t, "→", t.baho())
```

## Oʻzgaruvchan standart qiymat: field
!> `baholar: list = []` deb yozish mumkin emas (barcha obyektlar bitta roʻyxatni boʻlishib qoladi). `field(default_factory=list)` ishlating.

```py
from dataclasses import dataclass, field

@dataclass
class Guruh:
    nom: str
    azolar: list = field(default_factory=list)

a = Guruh("A")
b = Guruh("B")
a.azolar.append("Ali")
print(a, b)
```

## Muzlatilgan (oʻzgarmas) va saralanadigan
```py
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Versiya:
    katta: int
    kichik: int

v = [Versiya(1, 10), Versiya(1, 2), Versiya(0, 9)]
print(sorted(v))
print(max(v))
try:
    v[0].katta = 5
except Exception as e:
    print(type(e).__name__)
print({Versiya(1, 0): "barqaror"})   # frozen → lugʻat kaliti boʻla oladi
```

## asdict va __post_init__
```py
from dataclasses import dataclass, asdict

@dataclass
class Buyurtma:
    narx: int
    soni: int
    jami: int = 0

    def __post_init__(self):            # __init__ dan keyin ishlaydi
        self.jami = self.narx * self.soni

b = Buyurtma(12000, 3)
print(asdict(b))
```

## Esda tuting
- `@dataclass` — `__init__`, `__repr__`, `__eq__` avtomatik.
- `frozen=True` — oʻzgarmas; `order=True` — `<`, `sorted` ishlaydi.
- Roʻyxat/lugʻat standart qiymati: `field(default_factory=list)`.
''', [
    P('from dataclasses import dataclass\n@dataclass\nclass P:\n    x: int\n    y: int\nprint(P(1, 2))', "(1, 2)", "P(1, 2)", "<P object>"),
    P('from dataclasses import dataclass\n@dataclass\nclass P:\n    x: int\nprint(P(1) == P(1))', "False", "Xato", "None"),
    P('from dataclasses import dataclass\n@dataclass\nclass M:\n    nom: str\n    soni: int = 1\nprint(M("a").soni, M("b", 5).soni)', "None 5", "1 1", "Xato"),
    P('from dataclasses import dataclass\n@dataclass(frozen=True)\nclass P:\n    x: int\np = P(1)\ntry:\n    p.x = 2\nexcept Exception as e:\n    print(type(e).__name__)', "2", "AttributeError", "TypeError", lv=2),
    P('from dataclasses import dataclass\n@dataclass(order=True)\nclass V:\n    a: int\n    b: int\nprint(sorted([V(2, 1), V(1, 9), V(1, 3)]))', "[V(2, 1), V(1, 9), V(1, 3)]", "[V(1, 9), V(1, 3), V(2, 1)]", "Xato"),
    P('from dataclasses import dataclass, asdict\n@dataclass\nclass T:\n    ism: str\n    yosh: int\nprint(asdict(T("Ali", 17)))', "T(ism='Ali', yosh=17)", "('Ali', 17)", "['Ali', 17]"),
    P('from dataclasses import dataclass\n@dataclass\nclass B:\n    a: int\n    b: int = 0\n    def __post_init__(self):\n        self.b = self.a * 10\nprint(B(3, 1))', "B(a=3, b=1)", "B(a=3, b=0)", "Xato", lv=2),
    Q("`@dataclass` qaysi metodlarni avtomatik yaratadi?", "__init__, __repr__, __eq__", "Faqat __init__", "__str__ va __len__", "Hech qaysini"),
    Q("Dataclass'da roʻyxat turidagi standart qiymat qanday beriladi?", "field(default_factory=list)", "royxat: list = []", "royxat = list", "royxat: list = None()"),
    F("Mahsulot", "`@dataclass` `Mahsulot(nom: str, narx: int, soni: int = 1)` va `jami()` metodi.",
      "from dataclasses import dataclass\n\n\n@dataclass\nclass Mahsulot:\n    nom: str\n    narx: int\n    soni: int = 1\n\n    def jami(self):\n        return self.narx * self.soni",
      'Mahsulot("non", 4000).jami()', 'Mahsulot("sut", 12000, 3).jami()', 'repr(Mahsulot("a", 1))', 'Mahsulot("a", 1) == Mahsulot("a", 1, 1)', lv=1),
    F("Nuqta", "`@dataclass(frozen=True)` `Nuqta(x: int, y: int)` — `masofa(boshqa)` (Manhetten: `|x1-x2| + |y1-y2|`). Muzlatilgani uchun `set` ga qoʻshish mumkin boʻlsin.",
      "from dataclasses import dataclass\n\n\n@dataclass(frozen=True)\nclass Nuqta:\n    x: int\n    y: int\n\n    def masofa(self, b):\n        return abs(self.x - b.x) + abs(self.y - b.y)",
      "Nuqta(0, 0).masofa(Nuqta(3, 4))", "len({Nuqta(1, 1), Nuqta(1, 1), Nuqta(2, 2)})", "repr(Nuqta(5, -1))"),
    F("Guruh", "`@dataclass` `Guruh(nom: str, azolar: list = field(default_factory=list))` — `qosh(ism)` va `soni()` metodlari. Har bir guruhning roʻyxati alohida boʻlsin.",
      "from dataclasses import dataclass, field\n\n\n@dataclass\nclass Guruh:\n    nom: str\n    azolar: list = field(default_factory=list)\n\n    def qosh(self, ism):\n        self.azolar.append(ism)\n\n    def soni(self):\n        return len(self.azolar)",
      '(g := Guruh("A"), g.qosh("Ali"), g.qosh("Vali"), g.soni())[-1]', '(a := Guruh("A"), b := Guruh("B"), a.qosh("x"), b.soni())[-1]', 'repr(Guruh("C"))', lv=2),
    F("Reyting", "`@dataclass(order=True)` `Natija` — saralash **ball** boʻyicha boʻlsin: maydonlar tartibi `ball: int`, `ism: str`. `top3(natijalar)` — eng yaxshi 3 ta ism (kamayish tartibida).",
      "from dataclasses import dataclass\n\n\n@dataclass(order=True)\nclass Natija:\n    ball: int\n    ism: str\n\n\ndef top3(natijalar):\n    return [n.ism for n in sorted(natijalar, reverse=True)[:3]]",
      'top3([Natija(80, "A"), Natija(95, "B"), Natija(70, "C"), Natija(88, "D")])', 'top3([Natija(1, "X")])', 'Natija(5, "a") < Natija(7, "b")'),
    F("Buyurtma", "`@dataclass` `Buyurtma(narx: int, soni: int)` — `__post_init__` da `jami` atributini hisoblang; soni 0 dan kichik boʻlsa `ValueError`. `asdict` bilan lugʻatga aylantirish ishlasin (jami ham kirsin — uni `field(init=False)` qiling).",
      "from dataclasses import dataclass, field\n\n\n@dataclass\nclass Buyurtma:\n    narx: int\n    soni: int\n    jami: int = field(init=False)\n\n    def __post_init__(self):\n        if self.soni < 0:\n            raise ValueError('soni manfiy')\n        self.jami = self.narx * self.soni",
      "Buyurtma(5000, 3).jami", "__import__('dataclasses').asdict(Buyurtma(100, 2))", "Buyurtma(1, -1)", lv=3),
    F("Lugʻatdan", "`@dataclass` `Talaba(ism: str, ball: int)` va `@classmethod` `lugatdan(d)` — `{\"ism\": ..., \"ball\": ...}` dan obyekt yasasin; ortiqcha kalitlarni eʼtiborsiz qoldirsin.",
      "from dataclasses import dataclass\n\n\n@dataclass\nclass Talaba:\n    ism: str\n    ball: int\n\n    @classmethod\n    def lugatdan(cls, d):\n        return cls(d['ism'], d['ball'])",
      'repr(Talaba.lugatdan({"ism": "Ali", "ball": 90}))', 'Talaba.lugatdan({"ism": "V", "ball": 5, "yosh": 17}).ball', 'Talaba.lugatdan({"ism": "a", "ball": 1}) == Talaba("a", 1)'),
    F("Kontakt kitobi", "`@dataclass` `Kontakt(ism: str, tel: str)`. `qidir(kontaktlar, soz)` — ismida `soz` (katta-kichik farqsiz) bor kontaktlar ismlarini alifbo boʻyicha qaytarsin.",
      "from dataclasses import dataclass\n\n\n@dataclass\nclass Kontakt:\n    ism: str\n    tel: str\n\n\ndef qidir(kontaktlar, soz):\n    return sorted(k.ism for k in kontaktlar if soz.lower() in k.ism.lower())",
      'qidir([Kontakt("Ali", "1"), Kontakt("Valijon", "2"), Kontakt("Bek", "3")], "ALI")', 'qidir([], "a")', 'Kontakt("A", "1") == Kontakt("A", "1")'),
    L("docs", "py-dataclasses"),
    L("exercism", "tisbury-treasure-hunt"),
    L("lc", "time-based-key-value-store"),
    L("lc", "design-underground-system"),
])

# ---------------------------------------------------------------- 8.12
TOPIC("ichki-sinf", "Ichki sinflar va Enum", "Sinf ichida sinf, sanab oʻtiladigan qiymatlar", 15, r'''
Sinf ichida boshqa sinfni ham yaratish mumkin. **Ichki sinf** faqat tashqi sinf bilan birga maʼnoga ega boʻlgan yordamchi tushunchalar uchun ishlatiladi.

```py
class Avtomobil:
    class Dvigatel:
        def __init__(self, ot_kuchi):
            self.ot_kuchi = ot_kuchi

        def ishga_tushir(self):
            return f"{self.ot_kuchi} o.k. dvigatel ishladi"

    def __init__(self, model, ot_kuchi):
        self.model = model
        self.dvigatel = Avtomobil.Dvigatel(ot_kuchi)   # tarkib (has-a)

    def yur(self):
        return f"{self.model}: {self.dvigatel.ishga_tushir()}"

m = Avtomobil("Malibu", 250)
print(m.yur())
print(type(m.dvigatel).__qualname__)
```

> Ichki sinf — **nomlar maydonini tartiblash** usuli. U tashqi obyektning atributlarini avtomatik koʻrmaydi — kerak boʻlsa, uzatish kerak.

## Hayotiy misol: Django'dagi Meta
Django modellarida ichki `Meta` sinfi sozlamalar uchun ishlatiladi (bu kodni 13-boʻlimda koʻramiz):

```py norun
class Maqola(models.Model):
    sarlavha = models.CharField(max_length=200)

    class Meta:
        ordering = ["-sana"]
        verbose_name = "Maqola"
```

## Enum — chegaralangan qiymatlar toʻplami
Holat, rang, hafta kuni kabi **oldindan maʼlum** qiymatlar uchun `enum` eng toʻgʻri tanlov:

```py
from enum import Enum

class Holat(Enum):
    YANGI = 1
    JARAYONDA = 2
    BAJARILDI = 3

h = Holat.JARAYONDA
print(h)
print(h.name, h.value)
print(h == Holat.JARAYONDA)
print(Holat(3))
print([x.name for x in Holat])
```

## Ichki sinf + Enum: buyurtma
```py
from enum import Enum

class Buyurtma:
    class Holat(Enum):
        YANGI = "yangi"
        YOLDA = "yoʻlda"
        YETKAZILDI = "yetkazildi"

    def __init__(self, raqam):
        self.raqam = raqam
        self.holat = Buyurtma.Holat.YANGI

    def keyingi(self):
        royxat = list(Buyurtma.Holat)
        i = royxat.index(self.holat)
        if i < len(royxat) - 1:
            self.holat = royxat[i + 1]

b = Buyurtma(101)
for _ in range(3):
    print(b.raqam, b.holat.value)
    b.keyingi()
```

## Esda tuting
- Ichki sinf — `Tashqi.Ichki` orqali murojaat qilinadi.
- `Enum` — xato yozilgan "sehrli satrlar" oʻrniga xavfsiz nomlar.
''', [
    P('class A:\n    class B:\n        x = 5\nprint(A.B.x)', "Xato", "B", "None"),
    P('class A:\n    class B:\n        pass\nprint(A.B.__qualname__)', "B", "A", "__main__.B"),
    P('from enum import Enum\nclass R(Enum):\n    QIZIL = 1\n    YASHIL = 2\nprint(R.YASHIL.name, R.YASHIL.value)', "R.YASHIL 2", "2 YASHIL", "YASHIL YASHIL"),
    P('from enum import Enum\nclass R(Enum):\n    A = 1\n    B = 2\nprint(R(1))', "A", "1", "⚠ ValueError"),
    P('from enum import Enum\nclass R(Enum):\n    A = 1\n    B = 2\n    C = 3\nprint(len(R), [r.value for r in R])', "3 [A, B, C]", "[1, 2, 3]", "Xato"),
    P('from enum import Enum\nclass R(Enum):\n    A = 1\nprint(R.A == 1)', "True", "Xato", "1", lv=3,
      why="Enum aʼzosi oddiy son emas. `R.A.value == 1` toʻgʻri, `R.A == 1` — `False`."),
    P('class T:\n    class I:\n        def f(self):\n            return "ichki"\n    def g(self):\n        return T.I().f()\nprint(T().g())', "g", "T.I", "Xato"),
    Q("Ichki sinf qachon mos keladi?", "Faqat tashqi sinf bilan maʼnoga ega yordamchi tushuncha uchun", "Har doim — u kodni tezlashtiradi", "Global oʻzgaruvchilar oʻrniga", "Vorislik oʻrniga"),
    Q("`Enum` ning `\"yangi\"`, `\"bajarildi\"` kabi satrlardan afzalligi?", "Xato yozilgan nom darhol xato beradi va qiymatlar roʻyxati aniq", "Tezroq ishlaydi", "Kamroq xotira oladi", "Hech qanday farqi yoʻq"),
    F("Svetofor", "`Rang(Enum)`: `QIZIL`, `SARIQ`, `YASHIL` (qiymatlar 1, 2, 3). `keyingi(r)` funksiyasi: qizil → yashil, yashil → sariq, sariq → qizil; natijaning `.name` ini qaytarsin.",
      "from enum import Enum\n\n\nclass Rang(Enum):\n    QIZIL = 1\n    SARIQ = 2\n    YASHIL = 3\n\n\ndef keyingi(r):\n    tartib = {Rang.QIZIL: Rang.YASHIL, Rang.YASHIL: Rang.SARIQ, Rang.SARIQ: Rang.QIZIL}\n    return tartib[r].name",
      "keyingi(Rang.QIZIL)", "keyingi(Rang.YASHIL)", "keyingi(Rang.SARIQ)", "Rang(2).name", lv=1),
    F("Kutubxona", "`Kutubxona` sinfi ichida `Kitob(nom, muallif)` ichki sinfi. `qosh(nom, muallif)` kitob qoʻshsin; `muallifi(muallif)` — shu muallif kitoblari nomlari roʻyxati.",
      "class Kutubxona:\n    class Kitob:\n        def __init__(self, nom, muallif):\n            self.nom, self.muallif = nom, muallif\n\n    def __init__(self):\n        self.kitoblar = []\n\n    def qosh(self, nom, muallif):\n        self.kitoblar.append(Kutubxona.Kitob(nom, muallif))\n\n    def muallifi(self, muallif):\n        return [k.nom for k in self.kitoblar if k.muallif == muallif]",
      '(k := Kutubxona(), k.qosh("Oʻtkan kunlar", "Qodiriy"), k.qosh("Mehrobdan chayon", "Qodiriy"), k.qosh("Sarob", "Qahhor"), k.muallifi("Qodiriy"))[-1]', 'Kutubxona().muallifi("x")', 'Kutubxona.Kitob("a", "b").muallif'),
    F("Buyurtma holati", "`Buyurtma` ichida `Holat(Enum)`: `YANGI`, `YOLDA`, `YETKAZILDI`. `keyingi()` holatni bir qadam surib (oxirgisida qoladi), `holat.name` qaytarsin.",
      "from enum import Enum\n\n\nclass Buyurtma:\n    class Holat(Enum):\n        YANGI = 1\n        YOLDA = 2\n        YETKAZILDI = 3\n\n    def __init__(self):\n        self.holat = Buyurtma.Holat.YANGI\n\n    def keyingi(self):\n        r = list(Buyurtma.Holat)\n        i = r.index(self.holat)\n        self.holat = r[min(i + 1, len(r) - 1)]\n        return self.holat.name",
      "Buyurtma().keyingi()", "(b := Buyurtma(), b.keyingi(), b.keyingi(), b.keyingi())[-1]", "Buyurtma().holat.name", lv=2),
    F("Hafta kunlari", "`Kun(Enum)` — `DU=1 ... YA=7` (DU, SE, CH, PA, JU, SH, YA). `dam_olishmi(kun)` — SH yoki YA boʻlsa `True`. `kun_nomi(n)` — raqamdan nom.",
      "from enum import Enum\n\n\nclass Kun(Enum):\n    DU = 1\n    SE = 2\n    CH = 3\n    PA = 4\n    JU = 5\n    SH = 6\n    YA = 7\n\n\ndef dam_olishmi(kun):\n    return kun in (Kun.SH, Kun.YA)\n\n\ndef kun_nomi(n):\n    return Kun(n).name",
      "dam_olishmi(Kun.SH)", "dam_olishmi(Kun.CH)", "kun_nomi(5)", "[k.name for k in Kun if not dam_olishmi(k)]"),
    F("Daraxt tugunlari", "`Daraxt` sinfi ichida `Tugun(qiymat)` (bolalar roʻyxati bilan). `Daraxt(ildiz_qiymat)`; `qosh(ota_tugun, qiymat)` yangi tugun qaytarsin; `yigindi()` — barcha qiymatlar yigʻindisi (rekursiya).",
      "class Daraxt:\n    class Tugun:\n        def __init__(self, qiymat):\n            self.qiymat = qiymat\n            self.bolalar = []\n\n    def __init__(self, ildiz_qiymat):\n        self.ildiz = Daraxt.Tugun(ildiz_qiymat)\n\n    def qosh(self, ota, qiymat):\n        t = Daraxt.Tugun(qiymat)\n        ota.bolalar.append(t)\n        return t\n\n    def yigindi(self):\n        def s(t):\n            return t.qiymat + sum(s(b) for b in t.bolalar)\n        return s(self.ildiz)",
      "Daraxt(5).yigindi()", "(d := Daraxt(1), a := d.qosh(d.ildiz, 2), d.qosh(a, 3), d.qosh(d.ildiz, 4), d.yigindi())[-1]", "len(Daraxt(0).ildiz.bolalar)", lv=3),
    F("Holat mashinasi", "`Eshik` sinfi ichida `Holat(Enum)`: `YOPIQ`, `OCHIQ`, `QULFLANGAN`. Metodlar `och()`, `yop()`, `qulfla()`, `qulfni_och()` — faqat mantiqiy oʻtishlar ishlasin (qulflangan eshik ochilmaydi, ochiq eshik qulflanmaydi), har biri joriy holat nomini qaytarsin.",
      "from enum import Enum\n\n\nclass Eshik:\n    class Holat(Enum):\n        YOPIQ = 1\n        OCHIQ = 2\n        QULFLANGAN = 3\n\n    def __init__(self):\n        self.h = Eshik.Holat.YOPIQ\n\n    def och(self):\n        if self.h == Eshik.Holat.YOPIQ:\n            self.h = Eshik.Holat.OCHIQ\n        return self.h.name\n\n    def yop(self):\n        if self.h == Eshik.Holat.OCHIQ:\n            self.h = Eshik.Holat.YOPIQ\n        return self.h.name\n\n    def qulfla(self):\n        if self.h == Eshik.Holat.YOPIQ:\n            self.h = Eshik.Holat.QULFLANGAN\n        return self.h.name\n\n    def qulfni_och(self):\n        if self.h == Eshik.Holat.QULFLANGAN:\n            self.h = Eshik.Holat.YOPIQ\n        return self.h.name",
      "Eshik().och()", "(e := Eshik(), e.qulfla(), e.och())[-1]", "(e := Eshik(), e.och(), e.qulfla())[-1]", "(e := Eshik(), e.qulfla(), e.qulfni_och(), e.och())[-1]", lv=3),
    F("Oʻlchov birligi", "`Birlik(Enum)` — `MM = 0.001`, `SM = 0.01`, `M = 1`, `KM = 1000`. `aylantir(qiymat, dan, ga)` — `qiymat * dan.value / ga.value` ni 4 xonagacha yaxlitlasin.",
      "from enum import Enum\n\n\nclass Birlik(Enum):\n    MM = 0.001\n    SM = 0.01\n    M = 1\n    KM = 1000\n\n\ndef aylantir(qiymat, dan, ga):\n    return round(qiymat * dan.value / ga.value, 4)",
      "aylantir(5, Birlik.KM, Birlik.M)", "aylantir(150, Birlik.SM, Birlik.M)", "aylantir(1, Birlik.M, Birlik.MM)", "Birlik(1000).name"),
    L("docs", "py-enum"),
    L("lc", "implement-trie-prefix-tree", note="Ichki `Tugun` sinfi bilan yechiladigan klassik masala."),
    L("exercism", "tree-building"),
    L("lc", "design-twitter"),
])
