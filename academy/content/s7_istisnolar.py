from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(7, "Istisnolar (xatolar)", "Xatolarni tushunish, ushlash va boshqarish", "🛡️")

# ---------------------------------------------------------------- 7.1
TOPIC("istisno-nima", "Istisno nima va xabarni oʻqish", "Traceback, xato turlari va ularning sababi", 20, r'''
Dastur ishlayotganda kutilmagan holat yuz bersa, Python **istisno** (exception) chiqaradi va — agar uni hech kim ushlamasa — dastur toʻxtaydi.

```py xato
narxlar = [4000, 12000]
print(narxlar[5])
```

## Xato xabarini oʻqishni oʻrganing
Xabar (traceback) **pastdan yuqoriga** oʻqiladi:

```py norun
Traceback (most recent call last):
  File "main.py", line 2, in <module>
    print(narxlar[5])
IndexError: list index out of range
```

| Qism | Maʼnosi |
|---|---|
| `line 2` | xato qaysi qatorda |
| `IndexError` | xato **turi** |
| `list index out of range` | qisqa izoh |

> Eng muhim qator — **oxirgisi**. Avval turini va izohini oʻqing, keyin qator raqamiga qarang.

## Sintaksis xatosi va istisno
- **SyntaxError** — kod umuman ishga tushmaydi (qavs yopilmagan, `:` unutilgan).
- **Istisno** — kod ishlab turib, maʼlum qatorda muammoga duch keladi.

## Eng koʻp uchraydigan istisnolar
| Tur | Qachon | Misol |
|---|---|---|
| `ZeroDivisionError` | nolga boʻlish | `5 / 0` |
| `ValueError` | qiymat notoʻgʻri | `int("abc")` |
| `TypeError` | tur mos emas | `"5" + 3` |
| `IndexError` | indeks chegaradan tashqarida | `[1, 2][9]` |
| `KeyError` | lugʻatda kalit yoʻq | `{}["x"]` |
| `NameError` | oʻzgaruvchi aniqlanmagan | `print(yoq)` |
| `AttributeError` | obyektda bunday metod yoʻq | `5.append(1)` |

```py xato
yosh = int("oʻn yetti")
```

```py xato
print("Yosh: " + 17)
```

```py xato
d = {"ism": "Ali"}
print(d["familiya"])
```

## Istisno — bu ham obyekt
Har bir istisno — sinf. Ular oilaga birlashgan: masalan, `ZeroDivisionError` — `ArithmeticError` ning bolasi, hammasi esa `Exception` dan tarqaladi.

```py
print(issubclass(ZeroDivisionError, ArithmeticError))
print(issubclass(KeyError, LookupError))
print(issubclass(ValueError, Exception))
```

## Esda tuting
- Traceback oxirgi qatoridan oʻqiladi: **tur + izoh**.
- Xato — dushman emas, u sizga *nima* va *qayerda* notoʻgʻri ekanini aytadi.
''', [
    P('print(10 / 0)', "0", "inf", "⚠ ValueError"),
    P('print(int("12a"))', "12", "⚠ TypeError", "12a"),
    P('print("5" + 3)', "8", "53", "⚠ ValueError"),
    P('a = [1, 2, 3]\nprint(a[3])', "3", "None", "⚠ KeyError"),
    P('d = {"a": 1}\nprint(d["b"])', "None", "⚠ IndexError", "0"),
    P('print("boshlandi")\nprint(x)', "boshlandi", "⚠ NameError", "boshlandi\nx", lv=2,
      why="Birinchi qator bajariladi, xato faqat ikkinchi qatorda chiqadi."),
    P('print(len(5))', "1", "5", "⚠ ValueError"),
    Q("Traceback'ning qaysi qismini birinchi oʻqish kerak?", "Oxirgi qatorini — xato turi va izohini", "Birinchi qatorini", "Fayl nomini", "Oʻrtasini"),
    Q("`int(\"abc\")` qanday xato beradi?", "ValueError", "TypeError", "SyntaxError", "NameError"),
    F("Xato turi", "`tur(kod)` — berilgan ifoda satrini `eval` qiling. Xato chiqsa, uning **turi nomini** (`\"ZeroDivisionError\"` kabi) qaytaring, aks holda `\"OK\"`.",
      "def tur(kod):\n    try:\n        eval(kod)\n        return 'OK'\n    except Exception as e:\n        return type(e).__name__", 'tur("1 / 0")', 'tur("int(\'x\')")', 'tur("[1][5]")', 'tur("2 + 2")', 'tur("{}[1]")', lv=2),
    F("Xavfsiz indeks", "`ol(a, i)` — `a[i]` ni qaytaring; indeks chegaradan tashqarida boʻlsa `None` (hozircha `if` bilan tekshiring).",
      "def ol(a, i):\n    if -len(a) <= i < len(a):\n        return a[i]\n    return None", "ol([1, 2, 3], 1)", "ol([1, 2, 3], 3)", "ol([], 0)", "ol([5, 6], -1)", lv=1),
    F("Xavfsiz boʻlish", "`bol(a, b)` — `a / b`; b nol boʻlsa `None` (`if` bilan).",
      "def bol(a, b):\n    if b == 0:\n        return None\n    return a / b", "bol(10, 2)", "bol(1, 0)", "bol(0, 5)", lv=1),
    F("Sonmi", "`sonmi(s)` — satr butun son boʻla oladimi? (`\"-12\"` ham son). `isdigit` va `startswith` dan foydalaning.",
      "def sonmi(s):\n    if s.startswith('-'):\n        s = s[1:]\n    return s.isdigit()", 'sonmi("123")', 'sonmi("-7")', 'sonmi("12a")', 'sonmi("")', 'sonmi("-")'),
    F("Kalit bormi", "`qiymat(d, k)` — kalit boʻlsa qiymatini, aks holda `\"yoʻq\"` satrini qaytaring.",
      "def qiymat(d, k):\n    return d[k] if k in d else 'yoʻq'", 'qiymat({"a": 1}, "a")', 'qiymat({"a": 1}, "b")', 'qiymat({}, 0)', lv=1),
    F("Oila", "`arifmetikmi(nom)` — berilgan xato nomi `ArithmeticError` oilasigami? Nomlar: `ZeroDivisionError`, `OverflowError`, `ValueError`, `KeyError`.",
      "def arifmetikmi(nom):\n    import builtins\n    return issubclass(getattr(builtins, nom), ArithmeticError)", 'arifmetikmi("ZeroDivisionError")', 'arifmetikmi("ValueError")', 'arifmetikmi("OverflowError")', 'arifmetikmi("KeyError")', lv=3),
    F("Xatoni tuzating", "Quyidagi funksiya ishlamayapti. Tuzating: `yosh_matn(yosh)` → `\"Yoshingiz: 17\"`.",
      "def yosh_matn(yosh):\n    return 'Yoshingiz: ' + str(yosh)", "yosh_matn(17)", "yosh_matn(0)", "yosh_matn(100)",
      starter="def yosh_matn(yosh):\n    return 'Yoshingiz: ' + yosh\n"),
    L("exercism", "hello-world", note="Xato xabarlari bilan tanishish uchun eng oddiy mashq."),
    L("lc", "string-to-integer-atoi", note="Notoʻgʻri kirishni ehtiyotkorlik bilan qayta ishlash."),
    L("exercism", "isbn-verifier"),
    L("acmp", 1),
])

