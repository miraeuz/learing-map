from dsl import TOPIC, P, Q, F, PR, L

# Section 6 continues (SECTION is declared in s6_tuzilmalar.py).

# ---------------------------------------------------------------- 6.7
TOPIC("lugat", "Lugʻat (dict)", "Kalit → qiymat juftliklari", 20, r'''
**Lugʻat** (`dict`) — har bir qiymatni **kalit** orqali saqlaydi. Telefon kitobchasi kabi: ism (kalit) → raqam (qiymat).

```py
talaba = {
    "ism": "Madina",
    "yosh": 16,
    "sinf": "10-A",
}
print(talaba["ism"])
print(talaba["yosh"] + 1)
print(len(talaba))
```

## Qoʻshish, oʻzgartirish, oʻchirish
```py
narx = {"non": 4000, "sut": 12000}
narx["tuxum"] = 1500      # yangi kalit — qoʻshiladi
narx["non"] = 4500        # bor kalit — yangilanadi
del narx["sut"]
print(narx)
```

## Xavfsiz oʻqish: get()
```py
narx = {"non": 4000}
print(narx.get("non"))
print(narx.get("choy"))
print(narx.get("choy", 0))
print("choy" in narx)
```

!> `narx["choy"]` — kalit yoʻq boʻlsa `KeyError`. Ishonchingiz komil boʻlmasa `get()` ishlating.

## Aylanib chiqish
```py
baholar = {"Ali": 5, "Vali": 4, "Sardor": 3}
for ism in baholar:
    print(ism, end=" ")
print()
for ism, baho in baholar.items():
    print(f"{ism}: {baho}")
print(list(baholar.keys()))
print(list(baholar.values()))
```

## Kalit qanday boʻlishi mumkin?
Faqat **oʻzgarmas** qiymat: son, satr, kortej. Roʻyxat kalit boʻla olmaydi.

```py
xarita = {(0, 0): "start", (3, 4): "xazina"}
print(xarita[(3, 4)])
```

## Foydali metodlar
| Metod | Nima qiladi |
|---|---|
| `d.get(k, std)` | kalit boʻlmasa std qaytaradi |
| `d.items()` | (kalit, qiymat) juftliklari |
| `d.pop(k)` | oʻchiradi va qiymatini qaytaradi |
| `d.update(boshqa)` | boshqa lugʻatni qoʻshadi |
| `d.setdefault(k, std)` | kalit yoʻq boʻlsa std bilan qoʻshadi |

> Python 3.7+ da lugʻat elementlari **qoʻshilgan tartibda** saqlanadi.

## Esda tuting
- `d[kalit]` — oʻqish/yozish; `get` — xavfsiz oʻqish.
- `for k, v in d.items()` — eng koʻp ishlatiladigan sikl.
''', [
    P('d = {"a": 1, "b": 2}\nprint(d["b"])', "1", "b", "{'b': 2}"),
    P('d = {"a": 1}\nd["a"] = 5\nd["c"] = 3\nprint(d)', "{'a': 1, 'c': 3}", "{'a': 1, 'a': 5, 'c': 3}", "{'c': 3, 'a': 5}"),
    P('d = {"x": 10}\nprint(d.get("y", 0) + d.get("x", 0))', "Xato", "None", "0"),
    P('d = {"x": 10}\nprint(d["y"])', "None", "0", "⚠ IndexError", lv=2),
    P('d = {"a": 1, "b": 2, "c": 3}\nprint(len(d), "b" in d, 2 in d)', "3 True True", "6 True False", "3 False True"),
    P('d = {"a": 1, "a": 2}\nprint(d)', "{'a': 1}", "{'a': 1, 'a': 2}", "Xato", lv=2, why="Kalit takrorlanmaydi — keyingi qiymat oldingisini almashtiradi."),
    P('d = {"x": 1, "y": 2}\nfor k, v in d.items():\n    print(k * v)', "1\n2", "x\ny", "xy"),
    Q("Kalit yoʻq boʻlsa xato bermasdan qiymat olish usuli?", "d.get(kalit)", "d[kalit]", "d.find(kalit)", "d.value(kalit)"),
    Q("Qaysi biri lugʻat kaliti boʻla **olmaydi**?", "[1, 2]", "(1, 2)", "\"ism\"", "42"),
    F("Narx", "`narx_ol(narxlar, mahsulot)` — mahsulot narxi; yoʻq boʻlsa `-1`.",
      "def narx_ol(narxlar, mahsulot):\n    return narxlar.get(mahsulot, -1)", 'narx_ol({"non": 4000}, "non")', 'narx_ol({"non": 4000}, "sut")', 'narx_ol({}, "x")', lv=1),
    F("Jami narx", "`jami(savat)` — `{mahsulot: narx}` lugʻatidagi narxlar yigʻindisi.",
      "def jami(savat):\n    return sum(savat.values())", 'jami({"non": 4000, "sut": 12000})', "jami({})", 'jami({"a": 1})', lv=1),
    F("Eng yaxshi oʻquvchi", "`eng_yaxshi(baholar)` — eng yuqori ball olgan oʻquvchi ismini qaytaring.",
      "def eng_yaxshi(baholar):\n    return max(baholar, key=baholar.get)", 'eng_yaxshi({"Ali": 80, "Vali": 95, "Bek": 70})', 'eng_yaxshi({"Yolgʻiz": 1})', 'eng_yaxshi({"A": -1, "B": -5})'),
    F("Teskari lugʻat", "`teskari(d)` — kalit va qiymatlar oʻrnini almashtiring.",
      "def teskari(d):\n    return {v: k for k, v in d.items()}", 'teskari({"a": 1, "b": 2})', "teskari({})", 'teskari({1: "bir"})'),
    F("Juftliklardan", "`yasash(kalitlar, qiymatlar)` — ikki roʻyxatdan lugʻat yasang.",
      "def yasash(kalitlar, qiymatlar):\n    return dict(zip(kalitlar, qiymatlar))", 'yasash(["a", "b"], [1, 2])', "yasash([], [])", 'yasash(["x"], [True])'),
    F("Oʻtganlar", "`otganlar(baholar)` — 60 va undan yuqori ball olganlar ismlari (lugʻatdagi tartibda).",
      "def otganlar(baholar):\n    return [ism for ism, b in baholar.items() if b >= 60]", 'otganlar({"Ali": 59, "Vali": 60, "Bek": 99})', "otganlar({})", 'otganlar({"A": 10})'),
    F("Narxni oshirish", "`oshir(narxlar, foiz)` — har bir narxni `foiz` % ga oshirilgan **yangi** lugʻat (butun songa yaxlitlang: `round`).",
      "def oshir(narxlar, foiz):\n    return {k: round(v * (100 + foiz) / 100) for k, v in narxlar.items()}", 'oshir({"non": 4000, "sut": 12000}, 10)', 'oshir({}, 50)', 'oshir({"x": 99}, 0)', lv=3),
    L("lc", "two-sum", note="Lugʻatda «koʻrilgan son → indeks»ni saqlang — O(n) yechim."),
    L("lc", "ransom-note"),
    L("exercism", "inventory-management", note="Lugʻatlar boʻyicha maxsus mashq."),
    L("lc", "decode-the-message"),
])

