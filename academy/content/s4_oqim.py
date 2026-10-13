from dsl import SECTION, TOPIC, P, Q, PR, L

SECTION(4, "Boshqaruv oqimi", "Shartlar, sikllar va dastur yoʻnalishini boshqarish", "🔀")

# ---------------------------------------------------------------- 4.1
TOPIC("if-elif-else", "if / elif / else", "Dasturga qaror qabul qilishni oʻrgatamiz", 20, r'''
Hozirgacha dasturlarimiz har doim bir xil yoʻldan yurdi. **Shart operatori** dasturga tanlash imkonini beradi: "agar … boʻlsa — buni qil, aks holda — boshqasini".

## if
```py
harorat = 32
if harorat > 30:
    print("Juda issiq!")
    print("Koʻproq suv iching")
print("Dastur tugadi")
```

Shartdan keyin **ikki nuqta** `:` va keyingi qatorlar **chekinish** bilan yoziladi.

## if / else
```py
yosh = 15
if yosh >= 18:
    print("Saylovda qatnashishingiz mumkin")
else:
    print("Hali erta")
```

## if / elif / else
Bir nechta variant boʻlsa — `elif` ("else if"):

```py
ball = 78
if ball >= 86:
    baho = 5
elif ball >= 71:
    baho = 4
elif ball >= 56:
    baho = 3
else:
    baho = 2
print("Baho:", baho)
```

> Shartlar yuqoridan pastga tekshiriladi va **birinchi rost** shart bajariladi — qolganlari tashlab ketiladi. Shuning uchun tartib muhim.

## Tartib xatosi
```py
ball = 95
if ball >= 56:
    print(3)
elif ball >= 86:
    print(5)
```

95 ball — lekin `3` chiqdi! Birinchi shart allaqachon rost boʻldi. Kattadan kichikka tekshiring.

## Amaliy misol: kommunal toʻlov
```py input=350
kvt = int(input())
if kvt <= 200:
    summa = kvt * 600
elif kvt <= 1000:
    summa = 200 * 600 + (kvt - 200) * 900
else:
    summa = 200 * 600 + 800 * 900 + (kvt - 1000) * 1350
print(f"Toʻlov: {summa:,} soʻm")
```

## Esda tuting
- `if shart:` — ikki nuqta va chekinish majburiy.
- `elif` — cheksiz koʻp boʻlishi mumkin, `else` — eng koʻpi bilan bitta.
- Faqat birinchi rost tarmoq bajariladi.
''', [
    P('x = 7\nif x > 5:\n    print("katta")\nelse:\n    print("kichik")', "kichik", "katta\nkichik", "True"),
    P('x = 5\nif x > 5:\n    print("A")\nelif x == 5:\n    print("B")\nelse:\n    print("C")', "A", "A\nB", "C"),
    P('b = 95\nif b >= 56:\n    print(3)\nelif b >= 86:\n    print(5)', "5", "3\n5", "Hech narsa"),
    P('x = 0\nif x:\n    print("rost")\nelse:\n    print("yolgʻon")', "rost", "0", "Xato"),
    P('n = 10\nif n % 2 == 0:\n    print("juft")\nif n % 5 == 0:\n    print("beshga")', "juft", "beshga", "juft beshga"),
    P('n = 10\nif n % 2 == 0:\n    print("juft")\nelif n % 5 == 0:\n    print("beshga")', "juft\nbeshga", "beshga", "Hech narsa"),
    P('t = -5\nif t > 0:\n    print("+")\nelif t < -10:\n    print("--")\nelse:\n    print("-")', "--", "+", "Hech narsa"),
    Q("`if` dan keyin qator oxirida nima qoʻyiladi?", ":", ";", "{", "then"),
    Q("Bitta `if` blokida nechta `elif` boʻlishi mumkin?", "Istalgancha", "Faqat bitta", "Koʻpi bilan uchta", "elif ishlatib boʻlmaydi"),
    PR("Musbat, manfiy, nol", "Kirishda son. `musbat`, `manfiy` yoki `nol` chiqaring.", 'x = int(input())\nif x > 0:\n    print("musbat")\nelif x < 0:\n    print("manfiy")\nelse:\n    print("nol")', "5", "-3", "0"),
    PR("Baho", "Kirishda ball (0–100). 86+ → 5, 71+ → 4, 56+ → 3, qolgani → 2.", "b = int(input())\nif b >= 86:\n    print(5)\nelif b >= 71:\n    print(4)\nelif b >= 56:\n    print(3)\nelse:\n    print(2)", "95", "71", "10"),
    PR("Kattasi", "Kirishda uch son. `max` ishlatmasdan eng kattasini chiqaring.", "a, b, c = map(int, input().split())\nm = a\nif b > m:\n    m = b\nif c > m:\n    m = c\nprint(m)", "1 5 3", "9 2 9", "-1 -5 -2"),
    PR("Fasl", "Kirishda oy raqami (1–12). Faslni chiqaring: `qish` (12,1,2), `bahor` (3–5), `yoz` (6–8), `kuz` (9–11).", 'm = int(input())\nif m == 12 or m <= 2:\n    print("qish")\nelif m <= 5:\n    print("bahor")\nelif m <= 8:\n    print("yoz")\nelse:\n    print("kuz")', "1", "7", "11"),
    PR("Kvadrat tenglama", "Kirishda `a b c` (a≠0). Ildizlar soni: D>0 → 2, D=0 → 1, D<0 → 0.", "a, b, c = map(int, input().split())\nd = b * b - 4 * a * c\nif d > 0:\n    print(2)\nelif d == 0:\n    print(1)\nelse:\n    print(0)", "1 -3 2", "1 2 1", "1 0 1"),
    PR("Chipta", "Kirishda yosh. 0–6 → `bepul`, 7–17 → `5000`, 18–64 → `10000`, 65+ → `bepul`.", 'y = int(input())\nif y <= 6 or y >= 65:\n    print("bepul")\nelif y <= 17:\n    print(5000)\nelse:\n    print(10000)', "5", "12", "70"),
    PR("Elektr toʻlovi", "Kirishda kVt soat. 200 gacha — 600 soʻm/kVt, 200 dan yuqorisi — 900 soʻm/kVt. Jami summani chiqaring.", "k = int(input())\nif k <= 200:\n    print(k * 600)\nelse:\n    print(200 * 600 + (k - 200) * 900)", "150", "350", "200"),
    L("exercism", "meltdown-mitigation"),
    L("lc", "fizz-buzz"),
    L("acmp", 25),
    L("acmp", 19),
])

