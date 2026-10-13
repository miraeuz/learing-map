from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(9, "Modullar va paketlar", "Kodni fayllarga boʻlish, import va paketlar", "📦")

GEO = '''"""Geometriya yordamchilari."""
PI = 3.14159


def doira_yuzasi(r):
    return round(PI * r * r, 2)


def kvadrat_yuzasi(a):
    return a * a
'''

# ---------------------------------------------------------------- 9.1
TOPIC("modul-yaratish", "Modul yaratish va import", "Har bir .py fayl — modul", 20, r'''
Dastur kattalashgan sari bitta faylda saqlash noqulay boʻladi. **Modul** — bu oddiy `.py` fayl. Undagi funksiya, sinf va oʻzgaruvchilarni boshqa fayldan **import** qilib ishlatish mumkin.

Quyidagi misolda ikkita fayl bor — yuqoridagi tablarni bosib koʻring: `geometriya.py` — modul, `main.py` — uni ishlatadigan dastur.

```py file=geometriya.py
"""Geometriya yordamchilari."""
PI = 3.14159


def doira_yuzasi(r):
    return round(PI * r * r, 2)


def kvadrat_yuzasi(a):
    return a * a
```

```py
import geometriya

print(geometriya.PI)
print(geometriya.doira_yuzasi(10))
print(geometriya.kvadrat_yuzasi(7))
```

## import ning shakllari
```py file=geometriya.py
PI = 3.14159

def doira_yuzasi(r):
    return round(PI * r * r, 2)

def kvadrat_yuzasi(a):
    return a * a
```

```py
import geometriya                         # 1) butun modul
from geometriya import kvadrat_yuzasi     # 2) faqat kerakli nom
from geometriya import PI as pi           # 3) taxallus bilan
import geometriya as geo                  # 4) modulga taxallus

print(geometriya.kvadrat_yuzasi(2))
print(kvadrat_yuzasi(3))
print(pi)
print(geo.doira_yuzasi(1))
```

| Yozuv | Qachon |
|---|---|
| `import modul` | koʻp funksiya kerak, nom qayerdan kelgani aniq koʻrinsin |
| `from modul import nom` | bir-ikkita nom kerak |
| `import uzun_nom as qisqa` | `import numpy as np` kabi mashhur taxalluslar |

!> `from modul import *` — barcha nomlarni import qiladi va qaysi nom qayerdan kelganini yashiradi. Uni ishlatmang.

## Standart kutubxona ham — modullar
Python bilan birga yuzlab tayyor modullar keladi:

```py
import math
import random
from datetime import date

print(math.sqrt(144), math.pi)
random.seed(1)
print(random.randint(1, 6))
print(date(2026, 10, 13).isoformat())
```

## Modul nomlari
- Kichik harflar va pastki chiziq: `talaba_baholari.py`.
- Standart modul nomlarini takrorlamang: `random.py` yoki `math.py` deb nomlasangiz, Python sizning faylingizni import qilib qoʻyadi!

## Esda tuting
- Modul = `.py` fayl; nomi = fayl nomi (`.py` siz).
- Bir loyihadagi modullar bir papkada boʻlsa, `import nom` ishlaydi.
''', [
    P('import math\nprint(math.floor(3.7), math.ceil(3.2))', "3.7 3.2", "4 3", "3 3"),
    P('from math import sqrt as ildiz\nprint(ildiz(81))', "9", "81", "⚠ NameError"),
    P('import math as m\nprint(m.pi > 3, "math" in dir())', "True True", "False False", "Xato"),
    P('from math import pi\nprint(math.pi)', "3.141592653589793", "pi", "None", lv=2,
      why="`from math import pi` faqat `pi` nomini olib keladi, `math` nomi yaratilmaydi."),
    P('import random\nrandom.seed(42)\na = random.randint(1, 100)\nrandom.seed(42)\nb = random.randint(1, 100)\nprint(a == b)', "False", "Xato", "42"),
    P('import string\nprint(string.digits)', "digits", "1234567890", "Xato"),
    P('from collections import Counter\nimport collections\nprint(Counter is collections.Counter)', "False", "Xato", "None"),
    Q("Pythonda modul nima?", "Funksiya, sinf va oʻzgaruvchilar yozilgan oddiy .py fayl", "Faqat standart kutubxonadagi papka", "Maxsus .mod kengaytmali fayl", "Internetdan yuklanadigan dastur"),
    Q("Nega `from modul import *` tavsiya etilmaydi?", "Qaysi nom qayerdan kelgani noaniq boʻladi va nomlar toʻqnashishi mumkin", "U ishlamaydi", "U sekin", "U faqat bitta nomni import qiladi"),
    F("Modulni ishlatish", "`geometriya.py` moduli berilgan (tabga qarang). `hisobot(r, a)` funksiyasi undan foydalanib `\"Doira: X, Kvadrat: Y\"` satrini qaytarsin.",
      "import geometriya\n\n\ndef hisobot(r, a):\n    return f'Doira: {geometriya.doira_yuzasi(r)}, Kvadrat: {geometriya.kvadrat_yuzasi(a)}'",
      "hisobot(1, 2)", "hisobot(10, 5)", "hisobot(0, 0)", files={"geometriya.py": GEO}, lv=1),
    F("from … import", "`narxlar.py` modulidagi `QQS` va `qqs_bilan` dan `from ... import` bilan foydalanib, `savat(narxlar)` — har biriga QQS qoʻshilgan narxlar yigʻindisini qaytarsin.",
      "from narxlar import qqs_bilan\n\n\ndef savat(narxlar):\n    return sum(qqs_bilan(n) for n in narxlar)",
      "savat([10000, 5000])", "savat([])", "savat([1000])",
      files={"narxlar.py": "QQS = 0.12\n\n\ndef qqs_bilan(narx):\n    return round(narx * (1 + QQS))\n"}),
    F("Taxallus", "`import statistics as st` qilib, `tahlil(sonlar)` — `(oʻrtacha, mediana)` kortejini qaytarsin (`st.mean`, `st.median`).",
      "import statistics as st\n\n\ndef tahlil(sonlar):\n    return (st.mean(sonlar), st.median(sonlar))",
      "tahlil([1, 2, 3, 4])", "tahlil([5, 5, 5])", "tahlil([10, 1, 7])"),
    F("Ikki modul", "`matn_vositalari.py` va `raqam_vositalari.py` modullari berilgan. `tozala(s)` — satrdan raqamlarni olib tashlab (`raqamsiz`), soʻngra bosh harflarni katta qilsin (`sarlavha`).",
      "from matn_vositalari import sarlavha\nfrom raqam_vositalari import raqamsiz\n\n\ndef tozala(s):\n    return sarlavha(raqamsiz(s))",
      'tozala("mirae2026 academy")', 'tozala("123")', 'tozala("python 3 darslari")',
      files={"matn_vositalari.py": "def sarlavha(s):\n    return ' '.join(w.capitalize() for w in s.split())\n",
             "raqam_vositalari.py": "def raqamsiz(s):\n    return ''.join(h for h in s if not h.isdigit())\n"}, lv=2),
    F("Modul konstantasi", "`sozlamalar.py` da `MAKS_BALL` va `OTISH` bor. `natija(ball)` — `\"oʻtdi\"` yoki `\"yiqildi\"`; ball `MAKS_BALL` dan oshsa `ValueError`.",
      "import sozlamalar\n\n\ndef natija(ball):\n    if ball > sozlamalar.MAKS_BALL:\n        raise ValueError('ball juda katta')\n    return 'oʻtdi' if ball >= sozlamalar.OTISH else 'yiqildi'",
      "natija(60)", "natija(59)", "natija(101)",
      files={"sozlamalar.py": "MAKS_BALL = 100\nOTISH = 60\n"}),
    F("Tasodifiy, lekin takrorlanadigan", "`random` modulidan foydalanib `zar(n, urugʻ)` — `random.seed(urugʻ)` qilib, n marta 1..6 zar tashlab, natijalar roʻyxatini qaytarsin. (Bir xil urugʻ — bir xil natija.)",
      "import random\n\n\ndef zar(n, urug):\n    random.seed(urug)\n    return [random.randint(1, 6) for _ in range(n)]",
      "zar(5, 1) == zar(5, 1)", "len(zar(10, 7))", "all(1 <= x <= 6 for x in zar(50, 3))", lv=1),
    F("Standart modullar", "`math` dan foydalanib `aylana(r)` — `(uzunlik, yuza)` ni 2 xonagacha yaxlitlab qaytarsin (`math.pi`).",
      "import math\n\n\ndef aylana(r):\n    return (round(2 * math.pi * r, 2), round(math.pi * r * r, 2))",
      "aylana(1)", "aylana(10)", "aylana(0)"),
    L("docs", "py-modules"),
    L("exercism", "leap", note="Yechimni `leap.py` modulida yozib, boshqa fayldan import qilib sinab koʻring."),
    L("exercism", "grains"),
    L("docs", "py-importlib", title="importlib — modullarni dasturiy import qilish"),
])