# ---------------------------------------------------------------- 6.8
TOPIC("lugat-amaliy", "Lugʻat amaliyotda: sanash va guruhlash", "Counter, defaultdict, ichma-ich lugʻat", 25, r'''
Dasturlashdagi eng koʻp uchraydigan vazifalardan biri — **sanash**: qaysi soʻz necha marta, qaysi baho nechta, qaysi mahsulot qancha sotildi.

## Qoʻlda sanash
```py
matn = "olma nok olma uzum olma nok"
sanoq = {}
for soz in matn.split():
    sanoq[soz] = sanoq.get(soz, 0) + 1
print(sanoq)
```

## Counter — tayyor sanagich
```py
from collections import Counter

c = Counter("abrakadabra")
print(c["a"], c["z"])
print(c.most_common(2))

ovozlar = ["Ali", "Vali", "Ali", "Bek", "Ali", "Vali"]
print(Counter(ovozlar).most_common(1)[0])
```

## Guruhlash: defaultdict
```py
from collections import defaultdict

sozlar = ["olma", "anor", "nok", "nar", "uzum"]
guruh = defaultdict(list)
for s in sozlar:
    guruh[s[0]].append(s)
print(dict(guruh))
```

> `defaultdict(list)` — yoʻq kalitga murojaat qilinganda avtomatik `[]` yaratadi. `defaultdict(int)` esa `0`.

## Lugʻat ifodasi (comprehension)
```py
sonlar = [1, 2, 3, 4]
kvadrat = {x: x * x for x in sonlar}
print(kvadrat)

baholar = {"Ali": 85, "Vali": 45, "Bek": 70}
otganlar = {k: v for k, v in baholar.items() if v >= 60}
print(otganlar)
```

## Ichma-ich lugʻat — haqiqiy maʼlumot
JSON va API javoblari aynan shunday koʻrinadi:

```py
maktab = {
    "10-A": {"rahbar": "Karimova", "oquvchilar": ["Ali", "Vali"]},
    "10-B": {"rahbar": "Sobirov", "oquvchilar": ["Madina"]},
}
for sinf, info in maktab.items():
    print(sinf, info["rahbar"], len(info["oquvchilar"]))
```

## Saralash
```py
sotuv = {"non": 120, "sut": 300, "choy": 80}
for nom, soni in sorted(sotuv.items(), key=lambda p: p[1], reverse=True):
    print(f"{nom:<6}{soni:>5}")
```

## Esda tuting
- Sanash: `d[k] = d.get(k, 0) + 1` yoki `Counter`.
- Guruhlash: `defaultdict(list)`.
''', [
    P('d = {}\nfor h in "aba":\n    d[h] = d.get(h, 0) + 1\nprint(d)', "{'a': 1, 'b': 1}", "{'a': 2, 'b': 1, 'a': 1}", "{'b': 1, 'a': 2}"),
    P('from collections import Counter\nprint(Counter("hello")["l"])', "1", "3", "0"),
    P('from collections import Counter\nprint(Counter([1, 1, 2]).most_common(1))', "[(2, 1)]", "1", "(1, 2)"),
    P('print({x: x * 2 for x in range(3)})', "{0: 2, 1: 4, 2: 6}", "[0, 2, 4]", "{0, 2, 4}"),
    P('from collections import defaultdict\nd = defaultdict(int)\nd["a"] += 5\nprint(d["a"], d["b"])', "5 None", "Xato", "5 5", lv=2),
    P('d = {"b": 2, "a": 1}\nprint(sorted(d))', "[2, 1]", "[('a', 1), ('b', 2)]", "{'a': 1, 'b': 2}"),
    P('m = {"x": {"y": 7}}\nprint(m["x"]["y"])', "{'y': 7}", "x", "Xato"),
    Q("`Counter(soʻzlar).most_common(3)` nima qaytaradi?", "Eng koʻp uchragan 3 ta (element, soni) juftligi", "Eng uzun 3 ta soʻz", "Dastlabki 3 ta soʻz", "3 ta tasodifiy soʻz"),
    Q("`defaultdict(list)` ning foydasi?", "Yoʻq kalit uchun avtomatik boʻsh roʻyxat yaratadi", "Kalitlarni saralaydi", "Faqat roʻyxat saqlashga ruxsat beradi", "Takrorlarni olib tashlaydi"),
    F("Harflar soni", "`harflar(matn)` — har bir belgining necha marta uchrashini lugʻatda qaytaring (uchrash tartibida).",
      "def harflar(matn):\n    d = {}\n    for h in matn:\n        d[h] = d.get(h, 0) + 1\n    return d", 'harflar("salom")', 'harflar("")', 'harflar("aaab")', lv=1),
    F("Eng koʻp soʻz", "`eng_kop(matn)` — matnda eng koʻp uchragan soʻz (teng boʻlsa — avval uchragani).",
      "def eng_kop(matn):\n    from collections import Counter\n    return Counter(matn.split()).most_common(1)[0][0]", 'eng_kop("olma nok olma")', 'eng_kop("bir")', 'eng_kop("a b b a c")'),
    F("Anagramma", "`anagramma(a, b)` — ikki soʻz bir xil harflardan tuzilganmi?",
      "def anagramma(a, b):\n    from collections import Counter\n    return Counter(a) == Counter(b)", 'anagramma("listen", "silent")', 'anagramma("aab", "abb")', 'anagramma("", "")'),
    F("Bosh harf boʻyicha", "`guruhla(sozlar)` — soʻzlarni birinchi harfi boʻyicha guruhlang: `{harf: [soʻzlar]}`.",
      "def guruhla(sozlar):\n    d = {}\n    for s in sozlar:\n        d.setdefault(s[0], []).append(s)\n    return d", 'guruhla(["olma", "anor", "olcha"])', "guruhla([])", 'guruhla(["b", "a", "bb"])'),
    F("Bir marta", "`yagona(a)` — roʻyxatda **aynan bir marta** uchragan elementlar (uchrash tartibida).",
      "def yagona(a):\n    from collections import Counter\n    c = Counter(a)\n    return [x for x in a if c[x] == 1]", "yagona([1, 2, 1, 3])", "yagona([5, 5])", 'yagona(["x"])'),
    F("Sinf oʻrtachasi", "`ortachalar(d)` — `{ism: [ballar]}` dan `{ism: oʻrtacha}` lugʻatini yasang.",
      "def ortachalar(d):\n    return {k: sum(v) / len(v) for k, v in d.items()}", 'ortachalar({"Ali": [80, 90], "Vali": [70]})', "ortachalar({})", 'ortachalar({"A": [1, 2, 3, 4]})'),
    F("Birinchi takrorlanmas", "`birinchi_yagona(s)` — satrdagi birinchi takrorlanmaydigan belgi indeksi; yoʻq boʻlsa `-1`.",
      "def birinchi_yagona(s):\n    from collections import Counter\n    c = Counter(s)\n    for i, h in enumerate(s):\n        if c[h] == 1:\n            return i\n    return -1", 'birinchi_yagona("leetcode")', 'birinchi_yagona("aabb")', 'birinchi_yagona("loveleetcode")', lv=3),
    L("lc", "valid-anagram"),
    L("lc", "first-unique-character-in-a-string"),
    L("lc", "group-anagrams", note="Kalit sifatida `''.join(sorted(soz))` dan foydalaning."),
    L("exercism", "word-count"),
])

