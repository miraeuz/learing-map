from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(11, "PyPI va virtual muhitlar", "pip, venv, Pipenv, bogʻliqliklar va paket nashr qilish", "🧪")

# ---------------------------------------------------------------- 11.1
TOPIC("pypi-pip", "PyPI va pip", "Dunyodagi 600 mingdan ortiq tayyor paketdan foydalanish", 20, r'''
**PyPI** (Python Package Index, pypi.org) — Python paketlarining rasmiy "doʻkoni". U yerda 600 mingdan ortiq tayyor kutubxona bor: `requests` (internet), `pandas` (jadvallar), `django` (veb-saytlar), `pillow` (rasmlar)...

**pip** — ularni oʻrnatadigan dastur. U Python bilan birga keladi.

## Asosiy buyruqlar
```bash
pip install requests              # oxirgi versiyani oʻrnatish
pip install requests==2.32.3      # aniq versiya
pip install "django>=5.0,<6"      # oraliq
pip install --upgrade requests    # yangilash
pip uninstall requests            # oʻchirish
pip list                          # oʻrnatilganlar roʻyxati
pip show requests                 # paket haqida maʼlumot
pip freeze > requirements.txt     # aniq versiyalarni faylga yozish
pip install -r requirements.txt   # fayldagilarni oʻrnatish
```

> Windows'da `pip` topilmasa: `py -m pip install ...`, macOS/Linux'da: `python3 -m pip install ...`. `python -m pip` — aynan qaysi Python uchun oʻrnatilayotganini aniq qiladi.

## Versiya raqamlari
Koʻpchilik paketlar **semantik versiyalash**ga amal qiladi: `KATTA.KICHIK.TUZATISH`

| Oʻzgarish | Misol | Maʼnosi |
|---|---|---|
| TUZATISH | 2.31.**0** → 2.31.**1** | xato tuzatildi, xavfsiz |
| KICHIK | 2.**31** → 2.**32** | yangi imkoniyat, eski kod ishlaydi |
| KATTA | **2**.x → **3**.0 | eski kod buzilishi mumkin! |

Versiyalarni toʻgʻri solishtirish — satr sifatida emas, **sonlar** sifatida:

```py
def versiya(s):
    return tuple(int(x) for x in s.split("."))

print("2.10.0" > "2.9.1")                       # satr: notoʻgʻri!
print(versiya("2.10.0") > versiya("2.9.1"))     # son: toʻgʻri
print(sorted(["1.10", "1.2", "1.9"], key=versiya))
```

## Paket nomi va import nomi
Baʼzan oʻrnatish nomi va import nomi farq qiladi:

| `pip install ...` | `import ...` |
|---|---|
| `pillow` | `PIL` |
| `beautifulsoup4` | `bs4` |
| `python-dotenv` | `dotenv` |
| `scikit-learn` | `sklearn` |

## Oʻrnatilgan paketni dasturda tekshirish
```py
import importlib.util

for nom in ["json", "sqlite3", "mirae_yoq_paket"]:
    bor = importlib.util.find_spec(nom) is not None
    print(f"{nom:<16}", "✓ bor" if bor else "✗ yoʻq — pip install kerak")
```

> `"requests"` ni ham roʻyxatga qoʻshib koʻring: kompyuteringizda `pip install requests` qilingan boʻlsa — `✓`, aks holda `✗`. Bu ilova ichidagi Python'da faqat standart kutubxona bor.

!> Paketlarni oʻrnatishdan oldin nomini tekshiring: PyPI'da mashhur paketlarga oʻxshash nomli zararli paketlar ("typosquatting") uchrab turadi — `reqeusts`, `djang0`...

## Esda tuting
- `pip install nom`, `pip install -r requirements.txt` — eng koʻp ishlatiladigan buyruqlar.
- Versiyalarni sonlar kortejiga aylantirib solishtiring.
''', [
    P('print("1.10" > "1.9")', "True", "Xato", "1.10"),
    P('v = lambda s: tuple(map(int, s.split(".")))\nprint(v("1.10") > v("1.9"))', "False", "(1, 10)", "Xato"),
    P('print(sorted(["2.0", "10.0", "9.1"]))', "['2.0', '9.1', '10.0']", "['10.0', '9.1', '2.0']", "Xato"),
    P('import importlib.util\nprint(importlib.util.find_spec("json") is None, importlib.util.find_spec("mirae_yoq_xyz") is None)', "True False", "False False", "True True"),
    P('print("requests==2.32.3".split("=="))', "['requests', '=', '2.32.3']", "('requests', '2.32.3')", "requests 2.32.3"),
    P('q = "django>=5.0"\ni = q.index(">=")\nprint(q[:i], q[i + 2:])', "django >=5.0", "django> 5.0", "Xato"),
    P('m = {"pillow": "PIL", "beautifulsoup4": "bs4"}\nprint(m.get("python-dotenv", "dotenv"))', "python-dotenv", "None", "⚠ KeyError"),
    Q("`pip install requests==2.32.3` nima qiladi?", "requests paketining aynan 2.32.3 versiyasini oʻrnatadi", "2.32.3 dan yangi versiyani oʻrnatadi", "requests ni oʻchiradi", "Versiyani tekshiradi, oʻrnatmaydi"),
    Q("Semantik versiyada `3.0.0` → `4.0.0` oʻzgarishi nimani bildiradi?", "Katta oʻzgarish — eski kod buzilishi mumkin", "Faqat xato tuzatildi", "Hech narsa oʻzgarmadi", "Yangi imkoniyat, lekin hammasi mos"),
    F("Versiyalarni solishtirish", "`taqqosla(a, b)` — `a < b` boʻlsa `-1`, teng boʻlsa `0`, katta boʻlsa `1` (`\"1.2\" == \"1.2.0\"` deb hisoblang).",
      "def taqqosla(a, b):\n    x = [int(t) for t in a.split('.')]\n    y = [int(t) for t in b.split('.')]\n    n = max(len(x), len(y))\n    x += [0] * (n - len(x))\n    y += [0] * (n - len(y))\n    return (x > y) - (x < y)",
      'taqqosla("1.10", "1.9")', 'taqqosla("1.2", "1.2.0")', 'taqqosla("0.9.9", "1.0")', 'taqqosla("2.0.1", "2.0.0")', lv=1),
    F("Eng yangi versiya", "`eng_yangi(versiyalar)` — roʻyxatdan eng katta versiyani qaytarsin.",
      "def eng_yangi(versiyalar):\n    return max(versiyalar, key=lambda s: tuple(int(x) for x in s.split('.')))",
      'eng_yangi(["1.9", "1.10", "1.2.3"])', 'eng_yangi(["0.1"])', 'eng_yangi(["2.0.0", "10.0", "9.99.99"])', lv=1),
    F("Versiyani oshirish", "`oshir(versiya, qism)` — `qism` `\"major\"`, `\"minor\"` yoki `\"patch\"`: `\"1.4.2\"` → major `\"2.0.0\"`, minor `\"1.5.0\"`, patch `\"1.4.3\"`.",
      "def oshir(versiya, qism):\n    a, b, c = map(int, versiya.split('.'))\n    if qism == 'major':\n        return f'{a + 1}.0.0'\n    if qism == 'minor':\n        return f'{a}.{b + 1}.0'\n    if qism == 'patch':\n        return f'{a}.{b}.{c + 1}'\n    raise ValueError(qism)",
      'oshir("1.4.2", "major")', 'oshir("1.4.2", "minor")', 'oshir("1.4.2", "patch")', 'oshir("0.9.9", "minor")', 'oshir("1.0.0", "build")', lv=2),
    F("pip show tahlili", "`malumot(matn)` — `pip show` chiqishidan (`Kalit: qiymat` qatorlari) `{\"Name\", \"Version\", \"Requires\"}` ni qaytarsin; `Requires` — vergul bilan ajratilgan roʻyxat (boʻsh boʻlsa `[]`).",
      "def malumot(matn):\n    d = {}\n    for q in matn.splitlines():\n        if ': ' in q:\n            k, v = q.split(': ', 1)\n            d[k] = v.strip()\n        elif q.endswith(':'):\n            d[q[:-1]] = ''\n    req = [x.strip() for x in d.get('Requires', '').split(',') if x.strip()]\n    return {'Name': d.get('Name'), 'Version': d.get('Version'), 'Requires': req}",
      'malumot("Name: requests\\nVersion: 2.32.3\\nSummary: HTTP\\nRequires: certifi, idna, urllib3\\n")', 'malumot("Name: six\\nVersion: 1.16.0\\nRequires:\\n")', 'malumot("Name: x\\n")', lv=2,
      hint="Qator oxirida `:` boʻlsa qiymat boʻsh."),
    F("Import nomi", "`import_nomi(paket)` — pip nomidan import nomini qaytarsin: maxsus lugʻat (`pillow→PIL`, `beautifulsoup4→bs4`, `python-dotenv→dotenv`, `scikit-learn→sklearn`, `pyyaml→yaml`), aks holda nomdagi `-` larni `_` ga almashtirib, kichik harflarda.",
      "def import_nomi(paket):\n    maxsus = {'pillow': 'PIL', 'beautifulsoup4': 'bs4', 'python-dotenv': 'dotenv', 'scikit-learn': 'sklearn', 'pyyaml': 'yaml'}\n    p = paket.lower()\n    return maxsus.get(p, p.replace('-', '_'))",
      'import_nomi("Pillow")', 'import_nomi("python-dotenv")', 'import_nomi("Flask-Login")', 'import_nomi("requests")'),
    F("Oʻrnatilganmi", "`yetishmaydi(paketlar)` — roʻyxatdagi qaysi import nomlari mavjud emasligini (`importlib.util.find_spec`) aniqlab, ularni qaytarsin.",
      "import importlib.util\n\n\ndef yetishmaydi(paketlar):\n    return [p for p in paketlar if importlib.util.find_spec(p) is None]",
      'yetishmaydi(["json", "math", "mirae_yoq_1"])', "yetishmaydi([])", 'yetishmaydi(["yordam", "csv"])',
      files={"yordam.py": "X = 1\n"}),
    F("Typosquatting", "`shubhali(nom, mashhurlar)` — nom mashhur paketlardan biriga juda oʻxshash (bitta harf farq yoki ikki qoʻshni harf joyi almashgan), lekin aynan oʻzi boʻlmasa — oʻsha mashhur nomni qaytarsin; aks holda `None`.",
      "def shubhali(nom, mashhurlar):\n    def yaqin(a, b):\n        if a == b:\n            return False\n        if len(a) == len(b):\n            farq = [i for i in range(len(a)) if a[i] != b[i]]\n            if len(farq) == 1:\n                return True\n            if len(farq) == 2 and farq[1] == farq[0] + 1 and a[farq[0]] == b[farq[1]] and a[farq[1]] == b[farq[0]]:\n                return True\n        return False\n    for m in mashhurlar:\n        if yaqin(nom, m):\n            return m\n    return None",
      'shubhali("reqeusts", ["requests", "django"])', 'shubhali("djang0", ["requests", "django"])', 'shubhali("requests", ["requests"])', 'shubhali("flask", ["django"])', lv=3),
    L("docs", "py-installing"),
    L("docs", "pip-user-guide"),
    L("docs", "pkg-installing"),
    L("exercism", "bob", note="Birinchi tashqi paketingizni (masalan `pytest`) oʻrnatib, Exercism testlarini oʻzingiz ishga tushiring."),
])

