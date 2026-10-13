from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(10, "Standart kutubxona", "Fayllar, CSV, JSON, SQLite, sana-vaqt, regex va boshqalar", "🧰")

# ---------------------------------------------------------------- 10.1
TOPIC("pathlib", "Yoʻllar bilan ishlash (pathlib)", "Fayl va papka yoʻllarini xavfsiz yasash", 20, r'''
Windows'da yoʻl `C:\Users\Ali\hujjat.txt`, macOS/Linux'da esa `/home/ali/hujjat.txt`. Yoʻllarni satr sifatida qoʻlda yigʻish — xatolar manbai. **`pathlib`** bu muammoni hal qiladi: yoʻl — obyekt.

```py
from pathlib import Path

p = Path("loyiha") / "data" / "baholar.csv"     # / bilan birlashtirish
print(p.as_posix())
print(p.name)        # fayl nomi
print(p.stem)        # kengaytmasiz nom
print(p.suffix)      # kengaytma
print(p.parent.as_posix())
print(p.parts)
```

> `/` operatori yoʻlni har qanday tizimda toʻgʻri birlashtiradi. `as_posix()` — doim `/` bilan chiqaradi (chiroyli koʻrinish uchun).

## Yoʻlni oʻzgartirish
```py
from pathlib import Path

p = Path("rasmlar/tatil.jpeg")
print(p.with_suffix(".png").as_posix())
print(p.with_name("bayram.jpeg").as_posix())
print(p.with_stem("tatil_2026").as_posix())
```

## Mavjudligini tekshirish
```py
from pathlib import Path

Path("eslatma.txt").write_text("salom", encoding="utf-8")
p = Path("eslatma.txt")
print(p.exists(), p.is_file(), p.is_dir())
print(Path("yoq.txt").exists())
print(p.stat().st_size, "bayt")
```

## Joriy papka va toʻliq yoʻl
```py
from pathlib import Path

hozir = Path.cwd()
print(hozir.is_absolute())
print(Path("a/b/../c.txt").as_posix())
print(Path("data.csv").resolve().is_absolute())
```

| Metod / atribut | Natija (`Path("a/b/hisobot.pdf")`) |
|---|---|
| `.name` | `hisobot.pdf` |
| `.stem` | `hisobot` |
| `.suffix` | `.pdf` |
| `.parent` | `a/b` |
| `.exists()` | bormi? |
| `Path.home()` | foydalanuvchi papkasi |

!> Eski kodlarda `os.path.join(...)` ni koʻrasiz — u ham ishlaydi. Yangi kodda `pathlib` qulayroq va oʻqilishi oson.

## Esda tuting
- Yoʻllarni `Path("a") / "b"` bilan yasang, satr qoʻshib emas.
- `.name`, `.stem`, `.suffix`, `.parent` — eng koʻp ishlatiladigan qismlar.
''', [
    P('from pathlib import Path\nprint(Path("a/b/c.txt").name)', "c", "a/b", "txt"),
    P('from pathlib import Path\nprint(Path("arxiv.tar.gz").suffix)', ".tar.gz", "tar", "arxiv"),
    P('from pathlib import Path\nprint(Path("arxiv.tar.gz").suffixes)', "['.gz']", "['tar', 'gz']", ".tar.gz"),
    P('from pathlib import Path\nprint((Path("a") / "b" / "c.py").as_posix())', "abc.py", "a\\b\\c.py", "Xato"),
    P('from pathlib import Path\nprint(Path("rasm.jpeg").with_suffix(".png").name)', "rasm.jpeg.png", ".png", "rasm"),
    P('from pathlib import Path\nprint(Path("a/b/c").parent.parent.as_posix())', "c", "a/b", "b"),
    P('from pathlib import Path\nprint(Path("x/y.txt").stem, Path("x/y.txt").parts)', "y.txt ('x', 'y.txt')", "y ['x', 'y.txt']", "x ('y',)"),
    Q("Yoʻllarni birlashtirishning eng toʻgʻri usuli?", "Path(\"data\") / \"fayl.csv\"", "\"data\" + \"/\" + \"fayl.csv\"", "\"data\\\\fayl.csv\"", "join(\"data\", \"fayl.csv\")"),
    Q("`Path(\"hisobot.pdf\").stem` nima qaytaradi?", "hisobot", "hisobot.pdf", ".pdf", "pdf"),
    F("Kengaytma", "`kengaytma(yol)` — fayl kengaytmasini kichik harflarda, nuqtasiz qaytarsin (`\"Rasm.JPG\"` → `\"jpg\"`); kengaytma yoʻq boʻlsa `\"\"`.",
      "from pathlib import Path\n\n\ndef kengaytma(yol):\n    return Path(yol).suffix.lower().lstrip('.')",
      'kengaytma("Rasm.JPG")', 'kengaytma("a/b/hisobot.pdf")', 'kengaytma("README")', 'kengaytma("arxiv.tar.gz")', lv=1),
    F("Yoʻl yasash", "`yol(*qismlar)` — qismlarni `Path` bilan birlashtirib, `as_posix()` satrini qaytarsin.",
      "from pathlib import Path\n\n\ndef yol(*qismlar):\n    return Path(*qismlar).as_posix()",
      'yol("loyiha", "data", "a.csv")', 'yol("x")', 'yol("a", "b", "..", "c")', lv=1),
    F("Kengaytmani almashtirish", "`almashtir(fayllar, yangi)` — har bir fayl nomining kengaytmasini `yangi` ga almashtirib (`with_suffix`), roʻyxat qaytarsin.",
      "from pathlib import Path\n\n\ndef almashtir(fayllar, yangi):\n    return [Path(f).with_suffix(yangi).as_posix() for f in fayllar]",
      'almashtir(["a.jpeg", "rasmlar/b.JPG"], ".png")', 'almashtir([], ".x")', 'almashtir(["hujjat"], ".txt")'),
    F("Turlarga ajratish", "`guruhla(fayllar)` — `{kengaytma: [nomlar]}` lugʻati (kengaytma kichik harfda, nuqtasiz; kengaytmasiz fayllar `\"boshqa\"` ostida). Nomlar kelish tartibida.",
      "from pathlib import Path\n\n\ndef guruhla(fayllar):\n    d = {}\n    for f in fayllar:\n        k = Path(f).suffix.lower().lstrip('.') or 'boshqa'\n        d.setdefault(k, []).append(Path(f).name)\n    return d",
      'guruhla(["a.jpg", "b.PDF", "c.JPG", "Makefile", "d/e.pdf"])', "guruhla([])", 'guruhla(["x.py"])', lv=2),
    F("Ota papkalar", "`otalar(yol)` — yoʻlning barcha ota papkalari roʻyxati (`.parents`, `as_posix`), `.` ni qoʻshmang: `\"a/b/c.txt\"` → `[\"a/b\", \"a\"]`.",
      "from pathlib import Path\n\n\ndef otalar(yol):\n    return [p.as_posix() for p in Path(yol).parents if p.as_posix() != '.']",
      'otalar("a/b/c.txt")', 'otalar("x.txt")', 'otalar("loyiha/src/ilova/main.py")'),
    F("Fayl bormi", "`hajmi(nom)` — fayl mavjud boʻlsa uning hajmini (bayt), aks holda `-1` qaytarsin. Tekshiruvda fayllar `matn.txt` yaratiladi.",
      "from pathlib import Path\n\n\ndef hajmi(nom):\n    p = Path(nom)\n    return p.stat().st_size if p.is_file() else -1",
      'hajmi("matn.txt")', 'hajmi("yoq.txt")', 'hajmi("papka")',
      files={"matn.txt": "salom dunyo", "papka/ichki.txt": "x"}, lv=2),
    F("Yoʻlni soddalashtirish", "`soddalashtir(yol)` — `os.path.normpath` dan foydalanib, natijani `/` bilan qaytarsin: `\"a/./b/../c\"` → `\"a/c\"`.",
      "import os\n\n\ndef soddalashtir(yol):\n    return os.path.normpath(yol).replace('\\\\', '/')",
      'soddalashtir("a/./b/../c")', 'soddalashtir("x//y/")', 'soddalashtir("../a")', lv=2),
    L("docs", "py-pathlib"),
    L("lc", "simplify-path", note="Yoʻlni soddalashtirish — stek bilan klassik masala."),
    L("docs", "py-os", title="os.path — eski uslubdagi yoʻllar"),
    L("lc", "find-duplicate-file-in-system"),
])