# ---------------------------------------------------------------- 6.9
TOPIC("massiv", "Massiv (array) va roʻyxat", "array moduli, tezlik va xotira", 15, r'''
Pythonda "massiv" deganda koʻpincha oddiy **roʻyxat** nazarda tutiladi. Lekin standart kutubxonada haqiqiy massiv ham bor: `array`. U faqat **bir turdagi** sonlarni saqlaydi va kamroq xotira oladi.

```py
from array import array

a = array("i", [10, 20, 30])    # "i" — butun sonlar
a.append(40)
print(a)
print(a[1], len(a), sum(a))
```

## Tur kodlari
| Kod | Tur | Misol |
|---|---|---|
| `"i"` | butun son | `array("i", [1, 2])` |
| `"f"`, `"d"` | haqiqiy son | `array("d", [1.5])` |
| `"b"` | kichik butun (-128..127) | bayt maʼlumoti |

!> Massivga boshqa turdagi qiymat qoʻshib boʻlmaydi:

```py xato
from array import array
a = array("i", [1, 2])
a.append("salom")
```

## Roʻyxat va massiv
| | `list` | `array` |
|---|---|---|
| Turlar | aralash | faqat bitta |
| Xotira | koʻproq | kamroq |
| Qachon | deyarli doim | juda koʻp son saqlashda |

> Ilmiy hisob-kitoblarda **NumPy** massivlari ishlatiladi — ular yanada tez. Hozircha roʻyxat yetarli.

## Massiv tafakkuri: indeks bilan ishlash
Olimpiada masalalarida asosiy narsa — massiv ustida **indekslar** bilan ishlash: prefiks yigʻindi, ikki koʻrsatkich, siljuvchi oyna.

## Prefiks yigʻindi
`pre[i]` — dastlabki i ta element yigʻindisi. Keyin istalgan `[l, r)` oraliq yigʻindisi bitta ayirish bilan topiladi:

```py
a = [3, 1, 4, 1, 5, 9, 2]
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
print(pre)
l, r = 2, 5
print("a[2:5] yigʻindisi:", pre[r] - pre[l], "=", sum(a[l:r]))
```

## Ikki koʻrsatkich
Saralangan massivda yigʻindisi berilgan songa teng juftlik:

```py
a = [1, 3, 4, 6, 8, 11]
maqsad = 10
i, j = 0, len(a) - 1
while i < j:
    s = a[i] + a[j]
    if s == maqsad:
        print("Topildi:", a[i], a[j])
        break
    if s < maqsad:
        i += 1
    else:
        j -= 1
```

## Esda tuting
- Kundalik ishda — `list`; xotira muhim boʻlsa — `array`.
- Prefiks yigʻindi va ikki koʻrsatkich — massiv masalalarining asosiy usullari.
''', [
    P('from array import array\na = array("i", [1, 2, 3])\nprint(a[0] + a[2])', "3", "[1, 3]", "Xato"),
    P('from array import array\na = array("i", [5])\na.append(7)\nprint(len(a), sum(a))', "1 5", "2 7", "Xato"),
    P('from array import array\na = array("i", [1])\na.append(2.5)\nprint(a)', "array('i', [1, 2.5])", "array('i', [1, 2])", "[1, 2.5]", lv=2),
    P('a = [2, 4, 6]\npre = [0]\nfor x in a:\n    pre.append(pre[-1] + x)\nprint(pre)', "[2, 6, 12]", "[0, 2, 4, 6]", "12"),
    P('pre = [0, 3, 4, 8, 9]\nprint(pre[4] - pre[1])', "9", "5", "8"),
    P('a = [1, 2, 3, 4]\ni, j = 0, len(a) - 1\nwhile i < j:\n    a[i], a[j] = a[j], a[i]\n    i += 1\n    j -= 1\nprint(a)', "[1, 2, 3, 4]", "[4, 2, 3, 1]", "[2, 1, 4, 3]"),
    P('a = [5, 1, 4]\nprint(a.index(max(a)))', "5", "2", "1"),
    Q("`array` ning `list` dan asosiy farqi?", "Faqat bir turdagi qiymatlarni saqlaydi va kam xotira oladi", "U oʻzgarmas", "Unda indeks yoʻq", "U faqat satrlarni saqlaydi"),
    Q("Prefiks yigʻindi `pre` boʻlsa, `a[l:r]` yigʻindisi qanday topiladi?", "pre[r] - pre[l]", "pre[r] + pre[l]", "pre[l] - pre[r]", "pre[r - l]"),
    F("Prefiks yigʻindi", "`prefiks(a)` — `[0, a0, a0+a1, ...]` roʻyxatini qaytaring (uzunligi `len(a)+1`).",
      "def prefiks(a):\n    pre = [0]\n    for x in a:\n        pre.append(pre[-1] + x)\n    return pre", "prefiks([1, 2, 3])", "prefiks([])", "prefiks([5, -5])", lv=1),
    F("Oraliq yigʻindisi", "`oraliq(a, l, r)` — `a[l]` dan `a[r]` gacha (ikkalasi ham kiradi) elementlar yigʻindisi.",
      "def oraliq(a, l, r):\n    return sum(a[l:r + 1])", "oraliq([1, 2, 3, 4], 1, 2)", "oraliq([5], 0, 0)", "oraliq([1, 1, 1, 1], 0, 3)", lv=1),
    F("Juftlik bormi", "`juftlik(a, k)` — **saralangan** `a` da yigʻindisi k ga teng ikki xil indeksli element bormi? (ikki koʻrsatkich)",
      "def juftlik(a, k):\n    i, j = 0, len(a) - 1\n    while i < j:\n        s = a[i] + a[j]\n        if s == k:\n            return True\n        if s < k:\n            i += 1\n        else:\n            j -= 1\n    return False", "juftlik([1, 3, 4, 6], 10)", "juftlik([1, 2], 5)", "juftlik([5], 10)", "juftlik([2, 2, 3], 4)", lv=3),
    F("Nollarni oxiriga", "`nollar_oxiriga(a)` — nollarni oxiriga suring, qolganlar tartibi saqlansin.",
      "def nollar_oxiriga(a):\n    b = [x for x in a if x != 0]\n    return b + [0] * (len(a) - len(b))", "nollar_oxiriga([0, 1, 0, 3, 12])", "nollar_oxiriga([0])", "nollar_oxiriga([1, 2])"),
    F("Aylantirish", "`aylantir(a, k)` — roʻyxatni k qadam oʻngga aylantiring: `[1,2,3,4], 1 → [4,1,2,3]`.",
      "def aylantir(a, k):\n    if not a:\n        return a\n    k %= len(a)\n    return a[-k:] + a[:-k] if k else a[:]", "aylantir([1, 2, 3, 4], 1)", "aylantir([1, 2, 3], 3)", "aylantir([1, 2, 3], 5)", "aylantir([], 2)", lv=3),
    F("Oʻsuvchimi", "`osuvchi(a)` — har bir element oldingisidan kattami?",
      "def osuvchi(a):\n    return all(a[i] < a[i + 1] for i in range(len(a) - 1))", "osuvchi([1, 2, 5])", "osuvchi([1, 1, 2])", "osuvchi([])", "osuvchi([3, 2])"),
    F("Eng katta k-oyna", "`oyna(a, k)` — ketma-ket k ta element yigʻindisining eng kattasi.",
      "def oyna(a, k):\n    s = sum(a[:k])\n    eng = s\n    for i in range(k, len(a)):\n        s += a[i] - a[i - k]\n        eng = max(eng, s)\n    return eng", "oyna([1, 4, 2, 10, 2], 2)", "oyna([5, 5], 2)", "oyna([-1, -2, -3], 1)", lv=3),
    L("lc", "move-zeroes"),
    L("lc", "rotate-array"),
    L("lc", "two-sum-ii-input-array-is-sorted", note="Ikki koʻrsatkich usuli."),
    L("cses", 1646, note="Prefiks yigʻindi — klassik masala."),
])