# ---------------------------------------------------------------- 11.2
TOPIC("venv", "Virtual muhitlar (venv)", "Har bir loyihaga — alohida paketlar toʻplami", 20, r'''
Tasavvur qiling: A loyiha `django 4.2` ni, B loyiha esa `django 5.2` ni talab qiladi. Ikkalasini bitta kompyuterga global oʻrnatib boʻlmaydi. Yechim — **virtual muhit**: har bir loyiha uchun alohida "Python qutisi".

```text
loyiha_a/
├── .venv/          ← faqat shu loyihaning paketlari (django 4.2)
└── main.py
loyiha_b/
├── .venv/          ← boshqa paketlar (django 5.2)
└── main.py
```

## Yaratish va faollashtirish
```bash
# yaratish (bir marta)
python -m venv .venv

# faollashtirish
.venv\Scripts\activate          # Windows (cmd / PowerShell)
source .venv/bin/activate       # macOS / Linux

# endi pip shu muhitga oʻrnatadi
pip install requests

# chiqish
deactivate
```

> Faollashgan muhitda terminal boshida `(.venv)` yozuvi paydo boʻladi.

## Python qaysi muhitda ishlayapti?
```py
import sys

print(sys.prefix == sys.base_prefix)    # True — global Python, False — venv ichida
print("venv ichida" if sys.prefix != sys.base_prefix else "global Python")
```

| Atribut | Maʼnosi |
|---|---|
| `sys.executable` | ishlayotgan python fayli |
| `sys.prefix` | joriy muhit (venv boʻlsa — `.venv`) |
| `sys.base_prefix` | asosiy Python |

## VS Code'da
1. Loyiha papkasini oching;
2. `Ctrl+Shift+P` → **Python: Create Environment** → **Venv**;
3. Oʻng pastdagi Python versiyasini bosib, `.venv` ni tanlang (**Python: Select Interpreter**);
4. Yangi terminal ochsangiz, muhit avtomatik faollashadi.

## Qoidalar
- `.venv` ni **Git'ga qoʻshmang** — `.gitignore` ga yozing; oʻrniga `requirements.txt` ni saqlang.
- Muhitni "koʻchirib" boʻlmaydi — yangi joyda qayta yarating: `python -m venv .venv && pip install -r requirements.txt`.
- Har bir loyiha — oʻz muhiti.

```text
# .gitignore
.venv/
__pycache__/
*.pyc
.env
```

## Esda tuting
- `python -m venv .venv` → faollashtirish → `pip install ...`.
- `sys.prefix != sys.base_prefix` — virtual muhit ichida ekanini bildiradi.
''', [
    P('import sys\nprint(type(sys.prefix).__name__)', "path", "list", "None"),
    P('import sys\nprint(sys.prefix == sys.base_prefix)', "False", "venv", "Xato"),
    P('import os\nprint(os.path.join(".venv", "Scripts", "activate").replace("\\\\", "/"))', ".venv\\Scripts\\activate", "activate", "Xato"),
    P('qatorlar = [".venv/", "__pycache__/", "*.pyc"]\nprint(".venv/" in qatorlar, len(qatorlar))', "True 2", "False 3", "Xato"),
    P('import sys\nprint(callable(sys.executable))', "True", "python", "Xato"),
    P('print("(.venv) C:\\\\loyiha>".startswith("(.venv)"))', "False", "(.venv)", "Xato"),
    P('import sysconfig\nprint(type(sysconfig.get_paths()).__name__)', "list", "str", "None", lv=2),
    Q("Virtual muhitning asosiy vazifasi?", "Har bir loyiha uchun alohida, bir-biriga xalaqit bermaydigan paketlar toʻplami", "Python'ni tezlashtirish", "Kodni shifrlash", "Internet aloqasini tezlashtirish"),
    Q("`.venv` papkasini Git'ga qoʻshish kerakmi?", "Yoʻq — .gitignore ga yoziladi, oʻrniga requirements.txt saqlanadi", "Ha, doim", "Faqat Windows'da", "Faqat birinchi commit'da"),
    F("Faollashtirish buyrugʻi", "`faollashtir(tizim, papka=\".venv\")` — `\"windows\"` uchun `papka\\\\Scripts\\\\activate`, `\"linux\"` va `\"macos\"` uchun `source papka/bin/activate`; boshqasi — `ValueError`.",
      "def faollashtir(tizim, papka='.venv'):\n    if tizim == 'windows':\n        return papka + '\\\\Scripts\\\\activate'\n    if tizim in ('linux', 'macos'):\n        return f'source {papka}/bin/activate'\n    raise ValueError(tizim)",
      'faollashtir("windows")', 'faollashtir("macos")', 'faollashtir("linux", "env")', 'faollashtir("android")', lv=1),
    F("Venv ichidami", "`venvmi(prefix, base_prefix)` — ikki yoʻl farq qilsa `True`.",
      "def venvmi(prefix, base_prefix):\n    return prefix != base_prefix",
      'venvmi("/loyiha/.venv", "/usr")', 'venvmi("/usr", "/usr")', "venvmi(__import__('sys').prefix, __import__('sys').base_prefix)", lv=1),
    F("Python yoʻli", "`python_yoli(papka, tizim)` — venv ichidagi python fayli yoʻli: Windows → `papka/Scripts/python.exe`, boshqalar → `papka/bin/python` (`pathlib` + `as_posix`).",
      "from pathlib import PurePosixPath\n\n\ndef python_yoli(papka, tizim):\n    if tizim == 'windows':\n        return PurePosixPath(papka, 'Scripts', 'python.exe').as_posix()\n    return PurePosixPath(papka, 'bin', 'python').as_posix()",
      'python_yoli(".venv", "windows")', 'python_yoli(".venv", "linux")', 'python_yoli("/home/ali/loyiha/env", "macos")'),
    F("gitignore", "`gitignore_tekshir(matn)` — `.gitignore` matnida `.venv/` (yoki `.venv`), `__pycache__/` va `.env` bormi? Yetishmaganlarini roʻyxat qilib qaytarsin.",
      "def gitignore_tekshir(matn):\n    q = {x.strip().rstrip('/') for x in matn.splitlines() if x.strip() and not x.strip().startswith('#')}\n    kerak = ['.venv', '__pycache__', '.env']\n    return [k for k in kerak if k not in q]",
      'gitignore_tekshir(".venv/\\n__pycache__/\\n.env\\n")', 'gitignore_tekshir("# boʻsh\\n")', 'gitignore_tekshir(".venv\\n*.pyc\\n")', lv=2),
    F("Loyiha tayyorlash", "`buyruqlar(tizim, paketlar)` — yangi loyiha uchun terminal buyruqlari roʻyxati: venv yaratish (`python -m venv .venv`), faollashtirish (tizimga mos), har bir paket uchun `pip install nom`, oxirida `pip freeze > requirements.txt`.",
      "def buyruqlar(tizim, paketlar):\n    act = '.venv\\\\Scripts\\\\activate' if tizim == 'windows' else 'source .venv/bin/activate'\n    return ['python -m venv .venv', act] + [f'pip install {p}' for p in paketlar] + ['pip freeze > requirements.txt']",
      'buyruqlar("linux", ["requests"])', 'buyruqlar("windows", ["django", "pillow"])', 'len(buyruqlar("macos", []))', lv=2),
    F("Muhitlar jadvali", "`toqnashuv(loyihalar)` — `{loyiha: {paket: versiya}}` dan bir xil paketning har xil versiyalari kerak boʻlgan paketlarni `{paket: [versiyalar (saralangan)]}` qilib qaytarsin. (Aynan shu holatda virtual muhit zarur!)",
      "def toqnashuv(loyihalar):\n    d = {}\n    for paketlar in loyihalar.values():\n        for p, v in paketlar.items():\n            d.setdefault(p, set()).add(v)\n    return {p: sorted(v) for p, v in sorted(d.items()) if len(v) > 1}",
      'toqnashuv({"blog": {"django": "4.2", "pillow": "10.0"}, "dokon": {"django": "5.2", "pillow": "10.0"}})', "toqnashuv({})", 'toqnashuv({"a": {"x": "1"}, "b": {"x": "1"}})', lv=3),
    F("Interpreter tanlash", "`tanla(yollar)` — VS Code kabi: roʻyxatdagi yoʻllardan birinchisi `.venv` ichida boʻlganini, boʻlmasa birinchisini qaytarsin; roʻyxat boʻsh boʻlsa `None`.",
      "def tanla(yollar):\n    for y in yollar:\n        if '.venv' in y.replace('\\\\', '/').split('/'):\n            return y\n    return yollar[0] if yollar else None",
      'tanla(["/usr/bin/python3", "/loyiha/.venv/bin/python"])', 'tanla(["C:\\\\Python314\\\\python.exe"])', "tanla([])"),
    L("docs", "py-venv-tutorial"),
    L("docs", "vscode-envs"),
    L("docs", "pkg-venv-guide"),
    L("docs", "py-venv"),
])