# ---------------------------------------------------------------- 9.2
TOPIC("pyc-sys-path", "Modul qayerdan topiladi? (sys.path va .pyc)", "Qidiruv yoʻli, kesh va kompilyatsiya qilingan fayllar", 20, r'''
`import salom` yozilganda Python uchta ishni qiladi:

1. `sys.modules` ga qaraydi — modul **allaqachon yuklanganmi**?
2. Yuklanmagan boʻlsa, `sys.path` dagi papkalardan `salom.py` ni **qidiradi**;
3. Topilgan faylni **bir marta** bajaradi va natijani `sys.modules` ga saqlaydi.

## Modul faqat bir marta bajariladi
```py file=salom.py
print(">>> salom moduli yuklanmoqda")
XABAR = "Assalomu alaykum"
```

```py
import salom
import salom          # ikkinchi marta — hech narsa chiqmaydi
import sys

print(salom.XABAR)
print("salom" in sys.modules)
```

> Shu sababli modul ichida faqat **taʼriflar** (funksiya, sinf, konstanta) yozing. Hisob-kitob va `print` lar — `if __name__ == "__main__":` ichida (9.6 mavzu).

## sys.path — qidiruv yoʻli
```py
import sys

print(type(sys.path).__name__)
print(len(sys.path) > 0)
print(sys.path[0] != "")      # birinchi oʻrinda — joriy dastur papkasi
```

Tartib odatda shunday:
| # | Qayer |
|---|---|
| 1 | ishga tushirilgan skript turgan papka |
| 2 | `PYTHONPATH` muhit oʻzgaruvchisidagi papkalar |
| 3 | standart kutubxona |
| 4 | `site-packages` — `pip` bilan oʻrnatilgan paketlar |

!> Modul topilmasa — `ModuleNotFoundError`. Koʻpincha sababi: fayl boshqa papkada, nom xato yozilgan yoki paket oʻrnatilmagan.

```py xato
import mavjud_emas_modul
```

## .pyc fayllar va __pycache__
Python `.py` kodni avval **bayt-kod**ga oʻgiradi va keyingi safar tezroq yuklash uchun uni `__pycache__` papkasida `.pyc` fayl sifatida saqlaydi.

```py file=hisob.py
def qosh(a, b):
    return a + b
```

```py
import py_compile, os

yol = py_compile.compile("hisob.py")
print(yol.replace("\\", "/").split("/")[-2])     # papka nomi
print(yol.endswith(".pyc"))
print(os.path.exists(yol))
```

| Fayl | Nima |
|---|---|
| `hisob.py` | siz yozgan manba kod |
| `__pycache__/hisob.cpython-314.pyc` | Python 3.14 uchun bayt-kod (avtomatik) |

> `__pycache__` ni oʻchirish xavfsiz — Python uni qayta yaratadi. Git'da uni `.gitignore` ga qoʻshing.

## Modulni qayta yuklash
```py file=sozlama.py
TIL = "uz"
```

```py
import importlib
import sozlama

print(sozlama.TIL)
with open("sozlama.py", "w") as f:
    f.write('TIL = "en"\n')
importlib.reload(sozlama)
print(sozlama.TIL)
```

## Esda tuting
- Modul bir marta yuklanadi va `sys.modules` da saqlanadi.
- `sys.path` — Python modullarni qidiradigan papkalar roʻyxati.
''', [
    P('import sys\nprint(type(sys.modules).__name__)', "list", "module", "Xato"),
    P('import math, sys\nprint("math" in sys.modules)', "False", "math", "Xato"),
    P('import nomsiz_modul_xyz', "None", "⚠ ImportError", "⚠ NameError"),
    P('import json\nimport json as j\nprint(j is json)', "False", "Xato", "json"),
    P('from importlib.util import cache_from_source\nprint(cache_from_source("a.py").replace("\\\\", "/").split("/")[0])', "a.pyc", "a.py", "pycache"),
    P('import sys\nprint(isinstance(sys.path, list), all(isinstance(p, str) for p in sys.path))', "True False", "False True", "False False"),
    P('import os\nprint(os.path.splitext("hisob.cpython-314.pyc")[1])', "pyc", "hisob", ".cpython-314.pyc", lv=2),
    Q("Bir dasturda `import salom` ikki marta yozilsa, modul necha marta bajariladi?", "Bir marta", "Ikki marta", "Hech qachon", "Har safar chaqirilganda"),
    Q("`ModuleNotFoundError` ning eng koʻp uchraydigan sababi?", "Modul sys.path dagi papkalarda topilmadi (nom xato, boshqa papka yoki oʻrnatilmagan)", "Modul ichida xato bor", "Internet yoʻq", "Python versiyasi eski"),
    F("Yuklanganmi?", "`yuklanganmi(nom)` — `sys.modules` da shu nomli modul bormi?",
      "import sys\n\n\ndef yuklanganmi(nom):\n    return nom in sys.modules",
      'yuklanganmi("sys")', 'yuklanganmi("hech_qanday_modul_yoq")', '(__import__("json"), yuklanganmi("json"))[-1]', lv=1),
    F("Xavfsiz import", "`bormi(nom)` — modulni `importlib.import_module` bilan yuklashga urinib, muvaffaqiyatli boʻlsa `True`, `ModuleNotFoundError` boʻlsa `False` qaytarsin.",
      "import importlib\n\n\ndef bormi(nom):\n    try:\n        importlib.import_module(nom)\n        return True\n    except ModuleNotFoundError:\n        return False",
      'bormi("math")', 'bormi("mirae_yoq_modul")', 'bormi("collections.abc")', 'bormi("yordamchi")',
      files={"yordamchi.py": "X = 1\n"}),
    F("Dinamik import", "`chaqir(modul, funksiya, *args)` — modulni nomi boʻyicha import qilib (`importlib.import_module`), undagi funksiyani `getattr` bilan topib chaqirsin.",
      "import importlib\n\n\ndef chaqir(modul, funksiya, *args):\n    m = importlib.import_module(modul)\n    return getattr(m, funksiya)(*args)",
      'chaqir("math", "gcd", 12, 18)', 'chaqir("operator", "add", 2, 3)', 'chaqir("hisob", "kopaytir", 6, 7)',
      files={"hisob.py": "def kopaytir(a, b):\n    return a * b\n"}, lv=2),
    F("Kesh yoʻli", "`pyc_nomi(fayl)` — `importlib.util.cache_from_source` natijasidan faqat fayl nomini (papkasiz) qaytarsin, lekin versiya qismini `X` ga almashtiring: `hisob.py` → `hisob.cpython-X.pyc`.",
      "import importlib.util\nimport os\nimport re\n\n\ndef pyc_nomi(fayl):\n    nom = os.path.basename(importlib.util.cache_from_source(fayl))\n    return re.sub(r'cpython-\\d+', 'cpython-X', nom)",
      'pyc_nomi("hisob.py")', 'pyc_nomi("main.py")', 'pyc_nomi("paket/modul.py")', lv=3),
    F("Modul hisoblagichi", "`hisoblagich.py` moduli import qilinganda `YUKLANISH` ni 1 ga oshiradi. `sinov()` — modulni 3 marta import qilib (`import hisoblagich`), `hisoblagich.YUKLANISH` ni qaytarsin. (Javob 1 boʻlishi kerak — nega?)",
      "def sinov():\n    import hisoblagich\n    import hisoblagich\n    import hisoblagich\n    return hisoblagich.YUKLANISH",
      "sinov()", "sinov() + sinov()", "type(sinov()).__name__",
      files={"hisoblagich.py": "YUKLANISH = 0\nYUKLANISH += 1\n"}),
    F("Qidiruv yoʻliga qoʻshish", "`kutubxona/` papkasida `vosita.py` bor. `yukla()` — `sys.path` ga `\"kutubxona\"` ni qoʻshib (agar yoʻq boʻlsa), `import vosita` qilib, `vosita.salom()` natijasini qaytarsin.",
      "import sys\n\n\ndef yukla():\n    if 'kutubxona' not in sys.path:\n        sys.path.append('kutubxona')\n    import vosita\n    return vosita.salom()",
      "yukla()", "yukla().upper()", "len(yukla())",
      files={"kutubxona/vosita.py": "def salom():\n    return 'kutubxonadan salom'\n"}, lv=3),
    F("Modul qayerda?", "`modul_papkasi(nom)` — modulni import qilib, `__file__` yoʻlidan faqat fayl nomini qaytarsin (`os.path.basename`).",
      "import importlib\nimport os\n\n\ndef modul_papkasi(nom):\n    return os.path.basename(importlib.import_module(nom).__file__)",
      'modul_papkasi("yordamchi")', 'modul_papkasi("paket")', 'modul_papkasi("json")',
      files={"yordamchi.py": "X = 1\n", "paket/__init__.py": ""}, lv=2),
    L("docs", "py-sys"),
    L("docs", "py-compile"),
    L("docs", "py-import"),
    L("exercism", "sieve", note="Yechimni alohida modulga ajrating va boshqa fayldan import qilib sinang."),
])