# ---------------------------------------------------------------- 10.2
TOPIC("kataloglar", "Kataloglar (papkalar) bilan ishlash", "Yaratish, koʻrish, qidirish, nusxalash va oʻchirish", 20, r'''
Dastur koʻpincha papkalar bilan ishlaydi: rasmlarni saralash, hisobotlarni arxivlash, eski fayllarni tozalash.

## Yaratish
```py
from pathlib import Path

Path("hisobotlar/2026/oktabr").mkdir(parents=True, exist_ok=True)
print(Path("hisobotlar/2026/oktabr").is_dir())
```

- `parents=True` — ota papkalar ham yaratiladi;
- `exist_ok=True` — papka bor boʻlsa xato bermaydi.

## Ichidagilarni koʻrish
```py
from pathlib import Path

for nom in ["a.txt", "b.csv", "c.txt"]:
    Path(nom).write_text("x")
Path("rasmlar").mkdir()

for p in sorted(Path(".").iterdir()):
    tur = "📁" if p.is_dir() else "📄"
    print(tur, p.name)
```

## Qidirish: glob
```py
from pathlib import Path

for nom in ["a.txt", "b.txt", "eski/c.txt", "eski/d.csv"]:
    Path(nom).parent.mkdir(exist_ok=True)
    Path(nom).write_text("...")

print(sorted(p.as_posix() for p in Path(".").glob("*.txt")))
print(sorted(p.as_posix() for p in Path(".").rglob("*.txt")))   # ichki papkalarda ham
```

| Shablon | Maʼnosi |
|---|---|
| `*.txt` | shu papkadagi barcha `.txt` |
| `**/*.py` | barcha ichki papkalardagi `.py` |
| `rasm_??.png` | `?` — bitta istalgan belgi |

## Nusxalash, koʻchirish, oʻchirish
```py
import shutil
from pathlib import Path

Path("asl").mkdir()
Path("asl/hujjat.txt").write_text("muhim")
shutil.copytree("asl", "zaxira")                  # papkani nusxalash
shutil.copy("asl/hujjat.txt", "nusxa.txt")        # faylni nusxalash
Path("nusxa.txt").rename("yangi_nom.txt")         # nomini oʻzgartirish
shutil.rmtree("asl")                               # papkani butunlay oʻchirish
print(sorted(p.name for p in Path(".").iterdir()))
```

!> `shutil.rmtree` papkani **qaytarib boʻlmaydigan** tarzda oʻchiradi (savatga emas!). Real loyihalarda oldin nima oʻchirilishini `print` qilib tekshiring.

## Bo'sh papka va os moduli
```py
import os

os.makedirs("a/b", exist_ok=True)
print(os.listdir("a"))
os.rmdir("a/b")            # faqat boʻsh papka
print(os.listdir("a"))
```

## Esda tuting
- `mkdir(parents=True, exist_ok=True)` — xavfsiz yaratish.
- `iterdir()` — ichidagilar, `glob`/`rglob` — shablon boʻyicha qidirish.
- `shutil` — nusxalash va papkani oʻchirish.
''', [
    P('from pathlib import Path\nPath("a/b").mkdir(parents=True)\nprint(Path("a").is_dir(), Path("a/b").is_dir())', "False True", "⚠ FileNotFoundError", "True False"),
    P('from pathlib import Path\nPath("a/b").mkdir()', "None", "a/b", "⚠ FileExistsError", lv=2),
    P('from pathlib import Path\nPath("x").mkdir()\nPath("x").mkdir(exist_ok=True)\nprint("ok")', "⚠ FileExistsError", "x", "None"),
    P('from pathlib import Path\nfor n in ["b.txt", "a.txt", "c.py"]:\n    Path(n).write_text("")\nprint(sorted(p.name for p in Path(".").glob("*.txt")))', "['a.txt', 'b.txt', 'c.py']", "['b.txt', 'a.txt']", "[]"),
    P('import os\nos.makedirs("p/q")\nprint(os.listdir("p"))', "['p', 'q']", "[]", "q"),
    P('import os\nos.makedirs("p/q")\nos.rmdir("p")', "None", "p", "⚠ FileNotFoundError", lv=3,
      why="`os.rmdir` faqat **boʻsh** papkani oʻchiradi. Ichida `q` bor — OSError (Linux'da OSError, Windows'da ham shu oila)."),
    P('import shutil\nfrom pathlib import Path\nPath("a").mkdir()\nPath("a/f.txt").write_text("hi")\nshutil.copytree("a", "b")\nprint(Path("b/f.txt").read_text())', "a/f.txt", "Xato", "f.txt"),
    Q("`mkdir(parents=True, exist_ok=True)` nima qiladi?", "Ota papkalari bilan yaratadi, mavjud boʻlsa xato bermaydi", "Faqat ota papkani yaratadi", "Papkani oʻchirib qayta yaratadi", "Papka bor-yoʻqligini tekshiradi"),
    Q("Ichki papkalardagi barcha `.py` fayllarni qaysi biri topadi?", "Path(\".\").rglob(\"*.py\")", "Path(\".\").glob(\"*.py\")", "Path(\".\").iterdir(\"*.py\")", "os.listdir(\"*.py\")"),
    F("Papka yaratish", "`tuzilma(yollar)` — har bir yoʻl uchun papka yaratsin (`parents=True, exist_ok=True`), soʻng joriy papkadagi barcha papkalarni (ichkilari bilan) alifbo boʻyicha `as_posix` roʻyxat qilib qaytarsin.",
      "from pathlib import Path\n\n\ndef tuzilma(yollar):\n    for y in yollar:\n        Path(y).mkdir(parents=True, exist_ok=True)\n    return sorted(p.as_posix() for p in Path('.').rglob('*') if p.is_dir())",
      'tuzilma(["src/ilova", "tests"])', 'tuzilma(["a/b/c", "a/b"])', "tuzilma([])", lv=1),
    F("Fayllar soni", "`sanash(kengaytma)` — joriy papka va ichki papkalarda shu kengaytmali fayllar soni.",
      "from pathlib import Path\n\n\ndef sanash(kengaytma):\n    return sum(1 for p in Path('.').rglob('*' + kengaytma) if p.is_file())",
      'sanash(".txt")', 'sanash(".csv")', 'sanash(".py")',
      files={"a.txt": "1", "b.csv": "2", "docs/c.txt": "3", "docs/eski/d.txt": "4", "kod/e.py": "5"}),
    F("Eng katta fayl", "`eng_katta()` — joriy papkadagi (ichkilari bilan) eng katta faylning nomini qaytarsin.",
      "from pathlib import Path\n\n\ndef eng_katta():\n    fayllar = [p for p in Path('.').rglob('*') if p.is_file()]\n    return max(fayllar, key=lambda p: p.stat().st_size).name",
      "eng_katta()", "len(eng_katta())", "eng_katta().endswith('.log')",
      files={"kichik.txt": "a", "data/orta.csv": "a,b,c\n1,2,3\n", "logs/katta.log": "x" * 500}, lv=2),
    F("Saralovchi", "`sarala()` — joriy papkadagi fayllarni kengaytmasi boʻyicha papkalarga koʻchirsin (`jpg/`, `pdf/` …; kengaytmasizlari `boshqa/`). Soʻng har bir papkadagi fayllar sonini `{papka: soni}` lugʻat qilib qaytarsin.",
      "from pathlib import Path\nimport shutil\n\n\ndef sarala():\n    for p in list(Path('.').iterdir()):\n        if p.is_file():\n            k = p.suffix.lower().lstrip('.') or 'boshqa'\n            Path(k).mkdir(exist_ok=True)\n            shutil.move(str(p), str(Path(k) / p.name))\n    return {d.name: len(list(d.iterdir())) for d in sorted(Path('.').iterdir()) if d.is_dir()}",
      "sarala()", "sarala()['jpg']", "len(sarala())",
      files={"a.jpg": "", "b.JPG": "", "c.pdf": "", "README": ""}, lv=3),
    F("Zaxira nusxa", "`zaxira(papka)` — papkani `papka + \"_zaxira\"` nomi bilan nusxalasin (`shutil.copytree`), zaxira papkasidagi fayl nomlarini alifbo boʻyicha qaytarsin.",
      "import shutil\nfrom pathlib import Path\n\n\ndef zaxira(papka):\n    yangi = papka + '_zaxira'\n    shutil.copytree(papka, yangi)\n    return sorted(p.name for p in Path(yangi).rglob('*') if p.is_file())",
      'zaxira("hujjatlar")', 'zaxira("hujjatlar/2026")', 'zaxira("yoq_papka")',
      files={"hujjatlar/shartnoma.txt": "...", "hujjatlar/2026/hisobot.txt": "..."}),
    F("Tozalovchi", "`tozala(kengaytma)` — joriy papkadan (ichkilari bilan) shu kengaytmali fayllarni oʻchirib, oʻchirilganlar sonini qaytarsin.",
      "from pathlib import Path\n\n\ndef tozala(kengaytma):\n    n = 0\n    for p in list(Path('.').rglob('*' + kengaytma)):\n        if p.is_file():\n            p.unlink()\n            n += 1\n    return n",
      'tozala(".tmp")', 'tozala(".tmp")', '(tozala(".log"), sorted(p.name for p in __import__("pathlib").Path(".").rglob("*") if p.is_file()))',
      files={"a.tmp": "", "b/c.tmp": "", "d.log": "", "e.txt": ""}, lv=2),
    F("Daraxt", "`daraxt(papka)` — papka ichidagi barcha fayl va papkalarni nisbiy yoʻl (`as_posix`) bilan alifbo tartibida qaytarsin; papkalar oxirida `/` bilan.",
      "from pathlib import Path\n\n\ndef daraxt(papka):\n    p = Path(papka)\n    return sorted(x.relative_to(p).as_posix() + ('/' if x.is_dir() else '') for x in p.rglob('*'))",
      'daraxt("loyiha")', 'daraxt("loyiha/src")', 'len(daraxt("loyiha"))',
      files={"loyiha/README.md": "#", "loyiha/src/main.py": "", "loyiha/src/util/yordam.py": ""}, lv=2),
    L("docs", "py-shutil"),
    L("docs", "py-glob"),
    L("exercism", "grep", note="Fayllar ichidan qidirish — haqiqiy CLI vosita."),
    L("lc", "find-duplicate-file-in-system"),
])