# ---------------------------------------------------------------- 6.10
TOPIC("stek", "Stek (stack)", "Oxirgi kirgan — birinchi chiqadi (LIFO)", 20, r'''
**Stek** — likopchalar ustuni kabi: yangisi **tepaga** qoʻyiladi va olinadi ham **tepadan**. Bu qoida **LIFO** (Last In, First Out) deyiladi.

Hayotda: brauzerdagi "Orqaga" tugmasi, matn muharriridagi Ctrl+Z, funksiya chaqiruvlari.

## Pythonda stek = roʻyxat
```py
stek = []
stek.append("1-sahifa")   # push
stek.append("2-sahifa")
stek.append("3-sahifa")
print(stek[-1])           # tepada nima bor (peek)
print(stek.pop())         # olish (pop)
print(stek)
print(len(stek) == 0)     # boʻshmi?
```

| Amal | Python | Tezlik |
|---|---|---|
| push | `s.append(x)` | O(1) |
| pop | `s.pop()` | O(1) |
| peek | `s[-1]` | O(1) |
| boʻshmi | `not s` | O(1) |

!> `pop(0)` stek uchun emas — u sekin va LIFO emas. Faqat `pop()`.

## Klassik masala: qavslar toʻgʻrimi?
```py
def togri(s):
    juft = {")": "(", "]": "[", "}": "{"}
    stek = []
    for h in s:
        if h in "([{":
            stek.append(h)
        elif h in juft:
            if not stek or stek.pop() != juft[h]:
                return False
    return not stek

print(togri("([]{})"))
print(togri("([)]"))
print(togri("(("))
```

## Undo (bekor qilish)
```py
matn = ""
tarix = []
for harf in "salom":
    tarix.append(matn)
    matn += harf
print(matn)
matn = tarix.pop()
matn = tarix.pop()
print(matn)
```

## Satrni teskari aylantirish
```py
stek = list("Python")
natija = ""
while stek:
    natija += stek.pop()
print(natija)
```

## Esda tuting
- Stek: `append` + `pop` (oxiridan).
- "Oxirgisi bilan solishtirish" kerak boʻlgan har qanday masala — stek.
''', [
    P('s = []\ns.append(1)\ns.append(2)\ns.append(3)\nprint(s.pop())', "1", "[1, 2]", "2"),
    P('s = [1, 2, 3]\ns.pop()\ns.append(9)\nprint(s)', "[9, 1, 2]", "[1, 2, 3, 9]", "[9, 2, 3]"),
    P('s = [5]\nprint(s[-1], len(s))', "5 0", "[5] 1", "-1 1"),
    P('s = []\nprint(not s)', "False", "[]", "None"),
    P('s = list("abc")\nr = ""\nwhile s:\n    r += s.pop()\nprint(r)', "abc", "a", "c"),
    P('s = []\nfor x in [1, 2, 3]:\n    s.append(x * x)\nprint(s.pop() + s.pop())', "5", "14", "Xato"),
    P('s = []\ns.pop()', "None", "[]", "⚠ KeyError", lv=2),
    Q("Stek qaysi qoida boʻyicha ishlaydi?", "LIFO — oxirgi kirgan birinchi chiqadi", "FIFO — birinchi kirgan birinchi chiqadi", "Tasodifiy tartibda", "Eng kichigi birinchi chiqadi"),
    Q("Qaysi vazifa uchun stek eng mos?", "Qavslar toʻgʻri yopilganini tekshirish", "Bank navbatini boshqarish", "Sonlarni saralash", "Takrorlarni olib tashlash"),
    F("Qavslar", "`togri(s)` — `()[]{}` qavslar toʻgʻri yopilganmi?",
      'def togri(s):\n    juft = {")": "(", "]": "[", "}": "{"}\n    stek = []\n    for h in s:\n        if h in "([{":\n            stek.append(h)\n        elif h in juft:\n            if not stek or stek.pop() != juft[h]:\n                return False\n    return not stek', 'togri("()[]{}")', 'togri("(]")', 'togri("({[]})")', 'togri("(")', 'togri("")', lv=2),
    F("Stek bilan teskari", "`teskari(s)` — satrni stek yordamida teskari aylantiring.",
      "def teskari(s):\n    stek = list(s)\n    r = ''\n    while stek:\n        r += stek.pop()\n    return r", 'teskari("salom")', 'teskari("")', 'teskari("ab")', lv=1),
    F("Buyruqlar", "`bajar(buyruqlar)` — `\"push X\"` va `\"pop\"` buyruqlarini bajaring, oxirida stekni qaytaring.",
      "def bajar(buyruqlar):\n    s = []\n    for b in buyruqlar:\n        if b == 'pop':\n            s.pop()\n        else:\n            s.append(int(b.split()[1]))\n    return s", 'bajar(["push 1", "push 2", "pop", "push 5"])', "bajar([])", 'bajar(["push 7", "pop"])'),
    F("Qoʻshni juftlarni oʻchirish", "`tozala(s)` — yonma-yon turgan bir xil harflarni qayta-qayta oʻchiring: `\"abbaca\" → \"ca\"`.",
      "def tozala(s):\n    st = []\n    for h in s:\n        if st and st[-1] == h:\n            st.pop()\n        else:\n            st.append(h)\n    return ''.join(st)", 'tozala("abbaca")', 'tozala("aa")', 'tozala("abc")', lv=3),
    F("Backspace", "`yoz(s)` — `#` belgisi oldingi harfni oʻchiradi. Natijaviy matnni qaytaring: `\"ab#c\" → \"ac\"`.",
      "def yoz(s):\n    st = []\n    for h in s:\n        if h == '#':\n            if st:\n                st.pop()\n        else:\n            st.append(h)\n    return ''.join(st)", 'yoz("ab#c")', 'yoz("##a")', 'yoz("abc##")', 'yoz("")'),
    F("Teskari polyak yozuvi", "`hisobla(tokenlar)` — `[\"2\", \"3\", \"+\", \"4\", \"*\"]` → `(2+3)*4 = 20`. Amallar: `+ - *`.",
      "def hisobla(tokenlar):\n    st = []\n    for t in tokenlar:\n        if t in '+-*':\n            b = st.pop()\n            a = st.pop()\n            st.append(a + b if t == '+' else a - b if t == '-' else a * b)\n        else:\n            st.append(int(t))\n    return st[-1]", 'hisobla(["2", "3", "+", "4", "*"])', 'hisobla(["5"])', 'hisobla(["10", "4", "-", "2", "-"])', lv=3),
    F("Eng chuqur", "`chuqurlik(s)` — qavslarning eng katta ichma-ichlik darajasi: `\"(()(()))\" → 3`.",
      "def chuqurlik(s):\n    d = eng = 0\n    for h in s:\n        if h == '(':\n            d += 1\n            eng = max(eng, d)\n        elif h == ')':\n            d -= 1\n    return eng", 'chuqurlik("(()(()))")', 'chuqurlik("")', 'chuqurlik("()()")'),
    L("lc", "valid-parentheses"),
    L("lc", "baseball-game"),
    L("lc", "min-stack"),
    L("exercism", "matching-brackets"),
])