# ---------------------------------------------------------------- 7.2
TOPIC("try-except", "try / except", "Xatoni ushlash va dasturni toʻxtatmaslik", 20, r'''
`try` blokida xavfli kod yoziladi. Agar u yerda xato chiqsa, Python **toʻxtamaydi** — `except` blokiga oʻtadi.

```py
try:
    natija = 10 / 0
    print("Bu qator bajarilmaydi")
except ZeroDivisionError:
    print("Nolga boʻlib boʻlmaydi!")
print("Dastur davom etmoqda")
```

## Foydalanuvchi kiritgan maʼlumot
Eng koʻp ishlatiladigan holat — `input()` ni songa aylantirish:

```py input=oʻn yetti
matn = input("Yoshingiz: ")
try:
    yosh = int(matn)
    print("Keyingi yil:", yosh + 1)
except ValueError:
    print("Iltimos, raqam kiriting!")
```

## Toʻgʻri qiymat kiritilmaguncha soʻrash
```py input=abc|-5|17
while True:
    try:
        yosh = int(input())
        if yosh <= 0:
            print("Musbat son kiriting")
            continue
        break
    except ValueError:
        print("Bu son emas, qayta kiriting")
print("Qabul qilindi:", yosh)
```

## Xato haqida maʼlumot olish: as e
```py
try:
    int("salom")
except ValueError as e:
    print("Xato matni:", e)
    print("Turi:", type(e).__name__)
```

## Xato qayerda boʻlsa ham ushlanadi
`try` ichida chaqirilgan funksiyaning ichidagi xato ham ushlanadi:

```py
def oʻrtacha(a):
    return sum(a) / len(a)

try:
    print(oʻrtacha([]))
except ZeroDivisionError:
    print("Roʻyxat boʻsh")
```

!> `try` blokini kichik qiling — faqat xato chiqishi mumkin boʻlgan qatorlarni oʻrang. Katta blok haqiqiy xatolarni yashirib qoʻyadi.

## Esda tuting
- `try` — urinib koʻr; `except Tur` — shu xato chiqsa, bu yerga oʻt.
- `except ... as e` — xato obyektini olish.
''', [
    P('try:\n    print(1 / 0)\nexcept ZeroDivisionError:\n    print("X")', "⚠ ZeroDivisionError", "inf\nX", "0\nX"),
    P('try:\n    print("A")\n    int("q")\n    print("B")\nexcept ValueError:\n    print("C")', "A\nB\nC", "C", "A\nB"),
    P('try:\n    x = int("5")\nexcept ValueError:\n    x = 0\nprint(x * 2)', "0", "10\n0", "55"),
    P('try:\n    x = int("5a")\nexcept ValueError:\n    x = -1\nprint(x)', "5", "⚠ ValueError", "0"),
    P('try:\n    [1, 2][7]\nexcept ValueError:\n    print("ushlandi")', "ushlandi", "None", "[1, 2]", lv=2,
      why="`except ValueError` faqat ValueError ni ushlaydi; IndexError ushlanmay qoladi."),
    P('def f():\n    return 1 / 0\ntry:\n    f()\nexcept ZeroDivisionError:\n    print("ichkarida")', "⚠ ZeroDivisionError", "None", "1"),
    P('try:\n    int("abc")\nexcept ValueError as e:\n    print(type(e).__name__)', "abc", "e", "Xato"),
    Q("`try` blokida xato chiqsa nima boʻladi?", "Mos `except` blokiga oʻtiladi", "Dastur darhol toʻxtaydi", "Xato eʼtiborsiz qoldiriladi va keyingi qatordan davom etadi", "try qaytadan boshlanadi"),
    Q("Nega `try` blokini kichik qilish kerak?", "Kutilmagan joydagi haqiqiy xatolarni yashirib qoʻymaslik uchun", "Katta try ishlamaydi", "Python 10 qatordan koʻp ruxsat bermaydi", "Tezroq ishlashi uchun"),
    F("Xavfsiz int", "`butun(s)` — satrni `int` ga aylantiring; boʻlmasa `0` qaytaring (`try` bilan).",
      "def butun(s):\n    try:\n        return int(s)\n    except ValueError:\n        return 0", 'butun("42")', 'butun("4x")', 'butun("-7")', 'butun("")', lv=1),
    F("Xavfsiz boʻlish", "`bol(a, b)` — `a / b`; nolga boʻlishda `None` (`try` bilan).",
      "def bol(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None", "bol(9, 3)", "bol(1, 0)", "bol(-4, 8)", lv=1),
    F("Sonlarni yigʻ", "`yigindi(sozlar)` — roʻyxatdagi son boʻla oladigan satrlar yigʻindisi; qolganlarini oʻtkazib yuboring.",
      "def yigindi(sozlar):\n    s = 0\n    for x in sozlar:\n        try:\n            s += int(x)\n        except ValueError:\n            pass\n    return s", 'yigindi(["1", "a", "5", "2.5", "-3"])', "yigindi([])", 'yigindi(["x", "y"])'),
    F("Kalit yoki standart", "`ol(d, k, std)` — `d[k]`; KeyError boʻlsa std (`get` ishlatmasdan, `try` bilan).",
      "def ol(d, k, std):\n    try:\n        return d[k]\n    except KeyError:\n        return std", 'ol({"a": 1}, "a", 0)', 'ol({}, "a", 0)', 'ol({1: "bir"}, 2, "?")'),
    F("Xato matni", "`xabar(s)` — `int(s)` ni sinab koʻring. Muvaffaqiyatli boʻlsa `\"OK\"`, aks holda xato matnini (`str(e)`) qaytaring.",
      "def xabar(s):\n    try:\n        int(s)\n        return 'OK'\n    except ValueError as e:\n        return str(e)", 'xabar("12")', 'xabar("ab")', 'xabar("")'),
    F("Oʻrtacha", "`ortacha(a)` — oʻrtacha qiymat; roʻyxat boʻsh boʻlsa `0` (`try` bilan).",
      "def ortacha(a):\n    try:\n        return sum(a) / len(a)\n    except ZeroDivisionError:\n        return 0", "ortacha([2, 4])", "ortacha([])", "ortacha([7])"),
    F("Toʻgʻri kirishlar", "`togrilar(sozlar)` — son boʻla oladigan satrlarni `int` ga aylantirib roʻyxat qaytaring.",
      "def togrilar(sozlar):\n    natija = []\n    for x in sozlar:\n        try:\n            natija.append(int(x))\n        except ValueError:\n            continue\n    return natija", 'togrilar(["3", "uch", "03", " 4 "])', "togrilar([])", 'togrilar(["1e3"])'),
    L("exercism", "wordy", note="Notoʻgʻri savollarda `ValueError` ni qayta ishlash."),
    L("exercism", "phone-number"),
    L("lc", "valid-number", note="Qiyinroq: `float()` va `try` bilan qisqa yechim bor."),
    L("acmp", 109, note="A / B — nolga boʻlishni unutmang."),
])