# ---------------------------------------------------------------- 11.3
TOPIC("pipenv", "Pipenv va Pipfile", "Muhit va bogʻliqliklarni bitta vosita bilan boshqarish", 15, r'''
**Pipenv** — `pip` va `venv` ni bitta qulay vositaga birlashtiradi: muhitni avtomatik yaratadi, paketlarni `Pipfile` ga yozadi va aniq versiyalarni `Pipfile.lock` da qulflaydi.

```bash
pip install pipenv            # bir marta

pipenv install requests       # muhit + paket + Pipfile
pipenv install pytest --dev   # faqat ishlab chiqish uchun
pipenv shell                  # muhitga kirish
pipenv run python main.py     # muhitda buyruq bajarish
pipenv install                # Pipfile dagilarni oʻrnatish (yangi kompyuterda)
pipenv graph                  # bogʻliqliklar daraxti
```

## Pipfile — TOML formatida
```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
django = ">=5.0,<6.0"

[dev-packages]
pytest = "*"

[requires]
python_version = "3.12"
```

TOML'ni Python oʻzi oʻqiy oladi — `tomllib` moduli bilan:

```py
import tomllib

pipfile = """
[packages]
requests = "*"
django = ">=5.0,<6.0"

[dev-packages]
pytest = "*"

[requires]
python_version = "3.12"
"""
d = tomllib.loads(pipfile)
print(list(d["packages"]))
print(d["packages"]["django"])
print(d["requires"]["python_version"])
```

## Pipfile va Pipfile.lock
| Fayl | Nima saqlaydi | Kim yozadi |
|---|---|---|
| `Pipfile` | qaysi paketlar kerak (taxminiy talablar) | siz |
| `Pipfile.lock` | **aniq** versiyalar va xesh summalar | Pipenv avtomatik |

> Lock-fayl tufayli jamoadagi hamma va server **aynan bir xil** versiyalarni oʻrnatadi. Ikkala faylni ham Git'ga qoʻshing.

## Zamonaviy alternativalar
| Vosita | Fayl |
|---|---|
| pip + venv | `requirements.txt` |
| Pipenv | `Pipfile`, `Pipfile.lock` |
| Poetry | `pyproject.toml`, `poetry.lock` |
| uv | `pyproject.toml`, `uv.lock` (juda tez) |

## Esda tuting
- `pipenv install nom` — muhit, oʻrnatish va Pipfile — bitta buyruqda.
- `[packages]` — ishlab chiqarish, `[dev-packages]` — faqat dasturchi uchun.
''', [
    P('import tomllib\nprint(tomllib.loads(\'a = 5\\nb = "x"\'))', "{'a': '5', 'b': 'x'}", "a = 5", "Xato"),
    P('import tomllib\nd = tomllib.loads(\'[packages]\\nrequests = "*"\')\nprint(d["packages"]["requests"])', "requests", "None", "Xato"),
    P('import tomllib\nd = tomllib.loads("[a]\\nx = 1\\n[b]\\ny = 2")\nprint(sorted(d), d["b"]["y"])', "['x', 'y'] 2", "{'a', 'b'} 2", "Xato"),
    P('import tomllib\nprint(tomllib.loads("v = true")["v"])', "true", "1", "Xato"),
    P('import tomllib\ntomllib.loads("a = ")', "None", "{}", "⚠ ValueError"),
    P('import tomllib\nprint(tomllib.loads("s = [1, 2, 3]")["s"][-1])', "[1, 2, 3]", "1", "Xato"),
    P('import tomllib\nprint(type(tomllib.loads("[x]")["x"]).__name__)', "list", "str", "Xato", lv=2),
    Q("Pipfile.lock nima uchun kerak?", "Hamma joyda aynan bir xil (aniq) versiyalar oʻrnatilishi uchun", "Paketlarni shifrlash uchun", "Faqat Windows uchun", "Muhitni oʻchirish uchun"),
    Q("Faqat dasturchiga kerak paket (masalan pytest) qanday qoʻshiladi?", "pipenv install pytest --dev", "pipenv install pytest", "pip uninstall pytest", "pipenv dev pytest"),
    F("Pipfile oʻqish", "`paketlar(matn)` — Pipfile matnidan `[packages]` dagi paket nomlarini alifbo boʻyicha qaytarsin (boʻlim yoʻq boʻlsa `[]`).",
      "import tomllib\n\n\ndef paketlar(matn):\n    return sorted(tomllib.loads(matn).get('packages', {}))",
      "paketlar('[packages]\\nrequests = \"*\"\\ndjango = \">=5\"\\n')", "paketlar('[dev-packages]\\npytest = \"*\"\\n')", "paketlar('')", lv=1),
    F("Dev paketlar", "`hisobot(matn)` — `{\"asosiy\": N, \"dev\": M, \"python\": versiya yoki None}` qaytarsin.",
      "import tomllib\n\n\ndef hisobot(matn):\n    d = tomllib.loads(matn)\n    return {'asosiy': len(d.get('packages', {})), 'dev': len(d.get('dev-packages', {})), 'python': d.get('requires', {}).get('python_version')}",
      "hisobot('[packages]\\na = \"*\"\\nb = \"*\"\\n[dev-packages]\\npytest = \"*\"\\n[requires]\\npython_version = \"3.12\"\\n')", "hisobot('')", "hisobot('[packages]\\nx = \"==1.0\"\\n')"),
    F("Pipfile yozish", "`pipfile(paketlar, dev)` — ikki lugʻatdan TOML matnini yasasin: `[packages]` va `[dev-packages]` boʻlimlari, har qatorda `nom = \"talab\"` (nomlar alifbo boʻyicha), boʻlimlar orasida boʻsh qator.",
      "def pipfile(paketlar, dev):\n    q = ['[packages]'] + [f'{k} = \"{v}\"' for k, v in sorted(paketlar.items())]\n    q += ['', '[dev-packages]'] + [f'{k} = \"{v}\"' for k, v in sorted(dev.items())]\n    return '\\n'.join(q) + '\\n'",
      'pipfile({"requests": "*", "django": ">=5.0"}, {"pytest": "*"})', "pipfile({}, {})", "__import__('tomllib').loads(pipfile({'a': '1'}, {}))", lv=2),
    F("Toʻgʻri TOML'mi", "`yaroqli(matn)` — `tomllib.TOMLDecodeError` boʻlmasa `True`.",
      "import tomllib\n\n\ndef yaroqli(matn):\n    try:\n        tomllib.loads(matn)\n        return True\n    except tomllib.TOMLDecodeError:\n        return False",
      "yaroqli('a = 1')", "yaroqli('a = ')", "yaroqli('[x]\\ny = \"z\"')", "yaroqli('[x]\\n[x]')", lv=1),
    F("Lock fayl", "`qulflangan(lock_json)` — Pipfile.lock (JSON) dan `default` boʻlimidagi `{paket: versiya}` ni qaytarsin; versiya `\"==2.32.3\"` dan `\"2.32.3\"` ga tozalansin.",
      "import json\n\n\ndef qulflangan(lock_json):\n    d = json.loads(lock_json).get('default', {})\n    return {k: v['version'].lstrip('=') for k, v in sorted(d.items())}",
      'qulflangan(\'{"default": {"requests": {"version": "==2.32.3"}, "idna": {"version": "==3.7"}}, "develop": {}}\')', "qulflangan('{\"default\": {}}')", "qulflangan('{}')", lv=2),
    F("Vosita tanlash", "`fayllar(vosita)` — vosita nomiga mos fayllar roʻyxati: `pip` → `[\"requirements.txt\"]`, `pipenv` → `[\"Pipfile\", \"Pipfile.lock\"]`, `poetry` → `[\"pyproject.toml\", \"poetry.lock\"]`, `uv` → `[\"pyproject.toml\", \"uv.lock\"]`; nomaʼlum — `[]`.",
      "def fayllar(vosita):\n    return {'pip': ['requirements.txt'], 'pipenv': ['Pipfile', 'Pipfile.lock'], 'poetry': ['pyproject.toml', 'poetry.lock'], 'uv': ['pyproject.toml', 'uv.lock']}.get(vosita, [])",
      'fayllar("pipenv")', 'fayllar("uv")', 'fayllar("conda")'),
    F("Python versiyasi mosmi", "`mos(talab, joriy)` — Pipfile dagi `python_version` (`\"3.12\"`) joriy versiya (`\"3.12.4\"`) bilan katta va kichik raqami boʻyicha mos kelsa `True`.",
      "def mos(talab, joriy):\n    return joriy.split('.')[:2] == talab.split('.')[:2]",
      'mos("3.12", "3.12.4")', 'mos("3.12", "3.13.0")', 'mos("3.14", "3.14.2")', lv=1),
    L("docs", "pipenv-basics"),
    L("docs", "pkg-managing"),
    L("docs", "pkg-pyproject", title="pyproject.toml — zamonaviy loyiha fayli"),
    L("docs", "py-installing"),
])