# ---------------------------------------------------------------- 6.11
TOPIC("navbat", "Navbat (queue) va deque", "Birinchi kirgan — birinchi chiqadi (FIFO)", 20, r'''
**Navbat** — doʻkon kassasidagi navbat kabi: kim birinchi kelsa, oʻsha birinchi xizmat oladi. Bu qoida **FIFO** (First In, First Out).

Hayotda: printer vazifalari, server soʻrovlari, BFS algoritmi.

## deque — ikki tomonlama navbat
Roʻyxatda `pop(0)` sekin (hamma elementlar suriladi). Shuning uchun `collections.deque` ishlatiladi:

```py
from collections import deque

navbat = deque()
navbat.append("Ali")       # oxiriga qoʻshish
navbat.append("Vali")
navbat.append("Madina")
print(navbat.popleft())    # boshidan olish
print(navbat.popleft())
print(list(navbat))
```

| Amal | deque | Tezlik |
|---|---|---|
| oxiriga qoʻshish | `q.append(x)` | O(1) |
| boshidan olish | `q.popleft()` | O(1) |
| boshiga qoʻshish | `q.appendleft(x)` | O(1) |
| oxiridan olish | `q.pop()` | O(1) |
| aylantirish | `q.rotate(k)` | O(k) |

## Amaliy misol: kassa simulyatsiyasi
```py
from collections import deque

mijozlar = deque([("Ali", 3), ("Vali", 1), ("Madina", 2)])
vaqt = 0
while mijozlar:
    ism, daqiqa = mijozlar.popleft()
    vaqt += daqiqa
    print(f"{ism} {vaqt}-daqiqada ketdi")
```

## Aylana navbat: Iosif masalasi
n kishi aylana boʻlib turibdi, har k-chi chiqib ketadi:

```py
from collections import deque

def iosif(n, k):
    q = deque(range(1, n + 1))
    tartib = []
    while q:
        q.rotate(-(k - 1))
        tartib.append(q.popleft())
    return tartib

print(iosif(7, 2))
```

## maxlen — oxirgi N ta
```py
from collections import deque

oxirgi = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
    oxirgi.append(x)
print(list(oxirgi))
```

> Stek — oxiridan oladi (`pop`), navbat — boshidan (`popleft`). Ikkalasini ham `deque` bilan qilish mumkin.

## Esda tuting
- Navbat uchun `deque`: `append` + `popleft`.
- `list.pop(0)` kichik roʻyxatda ishlaydi, lekin katta maʼlumotda juda sekin.
''', [
    P('from collections import deque\nq = deque([1, 2, 3])\nprint(q.popleft())', "3", "[2, 3]", "deque([2, 3])"),
    P('from collections import deque\nq = deque([1, 2])\nq.appendleft(0)\nq.append(3)\nprint(list(q))', "[1, 2, 0, 3]", "[3, 1, 2, 0]", "[0, 3, 1, 2]"),
    P('from collections import deque\nq = deque([1, 2, 3, 4])\nq.rotate(1)\nprint(list(q))', "[2, 3, 4, 1]", "[1, 2, 3, 4]", "[4, 3, 2, 1]"),
    P('from collections import deque\nq = deque(maxlen=2)\nfor x in "abc":\n    q.append(x)\nprint("".join(q))', "abc", "ab", "c"),
    P('q = [1, 2, 3]\nq.append(q.pop(0))\nprint(q)', "[1, 2, 3, 1]", "[3, 1, 2]", "[1, 2]"),
    P('from collections import deque\nq = deque()\nq.append(5)\nq.append(6)\nprint(q.pop(), q.popleft())', "5 6", "5 5", "6 6"),
    P('from collections import deque\nq = deque(["A", "B"])\nwhile q:\n    x = q.popleft()\n    print(x, end="")\n    if x == "A":\n        q.append("C")', "AB", "ACB", "ABCA", lv=2),
    Q("Navbat qaysi qoida boʻyicha ishlaydi?", "FIFO — birinchi kirgan birinchi chiqadi", "LIFO — oxirgi kirgan birinchi chiqadi", "Eng kattasi birinchi chiqadi", "Tasodifiy"),
    Q("Nega navbat uchun `list.pop(0)` emas, `deque.popleft()` ishlatiladi?", "pop(0) barcha elementlarni suradi va sekin, popleft O(1)", "pop(0) xato beradi", "deque saralangan", "Farqi yoʻq"),
    F("Kassa", "`chiqish_vaqtlari(vaqtlar)` — har bir mijozga ketadigan daqiqalar berilgan; har biri navbatdan chiqadigan vaqtni qaytaring.",
      "def chiqish_vaqtlari(vaqtlar):\n    t = 0\n    natija = []\n    for v in vaqtlar:\n        t += v\n        natija.append(t)\n    return natija", "chiqish_vaqtlari([3, 1, 2])", "chiqish_vaqtlari([])", "chiqish_vaqtlari([5])", lv=1),
    F("Iosif", "`iosif(n, k)` — n kishi aylanada, har k-chi chiqadi. Oxirgi qolgan kishi raqamini qaytaring (1 dan).",
      "def iosif(n, k):\n    from collections import deque\n    q = deque(range(1, n + 1))\n    while len(q) > 1:\n        q.rotate(-(k - 1))\n        q.popleft()\n    return q[0]", "iosif(7, 2)", "iosif(1, 3)", "iosif(5, 3)", "iosif(10, 1)", lv=3),
    F("Aylana", "`aylana(a, k)` — navbat boshidagi elementni k marta oxiriga oʻtkazing va natijani roʻyxat sifatida qaytaring.",
      "def aylana(a, k):\n    from collections import deque\n    q = deque(a)\n    for _ in range(k):\n        if q:\n            q.append(q.popleft())\n    return list(q)", "aylana([1, 2, 3], 1)", "aylana([1, 2, 3], 3)", "aylana([], 5)"),
    F("Oxirgi uchtasi", "`oxirgi_n(a, n)` — oqimdagi oxirgi n ta element (deque maxlen bilan).",
      "def oxirgi_n(a, n):\n    from collections import deque\n    return list(deque(a, maxlen=n))", "oxirgi_n([1, 2, 3, 4, 5], 3)", "oxirgi_n([1], 3)", "oxirgi_n([1, 2], 0)"),
    F("Chipta navbati", "`chipta(t, k)` — `t[i]` — i-kishiga kerak chiptalar. Har kim 1 soniyada 1 chipta oladi va (kerak boʻlsa) navbat oxiriga turadi. k-kishi qachon tugatadi?",
      "def chipta(t, k):\n    from collections import deque\n    q = deque((v, i) for i, v in enumerate(t))\n    vaqt = 0\n    while q:\n        v, i = q.popleft()\n        vaqt += 1\n        if v == 1:\n            if i == k:\n                return vaqt\n        else:\n            q.append((v - 1, i))", "chipta([2, 3, 2], 2)", "chipta([5, 1, 1, 1], 0)", "chipta([1], 0)", lv=3),
    F("Siljuvchi oʻrtacha", "`ortacha_oqim(a, n)` — har qadamda oxirgi n ta qiymat oʻrtachasi roʻyxati.",
      "def ortacha_oqim(a, n):\n    from collections import deque\n    q = deque(maxlen=n)\n    natija = []\n    for x in a:\n        q.append(x)\n        natija.append(sum(q) / len(q))\n    return natija", "ortacha_oqim([2, 4, 6, 8], 2)", "ortacha_oqim([], 3)", "ortacha_oqim([3, 3, 9], 3)"),
    F("Navbat buyruqlari", "`navbat(buyruqlar)` — `\"add X\"` navbatga qoʻshadi, `\"next\"` boshidagini chiqaradi. Chiqarilganlar roʻyxatini qaytaring.",
      "def navbat(buyruqlar):\n    from collections import deque\n    q = deque()\n    chiqdi = []\n    for b in buyruqlar:\n        if b == 'next':\n            chiqdi.append(q.popleft())\n        else:\n            q.append(b.split()[1])\n    return chiqdi", 'navbat(["add Ali", "add Vali", "next", "add Bek", "next"])', "navbat([])", 'navbat(["add X", "next"])'),
    L("lc", "number-of-recent-calls"),
    L("lc", "time-needed-to-buy-tickets"),
    L("lc", "implement-queue-using-stacks"),
    L("cses", 2162, note="Iosif masalasi — `deque.rotate` bilan."),
])