# ---------------------------------------------------------------- 7.3
TOPIC("turli-istisnolar", "Turli istisnolarni ushlash", "Bir nechta except, else va tartib", 20, r'''
Bitta kod har xil xato berishi mumkin. Har biriga **alohida** javob qaytarish mumkin.

```py
def hisobla(a, b):
    try:
        return int(a) / int(b)
    except ValueError:
        return "Son kiriting"
    except ZeroDivisionError:
        return "Nolga boʻlib boʻlmaydi"

print(hisobla("10", "2"))
print(hisobla("10", "x"))
print(hisobla("10", "0"))
```

## Bir nechtasini birga ushlash
```py
for kirish in ["5", "abc", None]:
    try:
        print(int(kirish) * 2)
    except (ValueError, TypeError) as e:
        print("Notoʻgʻri:", type(e).__name__)
```

## else — xato boʻlmasa
`else` bloki faqat `try` **muvaffaqiyatli** tugaganda bajariladi:

```py
for s in ["8", "sakkiz"]:
    try:
        n = int(s)
    except ValueError:
        print(s, "→ son emas")
    else:
        print(s, "→ kvadrati", n * n)
```

> `else` ga xavfsiz kodni qoʻying — shunda `try` faqat haqiqatan xavfli qatorni oʻraydi.

## Tartib muhim!
Python `except` larni **yuqoridan pastga** tekshiradi va birinchi mosini tanlaydi. Shuning uchun aniq turlar — yuqorida, umumiylari — pastda:

```py
try:
    1 / 0
except ArithmeticError:
    print("ArithmeticError ushladi")
except ZeroDivisionError:
    print("Bu hech qachon bajarilmaydi")
```

## except Exception — oxirgi chora
```py
def xavfsiz(f, *args):
    try:
        return f(*args)
    except Exception as e:
        return f"{type(e).__name__}: {e}"

print(xavfsiz(int, "12"))
print(xavfsiz(int, "1.5"))
print(xavfsiz(max, []))
```

!> Boʻsh `except:` (turi koʻrsatilmagan) yozmang! U hatto Ctrl+C ni ham ushlaydi va xatolarni butunlay yashiradi. Kamida `except Exception` yozing.

## Esda tuting
- Bir nechta `except` — har xil xatoga har xil javob.
- `except (A, B)` — bir xil javob.
- `else` — xato boʻlmasa; aniq turlar doim yuqorida.
''', [
    P('try:\n    int("x")\nexcept ZeroDivisionError:\n    print("Z")\nexcept ValueError:\n    print("V")', "Z", "Z\nV", "⚠ ValueError"),
    P('try:\n    x = 5\nexcept ValueError:\n    print("xato")\nelse:\n    print("yaxshi")', "xato", "xato\nyaxshi", "5"),
    P('try:\n    1 / 0\nexcept ArithmeticError:\n    print("A")\nexcept ZeroDivisionError:\n    print("Z")', "Z", "A\nZ", "⚠ ZeroDivisionError", lv=2),
    P('try:\n    None + 1\nexcept (ValueError, TypeError):\n    print("ushlandi")', "1", "None", "⚠ TypeError"),
    P('try:\n    int("q")\nexcept ValueError:\n    print("V")\nelse:\n    print("E")', "E", "V\nE", "q"),
    P('for s in ["1", "a", "2"]:\n    try:\n        print(int(s))\n    except ValueError:\n        print("-")', "1\n2", "1\n-", "-\n-\n-"),
    P('try:\n    {}["k"]\nexcept LookupError:\n    print("L")', "⚠ KeyError", "k", "None", lv=2,
      why="`KeyError` — `LookupError` ning bolasi, shuning uchun ushlanadi."),
    Q("`else` bloki qachon bajariladi?", "try blokida xato chiqmaganda", "Har doim", "Xato chiqqanda", "except bajarilgandan keyin"),
    Q("Nega boʻsh `except:` yozish yomon?", "U barcha xatolarni, hatto Ctrl+C ni ham yashiradi", "U ishlamaydi", "U faqat SyntaxError ni ushlaydi", "U sekin"),
    F("Kalkulyator", "`hisobla(a, b)` — `int(a) / int(b)`. ValueError → `\"son emas\"`, ZeroDivisionError → `\"nol\"`.",
      "def hisobla(a, b):\n    try:\n        return int(a) / int(b)\n    except ValueError:\n        return 'son emas'\n    except ZeroDivisionError:\n        return 'nol'", 'hisobla("8", "2")', 'hisobla("8", "x")', 'hisobla("8", "0")', 'hisobla("y", "0")'),
    F("Element", "`element(a, i)` — `a[int(i)]`. Xato turi nomini qaytaring (`\"ValueError\"`, `\"IndexError\"`) yoki elementni.",
      "def element(a, i):\n    try:\n        return a[int(i)]\n    except (ValueError, IndexError) as e:\n        return type(e).__name__", 'element([10, 20], "1")', 'element([10, 20], "5")', 'element([10, 20], "bir")', 'element([], "0")'),
    F("Holat", "`holat(s)` — `int(s)` muvaffaqiyatli boʻlsa (`else` blokida) `\"juft\"`/`\"toq\"`, aks holda `\"xato\"`.",
      "def holat(s):\n    try:\n        n = int(s)\n    except ValueError:\n        return 'xato'\n    else:\n        return 'juft' if n % 2 == 0 else 'toq'", 'holat("4")', 'holat("7")', 'holat("x")', 'holat("-2")'),
    F("Xavfsiz chaqirish", "`xavfsiz(f, x)` — `f(x)` natijasini qaytaring; har qanday `Exception` boʻlsa — xato turi nomini.",
      "def xavfsiz(f, x):\n    try:\n        return f(x)\n    except Exception as e:\n        return type(e).__name__", "xavfsiz(int, '5')", "xavfsiz(int, 'a')", "xavfsiz(len, 5)", "xavfsiz(max, [])"),
    F("Hisobot", "`hisobot(sozlar)` — `{\"ok\": son_boʻla_olganlar_soni, \"xato\": qolganlar_soni}`.",
      "def hisobot(sozlar):\n    r = {'ok': 0, 'xato': 0}\n    for s in sozlar:\n        try:\n            int(s)\n        except (ValueError, TypeError):\n            r['xato'] += 1\n        else:\n            r['ok'] += 1\n    return r", 'hisobot(["1", "a", "2", None])', "hisobot([])", 'hisobot(["0"])'),
    F("Kalit yoki indeks", "`chuqur(d, kalit, i)` — `d[kalit][i]`; KeyError → `\"kalit yoʻq\"`, IndexError → `\"indeks yoʻq\"`.",
      "def chuqur(d, kalit, i):\n    try:\n        return d[kalit][i]\n    except KeyError:\n        return 'kalit yoʻq'\n    except IndexError:\n        return 'indeks yoʻq'", 'chuqur({"a": [1, 2]}, "a", 1)', 'chuqur({"a": [1, 2]}, "b", 0)', 'chuqur({"a": [1, 2]}, "a", 9)'),
    F("Turga qarab", "`aylantir(x)` — avval `int(x)`, boʻlmasa `float(x)`, u ham boʻlmasa satrni oʻzini qaytaring.",
      "def aylantir(x):\n    try:\n        return int(x)\n    except ValueError:\n        try:\n            return float(x)\n        except ValueError:\n            return x", 'aylantir("12")', 'aylantir("1.5")', 'aylantir("salom")', 'aylantir("-0")', lv=3),
    L("exercism", "ledger"),
    L("exercism", "all-your-base", note="Turli notoʻgʻri kirishlarda har xil ValueError xabarlari."),
    L("exercism", "rest-api"),
    L("lc", "evaluate-reverse-polish-notation"),
])