# ---------------------------------------------------------------- 11.4
TOPIC("bogliqliklar", "Bogʻliqliklarni boshqarish", "requirements.txt, versiya talablari va pip freeze", 20, r'''
Loyihangiz ishlashi uchun kerak boʻlgan paketlar — **bogʻliqliklar** (dependencies). Ularni toʻgʻri boshqarish — "mening kompyuterimda ishlaydi-ku!" muammosining yechimi.

## requirements.txt
```text
# Asosiy
django>=5.0,<6.0
requests==2.32.3
pillow~=10.4

# Ixtiyoriy izoh va boʻsh qatorlar mumkin
python-dotenv
```

```bash
pip install -r requirements.txt
pip freeze > requirements.txt     # joriy muhitdagi hamma narsa aniq versiyalar bilan
```

## Versiya talablari
| Talab | Maʼnosi | Misol mos keladi |
|---|---|---|
| `==2.32.3` | aynan shu | 2.32.3 |
| `>=5.0` | kamida | 5.0, 5.2, 6.1 |
| `<6.0` | dan kichik | 5.9 |
| `>=5.0,<6.0` | oraliq | 5.x |
| `~=10.4` | "mos keluvchi": `>=10.4, <11.0` | 10.4, 10.9 |
| `!=3.0` | shundan tashqari | 2.9, 3.1 |
| (yoʻq) | istalgan | — |

Talabni tekshirishni oʻzimiz yozib koʻramiz:

```py
def v(s):
    return tuple(int(x) for x in s.split("."))

def mosmi(versiya, talab):
    for shart in talab.split(","):
        shart = shart.strip()
        for op in ("==", ">=", "<=", "!=", ">", "<"):
            if shart.startswith(op):
                chap, ong = v(versiya), v(shart[len(op):])
                if not {"==": chap == ong, ">=": chap >= ong, "<=": chap <= ong,
                        "!=": chap != ong, ">": chap > ong, "<": chap < ong}[op]:
                    return False
                break
    return True

for ver in ["4.2", "5.0", "5.2.1", "6.0"]:
    print(ver, mosmi(ver, ">=5.0,<6.0"))
```

## Qaysi biri yaxshi: aniq yoki erkin?
| Yondashuv | Plyus | Minus |
|---|---|---|
| `==` (qulflash) | hamma joyda bir xil | yangilanishlar va xavfsizlik tuzatishlari kelmaydi |
| `>=` (erkin) | yangi versiyalar | kutilmaganda buzilishi mumkin |

> Amaliy qoida: **ilova** (sayt, bot) uchun versiyalarni qulflang (`pip freeze`, lock-fayl). **Kutubxona** yozsangiz — keng oraliq bering (`>=5.0,<6`).

## Ikki fayl uslubi
```text
requirements.txt       ← faqat ishlab chiqarish uchun
requirements-dev.txt   ← -r requirements.txt + pytest, black, ...
```

## Bogʻliqliklar daraxti
Bitta paket boshqalarini ham olib keladi: `requests` → `urllib3`, `idna`, `certifi`, `charset-normalizer`. `pip freeze` ularni ham yozadi.

## Esda tuting
- `pip freeze > requirements.txt` — joriy holatni saqlash; `pip install -r` — tiklash.
- `~=` — "shu katta versiya ichida yangilanaver" degani.
''', [
    P('q = "django>=5.0,<6.0"\nprint(q.split(","))', "['django', '>=5.0', '<6.0']", "['django>=5.0,<6.0']", "('django>=5.0', '<6.0')"),
    P('qatorlar = ["# izoh", "", "requests==2.32.3", "django"]\nprint([q for q in qatorlar if q and not q.startswith("#")])', "['requests==2.32.3']", "['# izoh', 'requests==2.32.3', 'django']", "2"),
    P('v = lambda s: tuple(map(int, s.split(".")))\nprint(v("5.2.1") >= v("5.0") and v("5.2.1") < v("6.0"))', "False", "(5, 2, 1)", "Xato"),
    P('import re\nprint(re.split(r"(==|>=|<=|~=|!=|<|>)", "pillow~=10.4", maxsplit=1))', "['pillow', '10.4']", "['pillow~=10.4']", "Xato"),
    P('print("~=10.4".lstrip("~="))', "~=10.4", "10.", "=10.4"),
    P('talablar = {"a": "==1", "b": ">=2"}\nprint(sum(1 for t in talablar.values() if t.startswith("==")))', "2", "0", "Xato"),
    P('freeze = "Django==5.2\\nrequests==2.32.3\\n"\nprint(dict(q.split("==") for q in freeze.split()))', "['Django', '5.2', 'requests', '2.32.3']", "Django==5.2", "Xato"),
    Q("`pillow~=10.4` qaysi versiyalarga ruxsat beradi?", ">=10.4 va <11.0", "Faqat 10.4", ">=10.4 (cheksiz)", "10.4 dan kichik"),
    Q("Ilova (masalan Telegram bot) uchun versiyalarni qanday koʻrsatish tavsiya etiladi?", "Aniq qulflash (== yoki lock-fayl)", "Hech qanday versiya koʻrsatmaslik", "Faqat eng eski versiyalar", "Har kuni qoʻlda oʻzgartirish"),
    F("requirements tahlili", "`tahlil(matn)` — requirements matnidan `{paket: talab}` lugʻati (izoh va boʻsh qatorlar tashlansin; talab yoʻq boʻlsa `\"*\"`; paket nomi kichik harfda).",
      "import re\n\n\ndef tahlil(matn):\n    d = {}\n    for q in matn.splitlines():\n        q = q.split('#')[0].strip()\n        if not q:\n            continue\n        m = re.match(r'([A-Za-z0-9_.-]+)\\s*(.*)', q)\n        d[m.group(1).lower()] = m.group(2).strip() or '*'\n    return d",
      'tahlil("# asosiy\\nDjango>=5.0,<6.0\\nrequests==2.32.3\\n\\npython-dotenv  # sozlamalar\\n")', 'tahlil("")', 'tahlil("pillow~=10.4")', lv=1),
    F("Talabga mosmi", "`mosmi(versiya, talab)` — `==`, `!=`, `>=`, `<=`, `>`, `<` shartlari (vergul bilan bir nechta) va `*` uchun tekshirsin.",
      "def mosmi(versiya, talab):\n    if talab.strip() in ('', '*'):\n        return True\n    v = lambda s: tuple(int(x) for x in s.split('.'))\n    amal = {'==': lambda a, b: a == b, '!=': lambda a, b: a != b, '>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b, '>': lambda a, b: a > b, '<': lambda a, b: a < b}\n    for shart in talab.split(','):\n        shart = shart.strip()\n        for op in ('==', '!=', '>=', '<=', '>', '<'):\n            if shart.startswith(op):\n                if not amal[op](v(versiya), v(shart[len(op):])):\n                    return False\n                break\n    return True",
      'mosmi("5.2.1", ">=5.0,<6.0")', 'mosmi("6.0", ">=5.0,<6.0")', 'mosmi("3.0", "!=3.0")', 'mosmi("1.0", "*")', 'mosmi("2.32.3", "==2.32.3")', lv=2),
    F("Mos keluvchi (~=)", "`mos_keluvchi(versiya, talab)` — `~=X.Y` → `>=X.Y` va `<(X+1)`; `~=X.Y.Z` → `>=X.Y.Z` va `<X.(Y+1)`.",
      "def mos_keluvchi(versiya, talab):\n    v = lambda s: tuple(int(x) for x in s.split('.'))\n    asos = v(talab.lstrip('~='))\n    yuqori = asos[:-2] + (asos[-2] + 1,)\n    return v(versiya) >= asos and v(versiya)[:len(yuqori)] < yuqori",
      'mos_keluvchi("10.9", "~=10.4")', 'mos_keluvchi("11.0", "~=10.4")', 'mos_keluvchi("2.32.9", "~=2.32.3")', 'mos_keluvchi("2.33.0", "~=2.32.3")', lv=3),
    F("Freeze farqi", "`farq(eski, yangi)` — ikki `pip freeze` matnini solishtirib `{\"qoshildi\": [...], \"olib_tashlandi\": [...], \"yangilandi\": [\"nom: eski→yangi\"]}` qaytarsin (har biri alifbo boʻyicha).",
      "def farq(eski, yangi):\n    o = lambda m: dict(q.split('==') for q in m.split())\n    a, b = o(eski), o(yangi)\n    return {'qoshildi': sorted(set(b) - set(a)), 'olib_tashlandi': sorted(set(a) - set(b)), 'yangilandi': sorted(f'{k}: {a[k]}→{b[k]}' for k in set(a) & set(b) if a[k] != b[k])}",
      'farq("django==5.1\\nrequests==2.31.0\\nsix==1.16.0\\n", "django==5.2\\nrequests==2.31.0\\npillow==10.4.0\\n")', 'farq("", "a==1")', 'farq("a==1", "a==1")', lv=2),
    F("Qulflash", "`qulfla(talablar, mavjud)` — `{paket: talab}` va `{paket: [versiyalar]}` dan har bir paket uchun talabga mos **eng yangi** versiyani tanlab `[\"paket==versiya\"]` (alifbo boʻyicha); mos versiya boʻlmasa `ValueError`. Talablar faqat `>=` va `<` dan iborat.",
      "def qulfla(talablar, mavjud):\n    v = lambda s: tuple(int(x) for x in s.split('.'))\n    def mos(ver, talab):\n        for sh in filter(None, (x.strip() for x in talab.split(','))):\n            if sh.startswith('>=') and not v(ver) >= v(sh[2:]):\n                return False\n            if sh.startswith('<') and not v(ver) < v(sh[1:]):\n                return False\n        return True\n    natija = []\n    for p, t in sorted(talablar.items()):\n        ok = [x for x in mavjud.get(p, []) if mos(x, t)]\n        if not ok:\n            raise ValueError(p)\n        natija.append(f'{p}=={max(ok, key=v)}')\n    return natija",
      'qulfla({"django": ">=5.0,<6.0", "requests": ">=2.0"}, {"django": ["4.2", "5.1", "5.2", "6.0"], "requests": ["2.31.0", "2.32.3"]})', 'qulfla({"x": ">=9"}, {"x": ["1.0"]})', "qulfla({}, {})", lv=3),
    F("Dev fayl", "`dev_talablar(asosiy, qoshimcha)` — `requirements-dev.txt` matnini yasasin: birinchi qator `-r requirements.txt`, keyin qoʻshimcha paketlar alifbo boʻyicha (asosiy roʻyxatda borlarini takrorlamang).",
      "def dev_talablar(asosiy, qoshimcha):\n    bor = {x.split('=')[0].split('>')[0].split('<')[0].split('~')[0].lower() for x in asosiy}\n    q = ['-r requirements.txt'] + sorted(x for x in qoshimcha if x.lower() not in bor)\n    return '\\n'.join(q) + '\\n'",
      'dev_talablar(["django>=5.0", "requests==2.32.3"], ["pytest", "black", "requests"])', "dev_talablar([], [])", 'dev_talablar(["a"], ["b"])'),
    F("Yangilash kerak", "`eskirgan(ornatilgan, oxirgi)` — `{paket: versiya}` lugʻatlaridan oʻrnatilgan versiyasi oxirgisidan eski paketlarni `\"nom: eski → yangi\"` koʻrinishida (alifbo boʻyicha) qaytarsin (`pip list --outdated` kabi).",
      "def eskirgan(ornatilgan, oxirgi):\n    v = lambda s: tuple(int(x) for x in s.split('.'))\n    return [f'{k}: {ornatilgan[k]} → {oxirgi[k]}' for k in sorted(ornatilgan) if k in oxirgi and v(ornatilgan[k]) < v(oxirgi[k])]",
      'eskirgan({"django": "5.1", "requests": "2.32.3", "six": "1.16.0"}, {"django": "5.2", "requests": "2.32.3"})', "eskirgan({}, {})", 'eskirgan({"a": "1.10"}, {"a": "1.9"})', lv=1),
    L("docs", "pip-requirements"),
    L("docs", "pkg-managing"),
    L("docs", "pip-user-guide", title="pip User Guide — requirements va constraints"),
    L("lc", "compare-version-numbers", note="Versiyalarni solishtirish — LeetCode klassikasi."),
])