# ---------------------------------------------------------------- 10.3
TOPIC("fayllar", "Fayllar: oʻqish va yozish", "open, rejimlar, kodlash va qatorma-qator ishlash", 20, r'''
Maʼlumotni dastur yopilgandan keyin ham saqlash uchun fayllarga yozamiz. Asosiy vosita — `open()` va `with`.

## Yozish va oʻqish
```py
with open("kundalik.txt", "w", encoding="utf-8") as f:
    f.write("Bugun Python oʻrgandim.\n")
    f.write("Ertaga — fayllar!\n")

with open("kundalik.txt", encoding="utf-8") as f:
    matn = f.read()
print(matn)
```

| Rejim | Maʼnosi | Fayl yoʻq boʻlsa |
|---|---|---|
| `"r"` | oʻqish (standart) | `FileNotFoundError` |
| `"w"` | yozish — eskisini **oʻchiradi** | yaratadi |
| `"a"` | oxiriga qoʻshish | yaratadi |
| `"x"` | faqat yangi fayl | yaratadi (bor boʻlsa xato) |
| `"rb"`, `"wb"` | ikkilik (rasm, zip) | — |

!> Oʻzbekcha matn uchun doim `encoding="utf-8"` yozing. Aks holda Windows'da `oʻ`, `gʻ`, `ʼ` buzilishi mumkin.

## Qatorma-qator
Katta fayllarni butunlay xotiraga yuklamang — qatorma-qator oʻqing:

```py
with open("ballar.txt", "w", encoding="utf-8") as f:
    f.write("Ali 85\nVali 92\nGani 78\n")

jami = 0
with open("ballar.txt", encoding="utf-8") as f:
    for qator in f:
        ism, ball = qator.split()
        jami += int(ball)
        print(f"{ism:<6}{ball:>4}")
print("Jami:", jami)
```

## Qoʻshib borish (log)
```py
from datetime import date

def log(xabar):
    with open("jurnal.log", "a", encoding="utf-8") as f:
        f.write(f"[{date(2026, 10, 13)}] {xabar}\n")

log("Dastur ishga tushdi")
log("Foydalanuvchi kirdi")
print(open("jurnal.log", encoding="utf-8").read())
```

## pathlib bilan qisqa yoʻl
```py
from pathlib import Path

p = Path("sozlama.txt")
p.write_text("til=uz\ntema=dark\n", encoding="utf-8")
qatorlar = p.read_text(encoding="utf-8").splitlines()
print(qatorlar)
sozlama = dict(q.split("=") for q in qatorlar)
print(sozlama)
```

## Faylni oʻchirish
```py
from pathlib import Path

p = Path("vaqtinchalik.txt")
p.write_text("...")
p.unlink()                       # oʻchirish
print(p.exists())
p.unlink(missing_ok=True)        # yoʻq boʻlsa ham xato bermaydi
```

## Esda tuting
- `with open(...)` — fayl avtomatik yopiladi.
- `"w"` eski mazmunni oʻchiradi, `"a"` oxiriga qoʻshadi.
- Katta fayl — `for qator in f:` bilan.
''', [
    P('with open("a.txt", "w") as f:\n    f.write("bir")\nwith open("a.txt", "w") as f:\n    f.write("ikki")\nprint(open("a.txt").read())', "birikki", "bir", "bir\nikki"),
    P('with open("a.txt", "w") as f:\n    f.write("bir")\nwith open("a.txt", "a") as f:\n    f.write("ikki")\nprint(open("a.txt").read())', "ikki", "bir\nikki", "bir"),
    P('print(open("yoq_fayl.txt").read())', "None", "''", "⚠ FileExistsError"),
    P('with open("a.txt", "w") as f:\n    n = f.write("salom")\nprint(n)', "None", "salom", "True"),
    P('open("q.txt", "w").write("1\\n2\\n3\\n")\nprint(len(open("q.txt").readlines()))', "4", "6", "1"),
    P('open("q.txt", "w").write("a\\nb\\n")\nprint(open("q.txt").read().splitlines())', "['a\\n', 'b\\n']", "['a', 'b', '']", "a b"),
    P('open("x.txt", "w").close()\nopen("x.txt", "x")', "None", "x.txt", "⚠ FileNotFoundError", lv=2),
    Q("Mavjud faylning oxiriga yozish uchun qaysi rejim?", "\"a\"", "\"w\"", "\"r\"", "\"x\""),
    Q("Katta faylni xotirani tejab oʻqishning eng yaxshi usuli?", "for qator in f: — qatorma-qator", "f.read() bilan bir marta", "f.readlines() bilan", "Faylni ikki marta ochish"),
    F("Faylga yozish", "`saqla(nom, qatorlar)` — roʻyxatdagi har bir satrni alohida qatorga yozsin (utf-8) va fayldagi belgilar sonini (`len(read())`) qaytarsin.",
      "def saqla(nom, qatorlar):\n    with open(nom, 'w', encoding='utf-8') as f:\n        for q in qatorlar:\n            f.write(q + '\\n')\n    with open(nom, encoding='utf-8') as f:\n        return len(f.read())",
      'saqla("a.txt", ["salom", "dunyo"])', 'saqla("b.txt", [])', 'saqla("c.txt", ["oʻzbek"])', lv=1),
    F("Qatorlar soni", "`qatorlar_soni(nom)` — fayldagi boʻsh boʻlmagan qatorlar soni.",
      "def qatorlar_soni(nom):\n    with open(nom, encoding='utf-8') as f:\n        return sum(1 for q in f if q.strip())",
      'qatorlar_soni("matn.txt")', 'qatorlar_soni("bosh.txt")', 'qatorlar_soni("yoq.txt")',
      files={"matn.txt": "bir\n\nikki\n   \nuch\n", "bosh.txt": ""}, lv=1),
    F("Soʻzlar statistikasi", "`statistika(nom)` — fayldagi `(qatorlar, soʻzlar, belgilar)` sonini qaytarsin (Unix `wc` kabi; belgilar — `len(read())`).",
      "def statistika(nom):\n    with open(nom, encoding='utf-8') as f:\n        matn = f.read()\n    return (len(matn.splitlines()), len(matn.split()), len(matn))",
      'statistika("hikoya.txt")', 'statistika("bir.txt")', 'statistika("bosh.txt")',
      files={"hikoya.txt": "Bir bor ekan,\nbir yoʻq ekan.\nQadim zamonda\n", "bir.txt": "x", "bosh.txt": ""}),
    F("Jurnal", "`log(nom, xabar)` — faylga `\"N. xabar\"` qatorini qoʻshsin (N — fayldagi qator raqami, 1 dan). Fayl yoʻq boʻlsa yaratilsin. Oxirgi qatorni qaytarsin.",
      "from pathlib import Path\n\n\ndef log(nom, xabar):\n    p = Path(nom)\n    n = len(p.read_text(encoding='utf-8').splitlines()) if p.exists() else 0\n    with open(nom, 'a', encoding='utf-8') as f:\n        f.write(f'{n + 1}. {xabar}\\n')\n    return f'{n + 1}. {xabar}'",
      'log("j.log", "start")', '(log("j.log", "a"), log("j.log", "b"))[-1]', '(log("k.log", "x"), open("k.log", encoding="utf-8").read())[-1]', lv=2),
    F("Sozlamalar fayli", "`oqi(nom)` — `kalit=qiymat` qatorlaridan lugʻat yasasin: boʻsh qatorlar va `#` bilan boshlanuvchi izohlarni tashlab, kalit va qiymat atrofidagi boʻsh joylarni olib tashlasin.",
      "def oqi(nom):\n    d = {}\n    with open(nom, encoding='utf-8') as f:\n        for q in f:\n            q = q.strip()\n            if not q or q.startswith('#'):\n                continue\n            k, v = q.split('=', 1)\n            d[k.strip()] = v.strip()\n    return d",
      'oqi("app.conf")', 'len(oqi("app.conf"))', 'oqi("bosh.conf")',
      files={"app.conf": "# Mirae sozlamalari\ntil = uz\n\ntema=dark\nurl = https://mirae.uz/?a=1\n", "bosh.conf": "# hech narsa\n"}, lv=2),
    F("Eng uzun qator", "`eng_uzun(nom)` — fayldagi eng uzun qator (`\\n` siz) va uning raqami (1 dan): `(raqam, qator)`.",
      "def eng_uzun(nom):\n    with open(nom, encoding='utf-8') as f:\n        qatorlar = f.read().splitlines()\n    i = max(range(len(qatorlar)), key=lambda k: len(qatorlar[k]))\n    return (i + 1, qatorlar[i])",
      'eng_uzun("she.txt")', 'eng_uzun("bir.txt")', 'eng_uzun("teng.txt")',
      files={"she.txt": "Vatan\nOna yurtim, xalqim\nSevaman\n", "bir.txt": "a", "teng.txt": "ab\ncd\n"}),
    F("Nusxa va katta harf", "`katta_nusxa(manba, natija)` — manbadagi matnni katta harflarga oʻtkazib natija fayliga yozsin, natija faylining birinchi qatorini qaytarsin.",
      "def katta_nusxa(manba, natija):\n    with open(manba, encoding='utf-8') as f, open(natija, 'w', encoding='utf-8') as g:\n        for q in f:\n            g.write(q.upper())\n    with open(natija, encoding='utf-8') as g:\n        return g.readline().rstrip('\\n')",
      'katta_nusxa("kirish.txt", "chiqish.txt")', 'katta_nusxa("bosh.txt", "b2.txt")', '(katta_nusxa("kirish.txt", "c.txt"), open("c.txt", encoding="utf-8").read().count("\\n"))[1]',
      files={"kirish.txt": "salom, mirae!\noʻzbekiston\n", "bosh.txt": ""}),
    L("docs", "py-inputoutput"),
    L("exercism", "grep"),
    L("lc", "find-duplicate-file-in-system"),
    L("exercism", "word-count", note="Fayldagi soʻzlarni sanash uchun ham shu gʻoya."),
])