# ---------------------------------------------------------------- 9.3
TOPIC("paketlar", "Paketlar va ichki paketlar", "Modullarni papkalarga tartiblash", 20, r'''
Modullar koʻpaysa, ularni **papkalarga** ajratamiz. Modullar joylashgan papka — **paket**.

```text
dokon/                  ← paket
├── __init__.py         ← "bu papka — paket" belgisi (boʻsh boʻlishi mumkin)
├── mahsulot.py
└── tolov/              ← ichki paket (sub-package)
    ├── __init__.py
    └── karta.py
```

```py file=dokon/__init__.py
"""Doʻkon paketi."""
VERSIYA = "1.0"
```

```py file=dokon/mahsulot.py
def narx_matni(nom, narx):
    return f"{nom}: {narx:,} soʻm"
```

```py file=dokon/tolov/__init__.py
```

```py file=dokon/tolov/karta.py
def komissiya(summa):
    return round(summa * 0.01)
```

```py
import dokon
from dokon import mahsulot
from dokon.tolov import karta
from dokon.tolov.karta import komissiya

print(dokon.VERSIYA)
print(mahsulot.narx_matni("Daftar", 12000))
print(karta.komissiya(250000))
print(komissiya(1000))
```

## __init__.py nima qiladi?
- Paket **birinchi marta** import qilinganda bajariladi.
- Paketning "yuzi": tez-tez ishlatiladigan nomlarni shu yerga chiqarib qoʻyish mumkin.

```py file=matematika/__init__.py
from .asosiy import qosh, ayir
__all__ = ["qosh", "ayir"]
```

```py file=matematika/asosiy.py
def qosh(a, b):
    return a + b

def ayir(a, b):
    return a - b
```

```py
import matematika

print(matematika.qosh(2, 3))       # matematika.asosiy.qosh emas — qisqaroq!
print(matematika.ayir(10, 4))
```

> `__init__.py` siz papka ham import qilinishi mumkin ("namespace package"), lekin oddiy loyihalarda `__init__.py` qoʻyish — aniq va xavfsiz odat.

## Haqiqiy loyiha tuzilishi
```text
mening_ilovam/
├── main.py
├── ilova/
│   ├── __init__.py
│   ├── modellar.py
│   ├── xizmatlar/
│   │   ├── __init__.py
│   │   ├── email.py
│   │   └── tolov.py
│   └── yordamchilar.py
└── tests/
    └── test_modellar.py
```

## Esda tuting
- Paket = `__init__.py` li papka; ichida modullar va ichki paketlar.
- Import nuqtalar bilan: `import paket.ichki.modul`.
''', [
    P('import os.path\nprint(os.path.basename("/a/b/c.py"))', "/a/b", "c", "b"),
    P('from os import path\nimport os\nprint(path is os.path)', "False", "Xato", "path"),
    P('import json.decoder\nprint(json.decoder.__name__)', "decoder", "json", "Xato"),
    P('import collections.abc as abc\nprint(isinstance([], abc.Sequence), isinstance({}, abc.Sequence))', "True True", "False False", "False True"),
    P('import xml\nprint(hasattr(xml, "__path__"))', "False", "xml", "Xato", lv=2,
      why="Paketlarda `__path__` atributi bor (modullar qidiriladigan papkalar). Oddiy modulda u yoʻq."),
    P('import math\nprint(hasattr(math, "__path__"))', "True", "math", "Xato", lv=2),
    P('import email.message\nprint(email.message.EmailMessage.__name__)', "email", "message", "Xato"),
    Q("Paket nima?", "Modullar joylashgan (odatda __init__.py li) papka", "Bitta katta .py fayl", "pip bilan oʻrnatiladigan zip fayl", "Python versiyasi"),
    Q("`__init__.py` qachon bajariladi?", "Paket birinchi marta import qilinganda", "Har bir modul import qilinganda", "Hech qachon", "Dastur tugaganda"),
    F("Paketdan import", "`hisob/` paketi berilgan (`soliq.py` va `chegirma.py`). `yakuniy(narx)` — avval 10% chegirma, keyin 12% soliq qoʻshib (`int`) qaytarsin.",
      "from hisob.chegirma import chegirma\nfrom hisob.soliq import soliq_bilan\n\n\ndef yakuniy(narx):\n    return soliq_bilan(chegirma(narx))",
      "yakuniy(100000)", "yakuniy(0)", "yakuniy(5000)",
      files={"hisob/__init__.py": "", "hisob/chegirma.py": "def chegirma(narx, foiz=10):\n    return narx * (100 - foiz) // 100\n",
             "hisob/soliq.py": "def soliq_bilan(narx):\n    return int(narx * 1.12)\n"}, lv=1),
    F("Ichki paket", "`ilova/xizmatlar/xabar.py` da `formatla(ism, matn)` bor. `bildirish(ism)` — `\"Darsingiz boshlandi\"` matni bilan formatlangan xabarni qaytarsin.",
      "from ilova.xizmatlar.xabar import formatla\n\n\ndef bildirish(ism):\n    return formatla(ism, 'Darsingiz boshlandi')",
      'bildirish("Ali")', 'bildirish("Madina")', 'len(bildirish(""))',
      files={"ilova/__init__.py": "", "ilova/xizmatlar/__init__.py": "", "ilova/xizmatlar/xabar.py": "def formatla(ism, matn):\n    return f'🔔 {ism}: {matn}'\n"}),
    F("Paket yuzi", "`kalk` paketining `__init__.py` si `qosh` va `kopaytir` ni oʻzidan eksport qiladi. `ifoda(a, b, c)` — `kalk.qosh(kalk.kopaytir(a, b), c)` ni qaytarsin (faqat `import kalk` bilan).",
      "import kalk\n\n\ndef ifoda(a, b, c):\n    return kalk.qosh(kalk.kopaytir(a, b), c)",
      "ifoda(2, 3, 4)", "ifoda(0, 9, 1)", "ifoda(-1, 5, 5)",
      files={"kalk/__init__.py": "from .amallar import qosh, kopaytir\n", "kalk/amallar.py": "def qosh(a, b):\n    return a + b\n\n\ndef kopaytir(a, b):\n    return a * b\n"}),
    F("Paket versiyasi", "`dokon` paketida `__init__.py` ichida `__version__` bor. `versiya_katta(minimal)` — paket versiyasi `\"1.4.2\"` kabi satr; minimal versiyadan katta yoki teng boʻlsa `True` (sonlar kortejiga aylantirib solishtiring).",
      "import dokon\n\n\ndef versiya_katta(minimal):\n    q = lambda s: tuple(int(x) for x in s.split('.'))\n    return q(dokon.__version__) >= q(minimal)",
      'versiya_katta("1.4.0")', 'versiya_katta("1.10")', 'versiya_katta("1.4.2")',
      files={"dokon/__init__.py": "__version__ = '1.4.2'\n"}, lv=2),
    F("Paketmi yoki modulmi", "`turi(nom)` — import qilib, `__path__` atributi boʻlsa `\"paket\"`, aks holda `\"modul\"` qaytarsin.",
      "import importlib\n\n\ndef turi(nom):\n    m = importlib.import_module(nom)\n    return 'paket' if hasattr(m, '__path__') else 'modul'",
      'turi("json")', 'turi("math")', 'turi("mening")', 'turi("mening.qism")',
      files={"mening/__init__.py": "", "mening/qism.py": "X = 1\n"}, lv=2),
    F("Paket ichidagi modullar", "`pkgutil.iter_modules` yordamida `modullar(paket_nomi)` — paket ichidagi modul nomlarini alifbo boʻyicha qaytarsin.",
      "import importlib\nimport pkgutil\n\n\ndef modullar(paket_nomi):\n    p = importlib.import_module(paket_nomi)\n    return sorted(m.name for m in pkgutil.iter_modules(p.__path__))",
      'modullar("asboblar")', 'len(modullar("asboblar"))', '"bolg" in modullar("asboblar")',
      files={"asboblar/__init__.py": "", "asboblar/bolg.py": "", "asboblar/arra.py": "", "asboblar/otvertka.py": ""}, lv=3),
    F("__all__", "`kutubxona/__init__.py` da `__all__` roʻyxati bor. `eksport(paket_nomi)` — paketning `__all__` ini alifbo tartibida qaytarsin; boʻlmasa boʻsh roʻyxat.",
      "import importlib\n\n\ndef eksport(paket_nomi):\n    return sorted(getattr(importlib.import_module(paket_nomi), '__all__', []))",
      'eksport("kutubxona")', 'eksport("boshqa")', 'len(eksport("kutubxona"))',
      files={"kutubxona/__init__.py": "from .a import qosh\nfrom .b import ayir\n__all__ = ['qosh', 'ayir']\n", "kutubxona/a.py": "def qosh(x, y):\n    return x + y\n",
             "kutubxona/b.py": "def ayir(x, y):\n    return x - y\n", "boshqa/__init__.py": ""}),
    L("docs", "py-modules", title="Packages — rasmiy qoʻllanma (6.4)"),
    L("docs", "py-import"),
    L("exercism", "kindergarten-garden", note="Bir nechta modulga ajratib yozib koʻring: maʼlumot, mantiq, testlar."),
    L("docs", "pkg-publish", title="Packaging Python Projects — paket tuzilishi"),
])

