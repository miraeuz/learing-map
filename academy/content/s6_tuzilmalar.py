from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(6, "Maʼlumotlar tuzilmalari", "Roʻyxat, kortej, toʻplam, lugʻat, stek va navbat", "🗂️")

# ---------------------------------------------------------------- 6.1
TOPIC("royxat", "Roʻyxat (list)", "Yaratish, indeks, kesish va oʻzgartirish", 20, r'''
**Roʻyxat** (`list`) — bir nechta qiymatni tartib bilan saqlaydigan konteyner. Sinfdagi oʻquvchilar, doʻkondagi narxlar, oʻyin ballari — hammasi roʻyxat.

```py
baholar = [5, 4, 5, 3]
ismlar = ["Ali", "Vali", "Madina"]
aralash = [1, "olma", 3.5, True]
bosh = []

print(baholar)
print(len(ismlar))
print(bosh)
```

## Indeks — elementning tartib raqami
Sanoq **0 dan** boshlanadi. Manfiy indeks oxiridan sanaydi: `-1` — oxirgi element.

```py
mevalar = ["olma", "nok", "uzum", "anor"]
print(mevalar[0])
print(mevalar[2])
print(mevalar[-1])
print(mevalar[-2])
```

| Indeks | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Element | olma | nok | uzum | anor |
| Manfiy | -4 | -3 | -2 | -1 |

!> Mavjud boʻlmagan indeks — `IndexError`. 4 elementli roʻyxatda `mevalar[4]` xato beradi.

## Kesish (slicing)
Satrlardagi kabi: `[boshi:oxiri:qadam]`, oxiri kirmaydi.

```py
sonlar = [10, 20, 30, 40, 50, 60]
print(sonlar[1:4])
print(sonlar[:3])
print(sonlar[3:])
print(sonlar[::2])
print(sonlar[::-1])
```

## Roʻyxat oʻzgaruvchan (mutable)
Satrdan farqli, roʻyxat elementini joyida almashtirish mumkin:

```py
narxlar = [12000, 8000, 15000]
narxlar[1] = 9000
print(narxlar)
```

## Amallar: + * in len
```py
a = [1, 2]
b = [3, 4]
print(a + b)
print(a * 3)
print(3 in b)
print(len(a + b))
```

## Diqqat: nusxa emas, havola!
`b = a` yangi roʻyxat yaratmaydi — ikkala nom **bitta** roʻyxatga ishora qiladi:

```py
a = [1, 2, 3]
b = a
b[0] = 99
print(a)

c = a.copy()      # yoki a[:]
c[0] = 0
print(a, c)
```

> Mustaqil nusxa kerak boʻlsa — `a.copy()`, `list(a)` yoki `a[:]`.

## Esda tuting
- Indeks 0 dan, `-1` — oxirgi.
- Kesish yangi roʻyxat qaytaradi.
- `b = a` — nusxa emas; `a.copy()` — nusxa.
''', [
    P('a = [10, 20, 30]\nprint(a[1])', "10", "30", "[20]"),
    P('a = [1, 2, 3, 4]\nprint(a[-1])', "1", "-1", "Xato"),
    P('a = [5, 6, 7]\na[0] = 9\nprint(a)', "[5, 6, 7]", "[9, 5, 6, 7]", "Xato"),
    P('a = [1, 2] + [3]\nprint(a, len(a))', "[1, 2, [3]] 3", "[1, 2, 3] 2", "[3, 1, 2] 3"),
    P('a = [0] * 3\nprint(a)', "[0]", "0", "[3]"),
    P('a = [1, 2, 3, 4, 5]\nprint(a[1:4])', "[1, 2, 3, 4]", "[2, 3, 4, 5]", "[1, 2, 3]"),
    P('a = [3, 1, 2]\nb = a\nb.append(4)\nprint(a)', "[3, 1, 2]", "[4]", "[1, 2, 3, 4]", lv=2,
      why="`b = a` nusxa emas — ikkala nom bitta roʻyxatni koʻrsatadi."),
    Q("5 elementli roʻyxatning oxirgi elementi indeksi qaysi?", "4 (yoki -1)", "5", "0", "-5"),
    Q("Roʻyxatning mustaqil nusxasini qanday olamiz?", "a.copy()", "b = a", "a.clone()", "copy a"),
    F("Birinchi va oxirgi", "`chet(a)` — roʻyxatning birinchi va oxirgi elementidan iborat `[birinchi, oxirgi]` roʻyxatni qaytaring.",
      "def chet(a):\n    return [a[0], a[-1]]", "chet([1, 2, 3])", "chet([7])", 'chet(["a", "b"])', "chet([4, 0, 0, 9])", lv=1),
    F("Teskari", "`teskari(a)` — roʻyxatni teskari tartibda qaytaring.",
      "def teskari(a):\n    return a[::-1]", "teskari([1, 2, 3])", "teskari([])", 'teskari(["x", "y"])', lv=1),
    F("Yigʻindi (sum siz)", "`jami(a)` — elementlar yigʻindisini sikl bilan hisoblang (`sum` ishlatmang).",
      "def jami(a):\n    s = 0\n    for x in a:\n        s += x\n    return s", "jami([1, 2, 3])", "jami([])", "jami([-5, 5, 10])", "jami([100])", lv=1),
    F("Ikki barobar", "`ikki_barobar(a)` — har bir element 2 ga koʻpaytirilgan **yangi** roʻyxat qaytaring.",
      "def ikki_barobar(a):\n    natija = []\n    for x in a:\n        natija.append(x * 2)\n    return natija", "ikki_barobar([1, 2, 3])", "ikki_barobar([])", "ikki_barobar([-4, 0])"),
    F("Juftlar soni", "`juft_soni(a)` — roʻyxatdagi juft sonlar nechta?",
      "def juft_soni(a):\n    k = 0\n    for x in a:\n        if x % 2 == 0:\n            k += 1\n    return k", "juft_soni([1, 2, 3, 4])", "juft_soni([1, 3])", "juft_soni([0, -2, 8])", "juft_soni([])"),
    F("Eng kattasi qayerda", "`maks_indeks(a)` — eng katta element **indeksini** qaytaring (bir nechta boʻlsa — birinchisi).",
      "def maks_indeks(a):\n    eng = 0\n    for i in range(1, len(a)):\n        if a[i] > a[eng]:\n            eng = i\n    return eng", "maks_indeks([3, 9, 2])", "maks_indeks([5])", "maks_indeks([1, 7, 7, 0])", "maks_indeks([-3, -1, -2])"),
    F("Chetlarni almashtir", "`almashtir(a)` — birinchi va oxirgi elementlar oʻrnini almashtirib, roʻyxatni qaytaring.",
      "def almashtir(a):\n    a = a[:]\n    a[0], a[-1] = a[-1], a[0]\n    return a", "almashtir([1, 2, 3])", "almashtir([5])", 'almashtir(["a", "b"])', "almashtir([9, 0, 0, 1])"),
    L("lc", "concatenation-of-array", note="`nums + nums` — bir qatorli yechim!"),
    L("lc", "build-array-from-permutation"),
    L("exercism", "card-games"),
    L("cses", 1083, note="Yetishmayotgan son: 1..n yigʻindisidan roʻyxat yigʻindisini ayiring."),
])