# ---------------------------------------------------------------- 7.4
TOPIC("finally", "finally — har doim bajariladigan blok", "Resurslarni tozalash va yakunlash", 15, r'''
`finally` bloki **har qanday holatda** bajariladi: xato boʻlsa ham, boʻlmasa ham, hatto `return` boʻlsa ham.

```py
for s in ["10", "oʻn"]:
    try:
        print("Natija:", int(s) * 2)
    except ValueError:
        print("Xato!")
    finally:
        print("— tekshiruv tugadi")
```

## Toʻliq tuzilma
```py norun
try:
    # xavfli kod
except XatoTuri:
    # xato boʻlsa
else:
    # xato boʻlmasa
finally:
    # har doim
```

## Qachon kerak?
Biror resursni **albatta** yopish yoki tozalash kerak boʻlganda: fayl, internet ulanishi, maʼlumotlar bazasi, qulf (lock), vaqtinchalik holat.

```py
holat = {"ulangan": False}

def ishla(buyruq):
    holat["ulangan"] = True
    print("Ulanish ochildi")
    try:
        if buyruq == "xato":
            raise ValueError("notoʻgʻri buyruq")
        print("Bajarildi:", buyruq)
    finally:
        holat["ulangan"] = False
        print("Ulanish yopildi")

ishla("salom")
try:
    ishla("xato")
except ValueError as e:
    print("Tashqarida ushlandi:", e)
print(holat)
```

> E'tibor bering: `finally` xatoni **ushlamaydi** — u faqat tozalab, xatoni yuqoriga oʻtkazib yuboradi.

## return va finally
```py
def f():
    try:
        return "try dan"
    finally:
        print("finally baribir ishladi")

print(f())
```

!> `finally` ichida `return` yozmang — u try dagi `return` ni ham, xatoni ham "yutib yuboradi".

## Vaqtni oʻlchash namunasi
```py
import time

boshlanish = time.perf_counter()
try:
    s = sum(range(100000))
finally:
    sarflandi = time.perf_counter() - boshlanish
    print("Hisoblandi:", sarflandi < 5)
```

## Esda tuting
- `finally` — doim bajariladi.
- Tozalash ishlari uchun; xatoni ushlash uchun emas.
''', [
    P('try:\n    print("A")\nfinally:\n    print("F")', "A", "F\nA", "F"),
    P('try:\n    int("x")\nexcept ValueError:\n    print("E")\nfinally:\n    print("F")', "E", "F", "F\nE"),
    P('def f():\n    try:\n        return 1\n    finally:\n        print("F")\nprint(f())', "1", "1\nF", "F"),
    P('try:\n    x = 1\nexcept ValueError:\n    print("E")\nelse:\n    print("L")\nfinally:\n    print("F")', "E\nF", "F\nL", "L"),
    P('try:\n    print(1 / 0)\nfinally:\n    print("F")', "F", "inf\nF", "⚠ ZeroDivisionError", lv=2,
      why="`finally` bajariladi, lekin xatoni ushlamaydi — xato davom etadi."),
    P('n = 0\nfor i in range(3):\n    try:\n        if i == 1:\n            continue\n    finally:\n        n += 1\nprint(n)', "2", "1", "0", lv=3),
    P('def f():\n    try:\n        return "T"\n    finally:\n        return "F"\nprint(f())', "T", "T\nF", "⚠ SyntaxError", lv=3),
    Q("`finally` bloki qachon bajariladi?", "Har doim — xato boʻlsa ham, boʻlmasa ham", "Faqat xato chiqqanda", "Faqat xato chiqmaganda", "Faqat return boʻlmasa"),
    Q("`finally` xatoni ushlaydimi?", "Yoʻq, faqat tozalaydi va xato yuqoriga oʻtadi", "Ha, barcha xatolarni", "Faqat ValueError ni", "Faqat oxirgi xatoni"),
    F("Jurnal", "`jurnal(s)` — roʻyxatga yozib boring: `\"start\"`, keyin `int(s)` muvaffaqiyatli boʻlsa `\"ok\"`, xato boʻlsa `\"xato\"`, va **har doim** `\"end\"`. Roʻyxatni qaytaring.",
      "def jurnal(s):\n    log = ['start']\n    try:\n        int(s)\n        log.append('ok')\n    except ValueError:\n        log.append('xato')\n    finally:\n        log.append('end')\n    return log", 'jurnal("5")', 'jurnal("x")', 'jurnal("-1")', lv=1),
    F("Urinishlar", "`urinishlar(sozlar)` — har bir satr uchun `int` ga aylantirishni sinang; jami **urinishlar** sonini `finally` da sanang. `(urinishlar, muvaffaqiyatlar)` qaytaring.",
      "def urinishlar(sozlar):\n    u = m = 0\n    for s in sozlar:\n        try:\n            int(s)\n            m += 1\n        except ValueError:\n            pass\n        finally:\n            u += 1\n    return (u, m)", 'urinishlar(["1", "a", "2"])', "urinishlar([])", 'urinishlar(["x"])'),
    F("Holatni tiklash", "`vaqtincha(holat, qiymat)` — `holat[\"rejim\"]` ni vaqtincha `qiymat` ga oʻzgartiring, `holat[\"rejim\"] * 2` ni hisoblang va **finally** da eski qiymatni tiklang. `(natija, holat)` qaytaring.",
      "def vaqtincha(holat, qiymat):\n    eski = holat['rejim']\n    holat['rejim'] = qiymat\n    try:\n        natija = holat['rejim'] * 2\n    finally:\n        holat['rejim'] = eski\n    return (natija, holat)", 'vaqtincha({"rejim": 1}, 5)', 'vaqtincha({"rejim": "a"}, "b")', 'vaqtincha({"rejim": 0}, 0)'),
    F("Yigʻ va yop", "`yigish(a)` — `a` dagi sonlarni yigʻing, lekin birinchi son boʻlmagan elementda toʻxtang. `(yigʻindi, \"yopildi\")` qaytaring — ikkinchi qism `finally` da qoʻyilsin.",
      "def yigish(a):\n    s = 0\n    holat = ''\n    try:\n        for x in a:\n            s += int(x)\n    except ValueError:\n        pass\n    finally:\n        holat = 'yopildi'\n    return (s, holat)", 'yigish(["1", "2", "x", "5"])', "yigish([])", 'yigish(["10"])'),
    F("Tartib", "`tartib(s)` — `try/except/else/finally` qaysi bloklar bajarilganini roʻyxatda qaytaring (s ni `int` ga aylantirish).",
      "def tartib(s):\n    r = []\n    try:\n        r.append('try')\n        int(s)\n    except ValueError:\n        r.append('except')\n    else:\n        r.append('else')\n    finally:\n        r.append('finally')\n    return r", 'tartib("1")', 'tartib("bir")', 'tartib("")'),
    F("Hisoblagich", "`sanash(amallar)` — har bir amal `(a, b)` uchun `a // b` hisoblang. ZeroDivisionError larni oʻtkazib yuboring. `{\"natijalar\": [...], \"jami\": urinishlar}` qaytaring.",
      "def sanash(amallar):\n    nat = []\n    jami = 0\n    for a, b in amallar:\n        try:\n            nat.append(a // b)\n        except ZeroDivisionError:\n            pass\n        finally:\n            jami += 1\n    return {'natijalar': nat, 'jami': jami}", "sanash([(7, 2), (1, 0), (9, 3)])", "sanash([])", "sanash([(5, 0)])"),
    F("Xavfsiz roʻyxat", "`qayta_ishlash(a)` — `a` ning har bir elementini 100 ga boʻling; xato boʻlsa `None` qoʻying. Natijani qaytaring.",
      "def qayta_ishlash(a):\n    r = []\n    for x in a:\n        try:\n            r.append(100 / x)\n        except (ZeroDivisionError, TypeError):\n            r.append(None)\n    return r", "qayta_ishlash([4, 0, 50])", "qayta_ishlash([])", 'qayta_ishlash(["x", 1])'),
    L("exercism", "paasio", note="Kontekst va resurslarni toʻgʻri yopish boʻyicha murakkab mashq."),
    L("exercism", "bank-account", note="Hisob yopilganda xatolarni boshqarish."),
    L("exercism", "circular-buffer"),
    L("acmp", 143),
])