# ---------------------------------------------------------------- 9.4
TOPIC("nisbiy-import", "Paket ichidagi havolalar (nisbiy import)", "from . import va from .. import", 15, r'''
Paket ichidagi modullar bir-birini import qilishi kerak boʻladi. Buning ikki usuli bor:

| Usul | Misol | Qachon |
|---|---|---|
| **Absolyut** | `from dokon.mahsulot import Mahsulot` | doim ishlaydi, eng aniq |
| **Nisbiy** | `from .mahsulot import Mahsulot` | paket ichida, paket nomi oʻzgarsa ham ishlaydi |

- `.` — shu paket (joriy papka)
- `..` — bitta yuqoridagi paket

```text
dokon/
├── __init__.py
├── mahsulot.py
├── savat.py          ← mahsulot.py dan foydalanadi
└── tolov/
    ├── __init__.py
    └── hisob.py      ← ..savat dan foydalanadi
```

```py file=dokon/__init__.py
```

```py file=dokon/mahsulot.py
class Mahsulot:
    def __init__(self, nom, narx):
        self.nom, self.narx = nom, narx
```

```py file=dokon/savat.py
from .mahsulot import Mahsulot      # nisbiy: shu paketdagi mahsulot.py


class Savat:
    def __init__(self):
        self.narsalar = []

    def qosh(self, nom, narx):
        self.narsalar.append(Mahsulot(nom, narx))

    def jami(self):
        return sum(m.narx for m in self.narsalar)
```

```py file=dokon/tolov/__init__.py
```

```py file=dokon/tolov/hisob.py
from ..savat import Savat           # bir pogʻona yuqoridagi savat.py


def chek(savat: Savat):
    return f"{len(savat.narsalar)} ta mahsulot, jami {savat.jami():,} soʻm"
```

```py
from dokon.savat import Savat
from dokon.tolov.hisob import chek

s = Savat()
s.qosh("Non", 4000)
s.qosh("Sut", 12000)
print(chek(s))
```

## Nisbiy importning cheklovi
!> Nisbiy import faqat **paket ichidagi** modulda ishlaydi. Oddiy skriptda (`python savat.py`) `from .mahsulot import ...` yozsangiz — `ImportError: attempted relative import with no known parent package`.

```py xato
from .mahsulot import Mahsulot
```

> Yechim: dasturni paketdan tashqaridan ishga tushiring yoki `python -m dokon.savat` bilan (9.6 mavzu).

## Aylanma import (circular import)
`a.py` → `b.py` ni, `b.py` esa → `a.py` ni import qilsa, muammo chiqishi mumkin. Yechim: umumiy qismni uchinchi modulga chiqaring yoki importni funksiya ichiga koʻchiring.

## Esda tuting
- `.` — shu paket, `..` — ota paket.
- Nisbiy import faqat paket ichida; skriptlarda absolyut import ishlating.
''', [
    P('from . import x', "x", "None", "⚠ ModuleNotFoundError"),
    P('print(len("..modul") - len("modul"))', "1", "0", "Xato"),
    P('import importlib.util\nprint(importlib.util.resolve_name(".savat", "dokon"))', ".savat", "savat", "Xato"),
    P('import importlib.util\nprint(importlib.util.resolve_name("..savat", "dokon.tolov"))', "dokon.tolov.savat", "..savat", "Xato", lv=2),
    P('import importlib.util\nprint(importlib.util.resolve_name("..", "a.b.c"))', "a.b.c", "a", "Xato", lv=3),
    P('import importlib.util\nprint(importlib.util.resolve_name("json", "a.b"))', "a.b.json", "a.json", "Xato"),
    P('import json\nprint(json.__package__)', "None", "json.json", "Xato"),
    Q("`from ..savat import Savat` dagi `..` nimani bildiradi?", "Joriy paketdan bir pogʻona yuqoridagi paketni", "Joriy papkani", "Python'ning standart kutubxonasini", "Fayl kengaytmasini"),
    Q("Paket ichida emas, oddiy skriptda nisbiy import yozilsa nima boʻladi?", "ImportError: attempted relative import with no known parent package", "Hammasi ishlaydi", "SyntaxError", "Modul ikki marta yuklanadi"),
    F("Nisbiy import", "`kutubxona/` paketida `kitob.py` va `qidiruv.py` bor; `qidiruv.py` nisbiy import bilan `kitob.py` dan foydalanadi. `top(nom)` — `kutubxona.qidiruv.topish` ni chaqirib natijani qaytarsin.",
      "from kutubxona.qidiruv import topish\n\n\ndef top(nom):\n    return topish(nom)",
      'top("Alpomish")', 'top("Yoʻq kitob")', 'top("Sarob")',
      files={"kutubxona/__init__.py": "", "kutubxona/kitob.py": "KITOBLAR = {'Alpomish': 'Xalq dostoni', 'Sarob': 'Abdulla Qahhor'}\n",
             "kutubxona/qidiruv.py": "from .kitob import KITOBLAR\n\n\ndef topish(nom):\n    return KITOBLAR.get(nom, 'topilmadi')\n"}, lv=1),
    F("Ota paketdan", "`ilova/sozlama.py` da `TIL`. `ilova/xizmat/salom.py` nisbiy `..` import bilan undan foydalanadi. `salom_ber(ism)` — `ilova.xizmat.salom.salom(ism)` natijasini qaytarsin.",
      "from ilova.xizmat.salom import salom\n\n\ndef salom_ber(ism):\n    return salom(ism)",
      'salom_ber("Ali")', 'salom_ber("Madina")', 'salom_ber("")',
      files={"ilova/__init__.py": "", "ilova/sozlama.py": "TIL = 'uz'\n", "ilova/xizmat/__init__.py": "",
             "ilova/xizmat/salom.py": "from ..sozlama import TIL\n\n\ndef salom(ism):\n    return ('Salom, ' if TIL == 'uz' else 'Hello, ') + ism\n"}),
    F("Nomni hal qilish", "`toliq_nom(nisbiy, paket)` — `importlib.util.resolve_name` bilan nisbiy nomni toʻliq nomga aylantirsin.",
      "import importlib.util\n\n\ndef toliq_nom(nisbiy, paket):\n    return importlib.util.resolve_name(nisbiy, paket)",
      'toliq_nom(".modellar", "ilova")', 'toliq_nom("..yordam", "ilova.xizmat")', 'toliq_nom("..", "a.b.c")'),
    F("Nuqtalarni sanash", "`daraja(nisbiy)` — nisbiy import satrining boshidagi nuqtalar soni (`\"..a\"` → 2, `\"a\"` → 0).",
      "def daraja(nisbiy):\n    return len(nisbiy) - len(nisbiy.lstrip('.'))",
      'daraja("..savat")', 'daraja(".x")', 'daraja("json")', 'daraja("...")', lv=1),
    F("Toʻliq paket", "`ombor/` paketi: `mahsulot.py` (`Mahsulot` dataclass), `ombor.py` (`.mahsulot` dan import, `Ombor` sinfi), `__init__.py` ikkalasini eksport qiladi. `qoldiq(royxat)` — `ombor.Ombor` ga `(nom, soni)` larni qoʻshib, `jami()` ni qaytarsin.",
      "import ombor\n\n\ndef qoldiq(royxat):\n    o = ombor.Ombor()\n    for nom, soni in royxat:\n        o.qosh(ombor.Mahsulot(nom, soni))\n    return o.jami()",
      'qoldiq([("non", 10), ("sut", 5)])', "qoldiq([])", 'qoldiq([("a", 1)] * 4)',
      files={"ombor/__init__.py": "from .mahsulot import Mahsulot\nfrom .ombor import Ombor\n",
             "ombor/mahsulot.py": "from dataclasses import dataclass\n\n\n@dataclass\nclass Mahsulot:\n    nom: str\n    soni: int\n",
             "ombor/ombor.py": "from .mahsulot import Mahsulot\n\n\nclass Ombor:\n    def __init__(self):\n        self.royxat: list[Mahsulot] = []\n\n    def qosh(self, m):\n        self.royxat.append(m)\n\n    def jami(self):\n        return sum(m.soni for m in self.royxat)\n"}, lv=2),
    F("Nisbiy yoki absolyut", "`turini_aniqla(qator)` — `\"from .x import y\"` → `\"nisbiy\"`, `\"from x import y\"` yoki `\"import x\"` → `\"absolyut\"`.",
      "def turini_aniqla(qator):\n    q = qator.split()\n    if q[0] == 'from' and q[1].startswith('.'):\n        return 'nisbiy'\n    return 'absolyut'",
      'turini_aniqla("from .mahsulot import Mahsulot")', 'turini_aniqla("from dokon.mahsulot import Mahsulot")', 'turini_aniqla("import os")', 'turini_aniqla("from .. import savat")'),
    F("Paket ichidagi zanjir", "`shakl/` paketi: `asos.py` (`Shakl`), `kvadrat.py` (`.asos` dan meros), `doira.py` (`.asos` dan meros). `__init__.py` ikkalasini eksport qiladi. `yuzalar(olchamlar)` — `[(\"kvadrat\", 3), (\"doira\", 1)]` kabi roʻyxatdan yuzalar roʻyxatini qaytarsin.",
      "import shakl\n\n\ndef yuzalar(olchamlar):\n    turlar = {'kvadrat': shakl.Kvadrat, 'doira': shakl.Doira}\n    return [turlar[t](x).yuza() for t, x in olchamlar]",
      'yuzalar([("kvadrat", 3), ("doira", 1)])', "yuzalar([])", 'yuzalar([("doira", 2)])',
      files={"shakl/__init__.py": "from .kvadrat import Kvadrat\nfrom .doira import Doira\n",
             "shakl/asos.py": "class Shakl:\n    def yuza(self):\n        return 0\n",
             "shakl/kvadrat.py": "from .asos import Shakl\n\n\nclass Kvadrat(Shakl):\n    def __init__(self, a):\n        self.a = a\n\n    def yuza(self):\n        return self.a * self.a\n",
             "shakl/doira.py": "from .asos import Shakl\n\n\nclass Doira(Shakl):\n    def __init__(self, r):\n        self.r = r\n\n    def yuza(self):\n        return round(3.14 * self.r * self.r, 2)\n"}, lv=2),
    L("docs", "py-import", title="Import tizimi: package-relative imports"),
    L("docs", "py-modules", title="Intra-package References (6.4.2)"),
    L("docs", "py-importlib"),
    L("exercism", "grade-school", note="Kodni `maktab/` paketiga boʻlib, nisbiy importlar bilan yozib koʻring."),
])