# ---------------------------------------------------------------- 6.2
TOPIC("royxat-metodlari", "Roʻyxat metodlari", "append, insert, remove, pop, sort va boshqalar", 20, r'''
Roʻyxat bilan ishlashning 90% i shu metodlar orqali boʻladi. Ularning koʻpchiligi roʻyxatni **joyida** oʻzgartiradi.

## Qoʻshish
```py
xarid = ["non", "sut"]
xarid.append("tuxum")          # oxiriga bitta
xarid.insert(0, "choy")        # 0-oʻringa
xarid.extend(["guruch", "yogʻ"])  # bir nechtasini
print(xarid)
```

## Oʻchirish
```py
a = [10, 20, 30, 20, 40]
a.remove(20)       # birinchi 20 ni oʻchiradi
print(a)
oxirgi = a.pop()   # oxirgisini olib tashlaydi va qaytaradi
print(oxirgi, a)
birinchi = a.pop(0)
print(birinchi, a)
```

!> `remove(x)` — x boʻlmasa `ValueError`. `pop()` boʻsh roʻyxatda — `IndexError`.

## Qidirish va sanash
```py
ballar = [7, 9, 7, 10, 7]
print(ballar.count(7))
print(ballar.index(10))
print(10 in ballar)
```

## Saralash: sort() va sorted()
```py
a = [5, 2, 9, 1]
b = sorted(a)          # YANGI roʻyxat, a oʻzgarmaydi
print(a, b)

a.sort()               # a ning oʻzi saralanadi, None qaytaradi
print(a)

a.sort(reverse=True)
print(a)

ismlar = ["Zafar", "ali", "Bek"]
print(sorted(ismlar, key=str.lower))
print(sorted(ismlar, key=len))
```

> `key=` — nimaga qarab saralashni koʻrsatadi: `len`, `str.lower`, yoki oʻzingizning funksiyangiz.

## Boshqa foydali metodlar
| Metod | Nima qiladi |
|---|---|
| `a.reverse()` | joyida teskari aylantiradi |
| `a.clear()` | hammasini oʻchiradi |
| `a.copy()` | nusxa qaytaradi |
| `min(a)`, `max(a)`, `sum(a)` | eng kichik, eng katta, yigʻindi |

## Amaliy misol: top-3 natija
```py
natijalar = [72, 95, 88, 61, 99, 85]
top = sorted(natijalar, reverse=True)[:3]
print("Top-3:", top)
```

## Esda tuting
- `append` — bitta element, `extend` — har bir elementni alohida qoʻshadi.
- `sort()` joyida va `None` qaytaradi; `sorted()` yangi roʻyxat beradi.
''', [
    P('a = [1, 2]\na.append([3, 4])\nprint(len(a))', "4", "2", "Xato"),
    P('a = [1, 2]\na.extend([3, 4])\nprint(a)', "[1, 2, [3, 4]]", "[3, 4, 1, 2]", "4"),
    P('a = [5, 3, 8]\nprint(a.pop(), a)', "5 [3, 8]", "8 [5, 3, 8]", "[5, 3] 8"),
    P('a = [3, 1, 2]\nb = a.sort()\nprint(b)', "[1, 2, 3]", "[3, 1, 2]", "Xato", lv=2,
      why="`sort()` roʻyxatni joyida saralaydi va `None` qaytaradi."),
    P('a = [3, 1, 2]\nprint(sorted(a), a)', "[1, 2, 3] [1, 2, 3]", "[3, 1, 2] [1, 2, 3]", "None [3, 1, 2]"),
    P('a = [1, 2, 1, 3, 1]\na.remove(1)\nprint(a)', "[2, 3]", "[1, 2, 1, 3]", "[2, 3, 1]"),
    P('a = ["b", "a", "c"]\na.insert(1, "x")\nprint(a)', "['x', 'b', 'a', 'c']", "['b', 'a', 'x', 'c']", "['b', 'x', 'c']"),
    Q("`append` va `extend` farqi nimada?", "append bitta element qoʻshadi, extend har bir elementni alohida qoʻshadi", "Farqi yoʻq", "extend boshiga qoʻshadi", "append roʻyxatni saralaydi"),
    Q("Asl roʻyxatni oʻzgartirmasdan saralangan nusxa olish uchun nima ishlatiladi?", "sorted(a)", "a.sort()", "a.order()", "sort(a)"),
    F("Takrorsiz qoʻshish", "`qosh(a, x)` — agar x roʻyxatda boʻlmasa, oxiriga qoʻshing. Roʻyxatni qaytaring.",
      "def qosh(a, x):\n    if x not in a:\n        a.append(x)\n    return a", "qosh([1, 2], 3)", "qosh([1, 2], 2)", "qosh([], 5)", lv=1),
    F("Hammasini oʻchir", "`tozala(a, x)` — roʻyxatdan **barcha** x larni olib tashlang va natijani qaytaring.",
      "def tozala(a, x):\n    return [y for y in a if y != x]", "tozala([1, 2, 1, 3], 1)", "tozala([5, 5], 5)", "tozala([1, 2], 9)"),
    F("Kamayish tartibida", "`kamayish(a)` — roʻyxatni kattadan kichikka saralab qaytaring.",
      "def kamayish(a):\n    return sorted(a, reverse=True)", "kamayish([3, 1, 2])", "kamayish([])", "kamayish([5, 5, 1, 9])", lv=1),
    F("Ikkinchi katta", "`ikkinchi(a)` — **har xil** qiymatlar ichida ikkinchi eng kattasini qaytaring (kamida 2 xil qiymat bor).",
      "def ikkinchi(a):\n    return sorted(set(a))[-2]", "ikkinchi([4, 9, 2])", "ikkinchi([5, 5, 3])", "ikkinchi([1, 2, 2, 2])", "ikkinchi([-1, -5, -3])", lv=3),
    F("Birinchi k ta", "`birinchi_k(a, k)` — saralangan roʻyxatning dastlabki k ta elementi.",
      "def birinchi_k(a, k):\n    return sorted(a)[:k]", "birinchi_k([5, 1, 4, 2], 2)", "birinchi_k([3], 5)", "birinchi_k([9, 8, 7], 0)"),
    F("Mediana", "`mediana(a)` — saralangandagi oʻrta element. Uzunlik juft boʻlsa — oʻrtadagi ikkitasining oʻrtachasi.",
      "def mediana(a):\n    b = sorted(a)\n    n = len(b)\n    if n % 2 == 1:\n        return b[n // 2]\n    return (b[n // 2 - 1] + b[n // 2]) / 2", "mediana([3, 1, 2])", "mediana([4, 1, 3, 2])", "mediana([7])", "mediana([10, 20])", lv=3),
    F("Uzunlik boʻyicha", "`uzunlik_boyicha(sozlar)` — soʻzlarni uzunligi boʻyicha (qisqadan uzunga) saralang.",
      "def uzunlik_boyicha(sozlar):\n    return sorted(sozlar, key=len)", 'uzunlik_boyicha(["olma", "uy", "kitob"])', 'uzunlik_boyicha([])', 'uzunlik_boyicha(["abc", "a", "ab"])'),
    L("lc", "remove-element"),
    L("lc", "merge-sorted-array"),
    L("lc", "third-maximum-number", note="`sorted(set(nums))` dan foydalaning."),
    L("exercism", "chaitanas-colossal-coaster", note="Roʻyxat metodlari boʻyicha toʻliq mashq."),
])