# ---------------------------------------------------------------- 10.4
TOPIC("zip-fayllar", "ZIP arxivlar", "zipfile: arxivlash, ochish va ichini koʻrish", 15, r'''
Koʻp faylni bitta ixcham faylga jamlash — **arxivlash**. Python'da buning uchun `zipfile` moduli bor.

## Arxiv yaratish
```py
import zipfile
from pathlib import Path

Path("hisobot.txt").write_text("Oktabr hisoboti\n" * 50, encoding="utf-8")
Path("rasm.txt").write_text("(rasm oʻrnida)", encoding="utf-8")

with zipfile.ZipFile("arxiv.zip", "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.write("hisobot.txt")
    z.write("rasm.txt", arcname="media/rasm.txt")     # arxiv ichidagi nomi
    z.writestr("eslatma.txt", "Toʻgʻridan-toʻgʻri matndan")

print(Path("arxiv.zip").exists())
```

## Ichini koʻrish
```py
import zipfile

with zipfile.ZipFile("demo.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("a.txt", "salom " * 100)
    z.writestr("papka/b.txt", "dunyo")

with zipfile.ZipFile("demo.zip") as z:
    for info in z.infolist():
        print(f"{info.filename:<12} {info.file_size:>5} → {info.compress_size:>4} bayt")
    print(z.namelist())
```

> `ZIP_DEFLATED` — siqish. Takrorlanuvchi matn kuchli siqiladi: 600 bayt → bir necha oʻn bayt.

## Oʻqish va ochish
```py
import zipfile

with zipfile.ZipFile("demo.zip", "w") as z:
    z.writestr("salom.txt", "Assalomu alaykum!")
    z.writestr("data/sonlar.txt", "1 2 3")

with zipfile.ZipFile("demo.zip") as z:
    print(z.read("salom.txt").decode("utf-8"))   # faylni ochmasdan oʻqish
    z.extractall("ochilgan")                      # hammasini papkaga chiqarish

from pathlib import Path
print(sorted(p.as_posix() for p in Path("ochilgan").rglob("*") if p.is_file()))
```

## Papkani butunlay arxivlash
```py
import shutil
from pathlib import Path

Path("loyiha/src").mkdir(parents=True)
Path("loyiha/src/main.py").write_text("print('hi')")
Path("loyiha/README.md").write_text("# Loyiha")

yol = shutil.make_archive("loyiha_zaxira", "zip", "loyiha")
print(Path(yol).name)
```

!> Notanish manbadan kelgan arxivni `extractall` qilishdan oldin ichini tekshiring: fayl nomlarida `../` boʻlsa, ular papkadan tashqariga yozilishi mumkin.

## Esda tuting
- `ZipFile(nom, "w")` — yaratish, `"r"` — oʻqish, `"a"` — qoʻshish.
- `namelist()`, `read()`, `extractall()` — eng koʻp ishlatiladigan metodlar.
''', [
    P('import zipfile\nwith zipfile.ZipFile("a.zip", "w") as z:\n    z.writestr("x.txt", "1")\n    z.writestr("y.txt", "2")\nprint(zipfile.ZipFile("a.zip").namelist())', "['x.txt']", "2", "['a.zip']"),
    P('import zipfile\nwith zipfile.ZipFile("a.zip", "w") as z:\n    z.writestr("m.txt", "salom")\nprint(zipfile.ZipFile("a.zip").read("m.txt"))', "salom", "'salom'", "m.txt"),
    P('import zipfile\nwith zipfile.ZipFile("a.zip", "w") as z:\n    z.writestr("d/e.txt", "x")\nprint(zipfile.ZipFile("a.zip").namelist())', "['e.txt']", "['d', 'd/e.txt']", "['d\\\\e.txt']"),
    P('import zipfile\nprint(zipfile.is_zipfile("yoq.zip"))', "True", "None", "⚠ FileNotFoundError"),
    P('import zipfile\nopen("t.txt", "w").write("oddiy matn")\nprint(zipfile.is_zipfile("t.txt"))', "True", "None", "⚠ BadZipFile"),
    P('import zipfile\nwith zipfile.ZipFile("a.zip", "w", zipfile.ZIP_DEFLATED) as z:\n    z.writestr("b.txt", "a" * 1000)\ni = zipfile.ZipFile("a.zip").getinfo("b.txt")\nprint(i.file_size, i.compress_size < 100)', "1000 False", "100 True", "a True", lv=2),
    P('import zipfile\nz = zipfile.ZipFile("a.zip", "w")\nz.writestr("1.txt", "")\nz.close()\nwith zipfile.ZipFile("a.zip", "a") as z:\n    z.writestr("2.txt", "")\nprint(len(zipfile.ZipFile("a.zip").namelist()))', "1", "0", "Xato"),
    Q("Arxivdagi faylni diskka chiqarmasdan oʻqish usuli?", "z.read(\"nom.txt\")", "z.extractall()", "open(\"arxiv.zip/nom.txt\")", "z.namelist(\"nom.txt\")"),
    Q("Nega notanish arxivni darhol `extractall` qilish xavfli?", "Nomlarida ../ boʻlsa, fayllar papkadan tashqariga yozilishi mumkin", "Arxiv buziladi", "Juda sekin ishlaydi", "Python taqiqlaydi"),
    F("Arxiv yarat", "`arxivla(nom, fayllar)` — `{fayl_nomi: matn}` lugʻatidagi fayllarni `writestr` bilan arxivga yozsin, soʻng arxivdagi nomlar roʻyxatini (alifbo boʻyicha) qaytarsin.",
      "import zipfile\n\n\ndef arxivla(nom, fayllar):\n    with zipfile.ZipFile(nom, 'w', zipfile.ZIP_DEFLATED) as z:\n        for k, v in fayllar.items():\n            z.writestr(k, v)\n    with zipfile.ZipFile(nom) as z:\n        return sorted(z.namelist())",
      'arxivla("a.zip", {"b.txt": "1", "a.txt": "2"})', 'arxivla("bosh.zip", {})', 'arxivla("c.zip", {"p/q.txt": "x"})', lv=1),
    F("Arxiv ichida qidirish", "`top(arxiv, soz)` — arxivdagi `.txt` fayllardan ichida `soz` uchraganlarining nomlarini alifbo boʻyicha qaytarsin. (Tekshiruv arxivni `tayyorla.py` yordamida yaratadi.)",
      "import zipfile\n\n\ndef top(arxiv, soz):\n    with zipfile.ZipFile(arxiv) as z:\n        return sorted(n for n in z.namelist() if n.endswith('.txt') and soz in z.read(n).decode('utf-8'))",
      '(__import__("tayyorla").arxiv(), top("hujjatlar.zip", "Python"))[-1]', 'top("hujjatlar.zip", "yoʻq")', 'top("hujjatlar.zip", "a")',
      files={"tayyorla.py": "import zipfile\n\n\ndef arxiv():\n    with zipfile.ZipFile('hujjatlar.zip', 'w') as z:\n        z.writestr('dars1.txt', 'Python asoslari')\n        z.writestr('dars2.txt', 'Sinflar va obyektlar')\n        z.writestr('kod/main.py', 'print(\"Python\")')\n"}),
    F("Siqish darajasi", "`siqish(matn)` — matnni `ZIP_DEFLATED` bilan arxivlab, `compress_size / file_size` ni foizda (butun son, `round`) qaytarsin.",
      "import zipfile\n\n\ndef siqish(matn):\n    with zipfile.ZipFile('s.zip', 'w', zipfile.ZIP_DEFLATED) as z:\n        z.writestr('f.txt', matn)\n    i = zipfile.ZipFile('s.zip').getinfo('f.txt')\n    return round(i.compress_size / i.file_size * 100)",
      'siqish("abc" * 1000) < 5', 'siqish("a") > 100', 'type(siqish("salom dunyo " * 10)).__name__', lv=2),
    F("Hajm hisoboti", "`hisobot(arxiv)` — `{nom: file_size}` lugʻati (faqat fayllar, papkalar emas), nomlar alifbo tartibida.",
      "import zipfile\n\n\ndef hisobot(arxiv):\n    with zipfile.ZipFile(arxiv) as z:\n        return {i.filename: i.file_size for i in sorted(z.infolist(), key=lambda i: i.filename) if not i.is_dir()}",
      '(lambda: (__import__("zipfile").ZipFile("t.zip", "w").close(), hisobot("t.zip"))[-1])()', '(lambda z: (z.writestr("b.txt", "12345"), z.writestr("a/c.txt", ""), z.close(), hisobot("u.zip"))[-1])(__import__("zipfile").ZipFile("u.zip", "w"))', 'hisobot("yoq.zip")', lv=2),
    F("Ochish va sanash", "`och(arxiv, papka)` — arxivni papkaga chiqarib, chiqarilgan fayllar sonini qaytarsin.",
      "import zipfile\nfrom pathlib import Path\n\n\ndef och(arxiv, papka):\n    with zipfile.ZipFile(arxiv) as z:\n        z.extractall(papka)\n    return sum(1 for p in Path(papka).rglob('*') if p.is_file())",
      '(lambda z: (z.writestr("a.txt", "1"), z.writestr("b/c.txt", "2"), z.close(), och("x.zip", "chiqdi"))[-1])(__import__("zipfile").ZipFile("x.zip", "w"))',
      '(lambda z: (z.close(), och("y.zip", "boshq"))[-1])(__import__("zipfile").ZipFile("y.zip", "w"))', 'och("yoq.zip", "z")'),
    F("Xavfsiz nomlar", "`xavfsizmi(nomlar)` — arxiv fayl nomlari roʻyxatida `..` qismi yoki `/` bilan boshlanuvchi nom boʻlsa `False`, aks holda `True`.",
      "def xavfsizmi(nomlar):\n    for n in nomlar:\n        q = n.replace('\\\\', '/')\n        if q.startswith('/') or '..' in q.split('/'):\n            return False\n    return True",
      'xavfsizmi(["a.txt", "b/c.txt"])', 'xavfsizmi(["../etc/passwd"])', 'xavfsizmi(["/root/x"])', 'xavfsizmi(["a..b.txt"])', lv=3),
    F("Matnlarni arxivlash", "`jamla(matnlar)` — `{nom: matn}` ni `jamlama.zip` ga yozib, soʻng arxivdan qayta oʻqib `{nom: matn}` lugʻatini (nomlar alifbo boʻyicha) qaytarsin. Oʻzbekcha harflar buzilmasin (utf-8).",
      "import zipfile\n\n\ndef jamla(matnlar):\n    with zipfile.ZipFile('jamlama.zip', 'w', zipfile.ZIP_DEFLATED) as z:\n        for k, v in matnlar.items():\n            z.writestr(k, v)\n    with zipfile.ZipFile('jamlama.zip') as z:\n        return {n: z.read(n).decode('utf-8') for n in sorted(z.namelist())}",
      'jamla({"b.txt": "gʻoya", "a.txt": "oʻrik"})', "jamla({})", 'jamla({"x/y.txt": "1"})'),
    L("docs", "py-zipfile"),
    L("docs", "py-shutil", title="shutil.make_archive — papkani arxivlash"),
    L("lc", "encode-and-decode-tinyurl"),
    L("exercism", "run-length-encoding", note="Oddiy siqish algoritmini oʻzingiz yozing."),
])