# ---------------------------------------------------------------- 9.5
TOPIC("dir-funksiyasi", "dir() va introspeksiya", "Modul va obyekt ichida nima borligini bilish", 15, r'''
Notanish modul yoki obyekt bilan ishlayotganda "ichida nima bor?" degan savol tugʻiladi. Python bunga oʻzi javob beradi — bu **introspeksiya**.

## dir() — nomlar roʻyxati
```py
import math

nomlar = dir(math)
print(len(nomlar) > 40)
print([n for n in nomlar if n.startswith("s")])
```

`dir()` argumentsiz — joriy joydagi nomlar:

```py
a = 5
def salom():
    pass

print([n for n in dir() if not n.startswith("_")])
```

## Ochiq nomlarni ajratish
`_` bilan boshlanadiganlar — ichki nomlar:

```py
nomlar = [n for n in dir(str) if not n.startswith("_")]
print(len(nomlar), nomlar[:6])
```

## Oʻz modulingizni oʻrganish
```py file=vosita.py
"""Kichik yordamchi vositalar."""
VERSIYA = "2.1"
_ICHKI = 42


def kvadrat(x):
    """x ning kvadratini qaytaradi."""
    return x * x


class Hisob:
    """Oddiy hisob."""
```

```py
import vosita

print([n for n in dir(vosita) if not n.startswith("_")])
print(vosita.__doc__)
print(vosita.kvadrat.__doc__)
print(vosita.__name__)
```

## getattr, hasattr, callable
```py
import math

nom = "sqrt"
if hasattr(math, nom):
    f = getattr(math, nom)
    print(callable(f), f(49))

print(getattr(math, "yoq_funksiya", "topilmadi"))
```

## type, vars, help
| Funksiya | Nima qaytaradi |
|---|---|
| `type(x)` | obyekt turi |
| `vars(obj)` | obyekt atributlari lugʻati |
| `help(x)` | hujjat (docstring) — konsolda |
| `x.__doc__` | docstring matni |
| `x.__module__` | qaysi modulda yaratilgan |

> Konsolda ishlayotganda `dir()` va `help()` — eng yaxshi doʻstlaringiz. Internetsiz ham hujjatni oʻqiysiz.

## Esda tuting
- `dir(x)` — x ichidagi nomlar; `_` bilan boshlanmaganlari — ochiq API.
- `getattr(obj, "nom", standart)` — nomi satrda berilgan atributni olish.
''', [
    P('print("upper" in dir(str), "append" in dir(str))', "True True", "False True", "False False"),
    P('import math\nprint(getattr(math, "factorial")(5))', "factorial", "5", "Xato"),
    P('import math\nprint(getattr(math, "yoq", 0))', "None", "⚠ AttributeError", "yoq"),
    P('def f():\n    """Salom qaytaradi."""\n    return "salom"\nprint(f.__doc__)', "salom", "None", "f"),
    P('x = 1\ny = 2\nprint(sorted(n for n in dir() if len(n) == 1))', "['x']", "[1, 2]", "[]"),
    P('import math\nprint(callable(math.pi), callable(math.sqrt))', "True True", "False False", "True False"),
    P('class A:\n    def __init__(self):\n        self.p = 1\n        self._q = 2\nprint([k for k in vars(A()) if not k.startswith("_")])', "['p', '_q']", "['_q']", "[]"),
    Q("`dir(modul)` nima qaytaradi?", "Modul ichidagi nomlar roʻyxatini", "Modul joylashgan papkani", "Modulning versiyasini", "Modul matnini"),
    Q("Nomi satrda berilgan funksiyani moduldan olish usuli?", "getattr(modul, \"nom\")", "modul[\"nom\"]", "modul.get(\"nom\")", "import modul.nom"),
    F("Ochiq API", "`ochiq(obj)` — `dir(obj)` dan `_` bilan boshlanmagan nomlar sonini qaytarsin.",
      "import vosita\n\n\ndef ochiq(obj):\n    return len([n for n in dir(obj) if not n.startswith('_')])",
      "ochiq(object())", "ochiq(vosita)", "ochiq(vosita) < ochiq(str)",
      files={"vosita.py": "A = 1\nB = 2\n_C = 3\n\n\ndef f():\n    pass\n"}, starter="import vosita\n\n\ndef ochiq(obj):\n    # Kodingizni shu yerga yozing\n    pass\n", lv=1),
    F("Funksiyalar roʻyxati", "`funksiyalar(modul_nomi)` — moduldagi ochiq (`_` siz) va **chaqiriladigan** nomlarni alifbo tartibida qaytarsin.",
      "import importlib\n\n\ndef funksiyalar(modul_nomi):\n    m = importlib.import_module(modul_nomi)\n    return sorted(n for n in dir(m) if not n.startswith('_') and callable(getattr(m, n)))",
      'funksiyalar("vositalar")', 'len(funksiyalar("vositalar"))', '"VERSIYA" in funksiyalar("vositalar")',
      files={"vositalar.py": "VERSIYA = '1.0'\n\n\ndef qosh(a, b):\n    return a + b\n\n\ndef ayir(a, b):\n    return a - b\n\n\nclass Hisob:\n    pass\n\n\ndef _ichki():\n    pass\n"}),
    F("Buyruq bajaruvchi", "`bajar(buyruq, *args)` — `amallar` modulidan shu nomdagi funksiyani `getattr` bilan topib chaqirsin; topilmasa `\"nomaʼlum buyruq\"`.",
      "import amallar\n\n\ndef bajar(buyruq, *args):\n    f = getattr(amallar, buyruq, None)\n    if not callable(f):\n        return 'nomaʼlum buyruq'\n    return f(*args)",
      'bajar("qosh", 2, 3)', 'bajar("kopaytir", 4, 5)', 'bajar("bol", 1, 2)', 'bajar("NOM")',
      files={"amallar.py": "NOM = 'kalkulyator'\n\n\ndef qosh(a, b):\n    return a + b\n\n\ndef kopaytir(a, b):\n    return a * b\n"}, lv=2),
    F("Hujjatlar", "`hujjatlar(modul_nomi)` — moduldagi har bir ochiq funksiya uchun `{nom: docstringning birinchi qatori}` lugʻatini qaytarsin (docstring yoʻq boʻlsa `\"—\"`).",
      "import importlib\nimport inspect\n\n\ndef hujjatlar(modul_nomi):\n    m = importlib.import_module(modul_nomi)\n    natija = {}\n    for n in sorted(dir(m)):\n        f = getattr(m, n)\n        if not n.startswith('_') and inspect.isfunction(f):\n            natija[n] = (f.__doc__ or '—').strip().split('\\n')[0]\n    return natija",
      'hujjatlar("matn")', 'len(hujjatlar("matn"))', 'hujjatlar("matn")["sanash"]',
      files={"matn.py": "def teskari(s):\n    \"\"\"Satrni teskari qaytaradi.\n\n    Misol: teskari('abc') -> 'cba'\n    \"\"\"\n    return s[::-1]\n\n\ndef sanash(s):\n    return len(s)\n\n\ndef _yashirin():\n    \"\"\"Ichki.\"\"\"\n"}, lv=3),
    F("Atributlar", "`malumot(obj)` — obyektning `vars()` lugʻatidan faqat ochiq atributlarni alifbo tartibida `\"kalit=qiymat\"` satrlari roʻyxati qilib qaytarsin. Tekshiruv uchun `Talaba(ism, yosh)` sinfini ham yozing (`_id` yashirin atributi bilan).",
      "class Talaba:\n    def __init__(self, ism, yosh):\n        self.ism = ism\n        self.yosh = yosh\n        self._id = 1\n\n\ndef malumot(obj):\n    return [f'{k}={v}' for k, v in sorted(vars(obj).items()) if not k.startswith('_')]",
      'malumot(Talaba("Ali", 17))', 'malumot(Talaba("", 0))', "len(vars(Talaba('a', 1)))"),
    F("Qaysi modul?", "`qayerdan(obj)` — funksiya yoki sinfning `__module__` atributini qaytarsin.",
      "def qayerdan(obj):\n    return obj.__module__",
      "qayerdan(__import__('json').dumps)", "qayerdan(__import__('collections').Counter)", "qayerdan(__import__('yordam').f)",
      files={"yordam.py": "def f():\n    pass\n"}),
    F("Imzo", "`imzo(f)` — `inspect.signature` bilan funksiya parametrlari nomlarini roʻyxat qilib qaytarsin.",
      "import inspect\n\n\ndef imzo(f):\n    return list(inspect.signature(f).parameters)",
      "imzo(lambda a, b=2, *c, **d: 0)", "imzo(print)[:1]", "imzo(imzo)"),
    L("docs", "py-pydoc"),
    L("docs", "py-modules", title="The dir() Function (6.3)"),
    L("exercism", "bob", note="Yechimdan keyin `dir()` va `help()` bilan oʻz modulingizni oʻrganing."),
    L("docs", "py-importlib"),
])