# ---------------------------------------------------------------- 6.3
TOPIC("royxat-ifodasi", "Roʻyxat ifodasi (comprehension)", "Bir qatorda yangi roʻyxat yasash", 20, r'''
Koʻpincha bir roʻyxatdan boshqasini yasaymiz: kvadratlar, filtrlash, oʻzgartirish. Python buni **bir qatorda** qilish imkonini beradi.

## Oddiy sikl bilan
```py
kvadratlar = []
for x in range(1, 6):
    kvadratlar.append(x * x)
print(kvadratlar)
```

## Comprehension bilan
```py
kvadratlar = [x * x for x in range(1, 6)]
print(kvadratlar)
```

Tuzilishi: `[IFODA for ELEMENT in TOʻPLAM]`

## Shart bilan filtrlash
```py
sonlar = [12, 7, 30, 5, 18, 3]
kattalar = [x for x in sonlar if x > 10]
juftlar = [x for x in sonlar if x % 2 == 0]
print(kattalar)
print(juftlar)
```

## if-else bilan oʻzgartirish
Shart **oldinga** yoziladi:

```py
ballar = [45, 80, 60, 92]
natija = ["oʻtdi" if b >= 60 else "yiqildi" for b in ballar]
print(natija)
```

## Satrlar bilan
```py
ismlar = ["ali", "madina", "bek"]
print([i.capitalize() for i in ismlar])
print([len(i) for i in ismlar])

matn = "3 14 15 92"
sonlar = [int(s) for s in matn.split()]
print(sonlar, sum(sonlar))
```

> `[int(s) for s in input().split()]` — olimpiada masalalarida kirishni oʻqishning eng mashhur usuli. `list(map(int, input().split()))` ham xuddi shunday.

## sum, min, max, any, all
```py
a = [4, 8, 15, 16, 23, 42]
print(sum(a), min(a), max(a))
print(any(x > 40 for x in a))   # birortasi?
print(all(x > 0 for x in a))    # hammasi?
```

!> Bunday ifodani juda uzun qilmang. Agar u ikki qatorga sigʻmasa — oddiy `for` yaxshiroq oʻqiladi.

## Esda tuting
- `[f(x) for x in a]` — oʻzgartirish.
- `[x for x in a if shart]` — filtrlash.
- `[A if shart else B for x in a]` — tanlash.
''', [
    P('print([x * x for x in range(4)])', "[1, 4, 9, 16]", "[0, 1, 2, 3]", "0 1 4 9"),
    P('print([x for x in [5, 2, 8, 1] if x > 3])', "[2, 1]", "[5, 2, 8]", "2"),
    P('a = [1, 2, 3]\ns = 0\nfor x in a:\n    s += x\nprint(s)', "3", "[1, 2, 3]", "123"),
    P('a = [2, 4, 6]\nprint(sum(a) // len(a))', "4.0", "12", "3"),
    P('print(any([0, 0, 3]), all([1, 0, 1]))', "False True", "True True", "3 0"),
    P('print(["ha" if x % 2 else "yoq" for x in [1, 2]])', "['yoq', 'ha']", "['ha', 'ha']", "ha yoq"),
    P('a = [1, 2, 3]\nfor x in a:\n    x = x * 10\nprint(a)', "[10, 20, 30]", "30", "Xato", lv=2,
      why="`x` — elementning nusxasi; unga yangi qiymat berish roʻyxatni oʻzgartirmaydi."),
    Q("`[x for x in a if x > 0]` nima qiladi?", "Faqat musbat elementlardan yangi roʻyxat yasaydi", "Manfiylarni 0 ga almashtiradi", "a ni joyida oʻzgartiradi", "True/False roʻyxatini qaytaradi"),
    Q("`max([])` nima beradi?", "ValueError xatosi", "0", "None", "[]"),
    F("Kvadratlar", "`kvadratlar(n)` — `[1, 4, 9, ..., n²]` roʻyxatini qaytaring.",
      "def kvadratlar(n):\n    return [i * i for i in range(1, n + 1)]", "kvadratlar(4)", "kvadratlar(1)", "kvadratlar(0)", lv=1),
    F("Musbatlar", "`musbatlar(a)` — faqat musbat (0 dan katta) elementlar.",
      "def musbatlar(a):\n    return [x for x in a if x > 0]", "musbatlar([3, -1, 0, 5])", "musbatlar([-2, -3])", "musbatlar([])", lv=1),
    F("Uzunliklar", "`uzunliklar(sozlar)` — har bir soʻz uzunligidan iborat roʻyxat.",
      "def uzunliklar(sozlar):\n    return [len(s) for s in sozlar]", 'uzunliklar(["salom", "dunyo", "!"])', "uzunliklar([])", 'uzunliklar([""])', lv=1),
    F("Juftlar yigʻindisi", "`juft_yigindi(a)` — juft elementlar yigʻindisi.",
      "def juft_yigindi(a):\n    return sum(x for x in a if x % 2 == 0)", "juft_yigindi([1, 2, 3, 4])", "juft_yigindi([1, 3])", "juft_yigindi([-2, 10])"),
    F("Raqamli satrlar", "`raqamlar(a)` — satrlar roʻyxatidan faqat raqamdan iboratlarini **son**ga aylantirib qaytaring.",
      "def raqamlar(a):\n    return [int(s) for s in a if s.isdigit()]", 'raqamlar(["12", "ab", "7", "3x"])', 'raqamlar([])', 'raqamlar(["007", "x"])'),
    F("Jamgʻarma", "`jamgarma(a)` — har bir oʻrinda shu joygacha boʻlgan yigʻindi: `[1,2,3] → [1,3,6]`.",
      "def jamgarma(a):\n    s = 0\n    natija = []\n    for x in a:\n        s += x\n        natija.append(s)\n    return natija", "jamgarma([1, 2, 3])", "jamgarma([])", "jamgarma([5, -5, 5])"),
    F("Baholash", "`baholar(ballar)` — har bir ball uchun 60 va undan yuqori boʻlsa `\"oʻtdi\"`, aks holda `\"yiqildi\"`.",
      'def baholar(ballar):\n    return ["oʻtdi" if b >= 60 else "yiqildi" for b in ballar]', "baholar([45, 60, 99])", "baholar([])", "baholar([59])"),
    L("lc", "squares-of-a-sorted-array"),
    L("lc", "count-items-matching-a-rule"),
    L("lc", "find-all-numbers-disappeared-in-an-array"),
    L("exercism", "making-the-grade", note="Sikl va roʻyxatlar boʻyicha mashq."),
])