# ---------------------------------------------------------------- 6.12
TOPIC("zip-enumerate", "zip va enumerate", "Bir nechta roʻyxatni birga aylanish", 15, r'''
Ikki qulay yordamchi: `enumerate` — element bilan birga **indeks**ni beradi, `zip` — bir nechta roʻyxatni **yonma-yon** aylantiradi.

## enumerate
```py
mevalar = ["olma", "nok", "uzum"]
for i, m in enumerate(mevalar):
    print(i, m)

for raqam, m in enumerate(mevalar, start=1):
    print(f"{raqam}. {m}")
```

> `range(len(a))` yozishdan oldin oʻylang: `enumerate(a)` koʻpincha chiroyliroq.

## zip
```py
ismlar = ["Ali", "Vali", "Madina"]
ballar = [85, 92, 78]
for ism, ball in zip(ismlar, ballar):
    print(f"{ism:<8}{ball}")
```

## zip — eng qisqasigacha
```py
print(list(zip([1, 2, 3], "ab")))
```

!> Roʻyxatlar uzunligi har xil boʻlsa, `zip` qisqasi tugashi bilan toʻxtaydi — ortiqcha elementlar jimgina tashlab yuboriladi.

## zip bilan lugʻat
```py
kalitlar = ["ism", "yosh", "shahar"]
qiymatlar = ["Aziz", 17, "Samarqand"]
odam = dict(zip(kalitlar, qiymatlar))
print(odam)
```

## Qoʻshni elementlar
```py
harorat = [18, 21, 19, 25, 24]
for kecha, bugun in zip(harorat, harorat[1:]):
    print(bugun - kecha, end=" ")
print()
```

## zip(*m) — transpozitsiya
```py
m = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*m)))
```

## Ikkalasi birga
```py
a = [3, 8, 1]
b = [3, 5, 1]
for i, (x, y) in enumerate(zip(a, b)):
    if x != y:
        print("Farq", i, "-oʻrinda:", x, "≠", y)
```

## Esda tuting
- `enumerate(a, start=1)` — 1 dan sanash.
- `zip(a, b)` — juftliklar; `dict(zip(...))` — lugʻat.
''', [
    P('for i, x in enumerate("ab"):\n    print(i, x)', "1 a\n2 b", "a 0\nb 1", "0 1\na b"),
    P('print(list(enumerate([7, 8], start=1)))', "[(0, 7), (1, 8)]", "[1, 2]", "[(7, 1), (8, 2)]"),
    P('print(list(zip([1, 2, 3], ["a", "b"])))', "[(1, 'a'), (2, 'b'), (3, None)]", "[1, 'a', 2, 'b']", "Xato"),
    P('print(dict(zip("ab", [1, 2])))', "[('a', 1), ('b', 2)]", "{'ab': [1, 2]}", "{1: 'a', 2: 'b'}"),
    P('a = [1, 4, 9]\nprint([y - x for x, y in zip(a, a[1:])])', "[1, 4, 9]", "[0, 3, 5]", "[3, 5, 0]"),
    P('print(list(zip(*[[1, 2], [3, 4]])))', "[(1, 2), (3, 4)]", "[1, 3, 2, 4]", "[[1, 3], [2, 4]]", lv=2),
    P('s = 0\nfor a, b in zip([1, 2], [10, 20]):\n    s += a * b\nprint(s)', "33", "30", "[10, 40]"),
    Q("`enumerate(a)` har qadamda nima beradi?", "(indeks, element) juftligini", "Faqat indeksni", "Faqat elementni", "Roʻyxat uzunligini"),
    Q("`zip([1, 2, 3], [4, 5])` nechta juftlik beradi?", "2", "3", "5", "Xato beradi"),
    F("Skalyar koʻpaytma", "`skalyar(a, b)` — `a0*b0 + a1*b1 + ...`.",
      "def skalyar(a, b):\n    return sum(x * y for x, y in zip(a, b))", "skalyar([1, 2, 3], [4, 5, 6])", "skalyar([], [])", "skalyar([2], [-3])", lv=1),
    F("Raqamlash", "`raqamla(a)` — `[\"olma\", \"nok\"] → [\"1. olma\", \"2. nok\"]`.",
      'def raqamla(a):\n    return [f"{i}. {x}" for i, x in enumerate(a, start=1)]', 'raqamla(["olma", "nok"])', "raqamla([])", 'raqamla(["x"])', lv=1),
    F("Farqlar soni", "`hamming(a, b)` — teng uzunlikdagi ikki satrda nechta oʻrinda harflar farq qiladi?",
      "def hamming(a, b):\n    return sum(x != y for x, y in zip(a, b))", 'hamming("GAGCC", "CATCC")', 'hamming("", "")', 'hamming("abc", "abc")'),
    F("Qoʻshni farqlar", "`farqlar(a)` — har bir qoʻshni juftlik uchun `keyingi - oldingi`.",
      "def farqlar(a):\n    return [y - x for x, y in zip(a, a[1:])]", "farqlar([1, 4, 9, 16])", "farqlar([5])", "farqlar([3, 1])"),
    F("Qayerda", "`indekslar(a, x)` — x uchragan barcha indekslar.",
      "def indekslar(a, x):\n    return [i for i, y in enumerate(a) if y == x]", "indekslar([1, 2, 1, 3, 1], 1)", "indekslar([], 1)", 'indekslar(["a", "b"], "b")'),
    F("Aralashtirish", "`aralash(a, b)` — elementlarni navbatma-navbat birlashtiring: `[1,2], [\"a\",\"b\"] → [1,\"a\",2,\"b\"]` (teng uzunlik).",
      "def aralash(a, b):\n    natija = []\n    for x, y in zip(a, b):\n        natija += [x, y]\n    return natija", 'aralash([1, 2], ["a", "b"])', "aralash([], [])", "aralash([0], [9])"),
    F("Eng katta oʻsish", "`eng_osish(a)` — qoʻshni kunlar orasidagi eng katta oʻsish (oʻsish boʻlmasa 0).",
      "def eng_osish(a):\n    return max([y - x for x, y in zip(a, a[1:])] + [0])", "eng_osish([3, 8, 2, 9])", "eng_osish([5, 4, 3])", "eng_osish([7])"),
    L("lc", "shuffle-string"),
    L("exercism", "hamming"),
    L("lc", "merge-strings-alternately"),
    L("lc", "sort-the-people"),
])