# ---------------------------------------------------------------- 7.5
TOPIC("with", "with — kontekst menejeri", "Fayllar va avtomatik yopish", 20, r'''
`with` — `try/finally` ning qisqa va xavfsiz shakli. U resursni ochadi va blok tugashi bilan — xato boʻlsa ham — **avtomatik yopadi**.

## Fayl bilan ishlash
```py norun
with open("eslatma.txt", "w", encoding="utf-8") as f:
    f.write("Salom, Mirae Academy!\n")
    f.write("Bugun: istisnolar\n")
# bu yerda fayl allaqachon yopilgan

with open("eslatma.txt", encoding="utf-8") as f:
    for qator in f:
        print(qator.strip())
```

Bu aynan shuning qisqasi:

```py norun
f = open("eslatma.txt", encoding="utf-8")
try:
    matn = f.read()
finally:
    f.close()
```

| Rejim | Maʼnosi |
|---|---|
| `"r"` | oʻqish (standart) |
| `"w"` | yozish (eskisini oʻchiradi!) |
| `"a"` | oxiriga qoʻshish |

!> Oʻzbekcha harflar uchun doim `encoding="utf-8"` yozing — aks holda Windows'da `oʻ`, `gʻ` buzilishi mumkin.

## Fayl yoʻq boʻlsa
```py
try:
    with open("yoq_fayl.txt", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("Fayl topilmadi")
```

## Xotiradagi "fayl": StringIO
```py
import io

with io.StringIO("olma\nnok\nuzum\n") as f:
    for i, qator in enumerate(f, 1):
        print(i, qator.strip())
```

## Oʻz kontekst menejeringiz
`__enter__` va `__exit__` metodli har qanday obyekt `with` bilan ishlaydi:

```py
class Taymer:
    def __enter__(self):
        print("⏱ boshlandi")
        return self
    def __exit__(self, tur, qiymat, iz):
        print("⏱ tugadi")
        return False   # xatoni yutmaymiz

with Taymer():
    print("ish bajarilmoqda...")
```

Qisqaroq usul — `contextlib`:

```py
from contextlib import contextmanager

@contextmanager
def boʻlim(nom):
    print(f"[{nom}] ochildi")
    try:
        yield
    finally:
        print(f"[{nom}] yopildi")

with boʻlim("hisob"):
    print(2 + 2)
```

## Esda tuting
- Fayllarni doim `with open(...)` bilan oching.
- `with` blokidan xato bilan chiqilsa ham, resurs yopiladi.
''', [
    P('import io\nwith io.StringIO("a\\nb") as f:\n    print(len(f.readlines()))', "1", "3", "a\nb"),
    P('import io\nwith io.StringIO("salom") as f:\n    print(f.read().upper())', "salom", "S", "⚠ ValueError"),
    P('import io\nf = io.StringIO("x")\nwith f:\n    pass\nprint(f.closed)', "False", "None", "x"),
    P('class T:\n    def __enter__(self):\n        print("E")\n    def __exit__(self, *a):\n        print("X")\nwith T():\n    print("B")', "B", "E\nX\nB", "B\nE\nX"),
    P('class T:\n    def __enter__(self):\n        return 42\n    def __exit__(self, *a):\n        return False\nwith T() as t:\n    print(t)', "T", "None", "True"),
    P('class T:\n    def __enter__(self):\n        return self\n    def __exit__(self, *a):\n        print("yopildi")\n        return False\ntry:\n    with T():\n        1 / 0\nexcept ZeroDivisionError:\n    print("ushlandi")', "ushlandi", "ushlandi\nyopildi", "yopildi", lv=3),
    P('try:\n    open("bunday_fayl_yoq_123.txt")\nexcept FileNotFoundError:\n    print("yoʻq")', "⚠ FileNotFoundError", "None", "bunday_fayl_yoq_123.txt"),
    Q("`with open(...) as f:` ning asosiy afzalligi?", "Fayl blok tugagach (xato boʻlsa ham) avtomatik yopiladi", "Fayl tezroq oʻqiladi", "Fayl shifrlanadi", "Fayl hech qachon yopilmaydi"),
    Q("`open(\"f.txt\", \"w\")` mavjud faylga nima qiladi?", "Eski mazmunni oʻchirib, yangidan yozadi", "Oxiriga qoʻshadi", "Xato beradi", "Faqat oʻqish uchun ochadi"),
    F("Qatorlar soni", "`qatorlar(matn)` — `io.StringIO(matn)` ni `with` bilan oching va qatorlar sonini qaytaring.",
      "def qatorlar(matn):\n    import io\n    with io.StringIO(matn) as f:\n        return len(f.readlines())", 'qatorlar("a\\nb\\nc")', 'qatorlar("")', 'qatorlar("bir qator")', lv=1),
    F("Soʻzlar", "`sozlar_soni(matn)` — `StringIO` dan qatorma-qator oʻqib, jami soʻzlar sonini toping.",
      "def sozlar_soni(matn):\n    import io\n    n = 0\n    with io.StringIO(matn) as f:\n        for q in f:\n            n += len(q.split())\n    return n", 'sozlar_soni("salom dunyo\\nmirae academy python")', 'sozlar_soni("")', 'sozlar_soni("\\n\\n a \\n")'),
    F("CSV oʻqish", "`ballar(csv)` — `\"ism,ball\"` qatorlaridan `{ism: ball}` lugʻatini yasang (ball — int).",
      "def ballar(csv):\n    import io\n    d = {}\n    with io.StringIO(csv) as f:\n        for q in f:\n            q = q.strip()\n            if q:\n                ism, b = q.split(',')\n                d[ism] = int(b)\n    return d", 'ballar("Ali,90\\nVali,75\\n")', 'ballar("")', 'ballar("A,1")'),
    F("Yozib oʻqish", "`yoz_oqi(qatorlar)` — `StringIO` ga har bir satrni yangi qator bilan yozing va `getvalue()` ni qaytaring.",
      "def yoz_oqi(qatorlar):\n    import io\n    with io.StringIO() as f:\n        for q in qatorlar:\n            f.write(q + '\\n')\n        return f.getvalue()", 'yoz_oqi(["a", "b"])', "yoz_oqi([])", 'yoz_oqi(["salom"])'),
    F("Kontekst jurnali", "`jurnal()` — `__enter__` da `\"kirdi\"`, `__exit__` da `\"chiqdi\"` ni roʻyxatga yozadigan sinf yarating; ichida `\"ish\"` yozing. Roʻyxatni qaytaring.",
      "def jurnal():\n    log = []\n    class K:\n        def __enter__(self):\n            log.append('kirdi')\n        def __exit__(self, *a):\n            log.append('chiqdi')\n            return False\n    with K():\n        log.append('ish')\n    return log", "jurnal()", "len(jurnal())", "jurnal()[-1]", lv=3),
    F("Fayl bormi", "`fayl_bor(nom)` — faylni ochishga urinib koʻring: ochilsa `True`, `FileNotFoundError` boʻlsa `False`.",
      "def fayl_bor(nom):\n    try:\n        with open(nom):\n            return True\n    except FileNotFoundError:\n        return False", 'fayl_bor("yoq_fayl_mirae_1.txt")', 'fayl_bor("yoq/papka/fayl.txt")', 'fayl_bor("yana_yoq.csv")', lv=1),
    F("Eng uzun qator", "`eng_uzun(matn)` — `StringIO` orqali oʻqib, eng uzun qatorni (yangi qator belgisisiz) qaytaring.",
      "def eng_uzun(matn):\n    import io\n    with io.StringIO(matn) as f:\n        return max((q.rstrip('\\n') for q in f), key=len, default='')", 'eng_uzun("ab\\nabcd\\nabc")', 'eng_uzun("")', 'eng_uzun("bir")'),
    L("exercism", "grep", note="Fayllar bilan ishlash boʻyicha amaliy mashq."),
    L("exercism", "tournament"),
    L("exercism", "kindergarten-garden"),
    L("acmp", 2),
])