# ---------------------------------------------------------------- 6.4
TOPIC("matritsa", "Ikki oʻlchovli roʻyxat (matritsa)", "Jadval, qator va ustunlar", 25, r'''
Roʻyxat ichida roʻyxat — bu **jadval** (matritsa). Shaxmat taxtasi, Excel jadvali, oʻyin xaritasi — hammasi shunday saqlanadi.

```py
jadval = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(jadval[0])       # 0-qator
print(jadval[1][2])    # 1-qator, 2-ustun
print(len(jadval), len(jadval[0]))
```

> `m[i][j]` — **i**-qator, **j**-ustun. Avval qator, keyin ustun.

## Aylanib chiqish
```py
m = [[1, 2, 3], [4, 5, 6]]
for qator in m:
    for x in qator:
        print(x, end=" ")
    print()
```

Indekslar bilan:

```py
m = [[1, 2, 3], [4, 5, 6]]
for i in range(len(m)):
    for j in range(len(m[i])):
        print(f"m[{i}][{j}]={m[i][j]}", end="  ")
    print()
```

## Toʻgʻri yaratish
```py
n, k = 3, 4
m = [[0] * k for _ in range(n)]
m[0][0] = 7
print(m)
```

!> `[[0] * k] * n` ishlatmang! U **bitta** qatorni n marta takrorlaydi — bittasini oʻzgartirsangiz, hammasi oʻzgaradi.

```py
yomon = [[0] * 3] * 2
yomon[0][0] = 5
print(yomon)
```

## Qator va ustun yigʻindilari
```py
m = [[1, 2, 3], [4, 5, 6]]
print([sum(q) for q in m])
print([sum(q[j] for q in m) for j in range(3)])
```

## Kirishdan matritsa oʻqish
```py input=2 3|1 2 3|4 5 6
n, k = map(int, input().split())
m = [list(map(int, input().split())) for _ in range(n)]
print(m)
```

## Transpozitsiya (qator ↔ ustun)
```py
m = [[1, 2, 3], [4, 5, 6]]
t = [list(q) for q in zip(*m)]
print(t)
```

## Esda tuting
- `m[i][j]` — qator, ustun.
- Yaratish: `[[0] * k for _ in range(n)]`.
''', [
    P('m = [[1, 2], [3, 4]]\nprint(m[1][0])', "2", "1", "4"),
    P('m = [[1, 2, 3], [4, 5, 6]]\nprint(len(m), len(m[0]))', "3 2", "6", "2 2"),
    P('m = [[1, 2, 3], [4, 5, 6]]\nprint([r[1] for r in m])', "[4, 5, 6]", "[1, 2, 3]", "[2, 4]"),
    P('m = [[0] * 2 for _ in range(2)]\nm[0][0] = 5\nprint(m)', "[[5, 0], [5, 0]]", "[[5, 5], [0, 0]]", "Xato"),
    P('m = [[0] * 2] * 2\nm[0][0] = 5\nprint(m)', "[[5, 0], [0, 0]]", "[[5, 5], [5, 5]]", "Xato", lv=3,
      why="`* 2` bitta ichki roʻyxatni ikki marta takrorlaydi — ikkala qator aslida bitta obyekt."),
    P('m = [[1, 2], [3, 4]]\nprint(sum(sum(r) for r in m))', "[3, 7]", "[4, 6]", "Xato"),
    P('m = [[1, 2], [3, 4]]\nfor r in m:\n    print(*r)', "[1, 2]\n[3, 4]", "1 2 3 4", "1\n2\n3\n4"),
    Q("`m[i][j]` da i va j nimani bildiradi?", "i — qator, j — ustun", "i — ustun, j — qator", "i — qiymat, j — indeks", "Ikkalasi ham qator"),
    Q("3×4 nol matritsani qaysi usul toʻgʻri yaratadi?", "[[0] * 4 for _ in range(3)]", "[[0] * 4] * 3", "[0] * 12", "[[0, 4], [0, 3]]"),
    F("Matritsa yigʻindisi", "`jami(m)` — matritsadagi barcha sonlar yigʻindisi.",
      "def jami(m):\n    return sum(sum(q) for q in m)", "jami([[1, 2], [3, 4]])", "jami([[5]])", "jami([[1, -1, 0], [2, 2, 2]])", lv=1),
    F("Qator yigʻindilari", "`qatorlar(m)` — har bir qator yigʻindisidan iborat roʻyxat.",
      "def qatorlar(m):\n    return [sum(q) for q in m]", "qatorlar([[1, 2], [3, 4]])", "qatorlar([[10]])", "qatorlar([[1, 1, 1], [0, 0, 0]])"),
    F("Ustun yigʻindilari", "`ustunlar(m)` — har bir ustun yigʻindisidan iborat roʻyxat.",
      "def ustunlar(m):\n    return [sum(q[j] for q in m) for j in range(len(m[0]))]", "ustunlar([[1, 2], [3, 4]])", "ustunlar([[1, 2, 3]])", "ustunlar([[5], [6], [7]])"),
    F("Transpozitsiya", "`transpoz(m)` — qatorlarni ustunga aylantiring.",
      "def transpoz(m):\n    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]", "transpoz([[1, 2, 3], [4, 5, 6]])", "transpoz([[1]])", "transpoz([[1], [2]])", lv=3),
    F("Diagonal", "`diagonal(m)` — kvadrat matritsaning bosh diagonali (`m[i][i]`) yigʻindisi.",
      "def diagonal(m):\n    return sum(m[i][i] for i in range(len(m)))", "diagonal([[1, 2], [3, 4]])", "diagonal([[7]])", "diagonal([[1, 0, 0], [0, 5, 0], [0, 0, 9]])"),
    F("Karra jadvali", "`karra(n)` — n×n jadval: `m[i][j] = (i+1)*(j+1)`.",
      "def karra(n):\n    return [[(i + 1) * (j + 1) for j in range(n)] for i in range(n)]", "karra(3)", "karra(1)", "karra(0)"),
    F("Eng katta element", "`eng_katta(m)` — matritsadagi eng katta son.",
      "def eng_katta(m):\n    return max(max(q) for q in m)", "eng_katta([[1, 9], [3, 4]])", "eng_katta([[-5, -2]])", "eng_katta([[0], [0], [1]])"),
    L("lc", "transpose-matrix"),
    L("lc", "matrix-diagonal-sum"),
    L("lc", "flipping-an-image"),
    L("exercism", "matrix", note="Matnni matritsaga aylantirish."),
])