# ---------------------------------------------------------------- 4.2
TOPIC("ichma-ich-if", "Ichma-ich if va pass", "Shart ichida shart; pass bilan boʻsh blok", 15, r'''
Baʼzan bir shart faqat boshqa shart bajarilganda tekshiriladi. Bunday holda `if` ichiga yana `if` yoziladi — bu **ichma-ich shart**.

```py
login = "admin"
parol = "1234"
if login == "admin":
    if parol == "1234":
        print("Xush kelibsiz!")
    else:
        print("Parol notoʻgʻri")
else:
    print("Bunday foydalanuvchi yoʻq")
```

## Har bir daraja — yangi chekinish
Ichki blok tashqi blokdan yana 4 ta boʻsh joy oʻngda yoziladi.

## Ichma-ich if yoki and?
Koʻp hollarda ichma-ich `if` ni `and` bilan soddalashtirish mumkin:

```py
yosh, guvohnoma = 20, True
# Ichma-ich
if yosh >= 18:
    if guvohnoma:
        print("Mashina haydash mumkin")
# Soddaroq
if yosh >= 18 and guvohnoma:
    print("Mashina haydash mumkin")
```

> Ichki shartning `else` qismi kerak boʻlganda (yuqoridagi login misoli kabi) — ichma-ich `if` ishlatiladi. Aks holda `and` toza koʻrinadi.

## pass — "hozircha hech narsa"
Pythonda blok boʻsh boʻlishi mumkin emas. Keyinroq yoziladigan joyga `pass` qoʻyiladi:

```py
x = 5
if x > 0:
    pass   # TODO: keyin yozaman
else:
    print("manfiy")
print("ishladi")
```

## Amaliy misol: yetkazib berish narxi
```py input=Toshkent|120000
shahar = input()
summa = int(input())
if shahar == "Toshkent":
    if summa >= 100000:
        narx = 0
    else:
        narx = 15000
else:
    narx = 35000
print("Yetkazish:", narx)
```

## Esda tuting
- Ichki `if` — qoʻshimcha chekinish.
- Ichma-ich shartni koʻpincha `and` bilan soddalashtirish mumkin.
- `pass` — boʻsh blok uchun joy egallovchi.
''', [
    P('x, y = 5, -2\nif x > 0:\n    if y > 0:\n        print("I")\n    else:\n        print("IV")', "I", "Hech narsa", "I\nIV"),
    P('x = -1\nif x > 0:\n    if x > 10:\n        print("katta")\nelse:\n    print("manfiy")', "katta", "Hech narsa", "Xato"),
    P('if True:\n    pass\nprint("ok")', "pass\nok", "Hech narsa", "Xato"),
    P('a = 3\nif a > 1:\n    if a > 2:\n        if a > 3:\n            print("A")\n        else:\n            print("B")', "A", "A\nB", "Hech narsa"),
    P('n = 15\nif n % 3 == 0:\n    if n % 5 == 0:\n        print("FizzBuzz")\n    else:\n        print("Fizz")', "Fizz", "Fizz\nFizzBuzz", "Hech narsa"),
    P('x = 0\nif x >= 0:\n    if x == 0:\n        print("nol")\n    print("musbat")', "nol", "musbat", "Hech narsa"),
    P('if 1 > 2:\n    pass\nelse:\n    print("else")', "pass", "Hech narsa", "Xato"),
    Q("`pass` nima uchun ishlatiladi?", "Hech narsa qilmaydigan boʻsh blok uchun", "Sikldan chiqish uchun", "Xatoni oʻtkazib yuborish uchun", "Dasturni toʻxtatish uchun"),
    Q("`if a: if b: ...` ni qanday soddalashtirish mumkin (ichki else boʻlmasa)?", "if a and b:", "if a or b:", "if a, b:", "if a if b:"),
    PR("Chorak", "Kirishda nuqta `x y` (nol emas). Qaysi chorakda ekanini chiqaring (1, 2, 3 yoki 4) — ichma-ich `if` bilan.", "x, y = map(int, input().split())\nif x > 0:\n    if y > 0:\n        print(1)\n    else:\n        print(4)\nelse:\n    if y > 0:\n        print(2)\n    else:\n        print(3)", "1 1", "-1 1", "-1 -1"),
    PR("Login", "Kirishda login va parol (ikki qator). Login `admin` boʻlmasa — `foydalanuvchi yoq`; login toʻgʻri, parol `1234` boʻlmasa — `parol xato`; ikkalasi toʻgʻri — `xush kelibsiz`.", 'l = input()\np = input()\nif l == "admin":\n    if p == "1234":\n        print("xush kelibsiz")\n    else:\n        print("parol xato")\nelse:\n    print("foydalanuvchi yoq")', "admin\n1234", "admin\n0000", "user\n1234"),
    PR("Yetkazish", "Kirishda shahar va summa (ikki qator). Toshkentda: summa ≥ 100000 → 0, aks holda 15000. Boshqa shaharlarda — 35000. Narxni chiqaring.", 's = input()\nm = int(input())\nif s == "Toshkent":\n    if m >= 100000:\n        print(0)\n    else:\n        print(15000)\nelse:\n    print(35000)', "Toshkent\n120000", "Toshkent\n5000", "Buxoro\n500000"),
    PR("FizzBuzz bitta son", "Kirishda son. 3 va 5 ga boʻlinsa `FizzBuzz`, faqat 3 ga — `Fizz`, faqat 5 ga — `Buzz`, aks holda sonning oʻzi.", 'n = int(input())\nif n % 3 == 0:\n    if n % 5 == 0:\n        print("FizzBuzz")\n    else:\n        print("Fizz")\nelif n % 5 == 0:\n    print("Buzz")\nelse:\n    print(n)', "15", "9", "7"),
    PR("Uchburchak turi", "Kirishda uch tomon. Uchburchak boʻlmasa `yoq`; boʻlsa: hammasi teng → `teng tomonli`, ikkitasi teng → `teng yonli`, aks holda `oddiy`.", 'a, b, c = map(int, input().split())\nif a + b > c and a + c > b and b + c > a:\n    if a == b == c:\n        print("teng tomonli")\n    elif a == b or b == c or a == c:\n        print("teng yonli")\n    else:\n        print("oddiy")\nelse:\n    print("yoq")', "3 3 3", "3 3 5", "1 2 10"),
    PR("Pass bilan", "Kirishda son. Agar u manfiy boʻlsa hech narsa qilmang (`pass`), aks holda uning kvadratini chiqaring. Oxirida har doim `tamom` chiqsin.", 'x = int(input())\nif x < 0:\n    pass\nelse:\n    print(x * x)\nprint("tamom")', "4", "-3", "0"),
    PR("Bank", "Kirishda balans va yechiladigan summa. Summa musbat boʻlmasa `notoʻgʻri summa`; balans yetmasa `mablagʻ yetarli emas`; aks holda yangi balansni chiqaring.", 'b, s = map(int, input().split())\nif s > 0:\n    if s <= b:\n        print(b - s)\n    else:\n        print("mablagʻ yetarli emas")\nelse:\n    print("notoʻgʻri summa")', "100000 30000", "100 500", "100 -5"),
    L("exercism", "meltdown-mitigation"),
    L("exercism", "black-jack"),
    L("acmp", 19),
    L("acmp", 66),
])