# ---------------------------------------------------------------- 11.5
TOPIC("nashr", "Paket nashr qilish", "pyproject.toml, build, TestPyPI va twine", 20, r'''
Oʻzingiz yozgan foydali kodni boshqalar ham `pip install` bilan ishlata olishi uchun uni **paket** sifatida PyPI'ga joylash mumkin.

## Loyiha tuzilishi (src layout)
```text
mirae-salom/
├── pyproject.toml        ← paket haqida hamma maʼlumot
├── README.md
├── LICENSE
├── src/
│   └── mirae_salom/
│       ├── __init__.py
│       └── asosiy.py
└── tests/
    └── test_asosiy.py
```

## pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mirae-salom"
version = "0.1.0"
description = "Oʻzbekcha salomlashuv funksiyalari"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [{ name = "Madina Karimova", email = "madina@example.com" }]
dependencies = ["requests>=2.31"]

[project.scripts]
salom = "mirae_salom.asosiy:main"
```

Uni Python bilan oʻqib koʻramiz:

```py
import tomllib

pyproject = """
[project]
name = "mirae-salom"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["requests>=2.31"]

[project.scripts]
salom = "mirae_salom.asosiy:main"
"""
p = tomllib.loads(pyproject)["project"]
print(p["name"], p["version"])
print(p["dependencies"])
print(p["scripts"])
```

## Yigʻish va yuklash
```bash
pip install build twine
python -m build                      # dist/ ichida .whl va .tar.gz yaratadi
twine upload --repository testpypi dist/*    # avval sinov serveriga!
twine upload dist/*                  # haqiqiy PyPI
```

| Fayl | Nima |
|---|---|
| `mirae_salom-0.1.0-py3-none-any.whl` | **wheel** — tayyor, tez oʻrnatiladi |
| `mirae_salom-0.1.0.tar.gz` | **sdist** — manba kod arxivi |

## Nom qoidalari
PyPI nomlarni **normallashtiradi**: katta-kichik harf, `-`, `_`, `.` farqi yoʻq. `Mirae_Salom`, `mirae.salom`, `mirae-salom` — bitta paket!

```py
import re

def normallashtir(nom):
    return re.sub(r"[-_.]+", "-", nom).lower()

for n in ["Mirae_Salom", "mirae.salom", "MIRAE--salom"]:
    print(n, "→", normallashtir(n))
```

!> Har bir yuklashda versiya **oshishi shart** — PyPI bir xil versiyani qayta yuklashga ruxsat bermaydi. Avval doim **TestPyPI** da sinab koʻring.

## Esda tuting
- `pyproject.toml` — zamonaviy standart; `python -m build` → `twine upload`.
- Nom normallashtiriladi, versiya har safar oshiriladi.
''', [
    P('import re\nprint(re.sub(r"[-_.]+", "-", "My_Cool.Package").lower())', "my_cool.package", "mycoolpackage", "My-Cool-Package"),
    P('import tomllib\nd = tomllib.loads(\'[project]\\nname = "x"\\nversion = "1.0"\')\nprint(d["project"]["version"])', "1", "x", "Xato"),
    P('import tomllib\nd = tomllib.loads(\'[project.scripts]\\nsalom = "pkg.m:main"\')\nprint(d["project"]["scripts"]["salom"].split(":"))', "pkg.m:main", "['pkg', 'm', 'main']", "Xato"),
    P('fayl = "mirae_salom-0.1.0-py3-none-any.whl"\nprint(fayl.split("-")[1])', "mirae_salom", "py3", "0.1"),
    P('print("dist/mirae_salom-0.1.0.tar.gz".endswith((".whl", ".tar.gz")))', "False", "tar.gz", "Xato"),
    P('import tomllib\nprint(tomllib.loads(\'d = ["a>=1", "b"]\')["d"][1])', "a>=1", "['b']", "Xato"),
    P('import tomllib\nprint(tomllib.loads(\'a = [{ n = "x" }]\')["a"][0]["n"])', "[{ n = \"x\" }]", "n", "Xato", lv=2),
    Q("Paketni haqiqiy PyPI'ga yuklashdan oldin qayerda sinash kerak?", "TestPyPI", "GitHub Issues", "localhost:8000", "Hech qayerda"),
    Q("`.whl` fayl nima?", "Wheel — tayyor, tez oʻrnatiladigan paket formati", "Manba kod arxivi", "Virtual muhit", "Paket hujjati"),
    F("Nomni normallashtirish", "`normal(nom)` — PEP 503 boʻyicha: `[-_.]+` → `-`, kichik harflar.",
      "import re\n\n\ndef normal(nom):\n    return re.sub(r'[-_.]+', '-', nom).lower()",
      'normal("Mirae_Salom")', 'normal("a.b-c__d")', 'normal("requests")', lv=1),
    F("pyproject tekshiruvi", "`tekshir(matn)` — `[project]` da `name`, `version`, `requires-python` boʻlmasa ularni roʻyxatda (shu tartibda) qaytarsin; hammasi bor boʻlsa `[]`.",
      "import tomllib\n\n\ndef tekshir(matn):\n    p = tomllib.loads(matn).get('project', {})\n    return [k for k in ('name', 'version', 'requires-python') if k not in p]",
      "tekshir('[project]\\nname = \"x\"\\nversion = \"0.1\"\\nrequires-python = \">=3.10\"\\n')", "tekshir('[project]\\nname = \"x\"\\n')", "tekshir('')"),
    F("Wheel nomi", "`wheel_tahlil(fayl)` — wheel fayl nomidan `{\"nom\", \"versiya\", \"python\", \"abi\", \"platforma\"}` qaytarsin (`.whl` siz, `-` boʻyicha 5 qism).",
      "def wheel_tahlil(fayl):\n    nom, versiya, py, abi, plat = fayl[:-4].split('-')\n    return {'nom': nom, 'versiya': versiya, 'python': py, 'abi': abi, 'platforma': plat}",
      'wheel_tahlil("mirae_salom-0.1.0-py3-none-any.whl")', 'wheel_tahlil("numpy-2.1.0-cp312-cp312-win_amd64.whl")["platforma"]', 'wheel_tahlil("x-1-py3-none-any.whl")["versiya"]', lv=2),
    F("Skript nuqtasi", "`kirish_nuqtasi(qiymat)` — `\"paket.modul:funksiya\"` dan `(\"paket.modul\", \"funksiya\")`; `:` yoʻq boʻlsa `ValueError`.",
      "def kirish_nuqtasi(qiymat):\n    if ':' not in qiymat:\n        raise ValueError(qiymat)\n    modul, f = qiymat.split(':', 1)\n    return (modul, f)",
      'kirish_nuqtasi("mirae_salom.asosiy:main")', 'kirish_nuqtasi("cli:run")', 'kirish_nuqtasi("faqat_modul")'),
    F("Qayta yuklash mumkinmi", "`yuklash_mumkin(yuklangan, yangi)` — PyPI qoidasi: yangi versiya avval yuklanganlarning **hammasidan** katta boʻlsa `True`.",
      "def yuklash_mumkin(yuklangan, yangi):\n    v = lambda s: tuple(int(x) for x in s.split('.'))\n    return all(v(yangi) > v(x) for x in yuklangan)",
      'yuklash_mumkin(["0.1.0", "0.1.1"], "0.2.0")', 'yuklash_mumkin(["0.1.0"], "0.1.0")', 'yuklash_mumkin([], "0.0.1")', 'yuklash_mumkin(["1.10.0"], "1.9.9")', lv=1),
    F("pyproject yasash", "`pyproject(nom, versiya, bogliqlar)` — minimal `[project]` boʻlimli TOML matn yasasin; natija `tomllib` bilan qayta oʻqilganda xuddi shu qiymatlar chiqishi kerak.",
      "def pyproject(nom, versiya, bogliqlar):\n    deps = ', '.join(f'\"{d}\"' for d in bogliqlar)\n    return f'[project]\\nname = \"{nom}\"\\nversion = \"{versiya}\"\\ndependencies = [{deps}]\\n'",
      "__import__('tomllib').loads(pyproject('mirae-salom', '0.1.0', ['requests>=2.31']))", "__import__('tomllib').loads(pyproject('x', '1', []))['project']['dependencies']", "pyproject('a', '2', ['b'])", lv=2),
    F("Nom bandmi", "`bandmi(nom, mavjudlar)` — normallashtirilgan nom mavjud paketlardan birining normallashtirilgani bilan bir xil boʻlsa `True` (`Mirae_Salom` va `mirae-salom` — bir xil).",
      "import re\n\n\ndef bandmi(nom, mavjudlar):\n    n = lambda s: re.sub(r'[-_.]+', '-', s).lower()\n    return n(nom) in {n(m) for m in mavjudlar}",
      'bandmi("Mirae_Salom", ["mirae-salom", "requests"])', 'bandmi("mirae-hello", ["mirae-salom"])', 'bandmi("Requests", ["requests"])'),
    L("docs", "pkg-publish"),
    L("docs", "pkg-pyproject"),
    L("docs", "py-installing"),
    L("lc", "compare-version-numbers"),
])