# ---------------------------------------------------------------- 6.5
TOPIC("kortej", "Kortej (tuple)", "Oʻzgarmas roʻyxat va qachon ishlatish", 15, r'''
**Kortej** (`tuple`) — roʻyxatga oʻxshaydi, lekin **oʻzgarmas**. Yaratilgandan soʻng elementini almashtirib boʻlmaydi.

```py
nuqta = (3, 4)
rang = (255, 128, 0)
sana = (2026, 10, 13)

print(nuqta[0], nuqta[1])
print(len(rang))
print(sana[-1])
```

## Nega oʻzgarmas kerak?
- Maʼlumot tasodifan oʻzgarib ketmaydi (koordinata, sana, sozlama).
- Lugʻat kaliti yoki toʻplam elementi boʻla oladi (roʻyxat boʻla olmaydi).
- Biroz tezroq va kam xotira oladi.

```py xato
t = (1, 2, 3)
t[0] = 10
```

## Bitta elementli kortej
Vergul muhim! Qavs emas, **vergul** kortej yasaydi:

```py
a = (5)
b = (5,)
c = 5, 6
print(type(a).__name__, type(b).__name__, type(c).__name__)
```

## Ochish (unpacking)
```py
odam = ("Aziz", 17, "Toshkent")
ism, yosh, shahar = odam
print(ism, "—", yosh, "yosh,", shahar)
```

## Funksiyadan bir nechta qiymat
```py
def bolish(a, b):
    return a // b, a % b

butun, qoldiq = bolish(17, 5)
print(butun, qoldiq)
print(divmod(17, 5))
```

## Metodlar
Faqat ikkita: `count` va `index`.

```py
t = (1, 2, 2, 3, 2)
print(t.count(2), t.index(3))
print(sorted(t))       # roʻyxat qaytaradi
print(list(t), tuple([1, 2]))
```

| | Roʻyxat `[]` | Kortej `()` |
|---|---|---|
| Oʻzgartirish | ✅ | ❌ |
| Lugʻat kaliti | ❌ | ✅ |
| Qachon | oʻzgaradigan toʻplam | qayd etilgan yozuv |

## Esda tuting
- `(5,)` — kortej, `(5)` — oddiy son.
- Kortejni oʻzgartirib boʻlmaydi, lekin yangisini yasash mumkin: `t + (4,)`.
''', [
    P('t = (1, 2, 3)\nprint(t[0] + t[-1])', "3", "(1, 3)", "Xato"),
    P('t = (5)\nprint(type(t).__name__)', "tuple", "list", "Xato"),
    P('t = (5,)\nprint(len(t))', "5", "0", "Xato"),
    P('t = (1, 2)\nt[0] = 9\nprint(t)', "(9, 2)", "(1, 2)", "⚠ IndexError", lv=2),
    P('a, b = (10, 20)\na, b = b, a\nprint(a, b)', "10 20", "(20, 10)", "Xato"),
    P('t = (1, 2) + (3,)\nprint(t)', "(1, 2, (3,))", "(4, 2)", "Xato"),
    P('print(divmod(20, 6))', "(3.33, 2)", "3 2", "(2, 3)"),
    Q("Kortejning roʻyxatdan asosiy farqi?", "Uni oʻzgartirib boʻlmaydi", "U faqat sonlarni saqlaydi", "Undan indeks bilan oʻqib boʻlmaydi", "U tartibsiz"),
    Q("Bitta elementli kortej qanday yoziladi?", "(7,)", "(7)", "[7]", "tuple 7"),
    F("Masofa", "`masofa(p)` — `p = (x, y)` nuqtadan koordinata boshigacha boʻlgan Manhetten masofa: `|x| + |y|`.",
      "def masofa(p):\n    x, y = p\n    return abs(x) + abs(y)", "masofa((3, 4))", "masofa((-2, 5))", "masofa((0, 0))", lv=1),
    F("Min va maks", "`min_maks(a)` — `(eng_kichik, eng_katta)` kortejini qaytaring.",
      "def min_maks(a):\n    return (min(a), max(a))", "min_maks([3, 1, 9])", "min_maks([5])", "min_maks([-1, -8, 0])", lv=1),
    F("Vaqt", "`vaqt(soniya)` — `(soat, daqiqa, soniya)` kortejini qaytaring.",
      "def vaqt(s):\n    return (s // 3600, s % 3600 // 60, s % 60)", "vaqt(3725)", "vaqt(59)", "vaqt(86399)"),
    F("Nuqtalarni qoʻshish", "`qosh(p, q)` — ikki vektor yigʻindisi: `(x1+x2, y1+y2)`.",
      "def qosh(p, q):\n    return (p[0] + q[0], p[1] + q[1])", "qosh((1, 2), (3, 4))", "qosh((0, 0), (5, -5))", "qosh((-1, -1), (1, 1))"),
    F("Eng uzoq nuqta", "`eng_uzoq(nuqtalar)` — `(x, y)` lar ichidan `x² + y²` eng katta boʻlgan nuqtani qaytaring.",
      "def eng_uzoq(nuqtalar):\n    return max(nuqtalar, key=lambda p: p[0] ** 2 + p[1] ** 2)", "eng_uzoq([(1, 1), (3, 0), (0, 2)])", "eng_uzoq([(5, 5)])", "eng_uzoq([(-4, 0), (1, 3)])", lv=3),
    F("Yosh boʻyicha saralash", "`saralash(odamlar)` — `(ism, yosh)` kortejlarini yosh boʻyicha oʻsish tartibida saralang.",
      "def saralash(odamlar):\n    return sorted(odamlar, key=lambda o: o[1])", 'saralash([("Ali", 20), ("Vali", 15)])', "saralash([])", 'saralash([("A", 3), ("B", 1), ("C", 2)])'),
    F("Ism-familiya", "`ajrat(toliq)` — `\"Aziz Karimov\"` dan `(\"Aziz\", \"Karimov\")` kortejini qaytaring.",
      "def ajrat(toliq):\n    ism, familiya = toliq.split()\n    return (ism, familiya)", 'ajrat("Aziz Karimov")', 'ajrat("Madina Sobirova")', 'ajrat("A B")'),
    L("lc", "sort-the-people", note="`zip` va kortejlar bilan juda qisqa yechiladi."),
    L("exercism", "tisbury-treasure-hunt", note="Kortejlar boʻyicha maxsus mashq."),
    L("lc", "kids-with-the-greatest-number-of-candies"),
    L("cses", 1068),
])