# ---------------------------------------------------------------- 4.3
TOPIC("match-case", "match-case", "Python 3.10+ dagi naqsh boʻyicha tanlash", 15, r'''
Bitta oʻzgaruvchini koʻp qiymatlar bilan solishtirish kerak boʻlsa, uzun `if/elif` zanjiri oʻrniga `match-case` ishlatish mumkin.

```py
kun = 3
match kun:
    case 1:
        print("Dushanba")
    case 2:
        print("Seshanba")
    case 3:
        print("Chorshanba")
    case _:
        print("Boshqa kun")
```

`case _` — "boshqa hamma holatlar" (`else` kabi).

## Bir nechta qiymat: |
```py
oy = 7
match oy:
    case 12 | 1 | 2:
        print("Qish")
    case 3 | 4 | 5:
        print("Bahor")
    case 6 | 7 | 8:
        print("Yoz")
    case _:
        print("Kuz")
```

## Satrlar bilan: menyu
```py input=narx
buyruq = input()
match buyruq:
    case "salom":
        print("Assalomu alaykum!")
    case "narx":
        print("Kurs narxi: 450 000 soʻm")
    case "chiqish":
        print("Xayr!")
    case _:
        print("Nomaʼlum buyruq")
```

## Shart qoʻshish: guard
`case` ga `if` qoʻshish mumkin:

```py
ball = 77
match ball:
    case b if b >= 86:
        print(5)
    case b if b >= 71:
        print(4)
    case _:
        print(3)
```

## Tuzilmani ochish
`match` kortej va roʻyxatlarni "ochib" oʻqiy oladi:

```py
nuqta = (0, 5)
match nuqta:
    case (0, 0):
        print("Markaz")
    case (0, y):
        print("Y oʻqida, y =", y)
    case (x, 0):
        print("X oʻqida, x =", x)
    case (x, y):
        print("Boshqa joyda")
```

!> `match` faqat Python 3.10 va undan yangi versiyalarda ishlaydi. Mirae Academy ichidagi Python — eng yangi, xavotir olmang.

## Esda tuting
- `match qiymat:` → `case variant:` → `case _:` (qolganlari).
- `case a | b:` — bir nechta qiymat.
- `case x if shart:` — qoʻshimcha shart.
''', [
    P('x = 2\nmatch x:\n    case 1:\n        print("bir")\n    case 2:\n        print("ikki")\n    case _:\n        print("?")', "bir", "ikki\n?", "?"),
    P('x = 9\nmatch x:\n    case 1:\n        print("bir")\n    case _:\n        print("boshqa")', "bir", "9", "Hech narsa"),
    P('m = 1\nmatch m:\n    case 12 | 1 | 2:\n        print("qish")\n    case _:\n        print("emas")', "emas", "12", "Xato"),
    P('s = "B"\nmatch s:\n    case "a":\n        print(1)\n    case "b":\n        print(2)\n    case _:\n        print(0)', "2", "1", "Xato"),
    P('p = (0, 7)\nmatch p:\n    case (0, 0):\n        print("markaz")\n    case (0, y):\n        print("y", y)', "markaz", "y", "0 7"),
    P('n = 50\nmatch n:\n    case x if x > 100:\n        print("katta")\n    case x if x > 10:\n        print("oʻrta")\n    case _:\n        print("kichik")', "katta", "kichik", "x"),
    P('x = 3\nmatch x:\n    case 3:\n        print("uch")\n    case 3:\n        print("yana uch")', "uch\nyana uch", "yana uch", "Xato"),
    Q("`match` dagi `case _:` nimani bildiradi?", "Boshqa barcha holatlar", "Boʻsh satr", "Xato holati", "Nol qiymat"),
    Q("`match-case` qaysi Python versiyasidan boshlab ishlaydi?", "3.10", "3.6", "2.7", "3.0"),
    PR("Hafta kuni", "Kirishda 1–7. `match` bilan kun nomini chiqaring: Dushanba, Seshanba, Chorshanba, Payshanba, Juma, Shanba, Yakshanba. Boshqa son — `xato`.", 'match int(input()):\n    case 1:\n        print("Dushanba")\n    case 2:\n        print("Seshanba")\n    case 3:\n        print("Chorshanba")\n    case 4:\n        print("Payshanba")\n    case 5:\n        print("Juma")\n    case 6:\n        print("Shanba")\n    case 7:\n        print("Yakshanba")\n    case _:\n        print("xato")', "1", "6", "9"),
    PR("Kalkulyator", "Kirishda `a amal b` (masalan `3 + 4`). Amal `+ - * /` boʻlishi mumkin. Natijani chiqaring; nomaʼlum amal — `xato`.", 'a, op, b = input().split()\na, b = int(a), int(b)\nmatch op:\n    case "+":\n        print(a + b)\n    case "-":\n        print(a - b)\n    case "*":\n        print(a * b)\n    case "/":\n        print(a / b)\n    case _:\n        print("xato")', "3 + 4", "10 / 4", "2 ^ 3"),
    PR("Fasl", "Kirishda oy (1–12). `match` va `|` bilan faslni chiqaring: `qish`, `bahor`, `yoz`, `kuz`.", 'match int(input()):\n    case 12 | 1 | 2:\n        print("qish")\n    case 3 | 4 | 5:\n        print("bahor")\n    case 6 | 7 | 8:\n        print("yoz")\n    case _:\n        print("kuz")', "1", "4", "10"),
    PR("Buyruq", "Kirishda buyruq: `start` → `Boshlandi`, `stop` → `Toʻxtatildi`, `help` → `Yordam: start, stop`, boshqasi → `Nomaʼlum buyruq`.", 'match input():\n    case "start":\n        print("Boshlandi")\n    case "stop":\n        print("Toʻxtatildi")\n    case "help":\n        print("Yordam: start, stop")\n    case _:\n        print("Nomaʼlum buyruq")', "start", "help", "run"),
    PR("Svetofor", "Kirishda rang: `qizil` → `toʻxta`, `sariq` → `tayyorlan`, `yashil` → `yur`. Boshqa → `nosoz`.", 'match input():\n    case "qizil":\n        print("toʻxta")\n    case "sariq":\n        print("tayyorlan")\n    case "yashil":\n        print("yur")\n    case _:\n        print("nosoz")', "qizil", "yashil", "koʻk"),
    PR("Nuqta", "Kirishda `x y`. `match` bilan: (0,0) → `markaz`, x=0 → `Y oʻqi`, y=0 → `X oʻqi`, aks holda `tekislik`.", 'x, y = map(int, input().split())\nmatch (x, y):\n    case (0, 0):\n        print("markaz")\n    case (0, _):\n        print("Y oʻqi")\n    case (_, 0):\n        print("X oʻqi")\n    case _:\n        print("tekislik")', "0 0", "0 5", "3 4"),
    PR("Baho matni", "Kirishda baho 2–5. `5` → `aʼlo`, `4` → `yaxshi`, `3` → `qoniqarli`, `2` → `qoniqarsiz`.", 'match int(input()):\n    case 5:\n        print("aʼlo")\n    case 4:\n        print("yaxshi")\n    case 3:\n        print("qoniqarli")\n    case _:\n        print("qoniqarsiz")', "5", "3", "2"),
    L("exercism", "raindrops"),
    L("exercism", "bob"),
    L("lc", "goal-parser-interpretation"),
    L("acmp", 35),
])