# ---------------------------------------------------------------- 10.5
TOPIC("csv", "CSV fayllar", "Jadval maʼlumotlarini oʻqish va yozish", 20, r'''
**CSV** (Comma-Separated Values) — eng oddiy jadval formati. Excel, Google Sheets, bank koʻchirmalari, onlayn doʻkon hisobotlari — hammasi CSV ga eksport qila oladi.

```text
ism,fan,ball
Ali,Matematika,85
Madina,Fizika,92
```

## Yozish
```py
import csv

talabalar = [
    ["ism", "fan", "ball"],
    ["Ali", "Matematika", 85],
    ["Madina", "Fizika", 92],
    ["Bek", "Informatika", 78],
]
with open("baholar.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(talabalar)

print(open("baholar.csv", encoding="utf-8").read())
```

> `newline=""` — CSV yozishda **majburiy**, aks holda Windows'da qatorlar orasida boʻsh qator paydo boʻladi.

## Oʻqish
```py
import csv

with open("baholar.csv", "w", newline="", encoding="utf-8") as f:
    f.write("ism,fan,ball\nAli,Matematika,85\nMadina,Fizika,92\n")

with open("baholar.csv", newline="", encoding="utf-8") as f:
    oqish = csv.reader(f)
    sarlavha = next(oqish)
    for qator in oqish:
        print(qator)
print("Sarlavha:", sarlavha)
```

!> CSV dagi hamma qiymat — **satr**. Son kerak boʻlsa `int()` / `float()` qiling.

## DictReader — ustun nomlari bilan
```py
import csv

with open("savdo.csv", "w", newline="", encoding="utf-8") as f:
    f.write("mahsulot,narx,soni\nNon,4000,30\nSut,12000,12\nChoy,25000,4\n")

jami = 0
with open("savdo.csv", newline="", encoding="utf-8") as f:
    for q in csv.DictReader(f):
        summa = int(q["narx"]) * int(q["soni"])
        jami += summa
        print(f"{q['mahsulot']:<6}{summa:>8,}")
print(f"{'JAMI':<6}{jami:>8,}")
```

## DictWriter
```py
import csv, io

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=["ism", "tel"])
w.writeheader()
w.writerow({"ism": "Ali", "tel": "+998901234567"})
w.writerow({"ism": "Vali, aka", "tel": "+998911112233"})
print(buf.getvalue())
```

> Qiymatda vergul boʻlsa (`Vali, aka`), `csv` uni avtomatik qoʻshtirnoqqa oladi. Shuning uchun CSV ni `split(",")` bilan emas, `csv` moduli bilan oʻqing!

## Boshqa ajratuvchilar
```py
import csv, io

matn = "ism;ball\nAli;85\n"
for q in csv.reader(io.StringIO(matn), delimiter=";"):
    print(q)
```

## Esda tuting
- `csv.writer`/`csv.reader` — roʻyxatlar; `DictWriter`/`DictReader` — lugʻatlar.
- Ochishda `newline=""` va `encoding="utf-8"`.
''', [
    P('import csv, io\nprint(next(csv.reader(io.StringIO("a,b,c"))))', "a,b,c", "('a', 'b', 'c')", "['a,b,c']"),
    P('import csv, io\nprint(next(csv.reader(io.StringIO(\'"Vali, aka",5\'))))', "['\"Vali', ' aka\"', '5']", "['Vali', 'aka', '5']", "Xato"),
    P('import csv, io\nr = next(csv.reader(io.StringIO("Ali,85")))\nprint(r[1] + r[1])', "170", "Ali85", "Xato"),
    P('import csv, io\nb = io.StringIO()\ncsv.writer(b).writerow(["a", "b,c", 3])\nprint(b.getvalue().strip())', "a,b,c,3", "['a', 'b,c', 3]", "a b,c 3"),
    P('import csv, io\nfor q in csv.DictReader(io.StringIO("x,y\\n1,2\\n")):\n    print(q["y"])', "y", "1", "{'x': '1', 'y': '2'}"),
    P('import csv, io\nprint(len(list(csv.reader(io.StringIO("a\\nb\\nc\\n")))))', "1", "4", "6"),
    P('import csv, io\nprint(list(csv.reader(io.StringIO("1;2"), delimiter=";")))', "[['1;2']]", "['1', '2']", "[[1, 2]]"),
    Q("CSV faylni yozish uchun `open` da nima qoʻshish tavsiya etiladi?", "newline=\"\" (va encoding=\"utf-8\")", "mode=\"csv\"", "sep=\",\"", "binary=True"),
    Q("Nega CSV qatorini `split(\",\")` bilan ajratish xavfli?", "Qiymat ichida vergul (qoʻshtirnoqda) boʻlsa notoʻgʻri boʻlinadi", "split juda sekin", "split faqat probellarda ishlaydi", "Hech qanday xavf yoʻq"),
    F("O'rtacha ball", "`ortacha(fayl)` — `ism,ball` sarlavhali CSV dan oʻrtacha ballni 2 xonagacha yaxlitlab qaytarsin.",
      "import csv\n\n\ndef ortacha(fayl):\n    with open(fayl, newline='', encoding='utf-8') as f:\n        ballar = [int(q['ball']) for q in csv.DictReader(f)]\n    return round(sum(ballar) / len(ballar), 2)",
      'ortacha("baholar.csv")', 'ortacha("bitta.csv")', 'ortacha("bosh.csv")',
      files={"baholar.csv": "ism,ball\nAli,85\nMadina,92\nBek,78\n", "bitta.csv": "ism,ball\nX,100\n", "bosh.csv": "ism,ball\n"}, lv=1),
    F("CSV yozish", "`yoz(fayl, odamlar)` — `[(ism, yosh), ...]` ni `ism,yosh` sarlavhasi bilan CSV ga yozsin va fayl matnini (`\\r\\n` larni `\\n` ga almashtirib) qaytarsin.",
      "import csv\n\n\ndef yoz(fayl, odamlar):\n    with open(fayl, 'w', newline='', encoding='utf-8') as f:\n        w = csv.writer(f)\n        w.writerow(['ism', 'yosh'])\n        w.writerows(odamlar)\n    with open(fayl, encoding='utf-8', newline='') as f:\n        return f.read().replace('\\r\\n', '\\n')",
      'yoz("a.csv", [("Ali", 17), ("Vali, aka", 30)])', 'yoz("b.csv", [])', 'yoz("c.csv", [("Oʻ\"tkir", 1)])'),
    F("Savdo hisoboti", "`hisobot(fayl)` — `mahsulot,narx,soni` CSV dan `{mahsulot: narx*soni}` lugʻati; bir xil mahsulot bir necha marta boʻlsa — qoʻshilsin.",
      "import csv\n\n\ndef hisobot(fayl):\n    d = {}\n    with open(fayl, newline='', encoding='utf-8') as f:\n        for q in csv.DictReader(f):\n            d[q['mahsulot']] = d.get(q['mahsulot'], 0) + int(q['narx']) * int(q['soni'])\n    return d",
      'hisobot("savdo.csv")', 'sum(hisobot("savdo.csv").values())', 'hisobot("bosh.csv")',
      files={"savdo.csv": "mahsulot,narx,soni\nNon,4000,30\nSut,12000,12\nNon,4000,5\n", "bosh.csv": "mahsulot,narx,soni\n"}),
    F("Filtrlash", "`otganlar(manba, natija)` — `ism,ball` CSV dan 60 va undan yuqori ball olganlarni yangi CSV ga (xuddi shu sarlavha bilan) yozsin; yozilgan qatorlar sonini qaytarsin.",
      "import csv\n\n\ndef otganlar(manba, natija):\n    with open(manba, newline='', encoding='utf-8') as f:\n        q = [r for r in csv.DictReader(f) if int(r['ball']) >= 60]\n    with open(natija, 'w', newline='', encoding='utf-8') as f:\n        w = csv.DictWriter(f, fieldnames=['ism', 'ball'])\n        w.writeheader()\n        w.writerows(q)\n    return len(q)",
      'otganlar("guruh.csv", "otgan.csv")', '(otganlar("guruh.csv", "o.csv"), open("o.csv", encoding="utf-8").read().splitlines())[1]', 'otganlar("hamma.csv", "h.csv")',
      files={"guruh.csv": "ism,ball\nAli,59\nMadina,92\nBek,60\nGani,10\n", "hamma.csv": "ism,ball\nA,100\nB,99\n"}, lv=2),
    F("Ajratuvchini aniqlash", "`ajratuvchi(matn)` — `csv.Sniffer().sniff(matn).delimiter` yordamida ajratuvchini qaytarsin.",
      "import csv\n\n\ndef ajratuvchi(matn):\n    return csv.Sniffer().sniff(matn).delimiter",
      'ajratuvchi("a;b;c\\n1;2;3\\n")', 'ajratuvchi("a,b\\n1,2\\n")', 'ajratuvchi("a\\tb\\n1\\t2\\n")', lv=3),
    F("Ustun yigʻindilari", "`ustunlar(fayl)` — sonli CSV (sarlavhali) dan har bir ustun yigʻindisini `{ustun: yigʻindi}` qilib qaytarsin.",
      "import csv\n\n\ndef ustunlar(fayl):\n    with open(fayl, newline='', encoding='utf-8') as f:\n        r = csv.DictReader(f)\n        jami = {k: 0 for k in r.fieldnames}\n        for q in r:\n            for k in jami:\n                jami[k] += float(q[k])\n    return jami",
      'ustunlar("oylar.csv")', 'ustunlar("bir.csv")', 'sum(ustunlar("oylar.csv").values())',
      files={"oylar.csv": "yanvar,fevral,mart\n10,20,30\n1.5,2.5,3.5\n", "bir.csv": "x\n5\n"}, lv=2),
    F("Eksport", "`eksport(talabalar)` — `[{\"ism\":…, \"ball\":…}]` roʻyxatini `io.StringIO` ga `DictWriter` bilan (`ism,ball` sarlavha, `lineterminator=\"\\n\"`) yozib, matnni qaytarsin.",
      "import csv\nimport io\n\n\ndef eksport(talabalar):\n    b = io.StringIO()\n    w = csv.DictWriter(b, fieldnames=['ism', 'ball'], lineterminator='\\n')\n    w.writeheader()\n    w.writerows(talabalar)\n    return b.getvalue()",
      'eksport([{"ism": "Ali", "ball": 85}, {"ism": "Vali, aka", "ball": 90}])', "eksport([])", 'eksport([{"ism": "X", "ball": 0}])', lv=1),
    L("docs", "py-csv"),
    L("exercism", "tournament", note="Jadvalni oʻqib, natijalar jadvalini chiqarish."),
    L("exercism", "etl"),
    L("lc", "sort-the-students-by-their-kth-score"),
])