# ---------------------------------------------------------------- 9.6
TOPIC("name-main", "Modulni skript sifatida ishga tushirish", "if __name__ == \"__main__\" va python -m", 20, r'''
Bitta fayl ikki xil ishlatilishi mumkin:
1. **Skript** sifatida: `python hisob.py` — fayl bevosita ishga tushiriladi;
2. **Modul** sifatida: `import hisob` — boshqa fayl uning funksiyalaridan foydalanadi.

Har bir modulda `__name__` oʻzgaruvchisi bor:
- fayl bevosita ishga tushirilsa → `"__main__"`;
- import qilinsa → modul nomi (`"hisob"`).

```py file=hisob.py
def kvadrat(x):
    return x * x

print("hisob.py: __name__ =", __name__)

if __name__ == "__main__":
    print("Bu qator faqat skript sifatida ishga tushganda chiqadi")
```

```py
import hisob

print("main.py: __name__ =", __name__)
print(hisob.kvadrat(9))
```

Natijaga qarang: `hisob.py` import qilinganda uning `if __name__ == "__main__":` ichidagi qator **bajarilmadi**.

## Toʻgʻri shablon
```py
def asosiy():
    ism = "Mirae"
    print(f"Salom, {ism}!")


if __name__ == "__main__":
    asosiy()
```

> Bu shablon har bir dasturda bor: modul import qilinganda "yon taʼsir" (print, fayl yozish, savol berish) boʻlmaydi, lekin skript sifatida ishlaydi.

## Modulni test bilan birga yozish
```py file=matn.py
def teskari(s):
    return s[::-1]


def palindrom(s):
    s = s.lower().replace(" ", "")
    return s == teskari(s)


if __name__ == "__main__":
    # Tez tekshiruvlar — faqat `python matn.py` da ishlaydi
    assert teskari("abc") == "cba"
    assert palindrom("Kiyik")
    print("Barcha tekshiruvlar oʻtdi ✓")
```

```py
from matn import palindrom

for s in ["Kiyik", "Olma", "A man a plan a canal Panama"]:
    print(s, "→", palindrom(s))
```

## python -m
```bash
python -m json.tool data.json      # JSON faylni chiroyli chiqaradi
python -m http.server 8000         # papkani veb-server qilib ochadi
python -m venv .venv               # virtual muhit yaratadi (11-boʻlim)
python -m pip install requests     # pip ni aynan shu Python bilan
python -m dokon.savat              # paket ichidagi modulni ishga tushirish
```

`-m` modulni `sys.path` dan topib, uni `__main__` sifatida ishga tushiradi. Paket ichidagi modullar uchun nisbiy importlar shunda toʻgʻri ishlaydi.

## __main__.py
Paket papkasida `__main__.py` boʻlsa, `python -m paket` aynan shu faylni ishga tushiradi.

## Esda tuting
- `if __name__ == "__main__":` — "faqat bevosita ishga tushirilganda".
- `python -m modul` — modulni skript sifatida, toʻgʻri import yoʻli bilan ishga tushirish.
''', [
    P('print(__name__)', "main", "__name__", "None"),
    P('if __name__ == "__main__":\n    print("A")\nelse:\n    print("B")', "B", "A\nB", "__main__"),
    P('import json\nprint(json.__name__)', "__main__", "json.py", "None"),
    P('def asosiy():\n    return 5\nif __name__ == "__main__":\n    print(asosiy() * 2)', "5", "None", "Hech narsa"),
    P('import collections.abc\nprint(collections.abc.__name__)', "abc", "collections", "__main__"),
    P('import sys\nprint(sys.argv[0] is not None, type(sys.argv).__name__)', "True tuple", "False list", "Xato", lv=2),
    P('x = __name__ == "__main__"\nprint(x and "skript" or "modul")', "modul", "True", "__main__"),
    Q("Fayl `import` qilinganda uning `__name__` qiymati qanday boʻladi?", "Modul nomi (masalan \"hisob\")", "\"__main__\"", "None", "Fayl yoʻli"),
    Q("`python -m json.tool fayl.json` nima qiladi?", "json.tool modulini skript sifatida ishga tushiradi", "json modulini oʻchiradi", "Yangi modul yaratadi", "Faylni JSON ga aylantirib saqlaydi"),
    F("Ikki rejimli modul", "`hisob.py` berilgan: import qilinganda hech narsa chiqarmasligi kerak, lekin hozir chiqaryapti! Uni ishlatib `natija(x)` = `hisob.kub(x)` ni qaytaring. `ekran()` funksiyasi `hisob` import qilinganda nima chiqqanini (`io.StringIO` + `contextlib.redirect_stdout` bilan ushlab, `importlib.reload`) qaytarsin.",
      "import contextlib\nimport importlib\nimport io\nimport hisob\n\n\ndef natija(x):\n    return hisob.kub(x)\n\n\ndef ekran():\n    buf = io.StringIO()\n    with contextlib.redirect_stdout(buf):\n        importlib.reload(hisob)\n    return buf.getvalue()",
      "natija(3)", "ekran()", "natija(-2)",
      files={"hisob.py": "def kub(x):\n    return x ** 3\n\n\nprint('test:', kub(2))\n"}, lv=3),
    F("Toʻgʻri shablon", "`tekshir(kod)` — berilgan modul matnida `if __name__ == \"__main__\":` qatori bormi (boʻsh joylar va qoʻshtirnoq turidan qatʼi nazar)? `True`/`False`.",
      "import re\n\n\ndef tekshir(kod):\n    return re.search(r'^if\\s+__name__\\s*==\\s*[\\'\\\"]__main__[\\'\\\"]\\s*:', kod, re.M) is not None",
      "tekshir('def f():\\n    pass\\n\\nif __name__ == \"__main__\":\\n    f()\\n')", "tekshir(\"if __name__=='__main__':\\n    pass\")", "tekshir('print(__name__)')", "tekshir('    if __name__ == \"__main__\":')", lv=2),
    PR("Skript", "Klassik shablon bilan dastur yozing: `asosiy()` funksiyasi kirishdan ism oʻqib, `Salom, ISM!` chiqarsin; u faqat `if __name__ == \"__main__\":` ichida chaqirilsin.",
      "def asosiy():\n    ism = input()\n    print(f'Salom, {ism}!')\n\n\nif __name__ == '__main__':\n    asosiy()",
      "Ali", "Mirae Academy", lv=1),
    F("Moduldan foydalanish", "`palindrom.py` moduli test kodlari bilan berilgan (ular `__main__` himoyasida). `nechta(sozlar)` — palindromlar sonini qaytarsin.",
      "from palindrom import palindrom\n\n\ndef nechta(sozlar):\n    return sum(palindrom(s) for s in sozlar)",
      'nechta(["kiyik", "olma", "anna", "Qoq"])', "nechta([])", 'nechta(["ab"])',
      files={"palindrom.py": "def palindrom(s):\n    s = s.lower()\n    return s == s[::-1]\n\n\nif __name__ == '__main__':\n    assert palindrom('Kiyik')\n    print('testlar oʻtdi')\n"}),
    PR("Buyruq satri simulyatsiyasi", "`sys.argv` ni qoʻlda `[\"kalk.py\", AMAL, A, B]` qilib bering (kirishdan bir qatorda `AMAL A B` oʻqiladi). `asosiy(argv)` funksiyasi `qosh`/`ayir`/`kopaytir` ni bajarib natijani chiqarsin; nomaʼlum amal — `xato`.",
      "import sys\n\n\ndef asosiy(argv):\n    amal, a, b = argv[1], int(argv[2]), int(argv[3])\n    if amal == 'qosh':\n        print(a + b)\n    elif amal == 'ayir':\n        print(a - b)\n    elif amal == 'kopaytir':\n        print(a * b)\n    else:\n        print('xato')\n\n\nif __name__ == '__main__':\n    sys.argv = ['kalk.py'] + input().split()\n    asosiy(sys.argv)",
      "qosh 2 3", "kopaytir 6 7", "bol 1 2", lv=2),
    F("Qaysi rejimda?", "`rejim()` — `yordamchi` modulining `REJIM` qiymatini qaytarsin. Modul ichida `REJIM` qiymati `__name__` ga qarab belgilanadi — import qilingani uchun javob `\"modul\"` boʻladi.",
      "import yordamchi\n\n\ndef rejim():\n    return yordamchi.REJIM",
      "rejim()", "rejim() == 'modul'", "len(rejim())",
      files={"yordamchi.py": "REJIM = 'skript' if __name__ == '__main__' else 'modul'\n"}),
    F("Modul sinovchisi", "`sinov.py` moduli `__main__` himoyasida testlar saqlaydi, lekin `ishlat()` funksiyasi ham bor. `hisobot()` — `sinov.ishlat()` natijasini va modulning `__name__` ini `(natija, nom)` kortej qilib qaytarsin.",
      "import sinov\n\n\ndef hisobot():\n    return (sinov.ishlat(), sinov.__name__)",
      "hisobot()", "hisobot()[1]", "type(hisobot()[0]).__name__",
      files={"sinov.py": "def ishlat():\n    return 42\n\n\nif __name__ == '__main__':\n    print('test rejimi')\n"}, lv=1),
    L("docs", "py-main"),
    L("docs", "py-argparse-howto", title="Argparse Tutorial — skriptga argumentlar"),
    L("exercism", "two-fer", note="Yechimga `if __name__ == \"__main__\":` bloki qoʻshib, skript sifatida ham sinang."),
    L("docs", "py-sys", title="sys.argv — buyruq satri argumentlari"),
])