# ---------------------------------------------------------------- 4.4
TOPIC("for", "for sikli va for…else", "Ketma-ketlik boʻylab takrorlash", 25, r'''
**Sikl** — kodni takror bajarish. `for` sikli ketma-ketlikning (satr, roʻyxat, `range`) har bir elementi uchun blokni bir marta bajaradi.

```py
for meva in ["olma", "nok", "uzum"]:
    print("Men", meva, "yaxshi koʻraman")
```

## range bilan
```py
for i in range(5):
    print(i, end=" ")
print()
for i in range(1, 6):
    print(i * i, end=" ")
```

## Yigʻindi va hisoblagich
```py
sonlar = [12, 7, 30, 5, 18]
jami = 0
katta = 0
for n in sonlar:
    jami += n
    if n > 10:
        katta += 1
print("Jami:", jami, "| 10 dan kattalar:", katta)
```

## break va continue
- `break` — sikldan butunlay chiqish.
- `continue` — joriy qadamni tashlab, keyingisiga oʻtish.

```py
for n in range(1, 10):
    if n % 2 == 0:
        continue
    if n > 7:
        break
    print(n, end=" ")
```

## for … else
`else` bloki sikl **break siz** tugaganda bajariladi. Qidiruvda juda qulay:

```py
ismlar = ["Ali", "Vali", "Gani"]
qidir = "Soli"
for ism in ismlar:
    if ism == qidir:
        print("Topildi!")
        break
else:
    print("Topilmadi")
```

## Amaliy misol: tub son
```py input=29
n = int(input())
for d in range(2, int(n ** 0.5) + 1):
    if n % d == 0:
        print(n, "— murakkab son, boʻluvchisi", d)
        break
else:
    print(n, "— tub son")
```

## Esda tuting
- `for x in ketma_ketlik:` — har bir element uchun bir marta.
- `break` — chiqish, `continue` — keyingi qadamga.
- `for…else` — `break` boʻlmasa `else` ishlaydi.
''', [
    P('for i in range(3):\n    print(i)', "1\n2\n3", "0\n1\n2\n3", "3"),
    P('s = 0\nfor x in [1, 2, 3, 4]:\n    s += x\nprint(s)', "4", "1234", "0"),
    P('for h in "abc":\n    print(h.upper(), end="")', "abc", "A B C", "A\nB\nC"),
    P('for i in range(10):\n    if i == 3:\n        break\n    print(i, end=" ")', "0 1 2 3", "3", "0 1 2 4 5 6 7 8 9"),
    P('for i in range(5):\n    if i == 2:\n        continue\n    print(i, end="")', "01234", "2", "01"),
    P('for x in [1, 2, 3]:\n    if x == 5:\n        break\nelse:\n    print("topilmadi")', "Hech narsa", "5", "1 2 3"),
    P('for x in [1, 5, 3]:\n    if x == 5:\n        print("bor")\n        break\nelse:\n    print("yoʻq")', "bor\nyoʻq", "yoʻq", "5"),
    Q("`continue` nima qiladi?", "Joriy qadamni tashlab, keyingisiga oʻtadi", "Sikldan chiqadi", "Siklni boshidan boshlaydi", "Dasturni toʻxtatadi"),
    Q("`for … else` dagi `else` qachon bajariladi?", "Sikl break siz tugaganda (hatto bir marta ham aylanmasa ham)", "Faqat sikl birinchi qadamida", "break boʻlganda", "Har bir qadamdan keyin"),
    PR("1 dan n gacha", "Kirishda n. 1 dan n gacha sonlarni bir qatorda chiqaring.", "n = int(input())\nfor i in range(1, n + 1):\n    print(i, end=\" \")\nprint()", "5", "1", "10"),
    PR("Yigʻindi", "Kirishda n. 1 dan n gacha sonlar yigʻindisini `for` bilan hisoblang.", "s = 0\nfor i in range(1, int(input()) + 1):\n    s += i\nprint(s)", "10", "1", "100"),
    PR("Faktorial", "Kirishda n. `n!` ni chiqaring.", "f = 1\nfor i in range(2, int(input()) + 1):\n    f *= i\nprint(f)", "5", "0", "20"),
    PR("Juft sonlar soni", "Kirishda sonlar (bir qatorda). Nechtasi juft ekanini chiqaring.", "k = 0\nfor x in input().split():\n    if int(x) % 2 == 0:\n        k += 1\nprint(k)", "1 2 3 4", "1 3 5", "0 0 7"),
    PR("Tub son", "Kirishda n (≥2). `for…else` bilan: tub boʻlsa `tub`, aks holda `murakkab`.", 'n = int(input())\nfor d in range(2, int(n ** 0.5) + 1):\n    if n % d == 0:\n        print("murakkab")\n        break\nelse:\n    print("tub")', "29", "21", "2"),
    PR("Birinchi manfiy", "Kirishda sonlar. Birinchi manfiy sonni chiqaring; yoʻq boʻlsa `yoq` (`break` va `else`).", 'for x in input().split():\n    if int(x) < 0:\n        print(x)\n        break\nelse:\n    print("yoq")', "3 -2 -5", "1 2 3", "-1"),
    PR("FizzBuzz", "Kirishda n. 1 dan n gacha: 15 ga boʻlinsa `FizzBuzz`, 3 ga — `Fizz`, 5 ga — `Buzz`, aks holda son. Har biri yangi qatorda.", 'for i in range(1, int(input()) + 1):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)', "15", "3", "5"),
    L("exercism", "making-the-grade"),
    L("lc", "running-sum-of-1d-array"),
    L("cses", 1068),
    L("acmp", 349),
])