# ---------------------------------------------------------------- 6.13
TOPIC("map-filter", "map, filter va sorted(key=)", "Funksiyani har bir elementga qoʻllash", 15, r'''
`map` va `filter` — roʻyxat ifodasining "funksional" egizaklari. Ular **iterator** qaytaradi, shuning uchun natijani koʻrish uchun `list()` ga oʻraymiz.

## map — har biriga funksiya
```py
matn = "4 8 15 16"
sonlar = list(map(int, matn.split()))
print(sonlar)

ismlar = ["ali", "vali"]
print(list(map(str.upper, ismlar)))
print(list(map(lambda x: x ** 2, [1, 2, 3])))
```

## filter — shartga moslarini qoldirish
```py
sonlar = [5, 12, 7, 20, 3]
print(list(filter(lambda x: x > 6, sonlar)))

sozlar = ["", "olma", "", "nok"]
print(list(filter(None, sozlar)))   # boʻsh satrlarni olib tashlaydi
```

## Comprehension bilan solishtirish
| map / filter | Comprehension |
|---|---|
| `list(map(f, a))` | `[f(x) for x in a]` |
| `list(filter(f, a))` | `[x for x in a if f(x)]` |

> Ikkalasi ham toʻgʻri. Tayyor funksiya boʻlsa (`int`, `str.upper`) — `map` qisqaroq. Murakkab ifoda boʻlsa — comprehension oʻqishga osonroq.

## sorted, min, max — key bilan
`key` — har bir elementdan **solishtirish kalitini** yasaydigan funksiya:

```py
talabalar = [("Ali", 85), ("Vali", 92), ("Madina", 78)]
print(sorted(talabalar, key=lambda t: t[1]))
print(max(talabalar, key=lambda t: t[1])[0])

sozlar = ["banan", "Olma", "anor"]
print(sorted(sozlar))
print(sorted(sozlar, key=str.lower))

# avval uzunlik, keyin alifbo
print(sorted(["bb", "a", "ab", "c"], key=lambda s: (len(s), s)))
```

## map — bir nechta roʻyxat bilan
```py
a = [1, 2, 3]
b = [10, 20, 30]
print(list(map(lambda x, y: x + y, a, b)))
```

!> `map` obyekti bir martalik: bir marta aylanib chiqilgandan keyin boʻsh boʻladi.

```py
m = map(int, ["1", "2"])
print(list(m))
print(list(m))
```

## Esda tuting
- `list(map(int, input().split()))` — sonlarni oʻqish.
- `key=lambda ...` — saralash qoidasini bering; kortej qaytarsa — bir necha mezon.
''', [
    P('print(list(map(int, ["3", "07"])))', "['3', '07']", "[3, 07]", "[37]"),
    P('print(list(filter(lambda x: x % 2, [1, 2, 3, 4])))', "[2, 4]", "[True, False, True, False]", "[1, 0, 1, 0]"),
    P('print(sorted(["bb", "a", "ccc"], key=len, reverse=True))', "['a', 'bb', 'ccc']", "['bb', 'a', 'ccc']", "[3, 2, 1]"),
    P('print(max(["olma", "ab", "kivi"], key=len))', "kivi", "ab", "4"),
    P('m = map(str, [1, 2])\nprint(list(m), list(m))', "['1', '2'] ['1', '2']", "[1, 2] []", "Xato", lv=2),
    P('print(list(filter(None, [0, 1, "", "a", None])))', "[0, 1, '', 'a', None]", "[0, '', None]", "[1]"),
    P('print(sorted([3, -5, 1], key=abs))', "[-5, 1, 3]", "[1, 3, 5]", "[3, 1, -5]"),
    Q("`list(map(f, a))` qaysi ifodaga teng?", "[f(x) for x in a]", "[x for x in a if f(x)]", "f(a)", "[f for x in a]"),
    Q("`sorted(a, key=lambda s: (len(s), s))` qanday saralaydi?", "Avval uzunlik, teng boʻlsa alifbo boʻyicha", "Faqat alifbo boʻyicha", "Faqat uzunlik boʻyicha kamayish", "Tasodifiy"),
    F("Satrdan sonlar", "`sonlar(matn)` — boʻsh joy bilan ajratilgan sonlarni `int` roʻyxatiga aylantiring (`map` bilan).",
      "def sonlar(matn):\n    return list(map(int, matn.split()))", 'sonlar("1 2 3")', 'sonlar("")', 'sonlar("  -5   10 ")', lv=1),
    F("Uzun soʻzlar", "`uzunlar(sozlar, n)` — uzunligi n dan katta soʻzlar (`filter` bilan).",
      "def uzunlar(sozlar, n):\n    return list(filter(lambda s: len(s) > n, sozlar))", 'uzunlar(["a", "olma", "nok"], 3)', "uzunlar([], 1)", 'uzunlar(["ab", "cd"], 0)', lv=1),
    F("Ball boʻyicha", "`reyting(t)` — `(ism, ball)` larni ball boʻyicha **kamayish** tartibida saralang; ball teng boʻlsa — ism boʻyicha alifbo.",
      "def reyting(t):\n    return sorted(t, key=lambda p: (-p[1], p[0]))", 'reyting([("Vali", 90), ("Ali", 90), ("Bek", 95)])', "reyting([])", 'reyting([("A", 1)])', lv=3),
    F("Yaqin son", "`eng_yaqin(a, x)` — a dagi x ga eng yaqin son (teng boʻlsa — kichigi).",
      "def eng_yaqin(a, x):\n    return min(a, key=lambda y: (abs(y - x), y))", "eng_yaqin([1, 5, 9], 6)", "eng_yaqin([1, 3], 2)", "eng_yaqin([10], -100)"),
    F("Juft indekslar", "`yigindi_juftlar(a, b)` — ikki roʻyxat elementlari yigʻindisi (`map` bilan, ikki argument).",
      "def yigindi_juftlar(a, b):\n    return list(map(lambda x, y: x + y, a, b))", "yigindi_juftlar([1, 2], [10, 20])", "yigindi_juftlar([], [])", "yigindi_juftlar([5], [-5])"),
    F("Raqamlar yigʻindisi boʻyicha", "`raqam_boyicha(a)` — sonlarni raqamlari yigʻindisi boʻyicha saralang (teng boʻlsa — son kattaligi boʻyicha).",
      "def raqam_boyicha(a):\n    return sorted(a, key=lambda n: (sum(map(int, str(n))), n))", "raqam_boyicha([19, 5, 30, 111])", "raqam_boyicha([])", "raqam_boyicha([21, 12, 3])", lv=3),
    F("Bosh harflar", "`bosh_harflar(matn)` — har soʻzning birinchi harfini katta qilib birlashtiring: `\"mirae academy\" → \"MA\"`.",
      "def bosh_harflar(matn):\n    return ''.join(map(lambda s: s[0].upper(), matn.split()))", 'bosh_harflar("mirae academy")', 'bosh_harflar("")', 'bosh_harflar("o zbekiston respublikasi")'),
    L("lc", "sort-array-by-parity"),
    L("lc", "how-many-numbers-are-smaller-than-the-current-number"),
    L("exercism", "acronym"),
    L("lc", "largest-number", note="Qiyinroq: `functools.cmp_to_key` haqida oʻqing."),
])