# ---------------------------------------------------------------- 10.6
TOPIC("json", "JSON fayllar", "Maʼlumot almashishning asosiy formati", 20, r'''
**JSON** — internetdagi maʼlumot almashishning asosiy formati: API javoblari, sozlama fayllari, mobil ilovalar va serverlar orasidagi "til". U Python lugʻat va roʻyxatlariga juda oʻxshaydi.

```text
{
  "ism": "Madina",
  "yosh": 16,
  "fanlar": ["matematika", "fizika"],
  "faol": true,
  "telefon": null
}
```

| JSON | Python |
|---|---|
| `{}` object | `dict` |
| `[]` array | `list` |
| `"satr"` | `str` |
| `5`, `3.14` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## Python → JSON (dumps / dump)
```py
import json

talaba = {"ism": "Oʻktam", "yosh": 17, "fanlar": ["fizika"], "faol": True, "tel": None}
matn = json.dumps(talaba, ensure_ascii=False)
print(matn)
print(json.dumps(talaba, ensure_ascii=False, indent=2))
```

> `ensure_ascii=False` — oʻzbekcha harflar `\u02bb` boʻlib ketmasligi uchun.

## JSON → Python (loads / load)
```py
import json

javob = '{"shahar": "Samarqand", "harorat": 24.5, "yomgir": false}'
d = json.loads(javob)
print(d["shahar"], d["harorat"] + 1, d["yomgir"])
print(type(d).__name__)
```

## Fayl bilan
```py
import json

sozlama = {"til": "uz", "tema": "qorongʻi", "shrift": 16}
with open("sozlama.json", "w", encoding="utf-8") as f:
    json.dump(sozlama, f, ensure_ascii=False, indent=2)

with open("sozlama.json", encoding="utf-8") as f:
    yuklandi = json.load(f)
print(yuklandi == sozlama, yuklandi["tema"])
```

## Ichma-ich maʼlumot
```py
import json

api = """
{"natijalar": [
  {"nom": "Registon", "reyting": 4.9, "manzil": {"shahar": "Samarqand"}},
  {"nom": "Ichan qalʼa", "reyting": 4.8, "manzil": {"shahar": "Xiva"}}
]}
"""
for joy in json.loads(api)["natijalar"]:
    print(f"{joy['nom']} ({joy['manzil']['shahar']}) — {joy['reyting']}")
```

## Nima JSON boʻla olmaydi?
!> `set`, `datetime`, oʻz sinflaringiz — `TypeError: Object of type ... is not JSON serializable`. Ularni avval roʻyxat/satrga aylantiring yoki `default=` parametrini bering.

```py
import json
from datetime import date

print(json.dumps({"sana": date(2026, 10, 13)}, default=str))
```

## Esda tuting
- `dumps`/`loads` — satr bilan, `dump`/`load` — fayl bilan (s — string).
- `ensure_ascii=False, indent=2` — oʻqiladigan, oʻzbekcha JSON.
''', [
    P('import json\nprint(json.dumps({"a": True, "b": None}))', '{"a": True, "b": None}', "{'a': true, 'b': null}", '{"a": "True", "b": "None"}'),
    P('import json\nd = json.loads(\'{"x": [1, 2, 3]}\')\nprint(sum(d["x"]))', "[1, 2, 3]", "123", "Xato"),
    P('import json\nprint(json.loads("[1, 2]") == [1, 2])', "False", "Xato", "[1, 2]"),
    P('import json\nprint(json.dumps("oʻ"))', '"oʻ"', "oʻ", "Xato", lv=2),
    P('import json\nprint(json.dumps({1, 2}))', "[1, 2]", "{1, 2}", "⚠ ValueError"),
    P('import json\nprint(json.dumps((1, 2)))', "(1, 2)", "⚠ TypeError", '"(1, 2)"', lv=2),
    P('import json\nprint(json.loads(\'{"a": 1, "a": 2}\'))', "{'a': 1}", "⚠ ValueError", "{'a': 1, 'a': 2}", lv=3),
    Q("`json.dump` va `json.dumps` farqi?", "dump — faylga yozadi, dumps — satr qaytaradi", "Farqi yoʻq", "dumps — faylga yozadi", "dump faqat roʻyxatlar uchun"),
    Q("JSON dagi `null` Python'da nima boʻladi?", "None", "0", "\"null\"", "False"),
    F("JSON dan maʼlumot", "`ism_va_yosh(matn)` — JSON satrdan `\"ISM (YOSH)\"` qaytarsin.",
      "import json\n\n\ndef ism_va_yosh(matn):\n    d = json.loads(matn)\n    return f\"{d['ism']} ({d['yosh']})\"",
      "ism_va_yosh('{\"ism\": \"Ali\", \"yosh\": 17}')", "ism_va_yosh('{\"yosh\": 9, \"ism\": \"Sevara\", \"shahar\": \"Termiz\"}')", "ism_va_yosh('{\"ism\": \"Oʻktam\", \"yosh\": 30}')", lv=1),
    F("Chiroyli JSON", "`chiroyli(d)` — lugʻatni `indent=2`, `ensure_ascii=False`, `sort_keys=True` bilan JSON satrga aylantirsin.",
      "import json\n\n\ndef chiroyli(d):\n    return json.dumps(d, indent=2, ensure_ascii=False, sort_keys=True)",
      'chiroyli({"b": 1, "a": "oʻ"})', "chiroyli({})", 'chiroyli({"x": [1, 2]})', lv=1),
    F("Ob-havo API", "`issiq_shaharlar(matn, chegara)` — API javobidagi (`{\"shaharlar\": [{\"nom\", \"harorat\"}]}`) haroratı chegaradan yuqori shaharlar nomlarini haroratining kamayishi boʻyicha qaytarsin.",
      "import json\n\n\ndef issiq_shaharlar(matn, chegara):\n    s = json.loads(matn)['shaharlar']\n    return [x['nom'] for x in sorted(s, key=lambda x: -x['harorat']) if x['harorat'] > chegara]",
      "issiq_shaharlar('{\"shaharlar\": [{\"nom\": \"Toshkent\", \"harorat\": 31}, {\"nom\": \"Nukus\", \"harorat\": 36}, {\"nom\": \"Chimgan\", \"harorat\": 19}]}', 25)",
      "issiq_shaharlar('{\"shaharlar\": []}', 0)", "issiq_shaharlar('{\"shaharlar\": [{\"nom\": \"A\", \"harorat\": 5}]}', 5)"),
    F("Saqlash va yuklash", "`hisoblagich(fayl)` — JSON fayldan `{\"marta\": N}` ni oʻqisin (yoʻq boʻlsa N=0), N ni 1 ga oshirib qayta yozsin va yangi N ni qaytarsin.",
      "import json\nfrom pathlib import Path\n\n\ndef hisoblagich(fayl):\n    p = Path(fayl)\n    d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'marta': 0}\n    d['marta'] += 1\n    p.write_text(json.dumps(d), encoding='utf-8')\n    return d['marta']",
      'hisoblagich("h.json")', '(hisoblagich("k.json"), hisoblagich("k.json"), hisoblagich("k.json"))[-1]', 'hisoblagich("bor.json")',
      files={"bor.json": '{"marta": 41}'}, lv=2),
    F("Ichma-ich", "`shaharlar(matn)` — `natijalar[*].manzil.shahar` qiymatlarini takrorsiz, alifbo boʻyicha qaytarsin; manzili yoʻqlarini tashlab ketsin.",
      "import json\n\n\ndef shaharlar(matn):\n    r = json.loads(matn)['natijalar']\n    return sorted({x['manzil']['shahar'] for x in r if 'manzil' in x})",
      "shaharlar('{\"natijalar\": [{\"manzil\": {\"shahar\": \"Xiva\"}}, {\"nom\": \"x\"}, {\"manzil\": {\"shahar\": \"Buxoro\"}}, {\"manzil\": {\"shahar\": \"Xiva\"}}]}')",
      "shaharlar('{\"natijalar\": []}')", "shaharlar('{\"natijalar\": [{\"manzil\": {\"shahar\": \"Andijon\"}}]}')", lv=2),
    F("Maxsus turlar", "`saqla(d)` — `set` larni saralangan roʻyxatga, `date` larni ISO satrga aylantirib (`default=` funksiyasi bilan) JSON satr qaytarsin.",
      "import json\nfrom datetime import date\n\n\ndef saqla(d):\n    def aylantir(x):\n        if isinstance(x, set):\n            return sorted(x)\n        if isinstance(x, date):\n            return x.isoformat()\n        raise TypeError(type(x).__name__)\n    return json.dumps(d, default=aylantir)",
      'saqla({"teglar": {"b", "a"}, "sana": __import__("datetime").date(2026, 10, 13)})', 'saqla({"x": 1})', 'saqla({"o": object()})', lv=3),
    F("Yaroqlimi", "`yaroqli(matn)` — matn toʻgʻri JSON boʻlsa `True`, `json.JSONDecodeError` boʻlsa `False`.",
      "import json\n\n\ndef yaroqli(matn):\n    try:\n        json.loads(matn)\n        return True\n    except json.JSONDecodeError:\n        return False",
      "yaroqli('{\"a\": 1}')", "yaroqli(\"{'a': 1}\")", "yaroqli('[1, 2,]')", "yaroqli('null')"),
    L("docs", "py-json"),
    L("exercism", "rest-api", note="JSON bilan ishlaydigan kichik REST API."),
    L("lc", "encode-and-decode-tinyurl"),
    L("exercism", "etl"),
])