# ---------------------------------------------------------------- 7.6
TOPIC("raise", "raise va oʻz istisnolaringiz", "Xatoni oʻzingiz chiqarish, assert", 20, r'''
Baʼzan xatoni **oʻzimiz** chiqarishimiz kerak: notoʻgʻri maʼlumot kelsa, jimgina notoʻgʻri natija qaytarishdan koʻra aniq xato bergan yaxshi.

```py
def yosh_belgila(yosh):
    if yosh < 0:
        raise ValueError("Yosh manfiy boʻlishi mumkin emas")
    return yosh

print(yosh_belgila(17))
try:
    yosh_belgila(-3)
except ValueError as e:
    print("Xato:", e)
```

## Qaysi turni tanlash?
| Holat | Tur |
|---|---|
| Qiymat notoʻgʻri (manfiy yosh) | `ValueError` |
| Tur notoʻgʻri (son oʻrniga roʻyxat) | `TypeError` |
| Kalit topilmadi | `KeyError` |
| Hali yozilmagan | `NotImplementedError` |

## Oʻz istisno sinfingiz
Katta dasturlarda oʻz xato turlaringiz kerak boʻladi:

```py
class MablagʻYetarliEmas(Exception):
    pass

def yechish(balans, summa):
    if summa > balans:
        raise MablagʻYetarliEmas(f"Balans {balans}, soʻralgan {summa}")
    return balans - summa

try:
    print(yechish(100000, 30000))
    print(yechish(100000, 250000))
except MablagʻYetarliEmas as e:
    print("Rad etildi:", e)
```

## Qayta chiqarish
Xatoni ushlab, qayd etib, yana yuqoriga yuborish:

```py
def oʻqi(s):
    try:
        return int(s)
    except ValueError:
        print("log: notoʻgʻri kirish", repr(s))
        raise

try:
    oʻqi("abc")
except ValueError:
    print("Yuqorida ham ushlandi")
```

## Xatoni boshqasiga aylantirish: from
```py
class SozlamaXatosi(Exception):
    pass

def port_ol(sozlama):
    try:
        return int(sozlama["port"])
    except (KeyError, ValueError) as e:
        raise SozlamaXatosi("port notoʻgʻri") from e

try:
    port_ol({"host": "localhost"})
except SozlamaXatosi as e:
    print(e, "| sabab:", type(e.__cause__).__name__)
```

## assert — "bu doim toʻgʻri boʻlishi kerak"
```py
def ortacha(a):
    assert len(a) > 0, "roʻyxat boʻsh"
    return sum(a) / len(a)

print(ortacha([4, 6]))
try:
    ortacha([])
except AssertionError as e:
    print("AssertionError:", e)
```

!> `assert` — dasturchi uchun tekshiruv (debug). Foydalanuvchi kiritgan maʼlumotni tekshirish uchun `if` + `raise` ishlating: `python -O` rejimida `assert` lar oʻchiriladi.

## Esda tuting
- `raise TurXato("izoh")` — xato chiqarish.
- `class MeningXatom(Exception): pass` — oʻz turingiz.
- Ushlab qayta yuborish: yalangʻoch `raise`.
''', [
    P('try:\n    raise ValueError("yomon")\nexcept ValueError as e:\n    print(e)', "ValueError", "ValueError: yomon", "⚠ ValueError"),
    P('def f(x):\n    if x < 0:\n        raise ValueError\n    return x\nprint(f(5))', "⚠ ValueError", "-5", "None"),
    P('class MenXato(Exception):\n    pass\ntry:\n    raise MenXato("!")\nexcept Exception:\n    print("ushlandi")', "!", "⚠ MenXato", "MenXato"),
    P('try:\n    try:\n        int("a")\n    except ValueError:\n        print("ichki")\n        raise\nexcept ValueError:\n    print("tashqi")', "ichki", "tashqi", "tashqi\nichki", lv=2),
    P('assert 2 + 2 == 4\nprint("OK")', "⚠ AssertionError", "True\nOK", "4"),
    P('assert 1 > 2, "notoʻgʻri"\nprint("OK")', "OK", "notoʻgʻri", "False"),
    P('class A(Exception):\n    pass\nclass B(A):\n    pass\ntry:\n    raise B()\nexcept A:\n    print("A")\nexcept B:\n    print("B")', "B", "A\nB", "⚠ B", lv=3,
      why="B — A ning bolasi; birinchi mos kelgan `except A` tanlanadi."),
    Q("Manfiy yosh kiritilganda qaysi xatoni chiqarish toʻgʻri?", "ValueError", "TypeError", "KeyError", "SyntaxError"),
    Q("Oʻz istisno sinfingizni qanday yaratasiz?", "class MeningXatom(Exception): pass", "def MeningXatom(): raise", "Exception = MeningXatom", "new Exception(\"MeningXatom\")"),
    F("Yosh tekshiruvi", "`yosh(n)` — n manfiy yoki 150 dan katta boʻlsa `ValueError` chiqaring, aks holda n ni qaytaring.",
      "def yosh(n):\n    if n < 0 or n > 150:\n        raise ValueError('yosh notoʻgʻri')\n    return n", "yosh(17)", "yosh(-1)", "yosh(151)", "yosh(0)", lv=1),
    F("Turi tekshiruvi", "`kvadrat(x)` — x `int` yoki `float` boʻlmasa `TypeError` chiqaring; aks holda `x * x`.",
      "def kvadrat(x):\n    if type(x) not in (int, float):\n        raise TypeError('son kerak')\n    return x * x", "kvadrat(3)", 'kvadrat("3")', "kvadrat(1.5)", "kvadrat([2])", lv=1),
    F("Bank", "`yechish(balans, summa)` — summa ≤ 0 boʻlsa `ValueError`, balansdan katta boʻlsa `RuntimeError` chiqaring; aks holda yangi balans.",
      "def yechish(balans, summa):\n    if summa <= 0:\n        raise ValueError('summa musbat boʻlsin')\n    if summa > balans:\n        raise RuntimeError('mablagʻ yetarli emas')\n    return balans - summa", "yechish(100, 30)", "yechish(100, 0)", "yechish(100, 101)", "yechish(50, 50)"),
    F("Parol", "`parol(p)` — 8 belgidan qisqa boʻlsa yoki raqam boʻlmasa `ValueError`; aks holda `\"qabul\"`.",
      "def parol(p):\n    if len(p) < 8 or not any(h.isdigit() for h in p):\n        raise ValueError('parol kuchsiz')\n    return 'qabul'", 'parol("mirae2026")', 'parol("qisqa1")', 'parol("raqamsizparol")', 'parol("12345678")'),
    F("Oʻz xatoyim", "`tekshir(n)` — `class ToqSon(Exception)` yarating; n toq boʻlsa uni chiqaring, juft boʻlsa `n // 2` qaytaring. Funksiya `(natija yoki \"ToqSon\")` qaytarsin — ichida ushlang.",
      "def tekshir(n):\n    class ToqSon(Exception):\n        pass\n    try:\n        if n % 2:\n            raise ToqSon()\n        return n // 2\n    except ToqSon as e:\n        return type(e).__name__", "tekshir(10)", "tekshir(7)", "tekshir(0)"),
    F("Uchburchak", "`uchburchak(a, b, c)` — tomonlar musbat va uchburchak tengsizligi bajarilsa perimetrni qaytaring, aks holda `ValueError`.",
      "def uchburchak(a, b, c):\n    if min(a, b, c) <= 0 or a + b <= c or a + c <= b or b + c <= a:\n        raise ValueError('uchburchak emas')\n    return a + b + c", "uchburchak(3, 4, 5)", "uchburchak(1, 2, 3)", "uchburchak(0, 1, 1)", "uchburchak(2, 2, 3)"),
    F("Aylantirish", "`port(s)` — satrni `int` ga aylantiring; boʻlmasa yoki 1..65535 oraligʻida boʻlmasa `ValueError(\"port notoʻgʻri\")` chiqaring.",
      "def port(s):\n    try:\n        n = int(s)\n    except ValueError:\n        raise ValueError('port notoʻgʻri') from None\n    if not 1 <= n <= 65535:\n        raise ValueError('port notoʻgʻri')\n    return n", 'port("8080")', 'port("http")', 'port("0")', 'port("70000")', lv=3),
    L("exercism", "binary-search", note="Element topilmasa ValueError chiqarish talab qilinadi."),
    L("exercism", "triangle"),
    L("exercism", "robot-name"),
    L("exercism", "nth-prime", note="0 uchun ValueError chiqarish talab qilinadi."),
])