# ---------------------------------------------------------------- 6.14
TOPIC("ochish", "Ochish (unpacking) va * operatori", "a, b = ..., *qolgan, ** lugʻatlar", 15, r'''
**Ochish** — toʻplamdagi qiymatlarni bir nechta oʻzgaruvchiga bir qatorda tarqatish.

## Oddiy ochish
```py
x, y = 3, 4
ism, yosh = ["Aziz", 17]
a, b, c = "xyz"
print(x, y, ism, yosh, a, b, c)
```

!> Chap va oʻngdagi elementlar soni teng boʻlishi kerak, aks holda `ValueError`.

## Almashtirish — Python usuli
```py
a, b = 1, 2
a, b = b, a
print(a, b)
```

## * — "qolganlari"
```py
birinchi, *qolgan = [10, 20, 30, 40]
print(birinchi, qolgan)

*boshi, oxirgi = [10, 20, 30, 40]
print(boshi, oxirgi)

bosh, *orta, oxir = "salom"
print(bosh, orta, oxir)
```

## Sikl ichida ochish
```py
juftlar = [("Ali", 85), ("Vali", 92)]
for ism, ball in juftlar:
    print(ism, ball)

nuqtalar = [(1, (2, 3)), (4, (5, 6))]
for n, (x, y) in nuqtalar:
    print(n, x + y)
```

## * — funksiya chaqiruvida yoyish
```py
sonlar = [3, 1, 4]
print(*sonlar)
print(*sonlar, sep=", ")
print(max(*sonlar))

def hajm(a, b, c):
    return a * b * c

olcham = (2, 3, 4)
print(hajm(*olcham))
```

## * va ** bilan birlashtirish
```py
a = [1, 2]
b = [3, 4]
print([*a, 0, *b])

asosiy = {"tema": "qorongʻi", "til": "uz"}
yangi = {**asosiy, "til": "en"}
print(yangi)
```

> `print(*a)` — roʻyxatni qavssiz, boʻsh joy bilan chiqarishning eng qisqa usuli. Olimpiadalarda juda koʻp ishlatiladi.

## `_` — keraksiz qiymat
```py
_, ikkinchi, _ = (1, 2, 3)
print(ikkinchi)
```

## Esda tuting
- `a, *b = ...` — b doim roʻyxat (boʻsh boʻlishi ham mumkin).
- Chaqiruvda `*a` roʻyxatni, `**d` lugʻatni yoyadi.
''', [
    P('a, b, c = [1, 2, 3]\nprint(b)', "1", "[2]", "3"),
    P('a, *b = [1, 2, 3]\nprint(b)', "2", "(2, 3)", "[1, 2, 3]"),
    P('*a, b = "abc"\nprint(a, b)', "abc c", "['a', 'b', 'c'] c", "ab c"),
    P('a, *b = [5]\nprint(a, b)', "5 None", "Xato", "5 [5]", lv=2),
    P('print(*[1, 2, 3], sep="-")', "[1, 2, 3]", "1 2 3", "-1-2-3-"),
    P('a, b = 1, 2\na, b = b, a + b\nprint(a, b)', "2 4", "1 3", "2 2"),
    P('d = {"a": 1}\nprint({**d, "b": 2, "a": 9})', "{'a': 1, 'b': 2}", "{'a': 1, 'b': 2, 'a': 9}", "Xato"),
    Q("`x, y = [1, 2, 3]` nima beradi?", "ValueError xatosi", "x=1, y=[2, 3]", "x=1, y=2", "x=[1, 2], y=3"),
    Q("`print(*a)` nima qiladi?", "Roʻyxat elementlarini qavssiz, boʻsh joy bilan chiqaradi", "Elementlarni koʻpaytirib chiqaradi", "Roʻyxatni koʻrsatkich sifatida chiqaradi", "Xato beradi"),
    F("Bosh va qolgan", "`bosh_qolgan(a)` — `(birinchi, qolganlar_roʻyxati)` kortejini qaytaring (`*` bilan).",
      "def bosh_qolgan(a):\n    bosh, *qolgan = a\n    return (bosh, qolgan)", "bosh_qolgan([1, 2, 3])", "bosh_qolgan([7])", 'bosh_qolgan("abc")', lv=1),
    F("Oʻrtasi", "`ortasi(a)` — birinchi va oxirgisiz qolgan elementlar (uzunlik ≥ 2).",
      "def ortasi(a):\n    _, *o, _ = a\n    return o", "ortasi([1, 2, 3, 4])", "ortasi([1, 2])", 'ortasi("salom")', lv=1),
    F("Hajm", "`hajm(olcham)` — `(a, b, c)` kortejidan quti hajmini toping.",
      "def hajm(olcham):\n    a, b, c = olcham\n    return a * b * c", "hajm((2, 3, 4))", "hajm((1, 1, 1))", "hajm((0, 5, 5))"),
    F("Fibonachchi", "`fib(n)` — n-chi Fibonachchi soni (`fib(0)=0, fib(1)=1`), `a, b = b, a + b` usuli bilan.",
      "def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a", "fib(0)", "fib(1)", "fib(10)", "fib(50)"),
    F("Birlashtir", "`birlashtir(a, b)` — `[*a, *b]` dan takrorsiz va saralangan roʻyxat.",
      "def birlashtir(a, b):\n    return sorted(set([*a, *b]))", "birlashtir([3, 1], [1, 2])", "birlashtir([], [])", "birlashtir([5], [5])"),
    F("Sozlamalar", "`sozlama(asosiy, yangi)` — ikki lugʻatni birlashtiring; ziddiyatda `yangi` ustun.",
      "def sozlama(asosiy, yangi):\n    return {**asosiy, **yangi}", 'sozlama({"til": "uz", "tema": "dark"}, {"til": "en"})', "sozlama({}, {})", 'sozlama({"a": 1}, {"b": 2})'),
    F("Ichma-ich ochish", "`yigindilar(t)` — `[(nom, (x, y)), ...]` dan `{nom: x + y}` lugʻatini yasang.",
      "def yigindilar(t):\n    return {nom: x + y for nom, (x, y) in t}", 'yigindilar([("a", (1, 2)), ("b", (3, 4))])', "yigindilar([])", 'yigindilar([("z", (0, -1))])', lv=3),
    L("exercism", "locomotive-engineer", note="Ochish va `*` boʻyicha maxsus mashq."),
    L("lc", "fibonacci-number"),
    L("exercism", "flatten-array"),
    L("lc", "plus-one"),
])