# ---------------------------------------------------------------- 4.5
TOPIC("ichma-ich-sikl", "Ichma-ich sikllar", "Sikl ichida sikl: jadvallar, naqshlar, juftliklar", 20, r'''
Sikl ichida yana sikl boʻlishi mumkin. Ichki sikl tashqi siklning **har bir** qadamida toʻliq bajariladi.

```py
for i in range(1, 4):
    for j in range(1, 4):
        print(i * j, end="\t")
    print()
```

Tashqi sikl 3 marta, ichki sikl har safar 3 marta — jami 9 marta.

## Naqshlar chizish
```py
n = 4
for i in range(1, n + 1):
    for j in range(i):
        print("*", end="")
    print()
```

## Barcha juftliklar
```py
jamoalar = ["Paxtakor", "Nasaf", "Navbahor"]
for i in range(len(jamoalar)):
    for j in range(i + 1, len(jamoalar)):
        print(jamoalar[i], "—", jamoalar[j])
```

## Ichma-ich sikldan chiqish
`break` faqat **ichki** sikldan chiqaradi. Ikkalasidan chiqish uchun bayroq (flag) ishlatiladi:

```py
topildi = False
for a in range(1, 10):
    for b in range(1, 10):
        if a * b == 24 and a < b:
            print(a, b)
            topildi = True
            break
    if topildi:
        break
```

## Murakkablik
Ichma-ich sikl tez "ogʻirlashadi": 1000 × 1000 = 1 000 000 qadam. Olimpiadada buni hisobga oling.

```py
qadam = 0
for i in range(100):
    for j in range(100):
        qadam += 1
print("Qadamlar:", qadam)
```

## Amaliy misol: koʻpaytirish jadvali
```py
for i in range(1, 6):
    qator = ""
    for j in range(1, 6):
        qator += f"{i * j:4}"
    print(qator)
```

## Esda tuting
- Ichki sikl tashqi siklning har qadamida toʻliq ishlaydi.
- `break` faqat eng ichki sikldan chiqaradi.
- n × m qadam — katta n da sekinlashadi.
''', [
    P('for i in range(2):\n    for j in range(3):\n        print(i, end="")\nprint()', "012012", "01", "001122"),
    P('n = 0\nfor i in range(4):\n    for j in range(5):\n        n += 1\nprint(n)', "9", "4", "5"),
    P('for i in range(1, 4):\n    print("*" * i)', "***\n**\n*", "*\n*\n*", "******"),
    P('for i in range(3):\n    for j in range(3):\n        if j == 1:\n            break\n        print(i, j)', "0 0", "0 0\n0 1", "Hech narsa"),
    P('s = 0\nfor i in range(1, 3):\n    for j in range(1, 3):\n        s += i * j\nprint(s)', "4", "6", "10"),
    P('for i in range(3):\n    for j in range(i):\n        print(j, end="")\nprint()', "012", "001122", "0101"),
    P('k = 0\nfor i in range(3):\n    for j in range(i + 1, 3):\n        k += 1\nprint(k)', "9", "6", "2"),
    Q("Tashqi sikl 10 marta, ichki sikl 20 marta aylansa, ichki blok jami necha marta bajariladi?", "200", "30", "20", "10"),
    Q("Ichki sikldagi `break` qayerdan chiqaradi?", "Faqat ichki sikldan", "Ikkala sikldan", "Dasturdan", "Faqat tashqi sikldan"),
    PR("Toʻrtburchak", "Kirishda `n m`. n qator, har birida m ta `*` chiqaring.", "n, m = map(int, input().split())\nfor i in range(n):\n    print(\"*\" * m)", "2 3", "1 1", "3 5"),
    PR("Uchburchak", "Kirishda n. i-qatorda 1 dan i gacha sonlarni (boʻsh joysiz) chiqaring.", "n = int(input())\nfor i in range(1, n + 1):\n    for j in range(1, i + 1):\n        print(j, end=\"\")\n    print()", "3", "1", "5"),
    PR("Jadval", "Kirishda n. n×n koʻpaytirish jadvalini chiqaring, qiymatlar boʻsh joy bilan ajratilgan.", "n = int(input())\nfor i in range(1, n + 1):\n    print(*[i * j for j in range(1, n + 1)])", "3", "1", "5"),
    PR("Juftliklar", "Kirishda n. 1 ≤ i < j ≤ n boʻlgan barcha juftliklar sonini sanab chiqaring.", "n = int(input())\nk = 0\nfor i in range(1, n + 1):\n    for j in range(i + 1, n + 1):\n        k += 1\nprint(k)", "3", "1", "10"),
    PR("Shaxmat", "Kirishda n. n×n shaxmat taxtasini `#` va `.` bilan chiqaring; chap yuqori burchak `#`.", 'n = int(input())\nfor i in range(n):\n    print("".join("#" if (i + j) % 2 == 0 else "." for j in range(n)))', "4", "1", "3"),
    PR("Yigʻindisi n", "Kirishda n. `a + b = n` boʻlgan barcha `1 ≤ a ≤ b` juftliklarni `a b` koʻrinishida chiqaring.", "n = int(input())\nfor a in range(1, n + 1):\n    for b in range(a, n + 1):\n        if a + b == n:\n            print(a, b)", "6", "2", "7"),
    PR("Teskari uchburchak", "Kirishda n. Birinchi qatorda n ta `*`, keyingisida n-1 ta… oxirgisida 1 ta.", 'n = int(input())\nfor i in range(n, 0, -1):\n    print("*" * i)', "3", "1", "5"),
    L("exercism", "diamond"),
    L("lc", "pascals-triangle"),
    L("acmp", 265),
    L("acmp", 197),
])