# ---------------------------------------------------------------- 10.7
TOPIC("sqlite", "SQLite maʼlumotlar bazasi", "SQL bilan maʼlumot saqlash va soʻrash", 30, r'''
Fayl va JSON kichik maʼlumot uchun yaxshi. Lekin minglab yozuvlar ichidan tez qidirish, saralash, guruhlash kerak boʻlsa — **maʼlumotlar bazasi** kerak. Python bilan birga **SQLite** keladi: server shart emas, butun baza — bitta fayl.

## Ulanish va jadval yaratish
```py
import sqlite3

con = sqlite3.connect(":memory:")       # yoki "maktab.db" — fayl
cur = con.cursor()
cur.execute("""
    CREATE TABLE talabalar (
        id    INTEGER PRIMARY KEY,
        ism   TEXT NOT NULL,
        sinf  TEXT,
        ball  INTEGER
    )
""")
cur.executemany(
    "INSERT INTO talabalar (ism, sinf, ball) VALUES (?, ?, ?)",
    [("Ali", "10-A", 85), ("Madina", "10-B", 92), ("Bek", "10-A", 78), ("Laylo", "10-B", 88)],
)
con.commit()
print("Qoʻshildi:", cur.execute("SELECT COUNT(*) FROM talabalar").fetchone()[0])
```

## SELECT — soʻrash
```py
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (ism TEXT, sinf TEXT, ball INTEGER)")
con.executemany("INSERT INTO t VALUES (?, ?, ?)",
                [("Ali", "10-A", 85), ("Madina", "10-B", 92), ("Bek", "10-A", 78), ("Laylo", "10-B", 88)])

for ism, ball in con.execute("SELECT ism, ball FROM t WHERE ball >= 80 ORDER BY ball DESC"):
    print(ism, ball)

print(con.execute("SELECT sinf, AVG(ball), COUNT(*) FROM t GROUP BY sinf").fetchall())
```

| SQL | Maʼnosi |
|---|---|
| `SELECT ... FROM jadval` | ustunlarni olish |
| `WHERE shart` | filtrlash |
| `ORDER BY ustun DESC` | saralash (kamayish) |
| `GROUP BY ustun` | guruhlash (`COUNT`, `AVG`, `SUM`) |
| `UPDATE ... SET ... WHERE` | oʻzgartirish |
| `DELETE FROM ... WHERE` | oʻchirish |

## UPDATE va DELETE
```py
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE mahsulot (nom TEXT, narx INTEGER)")
con.executemany("INSERT INTO mahsulot VALUES (?, ?)", [("non", 4000), ("sut", 12000), ("choy", 25000)])

con.execute("UPDATE mahsulot SET narx = narx + 500 WHERE nom = ?", ("non",))
con.execute("DELETE FROM mahsulot WHERE narx > ?", (20000,))
con.commit()
print(con.execute("SELECT * FROM mahsulot").fetchall())
```

## Xavfsizlik: doim ? ishlating
!> Soʻrovga foydalanuvchi kiritgan qiymatni **hech qachon** f-satr bilan qoʻshmang — bu **SQL injection** hujumiga yoʻl ochadi. Doim `?` va parametrlar kortejini ishlating.

```py
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE u (login TEXT)")
con.execute("INSERT INTO u VALUES ('admin')")

kirish = "x' OR '1'='1"
xavfli = con.execute(f"SELECT COUNT(*) FROM u WHERE login = '{kirish}'").fetchone()[0]
xavfsiz = con.execute("SELECT COUNT(*) FROM u WHERE login = ?", (kirish,)).fetchone()[0]
print("f-satr bilan topildi:", xavfli, "← hujum ishladi!")
print("? bilan topildi:", xavfsiz)
```

## Natijani lugʻat qilib olish
```py
import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
con.execute("CREATE TABLE k (nom TEXT, muallif TEXT)")
con.execute("INSERT INTO k VALUES ('Oʻtkan kunlar', 'Abdulla Qodiriy')")
q = con.execute("SELECT * FROM k").fetchone()
print(q["nom"], "—", q["muallif"])
print(dict(q))
```

## Esda tuting
- `connect` → `execute` → `commit` → `close` (yoki `with con:`).
- Parametrlar faqat `?` orqali — SQL injection'dan himoya.
''', [
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE t (x INTEGER)")\ncon.executemany("INSERT INTO t VALUES (?)", [(1,), (2,), (3,)])\nprint(con.execute("SELECT SUM(x) FROM t").fetchone())', "6", "[6]", "(1, 2, 3)"),
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE t (x)")\nprint(con.execute("SELECT * FROM t").fetchall())', "None", "[()]", "Xato"),
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE t (n TEXT, b INT)")\ncon.executemany("INSERT INTO t VALUES (?, ?)", [("a", 5), ("b", 9), ("c", 7)])\nprint(con.execute("SELECT n FROM t ORDER BY b DESC LIMIT 1").fetchone()[0])', "a", "c", "9"),
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE t (x)")\ncon.execute("INSERT INTO t VALUES (?)", (5,))\nprint(con.execute("SELECT x * 2 FROM t").fetchone()[0])', "5", "55", "(10,)"),
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("SELEC 1")', "None", "1", "⚠ SyntaxError"),
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE t (x INTEGER PRIMARY KEY, y)")\ncur = con.execute("INSERT INTO t (y) VALUES (\'a\')")\ncur = con.execute("INSERT INTO t (y) VALUES (\'b\')")\nprint(cur.lastrowid)', "1", "b", "None", lv=2),
    P('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE t (s TEXT, n INT)")\ncon.executemany("INSERT INTO t VALUES (?, ?)", [("A", 1), ("B", 2), ("A", 3)])\nprint(con.execute("SELECT s, SUM(n) FROM t GROUP BY s ORDER BY s").fetchall())', "[('A', 1), ('B', 2), ('A', 3)]", "[('A', 3), ('B', 2)]", "{'A': 4, 'B': 2}", lv=2),
    Q("SQL injection'dan himoyalanishning toʻgʻri usuli?", "Parametrlarni ? orqali uzatish", "f-satr bilan qiymat qoʻshish", "Qiymatni katta harfga oʻtkazish", "Soʻrovni ikki marta bajarish"),
    Q("`con.commit()` nima uchun kerak?", "Oʻzgarishlarni bazaga doimiy saqlash uchun", "Ulanishni ochish uchun", "Jadval yaratish uchun", "Natijani chiqarish uchun"),
    F("Jadval va yozuvlar", "`top_talaba(talabalar)` — `:memory:` bazada `t(ism, ball)` jadval yaratib, `[(ism, ball)]` larni qoʻshsin va eng yuqori ballli talaba ismini SQL bilan qaytarsin.",
      "import sqlite3\n\n\ndef top_talaba(talabalar):\n    con = sqlite3.connect(':memory:')\n    con.execute('CREATE TABLE t (ism TEXT, ball INTEGER)')\n    con.executemany('INSERT INTO t VALUES (?, ?)', talabalar)\n    return con.execute('SELECT ism FROM t ORDER BY ball DESC LIMIT 1').fetchone()[0]",
      'top_talaba([("Ali", 85), ("Madina", 92), ("Bek", 78)])', 'top_talaba([("X", 1)])', 'top_talaba([("A", -5), ("B", -1)])', lv=1),
    F("Guruh oʻrtachasi", "`ortachalar(qatorlar)` — `(ism, sinf, ball)` lardan har bir sinf oʻrtachasini SQL `GROUP BY` bilan hisoblab, `{sinf: oʻrtacha}` (1 xona) qaytarsin.",
      "import sqlite3\n\n\ndef ortachalar(qatorlar):\n    con = sqlite3.connect(':memory:')\n    con.execute('CREATE TABLE t (ism, sinf, ball)')\n    con.executemany('INSERT INTO t VALUES (?, ?, ?)', qatorlar)\n    return {s: round(o, 1) for s, o in con.execute('SELECT sinf, AVG(ball) FROM t GROUP BY sinf ORDER BY sinf')}",
      'ortachalar([("A", "10-A", 85), ("B", "10-B", 92), ("C", "10-A", 78), ("D", "10-B", 88)])', "ortachalar([])", 'ortachalar([("X", "9-A", 100)])'),
    F("Xavfsiz qidiruv", "`login_bor(foydalanuvchilar, login)` — jadvalga loginlarni qoʻshib, berilgan login borligini **parametrli** soʻrov bilan tekshirsin. Hujum satri `x' OR '1'='1` uchun `False` chiqishi kerak.",
      "import sqlite3\n\n\ndef login_bor(foydalanuvchilar, login):\n    con = sqlite3.connect(':memory:')\n    con.execute('CREATE TABLE u (login TEXT)')\n    con.executemany('INSERT INTO u VALUES (?)', [(x,) for x in foydalanuvchilar])\n    return con.execute('SELECT COUNT(*) FROM u WHERE login = ?', (login,)).fetchone()[0] > 0",
      'login_bor(["admin", "ali"], "ali")', 'login_bor(["admin"], "vali")', 'login_bor(["admin"], "x\' OR \'1\'=\'1")', lv=2),
    F("Fayl baza", "`dokon(fayl)` — fayldagi bazaga ulanib (`mahsulot(nom, narx)` jadvali allaqachon bor), narxi 10000 dan kam mahsulotlar narxini 10% oshirsin (`int`), commit qilsin va barcha mahsulotlarni nom boʻyicha saralab `[(nom, narx)]` qaytarsin. (Tekshiruv bazani `tayyorla.py` bilan yaratadi.)",
      "import sqlite3\n\n\ndef dokon(fayl):\n    con = sqlite3.connect(fayl)\n    con.execute('UPDATE mahsulot SET narx = CAST(narx * 1.1 AS INTEGER) WHERE narx < 10000')\n    con.commit()\n    natija = con.execute('SELECT nom, narx FROM mahsulot ORDER BY nom').fetchall()\n    con.close()\n    return natija",
      '(__import__("tayyorla").baza(), dokon("dokon.db"))[-1]', 'dokon("dokon.db")', '(__import__("tayyorla").baza(), len(dokon("dokon.db")))[-1]',
      files={"tayyorla.py": "import sqlite3\n\n\ndef baza():\n    c = sqlite3.connect('dokon.db')\n    c.execute('CREATE TABLE IF NOT EXISTS mahsulot (nom TEXT, narx INTEGER)')\n    c.execute('DELETE FROM mahsulot')\n    c.executemany('INSERT INTO mahsulot VALUES (?, ?)', [('non', 4000), ('sut', 12000), ('tuz', 2000)])\n    c.commit()\n    c.close()\n"}, lv=3),
    F("Row factory", "`kitoblar(royxat)` — `(nom, muallif, yil)` larni jadvalga yozib, `sqlite3.Row` bilan 2000-yildan keyingilarini `[{\"nom\":…, \"yil\":…}]` lugʻatlar roʻyxati qilib (yil boʻyicha) qaytarsin.",
      "import sqlite3\n\n\ndef kitoblar(royxat):\n    con = sqlite3.connect(':memory:')\n    con.row_factory = sqlite3.Row\n    con.execute('CREATE TABLE k (nom, muallif, yil)')\n    con.executemany('INSERT INTO k VALUES (?, ?, ?)', royxat)\n    return [dict(r) for r in con.execute('SELECT nom, yil FROM k WHERE yil > 2000 ORDER BY yil')]",
      'kitoblar([("A", "x", 1999), ("B", "y", 2015), ("C", "z", 2005)])', "kitoblar([])", 'kitoblar([("Eski", "x", 1900)])', lv=2),
    F("Ikki jadval (JOIN)", "`sotuvlar(mahsulotlar, buyurtmalar)` — `mahsulot(id, nom, narx)` va `buyurtma(mahsulot_id, soni)` jadvallarini yaratib, `JOIN` bilan har bir mahsulot boʻyicha jami tushumni `[(nom, summa)]` (summa kamayishi boʻyicha) qaytarsin.",
      "import sqlite3\n\n\ndef sotuvlar(mahsulotlar, buyurtmalar):\n    con = sqlite3.connect(':memory:')\n    con.execute('CREATE TABLE mahsulot (id INTEGER PRIMARY KEY, nom TEXT, narx INTEGER)')\n    con.execute('CREATE TABLE buyurtma (mahsulot_id INTEGER, soni INTEGER)')\n    con.executemany('INSERT INTO mahsulot VALUES (?, ?, ?)', mahsulotlar)\n    con.executemany('INSERT INTO buyurtma VALUES (?, ?)', buyurtmalar)\n    return con.execute('''SELECT m.nom, SUM(m.narx * b.soni) AS s FROM buyurtma b JOIN mahsulot m ON m.id = b.mahsulot_id GROUP BY m.id ORDER BY s DESC''').fetchall()",
      'sotuvlar([(1, "non", 4000), (2, "sut", 12000)], [(1, 10), (2, 2), (1, 5)])', 'sotuvlar([(1, "a", 1)], [])', 'sotuvlar([(1, "a", 10), (2, "b", 1)], [(2, 100)])', lv=3),
    F("CRUD", "`kundalik(amallar)` — `:memory:` bazada `vazifa(id INTEGER PRIMARY KEY, matn TEXT, bajarildi INTEGER DEFAULT 0)` jadvali. Amallar: `(\"qosh\", matn)`, `(\"bajar\", id)`, `(\"ochir\", id)`. Oxirida bajarilmagan vazifalar matnlarini id boʻyicha qaytarsin.",
      "import sqlite3\n\n\ndef kundalik(amallar):\n    con = sqlite3.connect(':memory:')\n    con.execute('CREATE TABLE vazifa (id INTEGER PRIMARY KEY, matn TEXT, bajarildi INTEGER DEFAULT 0)')\n    for amal, x in amallar:\n        if amal == 'qosh':\n            con.execute('INSERT INTO vazifa (matn) VALUES (?)', (x,))\n        elif amal == 'bajar':\n            con.execute('UPDATE vazifa SET bajarildi = 1 WHERE id = ?', (x,))\n        elif amal == 'ochir':\n            con.execute('DELETE FROM vazifa WHERE id = ?', (x,))\n    return [r[0] for r in con.execute('SELECT matn FROM vazifa WHERE bajarildi = 0 ORDER BY id')]",
      'kundalik([("qosh", "Python"), ("qosh", "SQL"), ("qosh", "Git"), ("bajar", 1), ("ochir", 3)])', "kundalik([])", 'kundalik([("qosh", "a"), ("bajar", 9)])', lv=2),
    L("docs", "py-sqlite3"),
    L("lc", "design-sql", note="SQL soʻrovlarini oʻzingiz simulyatsiya qilasiz (Premium boʻlishi mumkin)."),
    L("lc", "design-underground-system"),
    L("lc", "design-a-food-rating-system"),
])