# ---------------------------------------------------------------- 6.6
TOPIC("toplam", "Toʻplam (set)", "Takrorsiz elementlar va toʻplam amallari", 20, r'''
**Toʻplam** (`set`) — faqat **takrorlanmaydigan** elementlarni saqlaydi va tartibga ega emas. Eng katta afzalligi: `x in toplam` juda tez ishlaydi.

```py
mevalar = {"olma", "nok", "olma", "uzum"}
print(len(mevalar))
print("nok" in mevalar)

sonlar = [3, 1, 3, 2, 1, 3]
print(set(sonlar))
print(len(set(sonlar)))
```

!> Boʻsh toʻplam — `set()`. `{}` esa boʻsh **lugʻat** yaratadi!

## Qoʻshish va oʻchirish
```py
s = {1, 2}
s.add(3)
s.add(2)          # bor — hech narsa oʻzgarmaydi
s.discard(10)     # yoʻq boʻlsa ham xato bermaydi
s.remove(1)       # yoʻq boʻlsa KeyError
print(sorted(s))
```

## Toʻplam amallari
```py
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(sorted(a | b))   # birlashma
print(sorted(a & b))   # kesishma
print(sorted(a - b))   # ayirma
print(sorted(a ^ b))   # simmetrik ayirma
```

| Amal | Belgisi | Maʼnosi |
|---|---|---|
| Birlashma | `a \| b` | ikkalasidagi hammasi |
| Kesishma | `a & b` | ikkalasida ham bor |
| Ayirma | `a - b` | a da bor, b da yoʻq |
| Simm. ayirma | `a ^ b` | faqat bittasida bor |

## Amaliy misollar
```py
sinf_a = {"Ali", "Vali", "Sardor"}
sinf_b = {"Vali", "Madina"}
print("Ikkalasida:", sinf_a & sinf_b)

matn = "dasturlash"
print("Har xil harflar:", len(set(matn)))

royxat = [5, 3, 5, 1, 3]
print(sorted(set(royxat)))   # takrorsiz va saralangan
```

> Toʻplamda tartib kafolatlanmaydi — chiroyli chiqarish uchun `sorted()` dan foydalaning.

## Tezlik
`x in roʻyxat` — elementlarni bitta-bitta tekshiradi (sekin). `x in toʻplam` — xesh orqali birdaniga topadi (tez). Million elementda farq ming barobar!

## Esda tuting
- Takrorlarni olib tashlash: `set(a)`.
- Toʻplamga faqat oʻzgarmas qiymatlar kiradi: son, satr, kortej.
''', [
    P('print(len({1, 2, 2, 3, 3, 3}))', "6", "1", "{1, 2, 3}"),
    P('s = {1, 2}\ns.add(2)\ns.add(5)\nprint(len(s))', "4", "2", "Xato"),
    P('a = {1, 2, 3}\nb = {2, 3, 4}\nprint(sorted(a & b))', "[1, 2, 3, 4]", "[1, 4]", "[1]"),
    P('a = {1, 2, 3}\nb = {2, 3, 4}\nprint(sorted(a - b))', "[4]", "[1, 4]", "[2, 3]"),
    P('print(type({}).__name__)', "set", "list", "tuple", lv=2, why="`{}` — boʻsh lugʻat. Boʻsh toʻplam: `set()`."),
    P('s = {3, 1}\ns.discard(7)\nprint(sorted(s))', "Xato", "[1, 3, 7]", "[7]"),
    P('print(len(set("banana")))', "6", "2", "1"),
    Q("Toʻplamning asosiy xususiyati?", "Elementlar takrorlanmaydi", "Elementlar doim saralangan", "Elementlarni indeks bilan olish mumkin", "Faqat sonlar saqlanadi"),
    Q("`a | b` nima beradi?", "Ikkala toʻplamdagi barcha elementlar", "Faqat umumiylari", "a dagi, b da yoʻqlari", "Mantiqiy YOKI natijasi True/False"),
    F("Takrorlar bormi", "`takror_bor(a)` — roʻyxatda takrorlanuvchi element boʻlsa `True`.",
      "def takror_bor(a):\n    return len(set(a)) != len(a)", "takror_bor([1, 2, 3])", "takror_bor([1, 2, 1])", "takror_bor([])", lv=1),
    F("Har xillar soni", "`har_xil(a)` — nechta har xil qiymat bor?",
      "def har_xil(a):\n    return len(set(a))", "har_xil([1, 1, 2])", 'har_xil(["a", "b", "a", "c"])', "har_xil([])", lv=1),
    F("Umumiy elementlar", "`umumiy(a, b)` — ikkala roʻyxatda ham bor elementlar, **saralangan** roʻyxat koʻrinishida.",
      "def umumiy(a, b):\n    return sorted(set(a) & set(b))", "umumiy([1, 2, 3], [2, 3, 4])", "umumiy([1], [2])", "umumiy([5, 5, 1], [5, 1, 1])"),
    F("Faqat birida", "`faqat_birida(a, b)` — faqat bitta roʻyxatda uchraydigan elementlar (saralangan).",
      "def faqat_birida(a, b):\n    return sorted(set(a) ^ set(b))", "faqat_birida([1, 2, 3], [2, 3, 4])", "faqat_birida([1], [1])", "faqat_birida([], [7, 3])"),
    F("Pangramma", "`pangramma(matn)` — matnda ingliz alifbosining barcha 26 harfi bormi? (katta-kichik farqsiz)",
      "def pangramma(matn):\n    return set('abcdefghijklmnopqrstuvwxyz') <= set(matn.lower())", 'pangramma("The quick brown fox jumps over the lazy dog")', 'pangramma("Salom dunyo")', 'pangramma("")', lv=3),
    F("Takrorsiz tartib", "`takrorsiz(a)` — takrorlarni olib tashlang, lekin **birinchi uchrash tartibini** saqlang.",
      "def takrorsiz(a):\n    korilgan = set()\n    natija = []\n    for x in a:\n        if x not in korilgan:\n            korilgan.add(x)\n            natija.append(x)\n    return natija", "takrorsiz([3, 1, 3, 2, 1])", "takrorsiz([])", 'takrorsiz(["b", "a", "b"])', lv=3),
    F("Yetishmayotgan", "`yetishmaydi(a, n)` — 1 dan n gacha boʻlgan sonlardan roʻyxatda yoʻqlarini saralab qaytaring.",
      "def yetishmaydi(a, n):\n    return sorted(set(range(1, n + 1)) - set(a))", "yetishmaydi([1, 3], 4)", "yetishmaydi([1, 2, 3], 3)", "yetishmaydi([], 2)"),
    L("lc", "contains-duplicate"),
    L("lc", "intersection-of-two-arrays"),
    L("lc", "jewels-and-stones"),
    L("cses", 1621, note="Har xil qiymatlar soni — `len(set(...))`."),
])