# ---------------------------------------------------------------- 4.6
TOPIC("while", "while sikli va cheksiz sikllar", "Shart rost boʻlguncha takrorlash", 20, r'''
`for` — nechta qadam boʻlishi oldindan maʼlum boʻlganda. **while** — esa "shart rost ekan, takrorla" degan holatlar uchun: necha marta ekanini oldindan bilmaymiz.

```py
n = 1
while n <= 5:
    print(n, end=" ")
    n += 1
```

!> Shart ichida oʻzgaruvchini oʻzgartirishni unutsangiz — sikl hech qachon tugamaydi (**cheksiz sikl**). Mirae Academy bunday kodni bir necha soniyadan keyin avtomatik toʻxtatadi.

## Raqamlarga ajratish
```py
n = 90217
yigindi = 0
while n > 0:
    yigindi += n % 10
    n //= 10
print("Raqamlar yigʻindisi:", yigindi)
```

## Toʻgʻri javobgacha soʻrash
```py input=abc|42
while True:
    javob = input()
    if javob.isdigit():
        print("Rahmat! Siz", javob, "kiritdingiz")
        break
    print("Iltimos, son kiriting")
```

`while True` — ataylab qilingan cheksiz sikl, undan `break` bilan chiqiladi. Menyular, oʻyinlar va serverlarda koʻp ishlatiladi.

## while … else
`for` dagi kabi: `break` siz tugasa — `else` bajariladi.

## Amaliy misol: omonat
```py
summa = 10_000_000
yil = 0
while summa < 20_000_000:
    summa = summa * 1.2
    yil += 1
print(yil, "yilda pul ikki baravar boʻladi:", int(summa))
```

## Kollats gipotezasi
```py
n = 6
qadam = 0
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    qadam += 1
print("Qadamlar:", qadam)
```

## Esda tuting
- `while shart:` — shart rost ekan takrorlaydi.
- Sikl ichida shartga taʼsir qiluvchi oʻzgarish boʻlishi shart.
- `while True` + `break` — chiqish sharti oʻrtada boʻlganda.
''', [
    P('i = 0\nwhile i < 3:\n    print(i, end="")\n    i += 1', "0123", "123", "012012"),
    P('n = 10\nwhile n > 0:\n    n -= 3\nprint(n)', "0", "1", "-3"),
    P('n = 1234\ns = 0\nwhile n:\n    s += n % 10\n    n //= 10\nprint(s)', "1234", "4321", "4"),
    P('i = 0\nwhile True:\n    i += 1\n    if i == 4:\n        break\nprint(i)', "3", "5", "Cheksiz sikl"),
    P('x = 5\nwhile x > 10:\n    x += 1\nprint(x)', "10", "11", "Cheksiz sikl"),
    P('n, k = 6, 0\nwhile n != 1:\n    n = n // 2 if n % 2 == 0 else 3 * n + 1\n    k += 1\nprint(k)', "6", "3", "16"),
    P('i = 0\nwhile i < 5:\n    i += 1\n    if i % 2:\n        continue\n    print(i, end=" ")', "1 3 5", "2 4 6", "0 2 4"),
    Q("Qaysi holatda `while` sikli `for` dan qulayroq?", "Takrorlashlar soni oldindan nomaʼlum boʻlganda", "Roʻyxat elementlarini aylanishda", "1 dan 10 gacha sanashda", "Satr harflarini aylanishda"),
    Q("`while x < 10: print(x)` — bu kodda qanday muammo bor (x = 0)?", "x oʻzgarmaydi — cheksiz sikl", "Sintaksis xato", "Hech qanday", "Faqat bir marta ishlaydi"),
    PR("Raqamlar soni", "Kirishda natural son. `while` bilan uning raqamlari sonini toping.", "n = int(input())\nk = 0\nwhile n > 0:\n    n //= 10\n    k += 1\nprint(k)", "12345", "7", "1000000"),
    PR("Teskari son", "Kirishda natural son. `while` bilan raqamlarini teskari tartibda son qilib chiqaring.", "n = int(input())\nr = 0\nwhile n > 0:\n    r = r * 10 + n % 10\n    n //= 10\nprint(r)", "1234", "100", "7"),
    PR("Ikkining darajasi", "Kirishda n. n dan katta boʻlmagan eng katta ikkining darajasini chiqaring.", "n = int(input())\np = 1\nwhile p * 2 <= n:\n    p *= 2\nprint(p)", "100", "1", "1024"),
    PR("Kollats", "Kirishda n. Kollats qoidasi (juft → n/2, toq → 3n+1) bilan 1 ga yetguncha qadamlar sonini chiqaring.", "n = int(input())\nk = 0\nwhile n != 1:\n    n = n // 2 if n % 2 == 0 else 3 * n + 1\n    k += 1\nprint(k)", "6", "1", "27"),
    PR("Nolgacha", "Kirishda sonlar ketma-ketligi, har biri yangi qatorda, oxirida `0`. 0 gacha boʻlgan sonlar yigʻindisini chiqaring.", "s = 0\nwhile True:\n    x = int(input())\n    if x == 0:\n        break\n    s += x\nprint(s)", "5\n3\n0", "0", "10\n-4\n2\n0"),
    PR("Omonat", "Kirishda boshlangʻich summa va yillik foiz. Summa kamida ikki baravar boʻlishi uchun necha yil kerak (har yil `summa = summa + summa * foiz / 100`)?", "s, f = map(int, input().split())\nt = s * 2\ny = 0\nwhile s < t:\n    s = s + s * f / 100\n    y += 1\nprint(y)", "1000 20", "1000 100", "100 7"),
    PR("EKUB (Evklid)", "Kirishda ikki natural son. `while` va qoldiq bilan EKUB ni toping.", "a, b = map(int, input().split())\nwhile b:\n    a, b = b, a % b\nprint(a)", "12 18", "17 5", "100 75"),
    L("exercism", "collatz-conjecture"),
    L("lc", "happy-number"),
    L("cses", 1068),
    L("acmp", 147),
])