# ---------------------------------------------------------------- 10.8
TOPIC("sana-vaqt", "Sana va vaqt (datetime)", "Sanalar, vaqt farqlari va formatlash", 25, r'''
Tugʻilgan kun, toʻlov muddati, dars jadvali, "3 kun oldin" — sanalar har bir ilovada bor. Python'da asosiy modul — **`datetime`**.

## Sana, vaqt va sana-vaqt
```py
from datetime import date, time, datetime

d = date(2026, 10, 13)
t = time(14, 30)
dt = datetime(2026, 10, 13, 14, 30, 0)

print(d, d.year, d.month, d.day)
print(t)
print(dt)
print(d.weekday())        # 0 — dushanba, 6 — yakshanba
print(d.isoformat())
```

> Hozirgi vaqt: `datetime.now()`, bugungi sana: `date.today()`. Misollarda natija har doim bir xil boʻlishi uchun aniq sanalardan foydalanamiz.

## timedelta — vaqt oraligʻi
```py
from datetime import date, datetime, timedelta

bugun = date(2026, 10, 13)
print(bugun + timedelta(days=30))           # 30 kundan keyin
print(bugun - timedelta(weeks=2))           # 2 hafta oldin

yangi_yil = date(2027, 1, 1)
qoldi = yangi_yil - bugun
print(qoldi.days, "kun qoldi")

boshlanish = datetime(2026, 10, 13, 9, 0)
tugash = datetime(2026, 10, 13, 10, 35)
print(tugash - boshlanish, (tugash - boshlanish).total_seconds() / 60, "daqiqa")
```

## Formatlash: strftime
```py
from datetime import datetime

dt = datetime(2026, 10, 13, 9, 5)
print(dt.strftime("%d.%m.%Y"))
print(dt.strftime("%H:%M"))
print(dt.strftime("%Y-%m-%d %H:%M:%S"))
```

| Kod | Maʼnosi | Misol |
|---|---|---|
| `%d` | kun | `13` |
| `%m` | oy | `10` |
| `%Y` | yil | `2026` |
| `%H:%M` | soat:daqiqa | `09:05` |
| `%A`, `%B` | hafta kuni, oy nomi (inglizcha) | `Tuesday`, `October` |

## Satrdan sana: strptime
```py
from datetime import datetime

s = "25.12.2026 18:00"
dt = datetime.strptime(s, "%d.%m.%Y %H:%M")
print(dt, dt.year)
print(datetime.fromisoformat("2026-10-13T09:30:00"))
```

## Vaqt zonasi va timestamp
```py
from datetime import datetime, timezone, timedelta

toshkent = timezone(timedelta(hours=5), "UZT")
dt = datetime(2026, 10, 13, 12, 0, tzinfo=toshkent)
print(dt.astimezone(timezone.utc))
print(int(dt.timestamp()))              # 1970-yildan beri soniyalar
print(datetime.fromtimestamp(0, timezone.utc))
```

## time moduli
```py
import time

boshlash = time.perf_counter()
s = sum(range(100_000))
oʻtdi = time.perf_counter() - boshlash
print("Hisoblandi:", s, "| vaqt < 1 s:", oʻtdi < 1)
```

## Esda tuting
- `date`, `time`, `datetime`, `timedelta` — asosiy toʻrtlik.
- `strftime` — sanadan satr, `strptime` — satrdan sana.
''', [
    P('from datetime import date\nprint(date(2026, 10, 13).weekday())', "2", "13", "Seshanba"),
    P('from datetime import date, timedelta\nprint(date(2026, 12, 30) + timedelta(days=5))', "2026-12-35", "2026-01-04", "Xato"),
    P('from datetime import date\nprint((date(2027, 1, 1) - date(2026, 12, 25)).days)', "6", "8", "-7"),
    P('from datetime import datetime\nprint(datetime(2026, 1, 5, 9, 7).strftime("%d.%m %H:%M"))', "5.1 9:7", "05.01.2026 09:07", "01.05 07:09"),
    P('from datetime import datetime\nprint(datetime.strptime("03/04/2026", "%d/%m/%Y").month)', "3", "2026", "Mart"),
    P('from datetime import date\nprint(date(2024, 2, 29).replace(year=2025))', "2025-02-28", "2025-03-01", "2025-02-29", lv=3),
    P('from datetime import timedelta\nprint(timedelta(hours=25))', "25:00:00", "1 day", "1:01:00", lv=2),
    Q("Ikki sana orasidagi kunlar sonini qanday topamiz?", "(sana2 - sana1).days", "sana2.day - sana1.day", "len(sana2 - sana1)", "sana2 // sana1"),
    Q("`\"13.10.2026\"` satrini sanaga aylantirish uchun qaysi biri?", "datetime.strptime(s, \"%d.%m.%Y\")", "datetime.strftime(s, \"%d.%m.%Y\")", "date(s)", "int(s)"),
    F("Yosh", "`yosh(tugilgan, bugun)` — ikki `date` dan toʻliq yillar sonini qaytarsin (tugʻilgan kun hali kelmagan boʻlsa bir yil kam).",
      "def yosh(tugilgan, bugun):\n    y = bugun.year - tugilgan.year\n    if (bugun.month, bugun.day) < (tugilgan.month, tugilgan.day):\n        y -= 1\n    return y",
      "yosh(__import__('datetime').date(2009, 3, 15), __import__('datetime').date(2026, 10, 13))",
      "yosh(__import__('datetime').date(2009, 12, 31), __import__('datetime').date(2026, 10, 13))",
      "yosh(__import__('datetime').date(2026, 10, 13), __import__('datetime').date(2026, 10, 13))", lv=1),
    F("Muddat", "`muddat(sana_satr, kun)` — `\"DD.MM.YYYY\"` sanaga kun qoʻshib, natijani xuddi shu formatda qaytarsin.",
      "from datetime import datetime, timedelta\n\n\ndef muddat(sana_satr, kun):\n    d = datetime.strptime(sana_satr, '%d.%m.%Y') + timedelta(days=kun)\n    return d.strftime('%d.%m.%Y')",
      'muddat("13.10.2026", 30)', 'muddat("28.02.2028", 1)', 'muddat("01.01.2026", -1)'),
    F("Hafta kuni", "`kun_nomi(yil, oy, kun)` — oʻzbekcha hafta kuni nomini qaytarsin: Dushanba … Yakshanba.",
      "from datetime import date\n\n\ndef kun_nomi(yil, oy, kun):\n    nomlar = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']\n    return nomlar[date(yil, oy, kun).weekday()]",
      "kun_nomi(2026, 10, 13)", "kun_nomi(1991, 9, 1)", "kun_nomi(2027, 1, 1)", lv=1),
    F("Dars davomiyligi", "`davomiylik(boshlanish, tugash)` — `\"HH:MM\"` satrlaridan daqiqalar farqini qaytarsin; tugash boshlanishdan oldin boʻlsa (yarim tundan oʻtsa) ertasi kun deb hisoblang.",
      "from datetime import datetime, timedelta\n\n\ndef davomiylik(boshlanish, tugash):\n    a = datetime.strptime(boshlanish, '%H:%M')\n    b = datetime.strptime(tugash, '%H:%M')\n    if b < a:\n        b += timedelta(days=1)\n    return int((b - a).total_seconds() // 60)",
      'davomiylik("09:00", "10:35")', 'davomiylik("23:30", "00:15")', 'davomiylik("12:00", "12:00")', lv=2),
    F("Ish kunlari", "`ish_kunlari(boshi, oxiri)` — ikki `date` orasidagi (ikkalasi ham kiradi) dushanba–juma kunlari soni.",
      "from datetime import timedelta\n\n\ndef ish_kunlari(boshi, oxiri):\n    n = 0\n    d = boshi\n    while d <= oxiri:\n        if d.weekday() < 5:\n            n += 1\n        d += timedelta(days=1)\n    return n",
      "ish_kunlari(__import__('datetime').date(2026, 10, 12), __import__('datetime').date(2026, 10, 18))",
      "ish_kunlari(__import__('datetime').date(2026, 10, 1), __import__('datetime').date(2026, 10, 31))",
      "ish_kunlari(__import__('datetime').date(2026, 10, 17), __import__('datetime').date(2026, 10, 17))", lv=2),
    F("Qancha oldin", "`qachon(oldin, hozir)` — `datetime` farqiga qarab: 60 s dan kam → `\"hozirgina\"`, 1 soatdan kam → `\"N daqiqa oldin\"`, 1 kundan kam → `\"N soat oldin\"`, aks holda `\"N kun oldin\"`.",
      "def qachon(oldin, hozir):\n    s = int((hozir - oldin).total_seconds())\n    if s < 60:\n        return 'hozirgina'\n    if s < 3600:\n        return f'{s // 60} daqiqa oldin'\n    if s < 86400:\n        return f'{s // 3600} soat oldin'\n    return f'{s // 86400} kun oldin'",
      "qachon(__import__('datetime').datetime(2026, 10, 13, 9, 0, 0), __import__('datetime').datetime(2026, 10, 13, 9, 0, 30))",
      "qachon(__import__('datetime').datetime(2026, 10, 13, 9, 0), __import__('datetime').datetime(2026, 10, 13, 9, 45))",
      "qachon(__import__('datetime').datetime(2026, 10, 13, 1, 0), __import__('datetime').datetime(2026, 10, 13, 9, 30))",
      "qachon(__import__('datetime').datetime(2026, 10, 1), __import__('datetime').datetime(2026, 10, 13))", lv=3),
    F("Dars jadvali", "`jadval(boshlanish, davomiylik, soni, tanaffus)` — `\"HH:MM\"` dan boshlab, har biri `davomiylik` daqiqa boʻlgan `soni` ta dars va orasida `tanaffus` daqiqa. `[\"09:00–09:45\", …]` roʻyxatini qaytarsin.",
      "from datetime import datetime, timedelta\n\n\ndef jadval(boshlanish, davomiylik, soni, tanaffus):\n    t = datetime.strptime(boshlanish, '%H:%M')\n    natija = []\n    for _ in range(soni):\n        oxir = t + timedelta(minutes=davomiylik)\n        natija.append(f\"{t:%H:%M}–{oxir:%H:%M}\")\n        t = oxir + timedelta(minutes=tanaffus)\n    return natija",
      'jadval("09:00", 45, 3, 10)', 'jadval("13:30", 80, 2, 20)', 'jadval("08:00", 45, 0, 5)', lv=2),
    L("docs", "py-datetime"),
    L("exercism", "gigasecond"),
    L("lc", "number-of-days-between-two-dates"),
    L("exercism", "meetup", note="Oyning \"uchinchi seshanbasi\" kabi sanalarni topish."),
])