# ---------------------------------------------------------------- 11.6
TOPIC("docstring", "Docstring va pydoc", "Kodni hujjatlashtirish va doctest", 15, r'''
Kod bir marta yoziladi, lekin yuz marta oʻqiladi. **Docstring** — funksiya, sinf yoki modul boshidagi uch qoʻshtirnoqli matn — kodning "qoʻllanmasi".

```py
def kredit(summa, foiz, oy):
    """Oylik kredit toʻlovini hisoblaydi.

    Args:
        summa: kredit summasi (soʻm).
        foiz: yillik foiz stavkasi (masalan, 24).
        oy: muddat (oylarda).

    Returns:
        Bir oylik toʻlov (soʻm), butun songa yaxlitlangan.
    """
    jami = summa * (1 + foiz / 100 * oy / 12)
    return round(jami / oy)

print(kredit(12_000_000, 24, 12))
print(kredit.__doc__.splitlines()[0])
```

## Docstring qayerda koʻrinadi?
- `help(funksiya)` va `pydoc`;
- VS Code'da funksiya ustiga sichqoncha olib borganda;
- hujjat generatorlari (Sphinx, MkDocs).

```py
import inspect

def salom(ism):
    """Salomlashuv matnini qaytaradi."""
    return f"Salom, {ism}!"

print(inspect.getdoc(salom))
print(salom.__name__, "—", inspect.signature(salom))
```

## Uslublar
| Uslub | Belgisi |
|---|---|
| Google | `Args:`, `Returns:`, `Raises:` |
| NumPy | `Parameters`, `----------` |
| reST (Sphinx) | `:param x:`, `:return:` |

> Bitta loyihada bitta uslubni tanlang. Eng oddiy va mashhuri — **Google uslubi**.

## pydoc
```bash
python -m pydoc math            # terminalda hujjat
python -m pydoc -b              # brauzerda barcha modullar hujjati
python -m pydoc -w mening_modul # HTML fayl
```

```py
import pydoc

def kvadrat(x):
    """x ning kvadratini qaytaradi."""
    return x * x

print(pydoc.render_doc(kvadrat, renderer=pydoc.plaintext).splitlines()[-1].strip())
```

## doctest — hujjat ichidagi testlar
Docstring ichidagi `>>>` misollar avtomatik **test** sifatida tekshirilishi mumkin:

```py file=matn.py
def teskari(s):
    """Satrni teskari qaytaradi.

    >>> teskari("salom")
    'molas'
    >>> teskari("")
    ''
    """
    return s[::-1]
```

```py
import doctest
import matn

natija = doctest.testmod(matn)
print(natija)
print("Hammasi oʻtdi ✓" if natija.failed == 0 else "Xato bor!")
```

## Esda tuting
- Har bir ochiq funksiyaga: nima qiladi, nima oladi, nima qaytaradi.
- `>>>` misollar — ham hujjat, ham test (doctest).
''', [
    P('def f():\n    """Salom."""\nprint(f.__doc__)', "f", "None", "\"Salom.\""),
    P('def f():\n    pass\nprint(f.__doc__)', "''", "f", "Xato"),
    P('def f():\n    "Bir qatorli"\n    return 1\nprint(f.__doc__, f())', "None 1", "Bir qatorli None", "Xato"),
    P('import inspect\ndef f(a, b=2):\n    pass\nprint(inspect.signature(f))', "f(a, b=2)", "(a, b)", "Xato"),
    P('class A:\n    """Sinf hujjati."""\nprint(A.__doc__)', "A", "None", "Xato"),
    P('import inspect\ndef f():\n    """\n    Birinchi.\n      Ikkinchi.\n    """\nprint(inspect.getdoc(f).splitlines())', "['', 'Birinchi.', 'Ikkinchi.', '']", "Birinchi. Ikkinchi.", "Xato", lv=2),
    P('import doctest\nprint(type(doctest.testmod).__name__)', "testmod", "module", "Xato"),
    Q("Docstring qayerga yoziladi?", "Funksiya/sinf/modulning birinchi qatoriga, uch qoʻshtirnoq ichida", "Faylning oxiriga", "Izoh (#) sifatida funksiyadan oldin", "Alohida .txt faylga"),
    Q("doctest nima qiladi?", "Docstring ichidagi >>> misollarni bajarib, natijani tekshiradi", "Docstring'ni tarjima qiladi", "Kodni formatlaydi", "Hujjatni PDF qiladi"),
    F("Docstring yozing", "`yuza(a, b)` funksiyasini yozing: toʻrtburchak yuzasini qaytarsin va uning docstring'i aynan `\"Toʻrtburchak yuzasini qaytaradi.\"` boʻlsin.",
      "def yuza(a, b):\n    \"\"\"Toʻrtburchak yuzasini qaytaradi.\"\"\"\n    return a * b",
      "yuza(3, 4)", "yuza.__doc__", "yuza(0, 5)", lv=1),
    F("Birinchi qator", "`qisqa_hujjat(f)` — funksiya docstring'ining birinchi boʻsh boʻlmagan qatorini (`inspect.getdoc`) qaytarsin; docstring yoʻq boʻlsa `\"(hujjat yoʻq)\"`.",
      "import inspect\n\n\ndef qisqa_hujjat(f):\n    d = inspect.getdoc(f)\n    if not d:\n        return '(hujjat yoʻq)'\n    return d.strip().splitlines()[0]",
      "qisqa_hujjat(len)", "qisqa_hujjat(lambda: 0)", "qisqa_hujjat(qisqa_hujjat)"),
    F("Hujjatsizlar", "`hujjatsiz(modul_nomi)` — moduldagi docstring'i yoʻq ochiq funksiyalar nomlari (alifbo boʻyicha).",
      "import importlib\nimport inspect\n\n\ndef hujjatsiz(modul_nomi):\n    m = importlib.import_module(modul_nomi)\n    return sorted(n for n, f in inspect.getmembers(m, inspect.isfunction) if not n.startswith('_') and not f.__doc__)",
      'hujjatsiz("vosita")', 'len(hujjatsiz("vosita"))',
      'hujjatsiz("toliq")',
      files={"vosita.py": "def a():\n    \"\"\"Bor.\"\"\"\n\n\ndef b():\n    pass\n\n\ndef c():\n    return 1\n\n\ndef _d():\n    pass\n", "toliq.py": "def x():\n    \"\"\"Hujjat.\"\"\"\n"}, lv=2),
    F("Google uslubi", "`argumentlar(doc)` — Google uslubidagi docstring'ning `Args:` boʻlimidan argument nomlarini qaytarsin (boʻlim boʻlmasa `[]`).",
      "def argumentlar(doc):\n    natija = []\n    ichida = False\n    for q in doc.splitlines():\n        s = q.strip()\n        if s == 'Args:':\n            ichida = True\n            continue\n        if ichida:\n            if not s or s.endswith(':') and ' ' not in s:\n                break\n            if ':' in s:\n                natija.append(s.split(':')[0].strip())\n    return natija",
      'argumentlar("Hisob.\\n\\n    Args:\\n        summa: kredit.\\n        foiz: stavka.\\n\\n    Returns:\\n        toʻlov.")', 'argumentlar("Faqat matn.")', 'argumentlar("Args:\\n    x: son\\nReturns:\\n    y")', lv=3),
    F("doctest ishga tushirish", "`sinov(modul_nomi)` — `doctest.testmod` bilan modulni tekshirib, `(attempted, failed)` kortejini qaytarsin.",
      "import doctest\nimport importlib\n\n\ndef sinov(modul_nomi):\n    r = doctest.testmod(importlib.import_module(modul_nomi))\n    return (r.attempted, r.failed)",
      'sinov("togri")', 'sinov("xato")',
      'sinov("bosh")',
      files={"togri.py": "def kv(x):\n    \"\"\"\n    >>> kv(3)\n    9\n    >>> kv(-2)\n    4\n    \"\"\"\n    return x * x\n",
             "xato.py": "def yarim(x):\n    \"\"\"\n    >>> yarim(4)\n    2\n    \"\"\"\n    return x / 2\n",
             "bosh.py": "X = 1\n"}, lv=2),
    F("Imzo va hujjat", "`karta(f)` — `\"nom(imzo) — birinchi qator\"` satrini qaytarsin (`inspect.signature`, `inspect.getdoc`; hujjat yoʻq boʻlsa faqat `nom(imzo)`).",
      "import inspect\n\n\ndef karta(f):\n    d = inspect.getdoc(f)\n    bosh = f'{f.__name__}{inspect.signature(f)}'\n    return f'{bosh} — {d.splitlines()[0]}' if d else bosh",
      'karta(__import__("misol").kredit)', 'karta(__import__("misol").yordam)', 'karta(karta)',
      files={"misol.py": "def kredit(summa, foiz=24, oy=12):\n    \"\"\"Oylik toʻlovni hisoblaydi.\"\"\"\n\n\ndef yordam(x):\n    pass\n"}),
    F("Misol yozuvchi", "`doctest_misol(f, *args)` — funksiyani chaqirib, doctest formatidagi ikki qatorli misolni qaytarsin: `\">>> nom(argumentlar)\\nnatija_repr\"` (argumentlar `repr` bilan, vergul+boʻsh joy bilan).",
      "def doctest_misol(f, *args):\n    a = ', '.join(repr(x) for x in args)\n    return f'>>> {f.__name__}({a})\\n{f(*args)!r}'",
      "doctest_misol(len, 'salom')", "doctest_misol(max, 3, 9, 2)", "doctest_misol(str.upper, 'ok')", lv=2),
    L("docs", "py-controlflow"),
    L("docs", "py-pydoc"),
    L("exercism", "leap", note="Yechimga Google uslubida docstring va doctest misollar qoʻshing."),
    L("docs", "vscode-python"),
])