# ---------------------------------------------------------------- 4.7
TOPIC("iterable", "Iterable obyektlar", "for bilan aylanish mumkin boʻlgan narsalar: enumerate, zip, sorted…", 20, r'''
**Iterable** — elementlarini birma-bir berish mumkin boʻlgan obyekt. `for` sikli aynan iterable bilan ishlaydi.

Iterable larga misollar: satr, roʻyxat, kortej, lugʻat, toʻplam, `range`, fayl.

```py
for x in "abc":
    print(x, end=" ")
for x in (10, 20):
    print(x, end=" ")
for x in {"a": 1, "b": 2}:
    print(x, end=" ")
```

> Lugʻat boʻylab aylanganda **kalitlar** chiqadi.

## enumerate — indeks bilan
```py
mevalar = ["olma", "nok", "uzum"]
for i, meva in enumerate(mevalar, start=1):
    print(i, meva)
```

## zip — bir vaqtda bir nechtasini
```py
ismlar = ["Ali", "Vali", "Gani"]
ballar = [90, 75, 82]
for ism, ball in zip(ismlar, ballar):
    print(f"{ism}: {ball}")
```

## reversed va sorted
```py
for x in reversed([1, 2, 3]):
    print(x, end=" ")
print()
for x in sorted([5, 1, 4]):
    print(x, end=" ")
```

## Iterable ni qabul qiladigan funksiyalar
```py
sonlar = [4, 8, 15, 16, 23, 42]
print(sum(sonlar), min(sonlar), max(sonlar), len(sonlar))
print(list("salom"))
print(any(x > 40 for x in sonlar), all(x > 0 for x in sonlar))
```

## Iterator va next()
Iterable dan `iter()` bilan **iterator** olinadi — u elementlarni birma-bir beradi:

```py
it = iter([10, 20, 30])
print(next(it))
print(next(it))
print(next(it))
```

!> Elementlar tugagach `next()` — `StopIteration` xatosini beradi. `for` sikli buni ichkarida oʻzi boshqaradi.

## Esda tuting
- `for` istalgan iterable bilan ishlaydi.
- `enumerate` — indeks bilan, `zip` — parallel aylanish.
- `sum`, `max`, `min`, `sorted`, `any`, `all` — iterable qabul qiladi.
''', [
    P('for i, x in enumerate("ab"):\n    print(i, x)', "a 0\nb 1", "1 a\n2 b", "0\n1"),
    P('for a, b in zip([1, 2], ["x", "y"]):\n    print(a, b)', "1 2\nx y", "1 x", "(1, 'x')\n(2, 'y')"),
    P('print(list(reversed("abc")))', "cba", "['abc']", "['a', 'b', 'c']"),
    P('d = {"x": 1, "y": 2}\nfor k in d:\n    print(k, end="")', "12", "x1y2", "Xato"),
    P('print(sum(range(5)))', "15", "5", "4"),
    P('it = iter([7, 8])\nnext(it)\nprint(next(it))', "7", "Xato", "[7, 8]"),
    P('print(any([0, "", None]), all([1, "a"]))', "True True", "False False", "True False"),
    Q("`enumerate([\"a\", \"b\"], start=1)` qanday juftliklar beradi?", "(1, 'a'), (2, 'b')", "(0, 'a'), (1, 'b')", "('a', 1), ('b', 2)", "1, 2"),
    Q("Qaysi biri iterable EMAS?", "42 (butun son)", "\"salom\"", "[1, 2]", "range(3)"),
    PR("Raqamlangan roʻyxat", "Kirishda soʻzlar (bir qatorda). Har birini `1. soʻz` koʻrinishida (enumerate bilan) yangi qatorda chiqaring.", 'for i, s in enumerate(input().split(), 1):\n    print(f"{i}. {s}")', "olma nok uzum", "salom", "a b"),
    PR("Ism va ball", "Kirishda ikki qator: ismlar va ballar (boʻsh joy bilan). `zip` bilan `ism: ball` qatorlarini chiqaring.", 'for i, b in zip(input().split(), input().split()):\n    print(f"{i}: {b}")', "Ali Vali\n90 75", "X\n1", "a b c\n1 2 3"),
    PR("Teskari", "Kirishda sonlar. `reversed` bilan teskari tartibda bir qatorda chiqaring.", "print(*reversed(input().split()))", "1 2 3", "5", "a b"),
    PR("Saralangan", "Kirishda sonlar. Ularni oʻsish tartibida chiqaring (son sifatida saralang!).", "print(*sorted(map(int, input().split())))", "10 9 100 1", "5", "-1 -3 2"),
    PR("Statistika", "Kirishda sonlar. Yigʻindi, eng kichik va eng katta sonni bir qatorda chiqaring.", "a = list(map(int, input().split()))\nprint(sum(a), min(a), max(a))", "4 8 15", "7", "-1 0 1"),
    PR("Hammasi musbatmi", "Kirishda sonlar. Hammasi musbat boʻlsa `True` (`all` bilan).", "print(all(int(x) > 0 for x in input().split()))", "1 2 3", "1 -2 3", "5"),
    PR("Juft indekslar", "Kirishda soʻzlar. `enumerate` bilan faqat juft indeksdagi (0, 2, 4…) soʻzlarni bir qatorda chiqaring.", "print(*[s for i, s in enumerate(input().split()) if i % 2 == 0])", "a b c d e", "x", "bir ikki"),
    L("exercism", "card-games"),
    L("lc", "running-sum-of-1d-array"),
    L("lc", "shuffle-the-array"),
    L("acmp", 5),
])