# ---------------------------------------------------------------- 7.7
TOPIC("xato-narxi", "Istisnolar narxi va yaxshi odatlar", "EAFP va LBYL, tezlik, toza kod", 20, r'''
Istisnolar — kuchli vosita, lekin bepul emas. Ularni qachon ishlatish va qachon ishlatmaslikni bilish — tajribali dasturchining belgisi.

## Ikki falsafa
| | LBYL | EAFP |
|---|---|---|
| Maʼnosi | "Sakrashdan oldin qara" | "Ruxsat soʻragandan koʻra kechirim soʻra osonroq" |
| Usul | avval `if` bilan tekshir | `try` qil, xato boʻlsa ushla |
| Python uslubi | baʼzan | koʻpincha ✅ |

```py
d = {"a": 1}

# LBYL
if "b" in d:
    print(d["b"])
else:
    print("yoʻq")

# EAFP
try:
    print(d["b"])
except KeyError:
    print("yoʻq")
```

## Narxi qancha?
`try` blokiga **kirish** deyarli bepul. Lekin xato **chiqarilganda** Python traceback obyektini yaratadi — bu oddiy `if` dan bir necha oʻn barobar sekinroq.

```py
import time

def lbyl(n):
    s = 0
    for i in range(n):
        if i % 2 == 0:
            s += 1
    return s

def eafp(n):
    s = 0
    for i in range(n):
        try:
            if i % 2:
                raise ValueError
            s += 1
        except ValueError:
            pass
    return s

t = time.perf_counter(); lbyl(50000); a = time.perf_counter() - t
t = time.perf_counter(); eafp(50000); b = time.perf_counter() - t
print("Natijalar teng:", lbyl(10) == eafp(10))
print("Istisno usuli sekinroq:", b > a)
```

> Qoida: xato **kamdan-kam** boʻlsa — `try` (EAFP). Xato **tez-tez** boʻlsa (masalan, har ikkinchi element) — `if` (LBYL) tezroq.

## Yomon odatlar ❌
```py norun
# 1. Hamma narsani yutish
try:
    hisobla()
except:
    pass          # xato yoʻqoldi — endi uni hech kim topolmaydi

# 2. Juda katta try
try:
    # 50 qator kod...
except Exception:
    print("nimadir buzildi")

# 3. Oqimni boshqarish uchun istisnodan foydalanish
try:
    while True:
        i += 1
        if i == 10:
            raise StopIteration
except StopIteration:
    pass
```

## Yaxshi odatlar ✅
- Faqat **kutilgan** va **aniq** turni ushlang: `except ValueError`.
- `try` blokini 1–3 qatorga qisqartiring.
- Xatoni yutmang: hech boʻlmasa qayd eting (`print`/`logging`) yoki qayta chiqaring.
- Foydalanuvchiga tushunarli xabar bering, dasturchiga — toʻliq traceback.
- Resurslar uchun — `with`.

## Amaliy shablon: xavfsiz kirish
```py input=10|0|abc|5
def son_oqi():
    while True:
        try:
            return int(input())
        except ValueError:
            print("son kiriting")

a = son_oqi()
b = son_oqi()
while b == 0:
    print("nol boʻlmasin")
    b = son_oqi()
print(a / b)
```

## Esda tuting
- EAFP — Pythoncha, LBYL — tez-tez xato boʻlganda tezroq.
- Istisno — kutilmagan holatlar uchun; oddiy `if` oʻrnini bosmasin.
''', [
    P('d = {"a": 1}\nprint(d.get("b", "yoʻq"))', "None", "⚠ KeyError", "b"),
    P('def f(s):\n    try:\n        return int(s)\n    except ValueError:\n        return None\nprint([f(x) for x in ["1", "a"]])', "[1]", "⚠ ValueError", "[1, 'a']"),
    P('n = 0\nfor s in ["1", "x", "3"]:\n    if s.isdigit():\n        n += int(s)\nprint(n)', "13", "⚠ ValueError", "1"),
    P('try:\n    pass\nexcept Exception:\n    print("E")\nprint("tamom")', "E\ntamom", "E", "⚠ Exception"),
    P('xatolar = []\nfor s in ["1", "q", "w"]:\n    try:\n        int(s)\n    except ValueError as e:\n        xatolar.append(s)\nprint(xatolar)', "['1']", "2", "['q']"),
    P('try:\n    try:\n        1 / 0\n    except ValueError:\n        print("V")\nexcept ZeroDivisionError:\n    print("Z")', "V", "V\nZ", "⚠ ZeroDivisionError", lv=2),
    P('def f():\n    try:\n        return int("x")\n    except ValueError:\n        return -1\n    finally:\n        print("F")\nprint(f())', "-1", "-1\nF", "F", lv=3),
    Q("EAFP uslubi nimani anglatadi?", "Avval bajarib koʻr, xato boʻlsa ushla", "Avval hamma narsani if bilan tekshir", "Xatolarni hech qachon ushlama", "Har bir qatorni alohida try ga oʻra"),
    Q("Qaysi holatda `if` (LBYL) `try` dan afzal?", "Xato juda tez-tez yuz berganda", "Xato juda kam yuz berganda", "Hech qachon", "Fayl ochishda"),
    F("Ikki usul", "`lbyl(sozlar)` — `isdigit` bilan tekshirib, butun sonlar yigʻindisini qaytaring (`try` siz).",
      "def lbyl(sozlar):\n    return sum(int(s) for s in sozlar if s.isdigit())", 'lbyl(["1", "a", "22"])', "lbyl([])", 'lbyl(["-1", "5"])', lv=1),
    F("EAFP", "`eafp(sozlar)` — xuddi shuni `try/except` bilan qiling, lekin manfiy sonlarni ham hisoblang.",
      "def eafp(sozlar):\n    s = 0\n    for x in sozlar:\n        try:\n            s += int(x)\n        except ValueError:\n            pass\n    return s", 'eafp(["1", "a", "22"])', "eafp([])", 'eafp(["-1", "5"])'),
    F("Kirishni tozalash", "`tozala(kirishlar)` — har bir satrni `strip` qilib `int` ga aylantiring; 1..100 oraligʻidagilarni qoldiring, xatolarni oʻtkazib yuboring.",
      "def tozala(kirishlar):\n    r = []\n    for s in kirishlar:\n        try:\n            n = int(s.strip())\n        except ValueError:\n            continue\n        if 1 <= n <= 100:\n            r.append(n)\n    return r", 'tozala([" 5 ", "abc", "200", "100", "0"])', "tozala([])", 'tozala(["7"])'),
    F("Xatolar hisoboti", "`hisobot(amallar)` — `(a, b)` juftliklari uchun `a / b` hisoblang. Har xil xato turlari necha marta uchraganini lugʻatda qaytaring.",
      "def hisobot(amallar):\n    d = {}\n    for a, b in amallar:\n        try:\n            a / b\n        except Exception as e:\n            k = type(e).__name__\n            d[k] = d.get(k, 0) + 1\n    return d", 'hisobot([(1, 0), (1, "x"), (2, 0), (4, 2)])', "hisobot([])", "hisobot([(1, 1)])", lv=3),
    F("Birinchi xato", "`birinchi_xato(sozlar)` — son boʻlmagan birinchi satr indeksini qaytaring; hammasi son boʻlsa `-1`.",
      "def birinchi_xato(sozlar):\n    for i, s in enumerate(sozlar):\n        try:\n            int(s)\n        except ValueError:\n            return i\n    return -1", 'birinchi_xato(["1", "2", "x", "y"])', 'birinchi_xato(["5"])', "birinchi_xato([])"),
    F("Sana", "`sana(s)` — `\"KK.OO.YYYY\"` formatidagi satrdan `(kun, oy, yil)`; format yoki qiymat notoʻgʻri boʻlsa `None`. (oy 1–12, kun 1–31)",
      "def sana(s):\n    try:\n        k, o, y = map(int, s.split('.'))\n    except ValueError:\n        return None\n    if not (1 <= o <= 12 and 1 <= k <= 31):\n        return None\n    return (k, o, y)", 'sana("13.10.2026")', 'sana("32.01.2026")', 'sana("12-10-2026")', 'sana("1.2.3.4")', 'sana("ab.cd.ef")', lv=3),
    F("Qayta urinish", "`urin(natijalar)` — har bir element bitta urinish natijasi: `\"xato\"` yoki son. Birinchi muvaffaqiyatli sonni qaytaring; 3 urinishdan keyin ham boʻlmasa `RuntimeError` chiqaring.",
      "def urin(natijalar):\n    for i, r in enumerate(natijalar[:3]):\n        if r != 'xato':\n            return r\n    raise RuntimeError('3 urinish muvaffaqiyatsiz')", 'urin(["xato", 7])', 'urin([5])', 'urin(["xato", "xato", "xato", 9])', 'urin(["xato", "xato", 1])'),
    L("exercism", "luhn"),
    L("exercism", "say", note="Chegara tashqarisidagi sonlar uchun ValueError."),
    L("exercism", "largest-series-product"),
    L("exercism", "affine-cipher"),
])