# ---------------------------------------------------------------- 4.8
TOPIC("range", "range()", "Sonlar ketma-ketligini yaratish", 15, r'''
`range()` — sonlar ketma-ketligini hosil qiladi. U `for` bilan eng koʻp ishlatiladigan juftlik.

| Yozuv | Maʼnosi | Natija |
|---|---|---|
| `range(5)` | 0 dan 5 gacha (5 kirmaydi) | 0 1 2 3 4 |
| `range(2, 6)` | 2 dan 6 gacha | 2 3 4 5 |
| `range(1, 10, 2)` | 1 dan, 2 qadam bilan | 1 3 5 7 9 |
| `range(5, 0, -1)` | teskari | 5 4 3 2 1 |

```py
print(list(range(5)))
print(list(range(2, 6)))
print(list(range(1, 10, 2)))
print(list(range(5, 0, -1)))
```

> Oxirgi qiymat hech qachon kirmaydi — kesishdagi kabi. `1` dan `n` gacha: `range(1, n + 1)`.

## Qadam bilan
```py
for yil in range(2020, 2031, 5):
    print(yil, end=" ")
print()
for i in range(10, 0, -3):
    print(i, end=" ")
```

## range xotirani tejaydi
`range(1_000_000)` million son saqlamaydi — u faqat boshi, oxiri va qadamni eslaydi:

```py
r = range(0, 1_000_000, 7)
print(len(r))
print(r[10])
print(700 in r)
```

## Indeks orqali aylanish
```py
sozlar = ["bir", "ikki", "uch"]
for i in range(len(sozlar)):
    print(i, sozlar[i])
```

> Faqat elementlar kerak boʻlsa — `for soz in sozlar:`; indeks ham kerak boʻlsa — `enumerate` qulayroq.

## Amaliy misol: arifmetik progressiya
```py input=3|4|5
a1 = int(input())
d = int(input())
n = int(input())
for x in range(a1, a1 + d * n, d):
    print(x, end=" ")
```

## Esda tuting
- `range(boshi, oxiri, qadam)` — oxiri kirmaydi.
- Teskari sanash: manfiy qadam.
- `range` — dangasa: katta oraliqlar ham xotirani band qilmaydi.
''', [
    P('print(list(range(4)))', "[1, 2, 3, 4]", "[0, 1, 2, 3, 4]", "4"),
    P('print(list(range(2, 8, 3)))', "[2, 5, 8]", "[2, 3, 4, 5, 6, 7]", "[3, 6]"),
    P('print(list(range(5, 0, -2)))', "[5, 4, 3, 2, 1]", "[5, 3, 1, -1]", "[]"),
    P('print(list(range(5, 0)))', "[5, 4, 3, 2, 1]", "[0, 1, 2, 3, 4]", "Xato"),
    P('print(len(range(10, 20)))', "20", "11", "9"),
    P('print(sum(range(1, 11)))', "11", "45", "10"),
    P('print(9 in range(0, 10, 3))', "False", "3", "Xato"),
    Q("1 dan 10 gacha (10 ham kirsin) sonlar uchun qaysi biri toʻgʻri?", "range(1, 11)", "range(1, 10)", "range(10)", "range(0, 10)"),
    Q("`range(10, 0, -1)` qanday sonlar beradi?", "10 dan 1 gacha", "10 dan 0 gacha", "0 dan 10 gacha", "Hech narsa"),
    PR("Juft sonlar", "Kirishda n. 0 dan n gacha (n kiradi) juft sonlarni `range` qadami bilan bir qatorda chiqaring.", "print(*range(0, int(input()) + 1, 2))", "10", "1", "7"),
    PR("Teskari sanash", "Kirishda n. n dan 1 gacha sonlarni bir qatorda chiqaring.", "print(*range(int(input()), 0, -1))", "5", "1", "10"),
    PR("Progressiya", "Kirishda `a d n`. Birinchi hadi a, ayirmasi d boʻlgan n ta hadni chiqaring.", "a, d, n = map(int, input().split())\nprint(*[a + i * d for i in range(n)])", "3 4 5", "1 1 1", "10 -3 4"),
    PR("Karrali sonlar", "Kirishda `k n`. n dan oshmaydigan k ga karrali musbat sonlarni bir qatorda chiqaring.", "k, n = map(int, input().split())\nprint(*range(k, n + 1, k))", "3 20", "5 5", "7 50"),
    PR("Oraliq yigʻindisi", "Kirishda `a b` (a ≤ b). a dan b gacha (ikkalasi kiradi) sonlar yigʻindisini `sum(range(...))` bilan chiqaring.", "a, b = map(int, input().split())\nprint(sum(range(a, b + 1)))", "1 100", "5 5", "-3 3"),
    PR("Daraja jadvali", "Kirishda n. 0 dan n gacha har bir i uchun `2^i = qiymat` qatorlarini chiqaring.", 'for i in range(int(input()) + 1):\n    print(f"2^{i} = {2 ** i}")', "4", "0", "10"),
    PR("Boʻluvchilar", "Kirishda n. Uning barcha boʻluvchilarini oʻsish tartibida bir qatorda chiqaring.", "n = int(input())\nprint(*[d for d in range(1, n + 1) if n % d == 0])", "12", "1", "17"),
    L("lc", "fizz-buzz"),
    L("cses", 1070),
    L("acmp", 312),
    L("acmp", 47),
])
