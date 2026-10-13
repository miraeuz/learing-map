from dsl import SECTION, TOPIC, P, Q, F, PR, L

SECTION(13, "Django bilan veb-ilovalar", "Loyiha, view, model, admin, ORM, shablonlar, URL, API va deploy", "🌐")

KITOBLAR = '''KITOBLAR = [
    {"id": 1, "nom": "Oʻtkan kunlar", "muallif": "Abdulla Qodiriy", "yil": 1926, "narx": 45000, "janr": "roman"},
    {"id": 2, "nom": "Mehrobdan chayon", "muallif": "Abdulla Qodiriy", "yil": 1929, "narx": 40000, "janr": "roman"},
    {"id": 3, "nom": "Sariq devni minib", "muallif": "Xudoyberdi Toʻxtaboyev", "yil": 1968, "narx": 30000, "janr": "sarguzasht"},
    {"id": 4, "nom": "Ikki eshik orasi", "muallif": "Oʻtkir Hoshimov", "yil": 1986, "narx": 55000, "janr": "roman"},
    {"id": 5, "nom": "Dunyoning ishlari", "muallif": "Oʻtkir Hoshimov", "yil": 1982, "narx": 35000, "janr": "qissa"},
]
'''
BAZA = {"baza.py": KITOBLAR}

# ---------------------------------------------------------------- 13.1
TOPIC("django-kirish", "Django bilan tanishuv: birinchi loyiha", "Freymvork nima, MVT, loyiha va ilova yaratish", 25, r'''
**Django** — Python'dagi eng mashhur veb-freymvork. U "batareyalari bilan" keladi: maʼlumotlar bazasi bilan ishlash (ORM), tayyor admin panel, foydalanuvchilar va parollar, formalar, xavfsizlik — hammasi ichida. Instagram, Mozilla, Disqus kabi yirik loyihalar Django'da yozilgan.

## Django qanday ishlaydi: MVT
Foydalanuvchi brauzerda manzil yozadi → Django **URL** boʻyicha kerakli **View** ni topadi → View **Model** dan maʼlumot oladi → **Template** (shablon) bilan HTML yasaydi → javob brauzerga qaytadi.

| Qism | Fayl | Vazifasi |
|---|---|---|
| **M**odel | `models.py` | maʼlumotlar tuzilishi va baza |
| **V**iew | `views.py` | mantiq: soʻrovni qabul qilib, javob qaytaradi |
| **T**emplate | `templates/*.html` | foydalanuvchi koʻradigan HTML |
| URL | `urls.py` | qaysi manzil qaysi view'ga borishi |

Bu yoʻlni oddiy Python bilan "simulyatsiya" qilib koʻraylik:

```py
def bosh_sahifa(request):
    return "<h1>Mirae Academy</h1>"


def haqida(request):
    return "<p>Biz haqimizda</p>"


urlpatterns = {"": bosh_sahifa, "haqida/": haqida}

for yol in ["", "haqida/", "yoq/"]:
    view = urlpatterns.get(yol)
    print(repr(yol), "→", view(None) if view else "404 Not Found")
```

## Oʻrnatish va loyiha yaratish
Har doim **virtual muhit** ichida ishlang (11-boʻlimni eslang):

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install django
django-admin startproject mysite .
python manage.py runserver       # http://127.0.0.1:8000
```

`startproject` quyidagi tuzilmani yaratadi:

```text
manage.py            ← loyiha bilan ishlash buyruqlari
mysite/
    __init__.py
    settings.py      ← sozlamalar (ilovalar, baza, til, vaqt zonasi)
    urls.py          ← bosh URL roʻyxati
    asgi.py, wsgi.py ← server bilan ulanish nuqtalari
```

## Loyiha va ilova (app)
**Loyiha** — butun sayt. **Ilova** — uning bir qismi (blog, doʻkon, foydalanuvchilar). Bitta loyihada koʻp ilova boʻladi:

```bash
python manage.py startapp blog
```

Yangi ilovani `settings.py` dagi `INSTALLED_APPS` ga qoʻshish **shart**:

```py norun
# mysite/settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",                      # ← bizning ilova
]
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
```

## Birinchi sahifa
```py norun
# blog/views.py
from django.http import HttpResponse


def bosh_sahifa(request):
    return HttpResponse("<h1>Salom, Django!</h1>")
```

```py norun
# mysite/urls.py
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.bosh_sahifa, name="bosh"),
]
```

`python manage.py runserver` — va brauzerda `http://127.0.0.1:8000` ni oching. 🎉

## Eng koʻp ishlatiladigan buyruqlar
| Buyruq | Nima qiladi |
|---|---|
| `runserver` | ishlab chiqish serverini yoqadi |
| `startapp nom` | yangi ilova yaratadi |
| `makemigrations` | model oʻzgarishlaridan migratsiya fayli yasaydi |
| `migrate` | migratsiyalarni bazaga qoʻllaydi |
| `createsuperuser` | admin panel uchun foydalanuvchi yaratadi |
| `shell` | loyiha ichida Python konsoli |

> `runserver` faqat ishlab chiqish uchun. Haqiqiy saytda gunicorn/uvicorn kabi serverlar ishlatiladi (13.9-mavzu).

!> Ilova nomi Python identifikatori boʻlishi kerak: `blog`, `online_dars` — toʻgʻri; `my-blog`, `2blog` — notoʻgʻri. `django`, `test` kabi nomlar mavjud modullar bilan toʻqnashadi.
''', [
    P('print("django" in ["django.contrib.admin", "blog"])', "True", "Xato", "django"),
    P('ilovalar = ["django.contrib.admin", "django.contrib.auth"]\nilovalar.append("blog")\nprint(len(ilovalar), ilovalar[-1])', "2 blog", "3 django.contrib.auth", "Xato"),
    P('print("blog.apps.BlogConfig".split(".")[0])', "BlogConfig", "apps", "blog.apps"),
    P('manzil = "127.0.0.1:8000"\nhost, port = manzil.split(":")\nprint(int(port) + 1)', "8000:1", "80001", "Xato"),
    P('from pathlib import PurePosixPath\nBASE_DIR = PurePosixPath("/loyiha/mysite/settings.py").parent.parent\nprint(BASE_DIR / "db.sqlite3")', "/loyiha/mysite/db.sqlite3", "db.sqlite3", "Xato"),
    P('print("blog".isidentifier(), "my-blog".isidentifier())', "True True", "False False", "Xato"),
    P('DEBUG = True\nALLOWED_HOSTS = []\nprint(DEBUG and not ALLOWED_HOSTS)', "False", "[]", "Xato", lv=2,
      why="`not []` — `True`, demak `True and True` → `True`. DEBUG rejimida boʻsh `ALLOWED_HOSTS` bilan Django `localhost` ga ruxsat beradi, production'da esa bu xato."),
    Q("Django qaysi arxitektura naqshidan foydalanadi?", "MVT (Model – View – Template)", "Faqat Model va View", "Hech qaysi — hammasi bitta faylda", "Faqat Template"),
    Q("`python manage.py startapp blog` nima qiladi?", "Loyiha ichida `blog` nomli yangi ilova papkasini yaratadi", "Serverni ishga tushiradi", "Django'ni oʻrnatadi", "Bazani tozalaydi"),
    F("manage.py buyruqlari", "`buyruq(nom)` — `runserver` → `\"serverni ishga tushiradi\"`, `startapp` → `\"yangi ilova yaratadi\"`, `makemigrations` → `\"migratsiya fayllarini yaratadi\"`, `migrate` → `\"migratsiyalarni bazaga qoʻllaydi\"`, `createsuperuser` → `\"admin foydalanuvchi yaratadi\"`; boshqasi → `\"nomaʼlum buyruq\"`.",
      "def buyruq(nom):\n    return {\n        'runserver': 'serverni ishga tushiradi',\n        'startapp': 'yangi ilova yaratadi',\n        'makemigrations': 'migratsiya fayllarini yaratadi',\n        'migrate': 'migratsiyalarni bazaga qoʻllaydi',\n        'createsuperuser': 'admin foydalanuvchi yaratadi',\n    }.get(nom, 'nomaʼlum buyruq')",
      'buyruq("migrate")', 'buyruq("runserver")', 'buyruq("startapp")', 'buyruq("deploy")', lv=1),
    F("Ilova nomi", "`nom_togrimi(nom)` — ilova nomi toʻgʻri boʻlsa `True`: Python identifikatori, faqat kichik harflar, kalit soʻz emas (`keyword.iskeyword`) va `django`, `test`, `site` emas.",
      "import keyword\n\n\ndef nom_togrimi(nom):\n    return nom.isidentifier() and nom == nom.lower() and not keyword.iskeyword(nom) and nom not in ('django', 'test', 'site')",
      'nom_togrimi("blog")', 'nom_togrimi("online_dars")', 'nom_togrimi("my-blog")', 'nom_togrimi("Blog")', 'nom_togrimi("class")', 'nom_togrimi("test")', lv=1),
    F("INSTALLED_APPS", "`ilova_qosh(ilovalar, nom)` — `nom` roʻyxatda boʻlmasa oxiriga qoʻshilgan **yangi** roʻyxat qaytarsin (asl roʻyxat oʻzgarmasin).",
      "def ilova_qosh(ilovalar, nom):\n    return ilovalar if nom in ilovalar else ilovalar + [nom]",
      'ilova_qosh(["django.contrib.admin"], "blog")', 'ilova_qosh(["blog"], "blog")', '(a := ["x"], ilova_qosh(a, "y"), a)[2]', lv=1),
    F("runserver manzili", "`manzil(arg=\"\")` — `runserver` argumentini ajratsin: `\"\"` → `(\"127.0.0.1\", 8000)`, `\"8080\"` → `(\"127.0.0.1\", 8080)`, `\"0.0.0.0:9000\"` → `(\"0.0.0.0\", 9000)`.",
      "def manzil(arg=''):\n    host, port = '127.0.0.1', 8000\n    if ':' in arg:\n        host, p = arg.rsplit(':', 1)\n        port = int(p)\n    elif arg:\n        port = int(arg)\n    return host, port",
      "manzil()", 'manzil("8080")', 'manzil("0.0.0.0:9000")', 'manzil("localhost:80")'),
    F("Loyiha daraxti", "`daraxt(loyiha, ilova)` — `startproject` va `startapp` yaratadigan fayllar yoʻllari (alifbo boʻyicha saralangan): `manage.py`; loyiha papkasida `__init__.py`, `asgi.py`, `settings.py`, `urls.py`, `wsgi.py`; ilova papkasida `__init__.py`, `admin.py`, `apps.py`, `migrations/__init__.py`, `models.py`, `tests.py`, `views.py`.",
      "def daraxt(loyiha, ilova):\n    yollar = ['manage.py']\n    yollar += [f'{loyiha}/{f}' for f in ['__init__.py', 'asgi.py', 'settings.py', 'urls.py', 'wsgi.py']]\n    yollar += [f'{ilova}/{f}' for f in ['__init__.py', 'admin.py', 'apps.py', 'migrations/__init__.py', 'models.py', 'tests.py', 'views.py']]\n    return sorted(yollar)",
      'daraxt("mysite", "blog")', 'len(daraxt("a", "b"))', 'daraxt("mysite", "blog")[0]'),
    F("AppConfig nomi", "`config_nomi(ilova)` — `INSTALLED_APPS` uchun toʻliq yoʻl: `\"blog\"` → `\"blog.apps.BlogConfig\"`, `\"online_dars\"` → `\"online_dars.apps.OnlineDarsConfig\"`.",
      "def config_nomi(ilova):\n    sinf = ''.join(q.capitalize() for q in ilova.split('_'))\n    return f'{ilova}.apps.{sinf}Config'",
      'config_nomi("blog")', 'config_nomi("online_dars")', 'config_nomi("api")', lv=1),
    F("MVT qismi", "`qism(fayl)` — fayl nomiga qarab: `models.py` → `\"Model\"`, `views.py` → `\"View\"`, `.html` bilan tugasa → `\"Template\"`, `urls.py` → `\"URL\"`, boshqasi → `\"boshqa\"` (yoʻl berilishi mumkin: `blog/views.py`).",
      "def qism(fayl):\n    nom = fayl.rsplit('/', 1)[-1]\n    if nom.endswith('.html'):\n        return 'Template'\n    return {'models.py': 'Model', 'views.py': 'View', 'urls.py': 'URL'}.get(nom, 'boshqa')",
      'qism("blog/views.py")', 'qism("templates/blog/post_list.html")', 'qism("models.py")', 'qism("mysite/urls.py")', 'qism("settings.py")', lv=1),
    L("docs", "dj-install"),
    L("docs", "dj-tut1"),
    L("docs", "djgirls-intro"),
    L("docs", "dj-settings"),
])

# ---------------------------------------------------------------- 13.2
TOPIC("dj-views", "View'lar: soʻrov va javob", "HttpRequest, HttpResponse, GET/POST parametrlar va status kodlari", 25, r'''
**View** — soʻrov (`request`) ni qabul qilib, **javob** (`HttpResponse`) qaytaradigan oddiy Python funksiya. Django'dagi barcha mantiq shu yerda yashaydi.

```py norun
# blog/views.py
from django.http import HttpResponse, HttpResponseNotAllowed


def salom(request):
    ism = request.GET.get("ism", "mehmon")      # /salom/?ism=Madina
    return HttpResponse(f"<h1>Salom, {ism}!</h1>")


def izoh_qoldir(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])   # 405
    matn = request.POST.get("matn", "")
    return HttpResponse("Rahmat!", status=201)
```

## request ichida nimalar bor?
| Atribut | Maʼnosi |
|---|---|
| `request.method` | `"GET"`, `"POST"`, ... |
| `request.GET` | URL dagi `?kalit=qiymat` parametrlar |
| `request.POST` | formadan yuborilgan maʼlumotlar |
| `request.path` | `/blog/salom/` |
| `request.user` | kirgan foydalanuvchi (yoki anonim) |
| `request.headers` | sarlavhalar (`User-Agent` va h.k.) |

Django buni qanday qiladi — kichik nusxasini oʻzimiz yozib koʻraylik:

```py
class HttpResponse:
    def __init__(self, content="", status=200, content_type="text/html; charset=utf-8"):
        self.content, self.status_code, self.content_type = content, status, content_type

    def __repr__(self):
        return f"<HttpResponse status_code={self.status_code}, {self.content_type!r}>"


class HttpRequest:
    def __init__(self, method="GET", GET=None, POST=None):
        self.method, self.GET, self.POST = method, GET or {}, POST or {}


def salom(request):
    ism = request.GET.get("ism", "mehmon")
    return HttpResponse(f"<h1>Salom, {ism}!</h1>")


r = salom(HttpRequest(GET={"ism": "Madina"}))
print(r)
print(r.content)
print(salom(HttpRequest()).content)
```

## render — shablon bilan javob
Odatda HTML ni qoʻlda yozmaymiz — `render` shablonni kontekst bilan toʻldiradi (13.6-mavzu):

```py norun
from django.shortcuts import render, redirect


def postlar(request):
    sahifa = int(request.GET.get("sahifa", 1))
    kontekst = {"postlar": Post.objects.all()[(sahifa - 1) * 10: sahifa * 10]}
    return render(request, "blog/postlar.html", kontekst)


def eski_manzil(request):
    return redirect("/blog/")          # 302 → /blog/
```

## Status kodlari — javobning "kayfiyati"
```py
from http import HTTPStatus

for kod in [200, 201, 302, 400, 403, 404, 405, 500]:
    print(kod, HTTPStatus(kod).phrase)
```

> **Bitta qoida:** view har doim `HttpResponse` (yoki undan meros olgan obyekt) qaytaradi. `None` qaytarsa, Django `ValueError: The view ... didn't return an HttpResponse object` xatosini beradi.

## Class-based view (bir qarashda)
```py norun
from django.views import View


class SalomView(View):
    def get(self, request):
        return HttpResponse("GET soʻrov")

    def post(self, request):
        return HttpResponse("POST soʻrov", status=201)

# urls.py:  path("salom/", SalomView.as_view())
```

!> `request.GET` dagi hamma qiymatlar — **satr**. `?sahifa=2` → `"2"`. Son kerak boʻlsa `int()` qiling va notoʻgʻri qiymatga tayyor turing.
''', [
    P('GET = {"sahifa": "2"}\nprint(GET.get("sahifa", 1) + "0")', "3", "12", "Xato"),
    P('GET = {}\nprint(int(GET.get("sahifa", 1)) * 10)', "1", "Xato", "None"),
    P('method = "POST"\nprint("saqlandi" if method == "POST" else "forma")', "forma", "POST", "Xato"),
    P('def view(request):\n    pass\nprint(type(view(1)).__name__)', "None", "function", "Xato",
      why="`pass` bilan tugagan funksiya `None` qaytaradi. Django'da bunday view xato beradi — doim `HttpResponse` qaytaring."),
    P('from http import HTTPStatus\nprint(HTTPStatus.METHOD_NOT_ALLOWED.value)', "404", "400", "403"),
    P('javob = {"status": 200}\njavob.update(status=302, Location="/kirish/")\nprint(javob["status"], javob["Location"])', "200 /kirish/", "302", "Xato"),
    P('sarlavha = "text/html; charset=utf-8"\nprint(sarlavha.split(";")[0])', "charset=utf-8", "text/html; charset=utf-8", "Xato", lv=2),
    Q("Django view funksiyasi birinchi argument sifatida nimani oladi?", "`request` — HttpRequest obyekti", "URL satrini", "Modelni", "Shablon nomini"),
    Q("View nima qaytarishi shart?", "`HttpResponse` (yoki undan meros olgan) obyekt", "Oddiy satr", "Lugʻat", "Hech narsa"),
    F("Salomlashish view", "`salom_view(GET)` — `GET` lugʻatidan `ism` ni olsin (boʻsh joylari tozalanib, `.title()`), yoʻq yoki boʻsh boʻlsa `\"Mehmon\"`; `\"<h1>Salom, ISM!</h1>\"` qaytarsin.",
      "def salom_view(GET):\n    ism = GET.get('ism', '').strip().title() or 'Mehmon'\n    return f'<h1>Salom, {ism}!</h1>'",
      'salom_view({"ism": "madina"})', "salom_view({})", 'salom_view({"ism": "   "})', 'salom_view({"ism": " ali valiyev "})', lv=1),
    F("Metod tekshiruvi", "`metod_tekshir(method, ruxsat)` — `method` ruxsat roʻyxatida boʻlsa `(200, \"OK\")`, aks holda `(405, \"Method Not Allowed\")` (matnni `HTTPStatus` dan oling).",
      "from http import HTTPStatus\n\n\ndef metod_tekshir(method, ruxsat):\n    kod = 200 if method in ruxsat else 405\n    return kod, HTTPStatus(kod).phrase",
      'metod_tekshir("GET", ["GET", "POST"])', 'metod_tekshir("DELETE", ["GET"])', 'metod_tekshir("POST", [])', lv=1),
    F("Sahifa raqami", "`sahifa_raqami(GET, jami)` — `GET[\"sahifa\"]` ni butun songa aylantirsin; yoʻq yoki son emas boʻlsa 1; natija `1..jami` oraligʻiga siqilsin.",
      "def sahifa_raqami(GET, jami):\n    try:\n        s = int(GET.get('sahifa', 1))\n    except ValueError:\n        s = 1\n    return max(1, min(s, jami))",
      'sahifa_raqami({"sahifa": "3"}, 10)', 'sahifa_raqami({"sahifa": "abc"}, 10)', 'sahifa_raqami({}, 5)', 'sahifa_raqami({"sahifa": "99"}, 5)', 'sahifa_raqami({"sahifa": "-2"}, 5)'),
    F("Javob sarlavhalari", "`javob(content, status=200)` — `{\"status\": ..., \"Content-Length\": baytlardagi uzunlik (UTF-8), \"body\": content}` lugʻatini qaytarsin.",
      "def javob(content, status=200):\n    return {'status': status, 'Content-Length': len(content.encode('utf-8')), 'body': content}",
      'javob("Salom")', 'javob("Oʻzbekiston", 201)', 'javob("", 204)', lv=1),
    F("Yoʻnaltirish", "`yonaltir(url, doimiy=False)` — `(302, {\"Location\": url})`; `doimiy=True` boʻlsa 301. URL `/` bilan boshlanmasa va `http` bilan ham boshlanmasa — `ValueError`.",
      "def yonaltir(url, doimiy=False):\n    if not url.startswith(('/', 'http')):\n        raise ValueError(url)\n    return (301 if doimiy else 302), {'Location': url}",
      'yonaltir("/kirish/")', 'yonaltir("https://mirae.uz", doimiy=True)', 'yonaltir("kirish")'),
    F("Mini HttpResponse", "`Javob(content=\"\", status=200)` sinfi: `.content`, `.status_code` atributlari, `.ok` xususiyati (`@property`, status 400 dan kichik boʻlsa `True`) va `str()` → `\"<Javob 200>\"`.",
      "class Javob:\n    def __init__(self, content='', status=200):\n        self.content = content\n        self.status_code = status\n\n    @property\n    def ok(self):\n        return self.status_code < 400\n\n    def __str__(self):\n        return f'<Javob {self.status_code}>'",
      'str(Javob("x"))', 'Javob("", 404).ok', '(j := Javob("Salom"), j.content, j.status_code, j.ok)[1:]', 'str(Javob(status=302))', lv=2),
    F("Qidiruv view", "`qidiruv(GET, mahsulotlar)` — `GET[\"q\"]` (katta-kichik farqsiz) nomida uchragan mahsulotlar roʻyxati; `q` yoʻq yoki boʻsh boʻlsa — hammasi.",
      "def qidiruv(GET, mahsulotlar):\n    q = GET.get('q', '').strip().lower()\n    return [m for m in mahsulotlar if q in m.lower()]",
      'qidiruv({"q": "non"}, ["Non", "Patir non", "Somsa"])', 'qidiruv({}, ["A", "B"])', 'qidiruv({"q": "x"}, ["A"])', lv=1),
    L("docs", "dj-views"),
    L("docs", "dj-tut3"),
    L("docs", "dj-request-response"),
    L("lc", "design-browser-history", note="Brauzer tarixini dizayn qiling — soʻrovlar ketma-ketligini modellashtirish mashqi."),
])

# ---------------------------------------------------------------- 13.3
TOPIC("dj-modellar", "Modellar va migratsiyalar", "Maydonlar, makemigrations, migrate va modelni oʻzgartirish", 30, r'''
**Model** — bazadagi jadvalning Python'dagi tavsifi. Siz sinf yozasiz — Django jadvalni oʻzi yaratadi. SQL yozish shart emas!

```py norun
# blog/models.py
from django.db import models


class Post(models.Model):
    HOLAT = [("q", "Qoralama"), ("n", "Nashr etilgan")]

    sarlavha = models.CharField(max_length=200)
    matn = models.TextField()
    korishlar = models.IntegerField(default=0)
    holat = models.CharField(max_length=1, choices=HOLAT, default="q")
    yaratilgan = models.DateTimeField(auto_now_add=True)
    muallif = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.sarlavha
```

## Eng koʻp ishlatiladigan maydonlar
| Maydon | Bazada | Izoh |
|---|---|---|
| `CharField(max_length=N)` | `varchar(N)` | qisqa matn, `max_length` majburiy |
| `TextField()` | `text` | uzun matn |
| `IntegerField()` | `integer` | butun son |
| `DecimalField(max_digits, decimal_places)` | `decimal` | pul uchun |
| `BooleanField()` | `bool` | ha/yoʻq |
| `DateTimeField(auto_now_add=True)` | `datetime` | yaratilgan vaqt |
| `ForeignKey(Model, on_delete=...)` | `integer` + bogʻlanish | "koʻpdan-birga" |

## Migratsiya — bazaning "git"i
```bash
python manage.py makemigrations    # blog/migrations/0001_initial.py yaratiladi
python manage.py sqlmigrate blog 0001   # qanday SQL bajarilishini koʻrish
python manage.py migrate           # bazaga qoʻllash
```

Django ichida nima boʻladi? Model → SQL → baza. Buni `sqlite3` bilan oʻzimiz bajarib koʻramiz:

```py
import sqlite3

TURLAR = {"CharField": "varchar", "IntegerField": "integer", "BooleanField": "bool"}


def create_table(ilova, model, maydonlar):
    jadval = f"{ilova}_{model.lower()}"
    ustunlar = ['"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT']
    for nom, (tur, uzun) in maydonlar.items():
        sql = TURLAR[tur] + (f"({uzun})" if uzun else "")
        ustunlar.append(f'"{nom}" {sql} NOT NULL')
    return f'CREATE TABLE "{jadval}" ({", ".join(ustunlar)});'


sql = create_table("blog", "Post", {"sarlavha": ("CharField", 200), "korishlar": ("IntegerField", None)})
print(sql)

db = sqlite3.connect(":memory:")
db.execute(sql)
db.execute("INSERT INTO blog_post (sarlavha, korishlar) VALUES (?, ?)", ("Salom Django", 5))
print(db.execute("SELECT * FROM blog_post").fetchall())
```

> Jadval nomi: `ilova_model` (kichik harflarda). `id` ustuni avtomatik qoʻshiladi.

## Modelni oʻzgartirish
Yangi maydon qoʻshdingiz → yana `makemigrations` va `migrate`. Jadvalda eski yozuvlar boʻlsa, Django ular uchun **standart qiymat** soʻraydi — shuning uchun `default=` yoki `null=True` bering:

```py norun
class Post(models.Model):
    ...
    rasm = models.ImageField(upload_to="postlar/", null=True, blank=True)   # yangi
    teglar = models.CharField(max_length=100, default="")                  # yangi
```

Bazada bu `ALTER TABLE` boʻladi:

```py
import sqlite3

db = sqlite3.connect(":memory:")
db.execute('CREATE TABLE blog_post ("id" integer PRIMARY KEY AUTOINCREMENT, "sarlavha" varchar(200) NOT NULL)')
db.execute("INSERT INTO blog_post (sarlavha) VALUES ('Eski post')")

db.execute('ALTER TABLE blog_post ADD COLUMN "korishlar" integer NOT NULL DEFAULT 0')
db.execute("INSERT INTO blog_post (sarlavha, korishlar) VALUES ('Yangi post', 7)")
for qator in db.execute("SELECT * FROM blog_post"):
    print(qator)
```

Migratsiya fayllari raqamlanadi: `0001_initial.py`, `0002_post_korishlar.py`, ... Ular **Git'ga qoʻshiladi** — jamoadagi hamma bir xil bazaga ega boʻladi.

| `null=True` | `blank=True` |
|---|---|
| bazada `NULL` ruxsat | formada boʻsh qoldirish ruxsat |

!> Migratsiya fayllarini qoʻlda oʻchirmang va bir-biriga aralashtirmang — bu bazani chalkashtiradi. Xato boʻlsa, yangi migratsiya bilan tuzating.
''', [
    P('print("Post".lower(), "blog" + "_" + "Post".lower())', "Post blog_Post", "post blogpost", "Xato"),
    P('import sqlite3\ndb = sqlite3.connect(":memory:")\ndb.execute("CREATE TABLE t (id integer PRIMARY KEY AUTOINCREMENT, n text)")\ndb.execute("INSERT INTO t (n) VALUES (\'a\')")\ndb.execute("INSERT INTO t (n) VALUES (\'b\')")\nprint(db.execute("SELECT id FROM t").fetchall())', "[1, 2]", "[(0,), (1,)]", "['a', 'b']"),
    P('nomlar = ["0001_initial.py", "0003_post_rasm.py", "0002_post_nashr.py"]\nprint(sorted(nomlar)[-1])', "0002_post_nashr.py", "0001_initial.py", "Xato"),
    P('print(f"{2 + 1:04d}_post_muallif")', "3_post_muallif", "0002_post_muallif", "Xato"),
    P('import sqlite3\ndb = sqlite3.connect(":memory:")\ndb.execute("CREATE TABLE p (s text NOT NULL)")\ntry:\n    db.execute("INSERT INTO p (s) VALUES (NULL)")\nexcept sqlite3.IntegrityError as e:\n    print(type(e).__name__)', "None", "OperationalError", "Hech narsa chiqmaydi"),
    P('maydon = {"max_length": 200, "blank": True}\nprint(maydon.get("null", False), maydon["blank"])', "True True", "None True", "Xato"),
    P('HOLAT = [("q", "Qoralama"), ("n", "Nashr etilgan")]\nprint(dict(HOLAT)["n"])', "n", "Qoralama", "Xato", lv=2,
      why="`choices` — `(bazadagi qiymat, koʻrinadigan nom)` juftliklari. Django'da `post.get_holat_display()` xuddi shu ishni qiladi."),
    Q("Modelga yangi maydon qoʻshgandan keyin qaysi buyruqlar kerak?", "`makemigrations`, keyin `migrate`", "Faqat `runserver`", "`migrate`, keyin `makemigrations`", "`startapp` qaytadan"),
    Q("Yozuvlari bor jadvalga majburiy (NOT NULL) maydon qoʻshganda Django nimani soʻraydi?", "Eski yozuvlar uchun standart qiymatni (`default`)", "Admin parolini", "Jadvalni oʻchirishga ruxsat", "Hech narsa soʻramaydi"),
    F("Jadval nomi", "`jadval_nomi(ilova, model)` — Django jadval nomi: `ilova_model`, hammasi kichik harflarda.",
      "def jadval_nomi(ilova, model):\n    return f'{ilova}_{model}'.lower()",
      'jadval_nomi("blog", "Post")', 'jadval_nomi("dokon", "MahsulotTuri")', 'jadval_nomi("Kurs", "Dars")', lv=1),
    F("Ustun turi", "`ustun_sql(tur, max_length=None, null=False)` — `CharField` → `varchar(N)` (`max_length` yoʻq boʻlsa `ValueError`), `IntegerField` → `integer`, `BooleanField` → `bool`, `TextField` → `text`; oxiriga `null` boʻyicha ` NULL` yoki ` NOT NULL`. Nomaʼlum tur — `ValueError`.",
      "def ustun_sql(tur, max_length=None, null=False):\n    if tur == 'CharField':\n        if not max_length:\n            raise ValueError('max_length kerak')\n        sql = f'varchar({max_length})'\n    elif tur in ('IntegerField', 'BooleanField', 'TextField'):\n        sql = {'IntegerField': 'integer', 'BooleanField': 'bool', 'TextField': 'text'}[tur]\n    else:\n        raise ValueError(tur)\n    return sql + (' NULL' if null else ' NOT NULL')",
      'ustun_sql("CharField", max_length=200)', 'ustun_sql("IntegerField", null=True)', 'ustun_sql("TextField")', 'ustun_sql("CharField")', 'ustun_sql("JSONField")'),
    F("CREATE TABLE", "`create_table(ilova, model, maydonlar)` — `maydonlar`: `[(nom, tur, max_length_yoki_None)]` (`CharField`/`IntegerField`). Darsdagidek SQL qaytarsin: `CREATE TABLE \"blog_post\" (\"id\" integer NOT NULL PRIMARY KEY AUTOINCREMENT, \"sarlavha\" varchar(200) NOT NULL);`",
      "def create_table(ilova, model, maydonlar):\n    ustunlar = ['\"id\" integer NOT NULL PRIMARY KEY AUTOINCREMENT']\n    for nom, tur, uzun in maydonlar:\n        sql = {'CharField': 'varchar', 'IntegerField': 'integer'}[tur] + (f'({uzun})' if uzun else '')\n        ustunlar.append(f'\"{nom}\" {sql} NOT NULL')\n    return f'CREATE TABLE \"{ilova}_{model.lower()}\" ({\", \".join(ustunlar)});'",
      'create_table("blog", "Post", [("sarlavha", "CharField", 200)])', 'create_table("dokon", "Mahsulot", [("nom", "CharField", 100), ("narx", "IntegerField", None)])',
      '(db := __import__("sqlite3").connect(":memory:"), db.execute(create_table("kurs", "Dars", [("mavzu", "CharField", 50)])), [r[0] for r in db.execute("SELECT name FROM sqlite_master")])[-1]', lv=2),
    F("Migratsiya nomi", "`migratsiya_nomi(mavjud, model, maydon)` — `mavjud` fayllar roʻyxati boʻsh boʻlsa `\"0001_initial.py\"`; aks holda eng katta raqam + 1, 4 xonali: `\"0003_post_rasm.py\"`.",
      "def migratsiya_nomi(mavjud, model, maydon):\n    if not mavjud:\n        return '0001_initial.py'\n    n = max(int(f[:4]) for f in mavjud) + 1\n    return f'{n:04d}_{model.lower()}_{maydon}.py'",
      "migratsiya_nomi([], 'Post', 'x')", 'migratsiya_nomi(["0001_initial.py", "0002_post_nashr.py"], "Post", "rasm")', 'migratsiya_nomi(["0009_a.py", "0001_initial.py"], "Kurs", "narx")', lv=2),
    F("Oʻzgarishlarni aniqlash", "`farq(eski, yangi)` — ikki model holati (`{maydon: tur}`) dan amallar roʻyxati: avval `(\"AddField\", nom)`, keyin `(\"AlterField\", nom)` (tur oʻzgargan), keyin `(\"RemoveField\", nom)`; har bir guruh ichida nom alifbo boʻyicha. Bu `makemigrations` ning yuragi!",
      "def farq(eski, yangi):\n    qosh = [('AddField', n) for n in sorted(yangi) if n not in eski]\n    ozgar = [('AlterField', n) for n in sorted(yangi) if n in eski and eski[n] != yangi[n]]\n    ochir = [('RemoveField', n) for n in sorted(eski) if n not in yangi]\n    return qosh + ozgar + ochir",
      'farq({"sarlavha": "CharField", "matn": "TextField"}, {"sarlavha": "CharField", "matn": "CharField", "rasm": "ImageField"})', "farq({}, {})", 'farq({"a": "X", "b": "Y"}, {})', lv=3),
    F("ALTER TABLE", "`alter(jadval, nom, tur, default=None)` — `default` berilsa `ALTER TABLE \"jadval\" ADD COLUMN \"nom\" tur NOT NULL DEFAULT qiymat` (satr qiymat bitta tirnoqda: `'abc'`, son — oʻzi), berilmasa oxiri ` NULL`.",
      "def alter(jadval, nom, tur, default=None):\n    sql = f'ALTER TABLE \"{jadval}\" ADD COLUMN \"{nom}\" {tur}'\n    if default is None:\n        return sql + ' NULL'\n    q = f\"'{default}'\" if isinstance(default, str) else str(default)\n    return sql + ' NOT NULL DEFAULT ' + q",
      'alter("blog_post", "korishlar", "integer", 0)', 'alter("blog_post", "teg", "varchar(50)", "yangi")', 'alter("blog_post", "rasm", "varchar(100)")',
      '(db := __import__("sqlite3").connect(":memory:"), db.execute("CREATE TABLE t (a int)"), db.execute("INSERT INTO t VALUES (1)"), db.execute(alter("t", "b", "integer", 5)), db.execute("SELECT * FROM t").fetchall())[-1]', lv=2),
    F("Mini model", "`Post(sarlavha)` sinfi: `id` boshida `None`; `save(baza)` — `id` `None` boʻlsa `id = len(baza) + 1` qilib `baza` roʻyxatiga qoʻshsin (qayta `save` — qayta qoʻshmasin); `str()` → sarlavha.",
      "class Post:\n    def __init__(self, sarlavha):\n        self.sarlavha = sarlavha\n        self.id = None\n\n    def save(self, baza):\n        if self.id is None:\n            self.id = len(baza) + 1\n            baza.append(self)\n\n    def __str__(self):\n        return self.sarlavha",
      '(b := [], p := Post("Salom"), p.save(b), p.id, len(b))[3:]', '(b := [], [Post(s).save(b) for s in "abc"], [p.id for p in b])[-1]', 'str(Post("Django"))', '(b := [], p := Post("x"), p.save(b), p.save(b), len(b), p.id)[-2:]'),
    L("docs", "dj-models"),
    L("docs", "dj-migrations"),
    L("docs", "dj-tut2"),
    L("docs", "djgirls-models"),
])

# ---------------------------------------------------------------- 13.4
TOPIC("dj-admin", "Admin panel va uni sozlash", "createsuperuser, register, list_display, qidiruv va filtrlar", 20, r'''
Django'ning eng sevimli "sehrlaridan" biri — **tayyor admin panel**. Bir necha qator kod bilan maʼlumotlarni qoʻshish, tahrirlash, qidirish va oʻchirish mumkin.

```bash
python manage.py createsuperuser     # login, email va parol soʻraydi
python manage.py runserver           # → http://127.0.0.1:8000/admin/
```

## Modelni roʻyxatdan oʻtkazish
```py norun
# blog/admin.py
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("sarlavha", "muallif", "korishlar", "holat")   # ustunlar
    search_fields = ("sarlavha", "matn")                            # qidiruv maydoni
    list_filter = ("holat", "yaratilgan")                           # oʻng tomondagi filtrlar
    ordering = ("-korishlar",)                                      # saralash
    list_per_page = 20                                              # sahifadagi qatorlar
    readonly_fields = ("yaratilgan",)
```

> Modelda `__str__` boʻlmasa, admin'da hamma yozuv `Post object (1)` boʻlib koʻrinadi. `__str__` ni doim yozing!

## Admin ichida nima boʻladi?
Changelist sahifasi aslida: **qidiruv → filtr → saralash → ustunlarni tanlash**. Shu jarayonni oddiy Python bilan:

```py
POSTLAR = [
    {"id": 1, "sarlavha": "Django asoslari", "muallif": "Ali", "nashr": True, "korishlar": 120},
    {"id": 2, "sarlavha": "Python tiplari", "muallif": "Madina", "nashr": False, "korishlar": 45},
    {"id": 3, "sarlavha": "Django admin", "muallif": "Madina", "nashr": True, "korishlar": 300},
]


class PostAdmin:
    list_display = ("sarlavha", "muallif", "korishlar")
    search_fields = ("sarlavha",)
    ordering = ("-korishlar",)


def changelist(admin, qatorlar, q="", **filtr):
    r = [x for x in qatorlar if not q or any(q.lower() in str(x[f]).lower() for f in admin.search_fields)]
    r = [x for x in r if all(x[k] == v for k, v in filtr.items())]
    for f in reversed(admin.ordering):
        r.sort(key=lambda x: x[f.lstrip("-")], reverse=f.startswith("-"))
    return [tuple(x[f] for f in admin.list_display) for x in r]


for qator in changelist(PostAdmin, POSTLAR, q="django"):
    print(qator)
print(changelist(PostAdmin, POSTLAR, nashr=False))
```

## Foydali sozlamalar
| Sozlama | Nima qiladi |
|---|---|
| `list_display` | roʻyxatdagi ustunlar |
| `list_display_links` | qaysi ustun bosilsa tahrirga oʻtadi |
| `list_editable` | roʻyxatning oʻzida tahrirlash |
| `search_fields` | qidiruv (`__icontains` bilan) |
| `list_filter` | yon paneldagi filtrlar |
| `ordering` | standart saralash (`-` — kamayish) |
| `prepopulated_fields` | `{"slug": ("sarlavha",)}` — avtomatik slug |

## Admin manzillari
| Sahifa | URL |
|---|---|
| roʻyxat | `/admin/blog/post/` |
| qoʻshish | `/admin/blog/post/add/` |
| tahrirlash | `/admin/blog/post/5/change/` |
| oʻchirish | `/admin/blog/post/5/delete/` |

!> `list_display = ("sarlavha")` — bu **tuple emas**, oddiy satr! Bitta elementli tuple uchun vergul shart: `("sarlavha",)`.
''', [
    P('ordering = "-korishlar"\nprint(ordering.startswith("-"), ordering.lstrip("-"))', "False korishlar", "True -korishlar", "Xato"),
    P('list_display = ("sarlavha",)\nprint(type(list_display).__name__, len(list_display))', "str 8", "str 1", "list 1"),
    P('list_display = ("sarlavha")\nprint(type(list_display).__name__)', "tuple", "list", "Xato",
      why="Qavs tuple yasamaydi — **vergul** yasaydi. `(\"sarlavha\")` — oddiy satr. Admin bunda xato beradi."),
    P('class Post:\n    def __init__(self, s):\n        self.s = s\n\n    def __str__(self):\n        return self.s\n\n\nprint([str(Post("A")), str(Post("B"))])', "[<Post object>, <Post object>]", "['Post', 'Post']", "Xato"),
    P('qatorlar = list(range(1, 26))\nprint(qatorlar[10:20][-1])', "19", "25", "10"),
    P('print("dj" in "Django", "dj" in "Django".lower())', "True True", "False False", "Xato"),
    P('import math\nprint(math.ceil(45 / 20))', "2", "2.25", "Xato", lv=2),
    Q("Admin panelga kirish uchun foydalanuvchi qanday yaratiladi?", "`python manage.py createsuperuser`", "`python manage.py runserver admin`", "`settings.py` ga parol yozib", "`pip install admin`"),
    Q("`list_display` nima qiladi?", "Roʻyxat sahifasida qaysi ustunlar koʻrinishini belgilaydi", "Qidiruv maydonlarini belgilaydi", "Modelni bazadan oʻchiradi", "Admin rangini oʻzgartiradi"),
    F("Ustunlar", "`korsat(qator, list_display)` — `qator` lugʻatidan `list_display` dagi maydonlar qiymatlari tuple'i; yoʻq yoki `None` boʻlgan qiymat oʻrniga `\"-\"` (Django'ning `empty_value_display`).",
      "def korsat(qator, list_display):\n    return tuple('-' if qator.get(f) is None else qator[f] for f in list_display)",
      'korsat({"sarlavha": "Salom", "korishlar": 5}, ("sarlavha", "korishlar"))', 'korsat({"a": None}, ("a", "b"))', 'korsat({}, ())', lv=1),
    F("Qidiruv", "`qidir(qatorlar, q, search_fields)` — `q` (katta-kichik farqsiz) `search_fields` dan birortasida uchragan qatorlarning `id` lari; `q` boʻsh boʻlsa — hammasi.",
      "def qidir(qatorlar, q, search_fields):\n    q = q.strip().lower()\n    return [x['id'] for x in qatorlar if not q or any(q in str(x.get(f, '')).lower() for f in search_fields)]",
      'qidir([{"id": 1, "s": "Django"}, {"id": 2, "s": "Flask", "m": "django fan"}], "DJANGO", ("s", "m"))', 'qidir([{"id": 1, "s": "a"}], "", ("s",))', 'qidir([{"id": 1, "s": "a"}], "z", ("s",))'),
    F("Saralash", "`saralash(qatorlar, ordering)` — `ordering` tuple (masalan `(\"-nashr\", \"sarlavha\")`) boʻyicha saralangan `id` lar. `-` — kamayish. Birinchi maydon asosiy, keyingilari teng holatda.",
      "def saralash(qatorlar, ordering):\n    r = list(qatorlar)\n    for f in reversed(ordering):\n        r.sort(key=lambda x: x[f.lstrip('-')], reverse=f.startswith('-'))\n    return [x['id'] for x in r]",
      'saralash([{"id": 1, "n": True, "s": "b"}, {"id": 2, "n": False, "s": "a"}, {"id": 3, "n": True, "s": "a"}], ("-n", "s"))', 'saralash([{"id": 1, "k": 5}, {"id": 2, "k": 9}], ("-k",))', 'saralash([{"id": 1, "k": 5}, {"id": 2, "k": 9}], ())', lv=2),
    F("Filtr paneli", "`filtr_variantlari(qatorlar, maydon)` — yon panel uchun: birinchi `(\"Hammasi\", jami)`, keyin har bir turli qiymat va soni, qiymatlar `str` koʻrinishida alifbo boʻyicha.",
      "def filtr_variantlari(qatorlar, maydon):\n    sanoq = {}\n    for x in qatorlar:\n        sanoq[x[maydon]] = sanoq.get(x[maydon], 0) + 1\n    return [('Hammasi', len(qatorlar))] + sorted(sanoq.items(), key=lambda kv: str(kv[0]))",
      'filtr_variantlari([{"h": "n"}, {"h": "q"}, {"h": "n"}], "h")', 'filtr_variantlari([{"b": True}, {"b": False}], "b")', 'filtr_variantlari([], "x")', lv=2),
    F("Sahifalash", "`sahifa(qatorlar, list_per_page, p)` — `p`-sahifadagi (1 dan) qatorlar; `(qatorlar, jami_sahifalar)` qaytarsin. Boʻsh roʻyxatda ham jami sahifa 1.",
      "import math\n\n\ndef sahifa(qatorlar, list_per_page, p):\n    jami = max(1, math.ceil(len(qatorlar) / list_per_page))\n    return qatorlar[(p - 1) * list_per_page: p * list_per_page], jami",
      "sahifa(list(range(1, 46)), 20, 3)", "sahifa([1, 2, 3], 20, 1)", "sahifa([], 10, 1)", "sahifa(list(range(10)), 5, 2)"),
    F("Admin manzili", "`admin_url(ilova, model, amal=\"roʻyxat\", pk=None)` — `roʻyxat` → `/admin/ilova/model/`, `qoʻshish` → `.../add/`, `tahrir` → `.../PK/change/`, `oʻchirish` → `.../PK/delete/` (model kichik harfda). `tahrir`/`oʻchirish` da `pk` boʻlmasa `ValueError`.",
      "def admin_url(ilova, model, amal='roʻyxat', pk=None):\n    asos = f'/admin/{ilova}/{model.lower()}/'\n    if amal == 'roʻyxat':\n        return asos\n    if amal == 'qoʻshish':\n        return asos + 'add/'\n    if pk is None:\n        raise ValueError('pk kerak')\n    return asos + f\"{pk}/{'change' if amal == 'tahrir' else 'delete'}/\"",
      'admin_url("blog", "Post")', 'admin_url("blog", "Post", "qoʻshish")', 'admin_url("dokon", "Mahsulot", "tahrir", 5)', 'admin_url("blog", "Post", "oʻchirish", 12)', 'admin_url("blog", "Post", "tahrir")'),
    F("Admin sayti", "`Sayt` sinfi: `register(model, admin=\"ModelAdmin\")` — bir modelni ikki marta roʻyxatga olsa `ValueError(f\"{model} allaqachon roʻyxatda\")`; `royxat()` — modellar nomlari alifbo boʻyicha; `admin_of(model)` — admin sinfi nomi yoki `None`.",
      "class Sayt:\n    def __init__(self):\n        self._r = {}\n\n    def register(self, model, admin='ModelAdmin'):\n        if model in self._r:\n            raise ValueError(f'{model} allaqachon roʻyxatda')\n        self._r[model] = admin\n\n    def royxat(self):\n        return sorted(self._r)\n\n    def admin_of(self, model):\n        return self._r.get(model)",
      '(s := Sayt(), s.register("Post", "PostAdmin"), s.register("Izoh"), s.royxat())[-1]', '(s := Sayt(), s.register("Post", "PostAdmin"), s.admin_of("Post"), s.admin_of("Kurs"))[2:]', '(s := Sayt(), s.register("Post"), s.register("Post"))[-1]', lv=2),
    L("docs", "dj-admin"),
    L("docs", "dj-tut7"),
    L("lc", "sort-the-people", note="Saralash kaliti bilan ishlash — `ordering` ning oʻzi."),
    L("exercism", "grade-school"),
])

# ---------------------------------------------------------------- 13.5
TOPIC("dj-orm", "ORM: maʼlumotlar bazasi API", "objects.all, filter, exclude, get, order_by va lookup'lar", 30, r'''
**ORM** (Object-Relational Mapping) — SQL oʻrniga Python yozish usuli. Django har bir modelga `objects` menejerini beradi:

```py norun
Kitob.objects.all()                                # SELECT * FROM kitob
Kitob.objects.filter(janr="roman")                 # WHERE janr = 'roman'
Kitob.objects.filter(narx__gte=40000)              # WHERE narx >= 40000
Kitob.objects.filter(nom__icontains="kun")         # WHERE nom LIKE '%kun%' (katta-kichik farqsiz)
Kitob.objects.exclude(janr="qissa")                # WHERE NOT janr = 'qissa'
Kitob.objects.order_by("-yil")                     # ORDER BY yil DESC
Kitob.objects.get(pk=1)                            # bitta obyekt (yoki xato)
Kitob.objects.filter(janr="roman").count()         # SELECT COUNT(*) ...
Kitob.objects.all()[:3]                            # LIMIT 3

Kitob.objects.create(nom="Yangi", muallif="Men", yil=2026, narx=1000)
Kitob.objects.filter(janr="roman").update(narx=50000)
Kitob.objects.filter(yil__lt=1930).delete()
```

## Lookup'lar: `maydon__amal=qiymat`
| Lookup | Maʼnosi |
|---|---|
| `exact` (standart) | teng |
| `iexact` | teng, katta-kichik farqsiz |
| `gt`, `gte`, `lt`, `lte` | `>`, `>=`, `<`, `<=` |
| `contains`, `icontains` | ichida bor |
| `startswith` | bilan boshlanadi |
| `in` | roʻyxatda bor |
| `range` | oraliqda (ikkala chegara ham kiradi) |

## ORM'ning ichi qanday?
Kichik `QuerySet` ni oʻzimiz yozib, Django qanday "oʻylashini" koʻramiz:

```py
KITOBLAR = [
    {"id": 1, "nom": "Oʻtkan kunlar", "muallif": "Abdulla Qodiriy", "yil": 1926, "narx": 45000},
    {"id": 2, "nom": "Mehrobdan chayon", "muallif": "Abdulla Qodiriy", "yil": 1929, "narx": 40000},
    {"id": 3, "nom": "Sariq devni minib", "muallif": "Xudoyberdi Toʻxtaboyev", "yil": 1968, "narx": 30000},
    {"id": 4, "nom": "Ikki eshik orasi", "muallif": "Oʻtkir Hoshimov", "yil": 1986, "narx": 55000},
]

AMALLAR = {
    "exact": lambda a, v: a == v,
    "gt": lambda a, v: a > v,
    "gte": lambda a, v: a >= v,
    "lt": lambda a, v: a < v,
    "icontains": lambda a, v: v.lower() in a.lower(),
}


def mos(qator, kalit, qiymat):
    maydon, _, amal = kalit.partition("__")
    return AMALLAR[amal or "exact"](qator[maydon], qiymat)


class QuerySet:
    def __init__(self, qatorlar):
        self.qatorlar = list(qatorlar)

    def filter(self, **shart):
        return QuerySet(q for q in self.qatorlar if all(mos(q, k, v) for k, v in shart.items()))

    def order_by(self, maydon):
        return QuerySet(sorted(self.qatorlar, key=lambda q: q[maydon.lstrip("-")], reverse=maydon.startswith("-")))

    def count(self):
        return len(self.qatorlar)

    def __iter__(self):
        return iter(self.qatorlar)


objects = QuerySet(KITOBLAR)
print(objects.filter(narx__gte=40000).count())
for k in objects.filter(muallif__icontains="qodiriy").order_by("-yil"):
    print(k["yil"], k["nom"])
```

> Har bir `filter` **yangi** QuerySet qaytaradi — shuning uchun ularni zanjir qilib ulash mumkin: `.filter(...).exclude(...).order_by(...)`.

## QuerySet "dangasa" (lazy)
`Kitob.objects.filter(...)` yozilganda bazaga hali soʻrov ketmaydi! Soʻrov natija **haqiqatda kerak boʻlganda** bajariladi: `for`, `list()`, `len()`, `print()`, `[0]`.

## get va xatolar
```py norun
from django.shortcuts import get_object_or_404

try:
    k = Kitob.objects.get(pk=999)
except Kitob.DoesNotExist:
    print("Topilmadi")

# get() bir nechta topsa — Kitob.MultipleObjectsReturned
k = get_object_or_404(Kitob, pk=1)      # view'larda eng qulay yoʻl
```

## Agregatlar
```py norun
from django.db.models import Avg, Count, Max

Kitob.objects.aggregate(Avg("narx"), Max("yil"))
# {'narx__avg': 41250.0, 'yil__max': 1986}
Kitob.objects.values("muallif").annotate(soni=Count("id"))
```

!> Sikl ichida `Kitob.objects.get(...)` chaqirish — har safar alohida SQL soʻrov. Bitta `filter(id__in=[...])` bilan oling — tezlik oʻnlab barobar oshadi.
''', [
    P('print("narx__gte".partition("__"))', "('narx', 'gte')", "['narx', 'gte']", "Xato"),
    P('print("ism".partition("__"))', "('ism',)", "('ism', '__', '')", "Xato"),
    P('kitoblar = [{"n": "A", "narx": 50}, {"n": "B", "narx": 30}]\nprint([k["n"] for k in sorted(kitoblar, key=lambda k: -k["narx"])])', "['B', 'A']", "[50, 30]", "Xato"),
    P('print("TH".lower() in "Python".lower(), "TH" in "Python")', "True True", "False False", "Xato"),
    P('narxlar = [50, 30, 80]\nprint(round(sum(narxlar) / len(narxlar), 1), max(narxlar))', "53 80", "160 80", "Xato"),
    P('q = [1, 2, 3, 4, 5]\nprint(q[:2], q[2:4])', "[1, 2] [3, 4, 5]", "[0, 1] [2, 3]", "Xato"),
    P('a, b = 3, 7\nprint(10 in range(a, b + 1), 7 in range(a, b + 1))', "True True", "False False", "True False", lv=2,
      why="`__range=(3, 7)` — ikkala chegara ham kiradi (SQL `BETWEEN`). Python'da buning uchun `range(a, b + 1)`."),
    Q("`Kitob.objects.get(pk=999)` yozuv topilmasa nima boʻladi?", "`Kitob.DoesNotExist` xatosi koʻtariladi", "`None` qaytadi", "Boʻsh roʻyxat qaytadi", "Yangi yozuv yaratiladi"),
    Q("QuerySet bazaga qachon soʻrov yuboradi?", "Natija haqiqatda kerak boʻlganda (`for`, `list`, `len`, `print`) — u dangasa (lazy)", "`filter()` yozilishi bilanoq", "Har bir qatorda alohida", "Hech qachon"),
    F("Lookup'lar", "`mos(qator, kalit, qiymat)` — `kalit` = `maydon` yoki `maydon__amal`. Amallar: `exact`, `iexact`, `gt`, `gte`, `lt`, `lte`, `contains`, `icontains`, `startswith`, `in`, `range` (ikkala chegara kiradi). Nomaʼlum amal — `ValueError`.",
      "def mos(qator, kalit, qiymat):\n    maydon, _, amal = kalit.partition('__')\n    a = qator[maydon]\n    amal = amal or 'exact'\n    if amal == 'exact':\n        return a == qiymat\n    if amal == 'iexact':\n        return a.lower() == qiymat.lower()\n    if amal == 'gt':\n        return a > qiymat\n    if amal == 'gte':\n        return a >= qiymat\n    if amal == 'lt':\n        return a < qiymat\n    if amal == 'lte':\n        return a <= qiymat\n    if amal == 'contains':\n        return qiymat in a\n    if amal == 'icontains':\n        return qiymat.lower() in a.lower()\n    if amal == 'startswith':\n        return a.startswith(qiymat)\n    if amal == 'in':\n        return a in qiymat\n    if amal == 'range':\n        return qiymat[0] <= a <= qiymat[1]\n    raise ValueError(amal)",
      'mos(__import__("baza").KITOBLAR[0], "narx__gte", 45000)', 'mos(__import__("baza").KITOBLAR[0], "nom__icontains", "KUN")', 'mos(__import__("baza").KITOBLAR[2], "yil__range", (1960, 1970))',
      'mos(__import__("baza").KITOBLAR[3], "janr__in", ["qissa", "roman"])', 'mos(__import__("baza").KITOBLAR[1], "muallif__iexact", "abdulla qodiriy")', 'mos(__import__("baza").KITOBLAR[1], "yil__regex", "19")', lv=2, files=BAZA),
    F("filter()", "`filtrla(qatorlar, **shart)` — barcha shartlar bajarilgan qatorlarning `id` lari. Lookup'lar: `exact`, `gt`, `gte`, `lt`, `lte`, `icontains`.",
      "def filtrla(qatorlar, **shart):\n    amallar = {\n        'exact': lambda a, v: a == v,\n        'gt': lambda a, v: a > v,\n        'gte': lambda a, v: a >= v,\n        'lt': lambda a, v: a < v,\n        'lte': lambda a, v: a <= v,\n        'icontains': lambda a, v: v.lower() in a.lower(),\n    }\n    natija = []\n    for q in qatorlar:\n        if all(amallar[k.partition('__')[2] or 'exact'](q[k.partition('__')[0]], v) for k, v in shart.items()):\n            natija.append(q['id'])\n    return natija",
      'filtrla(__import__("baza").KITOBLAR, janr="roman")', 'filtrla(__import__("baza").KITOBLAR, janr="roman", narx__lt=50000)', 'filtrla(__import__("baza").KITOBLAR, muallif__icontains="hoshimov", yil__gte=1985)', 'filtrla(__import__("baza").KITOBLAR)', files=BAZA),
    F("exclude()", "`chiqarib_tashla(qatorlar, **shart)` — `filter` ning teskarisi: barcha shartlar **birga** bajarilgan qatorlardan tashqari qatorlarning `id` lari (faqat aniq tenglik).",
      "def chiqarib_tashla(qatorlar, **shart):\n    return [q['id'] for q in qatorlar if not all(q[k] == v for k, v in shart.items())]",
      'chiqarib_tashla(__import__("baza").KITOBLAR, janr="roman")', 'chiqarib_tashla(__import__("baza").KITOBLAR, janr="roman", yil=1926)', 'chiqarib_tashla([], janr="x")', lv=1, files=BAZA),
    F("get()", "`ol(qatorlar, **shart)` — aniq tenglik boʻyicha **bitta** qatorni qaytarsin; hech biri topilmasa `LookupError(\"DoesNotExist\")`, bir nechta topilsa `LookupError(\"MultipleObjectsReturned\")`.",
      "def ol(qatorlar, **shart):\n    r = [q for q in qatorlar if all(q[k] == v for k, v in shart.items())]\n    if not r:\n        raise LookupError('DoesNotExist')\n    if len(r) > 1:\n        raise LookupError('MultipleObjectsReturned')\n    return r[0]",
      'ol(__import__("baza").KITOBLAR, id=3)["nom"]', 'ol(__import__("baza").KITOBLAR, id=99)', 'ol(__import__("baza").KITOBLAR, janr="roman")', 'ol(__import__("baza").KITOBLAR, janr="qissa")["muallif"]', files=BAZA),
    F("order_by()", "`tartibla(qatorlar, *maydonlar)` — bir nechta maydon boʻyicha saralangan `id` lar (`-` — kamayish; birinchi maydon asosiy).",
      "def tartibla(qatorlar, *maydonlar):\n    r = list(qatorlar)\n    for m in reversed(maydonlar):\n        r.sort(key=lambda q: q[m.lstrip('-')], reverse=m.startswith('-'))\n    return [q['id'] for q in r]",
      'tartibla(__import__("baza").KITOBLAR, "-narx")', 'tartibla(__import__("baza").KITOBLAR, "janr", "-yil")', 'tartibla(__import__("baza").KITOBLAR)', files=BAZA),
    F("aggregate()", "`agregat(qatorlar, maydon)` — `{\"count\": ..., \"sum\": ..., \"avg\": ... (2 xona), \"min\": ..., \"max\": ...}`; boʻsh roʻyxatda `count` 0, qolganlari `None`.",
      "def agregat(qatorlar, maydon):\n    v = [q[maydon] for q in qatorlar]\n    if not v:\n        return {'count': 0, 'sum': None, 'avg': None, 'min': None, 'max': None}\n    return {'count': len(v), 'sum': sum(v), 'avg': round(sum(v) / len(v), 2), 'min': min(v), 'max': max(v)}",
      'agregat(__import__("baza").KITOBLAR, "narx")', 'agregat(__import__("baza").KITOBLAR, "yil")', 'agregat([], "narx")', files=BAZA),
    F("Zanjirli QuerySet", "`QuerySet(qatorlar)` sinfi: `filter(**shart)` (aniq tenglik) va `order_by(maydon)` — **yangi** QuerySet qaytarsin; `count()`, `first()` (boʻsh boʻlsa `None`) va `ids()` — `id` lar roʻyxati.",
      "class QuerySet:\n    def __init__(self, qatorlar):\n        self.q = list(qatorlar)\n\n    def filter(self, **shart):\n        return QuerySet(x for x in self.q if all(x[k] == v for k, v in shart.items()))\n\n    def order_by(self, maydon):\n        return QuerySet(sorted(self.q, key=lambda x: x[maydon.lstrip('-')], reverse=maydon.startswith('-')))\n\n    def count(self):\n        return len(self.q)\n\n    def first(self):\n        return self.q[0] if self.q else None\n\n    def ids(self):\n        return [x['id'] for x in self.q]",
      'QuerySet(__import__("baza").KITOBLAR).filter(janr="roman").count()', 'QuerySet(__import__("baza").KITOBLAR).filter(janr="roman").order_by("-narx").ids()',
      'QuerySet(__import__("baza").KITOBLAR).order_by("yil").first()["nom"]', 'QuerySet(__import__("baza").KITOBLAR).filter(janr="drama").first()',
      '(qs := QuerySet(__import__("baza").KITOBLAR), qs.filter(id=1), qs.count())[-1]', lv=3, files=BAZA),
    L("docs", "dj-queries"),
    L("docs", "djgirls-orm"),
    L("lc", "big-countries", note="SQL mashqi: `WHERE ... OR ...` — ORM dagi `filter` bilan solishtiring."),
    L("lc", "combine-two-tables", note="SQL JOIN — Django'da `ForeignKey` va `select_related` shuni qiladi."),
])

# ---------------------------------------------------------------- 13.6
TOPIC("dj-shablonlar", "Shablonlar, Bootstrap va umumiy layout", "{{ }}, filtrlar, {% for %}, {% extends %}, {% include %} va static", 30, r'''
**Shablon** (template) — ichida maxsus belgilar boʻlgan HTML fayl. View kontekst (lugʻat) beradi, shablon esa uni chiroyli HTML ga aylantiradi.

```py norun
# blog/views.py
from django.shortcuts import render


def postlar(request):
    return render(request, "blog/postlar.html", {"sarlavha": "Blog", "postlar": Post.objects.all()})
```

```html
<!-- blog/templates/blog/postlar.html -->
<h1>{{ sarlavha|upper }}</h1>

<ul>
  {% for post in postlar %}
    <li>{{ forloop.counter }}. {{ post.sarlavha }} — {{ post.muallif.username|default:"nomaʼlum" }}</li>
  {% empty %}
    <li>Hali post yoʻq</li>
  {% endfor %}
</ul>

{% if postlar|length > 10 %}<a href="?sahifa=2">Keyingi →</a>{% endif %}
```

## Sintaksis bir qarashda
| Belgi | Maʼnosi |
|---|---|
| `{{ ozgaruvchi }}` | qiymatni chiqarish |
| `{{ post.sarlavha }}` | nuqta — atribut, kalit yoki indeks |
| `{{ matn\|upper }}` | filtr (`\|` dan keyin) |
| `{% for %}...{% endfor %}` | sikl, `{% empty %}` — boʻsh boʻlsa |
| `{% if %}...{% endif %}` | shart |
| `{# izoh #}` | izoh |

## Shablon qanday ishlaydi? Mini-renderer
```py
import html
import re

FILTRLAR = {
    "upper": lambda v, a: str(v).upper(),
    "length": lambda v, a: len(v),
    "default": lambda v, a: v or a,
}


def qiymat(ifoda, kontekst):
    nom, *filtrlar = ifoda.strip().split("|")
    v = kontekst
    for qism in nom.split("."):
        v = v.get(qism, "") if isinstance(v, dict) else getattr(v, qism, "")
    for f in filtrlar:
        fnom, _, arg = f.partition(":")
        v = FILTRLAR[fnom](v, arg.strip('"'))
    return v


def render(shablon, kontekst):
    return re.sub(r"\{\{(.*?)\}\}", lambda m: html.escape(str(qiymat(m.group(1), kontekst))), shablon)


print(render("<h1>{{ sarlavha|upper }}</h1>", {"sarlavha": "Mirae blog"}))
print(render('Muallif: {{ post.muallif|default:"nomaʼlum" }}', {"post": {"muallif": ""}}))
print(render("{{ izoh }}", {"izoh": "<script>alert(1)</script>"}))
```

> Oxirgi qatorga qarang: Django **avtomatik ekranlaydi** (`<` → `&lt;`). Foydalanuvchi yozgan zararli `<script>` ishlamaydi. Bu XSS hujumidan himoya.

## Umumiy layout: `{% extends %}` va `{% block %}`
Har bir sahifada menyu, footer, Bootstrap ulanishi takrorlanmasligi uchun **bazaviy shablon** yasaymiz:

```html
<!-- templates/base.html -->
{% load static %}
<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Mirae{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'css/style.css' %}" rel="stylesheet">
</head>
<body>
  {% include "partials/navbar.html" %}
  <main class="container py-4">
    {% block content %}{% endblock %}
  </main>
</body>
</html>
```

```html
<!-- blog/templates/blog/postlar.html -->
{% extends "base.html" %}
{% block title %}Blog · {{ block.super }}{% endblock %}
{% block content %}
  <div class="row">
    {% for post in postlar %}
      <div class="col-md-4"><div class="card p-3 mb-3">{{ post.sarlavha }}</div></div>
    {% endfor %}
  </div>
{% endblock %}
```

Meros qanday ishlashini Python'da koʻraylik:

```py
import re

BASE = """<title>{% block title %}Mirae{% endblock %}</title>
<main>{% block content %}{% endblock %}</main>"""

SAHIFA = """{% extends "base.html" %}
{% block title %}Blog{% endblock %}
{% block content %}<h1>Postlar</h1>{% endblock %}"""

BLOK = r"\{% block (\w+) %\}(.*?)\{% endblock %\}"


def meros(bola, ota):
    bloklar = dict(re.findall(BLOK, bola, re.S))
    return re.sub(BLOK, lambda m: bloklar.get(m.group(1), m.group(2)), ota, flags=re.S)


print(meros(SAHIFA, BASE))
```

## Shablonlarni ilovalar orasida ulashish
```py norun
# settings.py
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],      # umumiy: base.html, partials/
    "APP_DIRS": True,                       # har bir ilovaning templates/ papkasi
    ...
}]
```

| Joy | Nima uchun |
|---|---|
| `templates/base.html` | butun sayt uchun umumiy layout |
| `templates/partials/navbar.html` | `{% include %}` bilan ulanadigan boʻlaklar |
| `blog/templates/blog/...` | faqat blog ilovasining sahifalari |

!> Ilova shablonlarini `blog/templates/blog/` ichiga qoʻying (ilova nomi ikki marta!). Aks holda ikki ilovada bir xil `index.html` boʻlsa, Django birinchisini olib, ikkinchisini "yoʻqotadi".
''', [
    P('import html\nprint(html.escape("<b>"))', "<b>", "b", "Xato"),
    P('print("mirae blog".upper(), len("mirae blog"))', "Mirae Blog 10", "MIRAE BLOG 9", "Xato"),
    P('v = ""\nprint(v or "nomaʼlum")', "''", "None", "Xato"),
    P('v = 0\nprint(v or "yoʻq")', "0", "None", "Xato", lv=2,
      why="`0` ham \"yolgʻon\" qiymat. Django'ning `default` filtri ham `0` ni almashtiradi — faqat `None` uchun `default_if_none` ishlating."),
    P('matn = "Django tez va qulay freymvork"\nprint(" ".join(matn.split()[:3]) + " …")', "Django tez va qulay …", "Dja …", "Xato"),
    P('import re\nprint(re.findall(r"\\{\\{\\s*(\\w+)\\s*\\}\\}", "Salom {{ ism }}, {{yosh}}"))', "['{{ ism }}', '{{yosh}}']", "['ism']", "Xato"),
    P('postlar = []\nfor p in postlar:\n    print(p)\nelse:\n    print("Hali post yoʻq")', "(hech narsa chiqmaydi)", "Xato", "None", lv=2,
      why="Python'da `for ... else` — sikl `break` siz tugaganda ishlaydi (boʻsh roʻyxatda ham). Django'dagi `{% empty %}` esa **faqat** roʻyxat boʻsh boʻlganda ishlaydi — oʻxshash, lekin bir xil emas."),
    Q("`{% extends \"base.html\" %}` qayerda turishi kerak?", "Shablonning eng birinchi tegi sifatida", "Faylning oxirida", "Istalgan joyda", "Faqat `base.html` ichida"),
    Q("Ikki ilovada bir xil `index.html` boʻlsa, chalkashmaslik uchun nima qilinadi?", "Shablonlar `ilova/templates/ilova/index.html` kabi ilova nomli papkaga joylanadi", "Bittasi oʻchiriladi", "`DEBUG = False` qilinadi", "Fayllar `.txt` ga oʻzgartiriladi"),
    F("Nuqtali qidiruv", "`qiymat(ifoda, kontekst)` — `\"post.muallif.ism\"` kabi yoʻlni hal qilsin: lugʻatda kalit, roʻyxatda raqamli indeks (`\"postlar.0\"`), aks holda atribut. Topilmasa — `\"\"` (Django xato bermaydi).",
      "def qiymat(ifoda, kontekst):\n    v = kontekst\n    for q in ifoda.split('.'):\n        try:\n            if isinstance(v, dict):\n                v = v[q]\n            elif isinstance(v, (list, tuple)) and q.isdigit():\n                v = v[int(q)]\n            else:\n                v = getattr(v, q)\n        except (KeyError, IndexError, AttributeError):\n            return ''\n    return v",
      'qiymat("post.muallif.ism", {"post": {"muallif": {"ism": "Ali"}}})', 'qiymat("postlar.1", {"postlar": ["a", "b"]})', 'qiymat("yoq.narsa", {})', 'qiymat("s.real", {"s": 3})', lv=2),
    F("Filtrlar", "`filtr(v, nom, arg=None)` — `upper`, `lower`, `title`, `length`, `default` (v yolgʻon boʻlsa `arg`), `truncatewords` (`arg` ta soʻz, kesilsa oxiriga ` …`), `join` (`arg` ajratuvchi bilan). Nomaʼlum — `ValueError(f\"Nomaʼlum filtr: {nom}\")`.",
      "def filtr(v, nom, arg=None):\n    if nom == 'upper':\n        return str(v).upper()\n    if nom == 'lower':\n        return str(v).lower()\n    if nom == 'title':\n        return str(v).title()\n    if nom == 'length':\n        return len(v)\n    if nom == 'default':\n        return v or arg\n    if nom == 'truncatewords':\n        s = str(v).split()\n        n = int(arg)\n        return ' '.join(s[:n]) + (' …' if len(s) > n else '')\n    if nom == 'join':\n        return arg.join(str(x) for x in v)\n    raise ValueError(f'Nomaʼlum filtr: {nom}')",
      'filtr("salom", "upper")', 'filtr("", "default", "yoʻq")', 'filtr("bir ikki uch toʻrt", "truncatewords", 2)', 'filtr(["a", "b"], "join", ", ")', 'filtr([1, 2, 3], "length")', 'filtr("x", "slugify")'),
    F("Mini render", "`render(shablon, kontekst)` — har bir `{{ ifoda }}` ni almashtirsin: ifoda `nom` yoki `nom|upper` / `nom|lower`; qiymat `html.escape` bilan ekranlansin, faqat `|safe` filtri boʻlsa ekranlanmasin. Yoʻq oʻzgaruvchi — boʻsh satr.",
      "import html\nimport re\n\n\ndef render(shablon, kontekst):\n    def almash(m):\n        nom, *filtrlar = [x.strip() for x in m.group(1).split('|')]\n        v = str(kontekst.get(nom, ''))\n        for f in filtrlar:\n            if f == 'upper':\n                v = v.upper()\n            elif f == 'lower':\n                v = v.lower()\n        return v if 'safe' in filtrlar else html.escape(v)\n    return re.sub(r'\\{\\{(.*?)\\}\\}', almash, shablon)",
      'render("<h1>{{ s|upper }}</h1>", {"s": "blog"})', 'render("{{ x }}", {"x": "<b>qalin</b>"})', 'render("{{ x|safe }}", {"x": "<b>qalin</b>"})', 'render("Salom, {{ ism }}!", {})', lv=2),
    F("for va empty", "`royxat(elementlar, bosh=\"Roʻyxat boʻsh\")` — har bir element uchun `\"N. element\"` qatori (`forloop.counter` 1 dan), `\\n` bilan birlashtirilgan; boʻsh boʻlsa — `bosh`.",
      "def royxat(elementlar, bosh='Roʻyxat boʻsh'):\n    if not elementlar:\n        return bosh\n    return '\\n'.join(f'{i}. {e}' for i, e in enumerate(elementlar, 1))",
      'royxat(["Django", "Flask"])', "royxat([])", 'royxat([], "Hali post yoʻq")', lv=1),
    F("Shablon merosi", "`meros(bola, ota)` — otadagi har bir `{% block nom %}...{% endblock %}` ni bolaning shu nomli bloki bilan almashtirsin (bolada boʻlmasa — otaniki qoladi). Bola blokida `{{ block.super }}` boʻlsa, u otaning shu blokdagi matni bilan almashtirilsin.",
      "import re\n\nBLOK = r'\\{% block (\\w+) %\\}(.*?)\\{% endblock %\\}'\n\n\ndef meros(bola, ota):\n    bloklar = dict(re.findall(BLOK, bola, re.S))\n\n    def almash(m):\n        if m.group(1) not in bloklar:\n            return m.group(2)\n        return bloklar[m.group(1)].replace('{{ block.super }}', m.group(2))\n    return re.sub(BLOK, almash, ota, flags=re.S)",
      'meros("{% block t %}Blog{% endblock %}", "<title>{% block t %}Mirae{% endblock %}</title>")', 'meros("", "<p>{% block a %}A{% endblock %}</p>")', 'meros("{% block t %}Blog · {{ block.super }}{% endblock %}", "<title>{% block t %}Mirae{% endblock %}</title>")',
      'meros("{% block x %}X{% endblock %}{% block b %}2{% endblock %}", "{% block a %}1{% endblock %}|{% block b %}{% endblock %}")', lv=3),
    F("static", "`static(yol, STATIC_URL=\"/static/\")` — `{% static %}` tegi kabi: `STATIC_URL` va `yol` ni bitta `/` bilan ulasin (ortiqcha `/` lar olib tashlansin).",
      "def static(yol, STATIC_URL='/static/'):\n    return STATIC_URL.rstrip('/') + '/' + yol.lstrip('/')",
      'static("css/style.css")', 'static("/img/logo.png", "https://cdn.mirae.uz/s")', 'static("js/app.js", "/assets/")', lv=1),
    F("Bootstrap jadval", "`jadval(sarlavhalar, qatorlar)` — `<table class=\"table table-striped\">` HTML satri: `<thead><tr><th>..</th></tr></thead><tbody><tr><td>..</td></tr>...</tbody></table>` (boʻsh joysiz, barcha qiymatlar `html.escape` bilan).",
      "import html\n\n\ndef jadval(sarlavhalar, qatorlar):\n    bosh = ''.join(f'<th>{html.escape(str(s))}</th>' for s in sarlavhalar)\n    tana = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(v))}</td>' for v in q) + '</tr>' for q in qatorlar)\n    return f'<table class=\"table table-striped\"><thead><tr>{bosh}</tr></thead><tbody>{tana}</tbody></table>'",
      'jadval(["Ism", "Ball"], [["Ali", 85], ["Madina", 92]])', 'jadval(["X"], [])', 'jadval(["<b>"], [["a & b"]])', lv=2),
    L("docs", "dj-templates"),
    L("docs", "dj-builtins"),
    L("docs", "djgirls-templates"),
    L("docs", "djgirls-css"),
])

# ---------------------------------------------------------------- 13.7
TOPIC("dj-url", "URL parametrlari, 404 va bosh sahifa", "path converter'lar, get_object_or_404, reverse va {% url %}", 30, r'''
Har bir post, mahsulot yoki talabaning oʻz sahifasi boʻladi: `/post/5/`, `/kurs/python-asoslari/`. Bu raqam yoki nom — **URL parametri**.

```py norun
# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"                      # nomlar fazosi: "blog:post"
urlpatterns = [
    path("", views.bosh_sahifa, name="bosh"),
    path("post/<int:pk>/", views.post_detail, name="post"),
    path("kategoriya/<slug:slug>/", views.kategoriya, name="kategoriya"),
]

# mysite/urls.py
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]
```

```py norun
# blog/views.py
from django.shortcuts import get_object_or_404, render


def post_detail(request, pk):           # pk allaqachon int!
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post.html", {"post": post})
```

## Path converter'lar
| Converter | Qabul qiladi | View'ga keladi |
|---|---|---|
| `<int:pk>` | `0`, `42` | `int` |
| `<str:nom>` | `/` dan boshqa hamma narsa | `str` |
| `<slug:slug>` | harf, raqam, `-`, `_` | `str` |
| `<uuid:id>` | UUID | `uuid.UUID` |
| `<path:yol>` | `/` bilan ham | `str` |

Django har bir `path` ni **regex** ga aylantiradi. Buni oʻzimiz qilib koʻraylik:

```py
import re

KONVERTER = {"int": (r"[0-9]+", int), "str": (r"[^/]+", str), "slug": (r"[-a-zA-Z0-9_]+", str)}


def moslashtir(yol, url):
    turlar = {}

    def almash(m):
        tur, nom = m.group(1) or "str", m.group(2)
        turlar[nom] = KONVERTER[tur][1]
        return f"(?P<{nom}>{KONVERTER[tur][0]})"

    regex = "^" + re.sub(r"<(?:(\w+):)?(\w+)>", almash, yol) + "$"
    m = re.match(regex, url)
    return {k: turlar[k](v) for k, v in m.groupdict().items()} if m else None


print(moslashtir("post/<int:pk>/", "post/42/"))
print(moslashtir("post/<int:pk>/", "post/abc/"))
print(moslashtir("kategoriya/<slug:slug>/", "kategoriya/python-asoslari/"))
```

## Bitta obyekt va 404
Mavjud boʻlmagan post soʻralsa, sayt **500 xato** emas, chiroyli **404** qaytarishi kerak:

```py
class Http404(Exception):
    pass


POSTLAR = {1: "Django asoslari", 2: "URL parametrlari"}


def get_object_or_404(baza, pk):
    try:
        return baza[pk]
    except KeyError:
        raise Http404(f"Post #{pk} topilmadi") from None


def post_detail(request, pk):
    return f"<h1>{get_object_or_404(POSTLAR, pk)}</h1>"


for pk in [1, 7]:
    try:
        print(200, post_detail(None, pk))
    except Http404 as e:
        print(404, e)
```

## URL larga nom orqali murojaat
Manzilni qoʻlda yozmang — **nom** bilan oling. Ertaga `post/` ni `maqola/` ga oʻzgartirsangiz, hamma havolalar oʻzi yangilanadi:

```py norun
from django.urls import reverse
from django.shortcuts import redirect

reverse("blog:post", args=[5])            # '/post/5/'
reverse("blog:kategoriya", kwargs={"slug": "django"})
redirect("blog:post", pk=5)               # nom bilan yoʻnaltirish
```

```html
<a href="{% url 'blog:post' post.pk %}">{{ post.sarlavha }}</a>
<a href="{% url 'blog:bosh' %}">Bosh sahifa</a>
```

## Bosh sahifa
Bosh sahifa — `path("", ...)` . U odatda eng soʻnggi postlar, mashhur kurslar kabi "vitrina" boʻladi:

```py norun
def bosh_sahifa(request):
    return render(request, "blog/bosh.html", {
        "songgi": Post.objects.filter(holat="n").order_by("-yaratilgan")[:5],
        "mashhur": Post.objects.order_by("-korishlar")[:3],
    })
```

> `APPEND_SLASH = True` (standart): `/haqida` soʻralsa, Django avtomatik `/haqida/` ga yoʻnaltiradi. Shuning uchun `path` lar `/` bilan tugaydi.

!> `<int:pk>` dagi nom (`pk`) view argumenti nomi bilan **bir xil** boʻlishi shart: `def post_detail(request, pk)`.
''', [
    P('import re\nm = re.match(r"^post/(?P<pk>[0-9]+)/$", "post/42/")\nprint(m["pk"], type(m["pk"]).__name__)', "42 int", "post/42/ str", "Xato",
      why="Regex har doim **satr** qaytaradi. Django `<int:pk>` converter'i uni `int()` ga aylantirib beradi."),
    P('import re\nprint(bool(re.match(r"^post/(?P<pk>[0-9]+)/$", "post/abc/")))', "True", "abc", "Xato"),
    P('import re\nslug = r"[-a-zA-Z0-9_]+"\nprint(bool(re.fullmatch(slug, "salom-dunyo_2")), bool(re.fullmatch(slug, "salom dunyo")))', "True True", "False False", "False True"),
    P('class Http404(Exception):\n    pass\n\n\ntry:\n    raise Http404("topilmadi")\nexcept Exception as e:\n    print(type(e).__name__, e)', "Exception topilmadi", "404", "Xato"),
    P('yol = "post/<int:pk>/"\nprint("/" + yol.replace("<int:pk>", str(5)))', "/post/<int:5>/", "post/5/", "Xato"),
    P('print("blog:post".split(":"))', "('blog', 'post')", "['blog:post']", "Xato"),
    P('yol = "haqida"\nprint(yol if yol.endswith("/") else yol + "/")', "haqida", "/haqida", "Xato", lv=2,
      why="Bu `APPEND_SLASH` ning mantiqi: `/` bilan tugamagan manzilga `/` qoʻshib yoʻnaltiriladi."),
    Q("`get_object_or_404(Post, pk=7)` obyekt topilmasa nima qiladi?", "`Http404` koʻtaradi — foydalanuvchi 404 sahifasini koʻradi", "`None` qaytaradi", "500 xato beradi", "Bosh sahifaga yoʻnaltiradi"),
    Q("Shablonda havolani qoʻlda yozish oʻrniga nima afzal?", "`{% url 'blog:post' post.pk %}` — URL nomi orqali", "`<a href=\"/post/5/\">` qattiq yozish", "JavaScript bilan yasash", "Havolasiz ishlash"),
    F("path → regex", "`namuna(yol)` — Django yoʻlini regex satriga aylantirsin: `<int:x>` → `(?P<x>[0-9]+)`, `<str:x>` va `<x>` → `(?P<x>[^/]+)`, `<slug:x>` → `(?P<x>[-a-zA-Z0-9_]+)`; boshiga `^`, oxiriga `$`.",
      "import re\n\n\ndef namuna(yol):\n    turlar = {'int': '[0-9]+', 'str': '[^/]+', 'slug': '[-a-zA-Z0-9_]+'}\n    return '^' + re.sub(r'<(?:(\\w+):)?(\\w+)>', lambda m: f'(?P<{m.group(2)}>{turlar[m.group(1) or \"str\"]})', yol) + '$'",
      'namuna("post/<int:pk>/")', 'namuna("kategoriya/<slug:slug>/")', 'namuna("salom/<ism>/")', 'namuna("")', lv=2),
    F("URL ni moslashtirish", "`moslashtir(yol, url)` — mos kelsa parametrlar lugʻati (`int` converter — `int` qiymat), mos kelmasa `None`. Converter'lar: `int`, `str`, `slug`.",
      "import re\n\n\ndef moslashtir(yol, url):\n    k = {'int': ('[0-9]+', int), 'str': ('[^/]+', str), 'slug': ('[-a-zA-Z0-9_]+', str)}\n    turlar = {}\n\n    def almash(m):\n        tur = m.group(1) or 'str'\n        turlar[m.group(2)] = k[tur][1]\n        return f'(?P<{m.group(2)}>{k[tur][0]})'\n    m = re.match('^' + re.sub(r'<(?:(\\w+):)?(\\w+)>', almash, yol) + '$', url)\n    return {n: turlar[n](v) for n, v in m.groupdict().items()} if m else None",
      'moslashtir("post/<int:pk>/", "post/42/")', 'moslashtir("post/<int:pk>/", "post/abc/")', 'moslashtir("kurs/<slug:s>/dars/<int:n>/", "kurs/python-1/dars/3/")', 'moslashtir("", "")', lv=3),
    F("Router", "`router(urlpatterns, url)` — `urlpatterns`: `[(yol, nom)]`; birinchi mos kelgan yoʻl uchun `(nom, parametrlar)`, hech biri mos kelmasa `(\"404\", {})`. Faqat `<int:x>` va `<slug:x>` converter'lari ishlatiladi.",
      "import re\n\n\ndef router(urlpatterns, url):\n    k = {'int': ('[0-9]+', int), 'slug': ('[-a-zA-Z0-9_]+', str)}\n    for yol, nom in urlpatterns:\n        turlar = {}\n\n        def almash(m):\n            turlar[m.group(2)] = k[m.group(1)][1]\n            return f'(?P<{m.group(2)}>{k[m.group(1)][0]})'\n        m = re.match('^' + re.sub(r'<(\\w+):(\\w+)>', almash, yol) + '$', url)\n        if m:\n            return nom, {n: turlar[n](v) for n, v in m.groupdict().items()}\n    return '404', {}",
      'router([("", "bosh"), ("post/<int:pk>/", "post")], "post/7/")', 'router([("", "bosh"), ("post/<int:pk>/", "post")], "")', 'router([("", "bosh")], "yoq/")', 'router([("k/<slug:s>/", "kat")], "k/web-dev/")', lv=2),
    F("reverse()", "`reverse(urlpatterns, nom, **kw)` — `urlpatterns`: `[(yol, nom)]`; nom boʻyicha yoʻlni topib, `<tur:x>` larni `kw[x]` bilan almashtirsin va boshiga `/` qoʻshsin. Nom topilmasa yoki parametr yetishmasa — `LookupError(f\"NoReverseMatch: {nom}\")`.",
      "import re\n\n\ndef reverse(urlpatterns, nom, **kw):\n    for yol, n in urlpatterns:\n        if n == nom:\n            try:\n                return '/' + re.sub(r'<(?:\\w+:)?(\\w+)>', lambda m: str(kw[m.group(1)]), yol)\n            except KeyError:\n                break\n    raise LookupError(f'NoReverseMatch: {nom}')",
      'reverse([("", "bosh"), ("post/<int:pk>/", "post")], "post", pk=5)', 'reverse([("", "bosh")], "bosh")', 'reverse([("post/<int:pk>/", "post")], "kurs")', 'reverse([("post/<int:pk>/", "post")], "post")'),
    F("get_object_or_404", "`Http404` xatosini (`Exception` dan meros) yarating va `ol_yoki_404(qatorlar, **shart)` yozing: aniq tenglik boʻyicha birinchi mos qatorni qaytarsin, topilmasa `Http404(\"Topilmadi\")` koʻtarsin.",
      "class Http404(Exception):\n    pass\n\n\ndef ol_yoki_404(qatorlar, **shart):\n    for q in qatorlar:\n        if all(q.get(k) == v for k, v in shart.items()):\n            return q\n    raise Http404('Topilmadi')",
      'ol_yoki_404(__import__("baza").KITOBLAR, id=2)["nom"]', 'ol_yoki_404(__import__("baza").KITOBLAR, id=42)', 'ol_yoki_404(__import__("baza").KITOBLAR, janr="qissa")["id"]', 'issubclass(Http404, Exception)', files=BAZA),
    F("slugify", "`slugify(matn)` — URL uchun: kichik harflar, `ʻ` `ʼ` `'` olib tashlansin, harf/raqam boʻlmagan har qanday belgilar ketma-ketligi bitta `-` ga, boshi va oxiridagi `-` olib tashlansin (faqat lotin harflari va raqamlar qoladi).",
      "import re\n\n\ndef slugify(matn):\n    m = re.sub(\"[ʻʼ']\", '', matn.lower())\n    return re.sub('[^a-z0-9]+', '-', m).strip('-')",
      'slugify("Oʻzbekiston — 2026!")', 'slugify("  Python asoslari  ")', 'slugify("Django & REST API")', 'slugify("---")', lv=2),
    F("Non ushoqlari", "`ushoq(url)` — bosh sahifadan boshlab navigatsiya (breadcrumbs): `\"/blog/post/5/\"` → `[(\"Bosh sahifa\", \"/\"), (\"blog\", \"/blog/\"), (\"post\", \"/blog/post/\"), (\"5\", \"/blog/post/5/\")]`.",
      "def ushoq(url):\n    natija = [('Bosh sahifa', '/')]\n    yol = '/'\n    for q in [x for x in url.split('/') if x]:\n        yol += q + '/'\n        natija.append((q, yol))\n    return natija",
      'ushoq("/blog/post/5/")', 'ushoq("/")', 'ushoq("kurslar")', lv=1),
    L("docs", "dj-urls"),
    L("docs", "dj-urlresolvers"),
    L("docs", "dj-shortcuts"),
    L("lc", "simplify-path", note="URL/fayl yoʻllarini normallashtirish — router yozishda juda foydali."),
])

# ---------------------------------------------------------------- 13.8
TOPIC("dj-api", "Django bilan API yaratish", "JsonResponse, serializatsiya, POST, status kodlari va sahifalash", 30, r'''
Bugungi ilovalar (mobil, React, Telegram bot) serverdan **HTML emas, JSON** oladi. Django bilan oddiy API yozish juda oson.

```py norun
# kutubxona/views.py
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Kitob


def kitob_json(k):
    return {"id": k.id, "nom": k.nom, "muallif": k.muallif, "narx": k.narx}


def kitoblar(request):                                  # GET /api/kitoblar/
    qs = Kitob.objects.all()
    if janr := request.GET.get("janr"):
        qs = qs.filter(janr=janr)
    return JsonResponse({"natijalar": [kitob_json(k) for k in qs]},
                        json_dumps_params={"ensure_ascii": False})


def kitob(request, pk):                                 # GET /api/kitoblar/5/
    return JsonResponse(kitob_json(get_object_or_404(Kitob, pk=pk)))


@require_http_methods(["POST"])
def kitob_qosh(request):                                # POST /api/kitoblar/yangi/
    data = json.loads(request.body)
    k = Kitob.objects.create(**data)
    return JsonResponse(kitob_json(k), status=201)
```

> `JsonResponse` faqat **lugʻat** qabul qiladi. Roʻyxat yubormoqchi boʻlsangiz: `JsonResponse([...], safe=False)` — yoki yaxshisi, roʻyxatni `{"natijalar": [...]}` ichiga oʻrang.

## Serializatsiya — obyektdan JSON ga
JSON faqat satr, son, `true/false`, `null`, roʻyxat va obyektni biladi. Sana, `Decimal`, model obyektlarini oldin oddiy turlarga aylantirish kerak:

```py
import json
from datetime import date


def serialize(obyekt, maydonlar):
    d = {}
    for m in maydonlar:
        v = obyekt[m]
        d[m] = v.isoformat() if isinstance(v, date) else v
    return d


kitob = {"id": 1, "nom": "Oʻtkan kunlar", "chiqqan": date(1926, 1, 1), "narx": 45000, "ichki_izoh": "maxfiy"}
print(json.dumps(serialize(kitob, ["id", "nom", "chiqqan"]), ensure_ascii=False))
print(json.dumps({"ok": True, "xato": None}))
```

## REST qoidalari
| Metod + URL | Amal | Javob kodi |
|---|---|---|
| `GET /api/kitoblar/` | roʻyxat | 200 |
| `GET /api/kitoblar/5/` | bittasi | 200 yoki 404 |
| `POST /api/kitoblar/` | yaratish | **201** |
| `PATCH /api/kitoblar/5/` | oʻzgartirish | 200 |
| `DELETE /api/kitoblar/5/` | oʻchirish | **204** (tanasiz) |

## Sahifalash (pagination)
Minglab yozuvni bir yoʻla yubormaymiz:

```py
import math

KITOBLAR = list(range(1, 24))    # 23 ta "kitob"


def sahifala(elementlar, sahifa, hajm=10):
    jami = max(1, math.ceil(len(elementlar) / hajm))
    return {
        "count": len(elementlar),
        "next": sahifa + 1 if sahifa < jami else None,
        "previous": sahifa - 1 if sahifa > 1 else None,
        "results": elementlar[(sahifa - 1) * hajm: sahifa * hajm],
    }


print(sahifala(KITOBLAR, 1))
print(sahifala(KITOBLAR, 3))
```

## API ni tekshirish
```py norun
import requests

r = requests.get("http://127.0.0.1:8000/api/kitoblar/", params={"janr": "roman"}, timeout=5)
print(r.status_code, r.json()["natijalar"][:2])

r = requests.post("http://127.0.0.1:8000/api/kitoblar/yangi/",
                  json={"nom": "Yangi kitob", "muallif": "Men", "narx": 1000}, timeout=5)
print(r.status_code)     # 201
```

> Katta loyihalarda **Django REST Framework** (DRF) ishlatiladi: serializer'lar, ruxsatlar, sahifalash va avtomatik hujjat tayyor holda keladi. Bu mavzudagi gʻoyalar — DRF ning aynan poydevori.

!> POST soʻrovlari uchun Django CSRF himoyasini talab qiladi. API uchun token/sessiya autentifikatsiyasidan foydalaning — `@csrf_exempt` ni oʻylamasdan qoʻyish xavfli.
''', [
    P('import json\nprint(json.dumps({"ism": "Oʻtkir"}))', '{"ism": "Oʻtkir"}', "{'ism': 'Oʻtkir'}", "Xato",
      why="Standart holatda `ensure_ascii=True` — ASCII boʻlmagan harflar `\\uXXXX` koʻrinishida yoziladi. Oʻqiladigan JSON uchun `ensure_ascii=False`."),
    P('import json\nprint(json.dumps({"ism": "Oʻtkir"}, ensure_ascii=False))', '{"ism": "O\\u02bbtkir"}', "{'ism': 'Oʻtkir'}", "Xato"),
    P('import json\nprint(json.dumps((1, 2)))', "(1, 2)", '"(1, 2)"', "Xato"),
    P('import json\nprint(json.dumps({"ok": True, "x": None}))', '{"ok": True, "x": None}', "{'ok': True, 'x': None}", "Xato"),
    P("import json\nbody = b'{\"nom\": \"Kitob\", \"narx\": 30000}'\nprint(json.loads(body)[\"narx\"] * 2)", "3000030000", "Xato", "None"),
    P('import math\njami, hajm = 23, 10\nprint(math.ceil(jami / hajm))', "2", "2.3", "Xato"),
    P('from datetime import date\nprint(date(2026, 10, 13).isoformat())', "13.10.2026", "2026/10/13", "Xato", lv=2),
    Q("Django view'dan JSON qaytarishning toʻgʻri usuli?", "`JsonResponse(lugʻat)`", "`HttpResponse(str(lugʻat))`", "`print(json)`", "`render(request, \"x.json\")`"),
    Q("POST bilan yangi resurs muvaffaqiyatli yaratilganda qaysi status kodi qaytariladi?", "201 Created", "200 OK", "204 No Content", "302 Found"),
    F("Serializatsiya", "`serialize(obyekt, maydonlar)` — faqat koʻrsatilgan maydonlardan lugʻat; `date`/`datetime` qiymatlar `.isoformat()` ga, `Decimal` — `str` ga aylantirilsin.",
      "from datetime import date\nfrom decimal import Decimal\n\n\ndef serialize(obyekt, maydonlar):\n    d = {}\n    for m in maydonlar:\n        v = obyekt[m]\n        if isinstance(v, date):\n            v = v.isoformat()\n        elif isinstance(v, Decimal):\n            v = str(v)\n        d[m] = v\n    return d",
      'serialize({"id": 1, "nom": "A", "sana": __import__("datetime").date(2026, 1, 5)}, ["id", "sana"])', 'serialize({"narx": __import__("decimal").Decimal("19.90"), "x": 1}, ["narx"])', 'serialize({"a": None}, [])', lv=2),
    F("JsonResponse", "`json_javob(data, status=200, safe=True)` — `(status, json_matn)` qaytarsin (`ensure_ascii=False`). `safe=True` va `data` lugʻat boʻlmasa — `TypeError(\"Lugʻat boʻlmagan obyekt uchun safe=False bering\")`.",
      "import json\n\n\ndef json_javob(data, status=200, safe=True):\n    if safe and not isinstance(data, dict):\n        raise TypeError('Lugʻat boʻlmagan obyekt uchun safe=False bering')\n    return status, json.dumps(data, ensure_ascii=False)",
      'json_javob({"ism": "Oʻtkir"})', 'json_javob([1, 2], safe=False)', 'json_javob([1, 2])', 'json_javob({"id": 5}, 201)', lv=1),
    F("Sahifalash", "`sahifala(elementlar, sahifa, hajm=10)` — `{\"count\", \"next\", \"previous\", \"results\"}`; `next`/`previous` — sahifa raqami yoki `None`. Sahifa 1 dan kichik yoki oxirgisidan katta boʻlsa — `ValueError(\"Notoʻgʻri sahifa\")` (boʻsh roʻyxatda yagona sahifa — 1).",
      "import math\n\n\ndef sahifala(elementlar, sahifa, hajm=10):\n    jami = max(1, math.ceil(len(elementlar) / hajm))\n    if not 1 <= sahifa <= jami:\n        raise ValueError('Notoʻgʻri sahifa')\n    return {'count': len(elementlar), 'next': sahifa + 1 if sahifa < jami else None,\n            'previous': sahifa - 1 if sahifa > 1 else None, 'results': elementlar[(sahifa - 1) * hajm: sahifa * hajm]}",
      "sahifala(list(range(1, 24)), 3)", "sahifala(list(range(5)), 1, 2)", "sahifala([], 1)", "sahifala([1, 2], 2)", lv=2),
    F("POST tanasini tekshirish", "`qabul(body, majburiy)` — `body` (bytes) JSON boʻlmasa `(400, {\"xato\": \"JSON notoʻgʻri\"})`; majburiy maydonlardan yetishmaganlari boʻlsa `(400, {\"xato\": \"Yetishmaydi: a, b\"})` (berilgan tartibda); hammasi joyida boʻlsa `(201, data)`.",
      "import json\n\n\ndef qabul(body, majburiy):\n    try:\n        data = json.loads(body)\n    except ValueError:\n        return 400, {'xato': 'JSON notoʻgʻri'}\n    yoq = [m for m in majburiy if m not in data]\n    if yoq:\n        return 400, {'xato': 'Yetishmaydi: ' + ', '.join(yoq)}\n    return 201, data",
      "qabul(b'{\"nom\": \"Kitob\", \"narx\": 1000}', [\"nom\", \"narx\"])", "qabul(b'{\"nom\": \"Kitob\"}', [\"nom\", \"narx\", \"muallif\"])", "qabul(b'salom', [\"nom\"])", "qabul(b'{}', [])", lv=2),
    F("Mini REST", "`api(metod, yol, baza)` — `baza`: kitoblar roʻyxati. `GET /api/kitoblar/` → `(200, [id lar])`; `GET /api/kitoblar/<id>/` → `(200, kitob)` yoki `(404, {\"xato\": \"Topilmadi\"})`; `DELETE /api/kitoblar/<id>/` → mavjud boʻlsa `(204, None)`, aks holda 404; boshqasi → `(405, {\"xato\": \"Ruxsat etilmagan\"})`.",
      "import re\n\n\ndef api(metod, yol, baza):\n    if yol == '/api/kitoblar/' and metod == 'GET':\n        return 200, [k['id'] for k in baza]\n    m = re.fullmatch(r'/api/kitoblar/(\\d+)/', yol)\n    if m and metod in ('GET', 'DELETE'):\n        k = next((k for k in baza if k['id'] == int(m.group(1))), None)\n        if k is None:\n            return 404, {'xato': 'Topilmadi'}\n        return (200, k) if metod == 'GET' else (204, None)\n    return 405, {'xato': 'Ruxsat etilmagan'}",
      'api("GET", "/api/kitoblar/", __import__("baza").KITOBLAR)', 'api("GET", "/api/kitoblar/3/", __import__("baza").KITOBLAR)[1]["nom"]', 'api("GET", "/api/kitoblar/9/", __import__("baza").KITOBLAR)',
      'api("DELETE", "/api/kitoblar/1/", __import__("baza").KITOBLAR)', 'api("PUT", "/api/kitoblar/", __import__("baza").KITOBLAR)', lv=3, files=BAZA),
    F("Soʻrov parametrlari", "`royxat(GET, kitoblar)` — `janr` (aniq), `min_narx` va `max_narx` (son, chegaralar kiradi) va `ordering` (`narx`, `-narx`, `yil`, `-yil`) parametrlarini qoʻllab, `id` lar roʻyxatini qaytarsin. `GET` qiymatlari — satrlar!",
      "def royxat(GET, kitoblar):\n    r = list(kitoblar)\n    if 'janr' in GET:\n        r = [k for k in r if k['janr'] == GET['janr']]\n    if 'min_narx' in GET:\n        r = [k for k in r if k['narx'] >= int(GET['min_narx'])]\n    if 'max_narx' in GET:\n        r = [k for k in r if k['narx'] <= int(GET['max_narx'])]\n    if 'ordering' in GET:\n        o = GET['ordering']\n        r.sort(key=lambda k: k[o.lstrip('-')], reverse=o.startswith('-'))\n    return [k['id'] for k in r]",
      'royxat({"janr": "roman", "ordering": "-narx"}, __import__("baza").KITOBLAR)', 'royxat({"min_narx": "35000", "max_narx": "45000"}, __import__("baza").KITOBLAR)', 'royxat({}, __import__("baza").KITOBLAR)', 'royxat({"ordering": "yil"}, __import__("baza").KITOBLAR)', files=BAZA),
    F("ETag", "`etag(data)` — keshlash uchun: `json.dumps(data, sort_keys=True, ensure_ascii=False)` ning UTF-8 baytlaridan `hashlib.md5` olib, `W/\"` + birinchi 12 hex belgi + `\"` qaytarsin. Kalitlar tartibi natijaga taʼsir qilmasin.",
      "import hashlib\nimport json\n\n\ndef etag(data):\n    h = hashlib.md5(json.dumps(data, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()\n    return f'W/\"{h[:12]}\"'",
      'etag({"id": 1, "nom": "A"})', 'etag({"nom": "A", "id": 1}) == etag({"id": 1, "nom": "A"})', 'etag([])', lv=2),
    L("exercism", "rest-api"),
    L("docs", "requests-quickstart"),
    L("lc", "encode-and-decode-tinyurl", note="Qisqa havola xizmati API si — klassik backend masala."),
    L("lc", "time-based-key-value-store", note="Vaqtga bogʻliq kesh — API javoblarini keshlash gʻoyasi."),
])

# ---------------------------------------------------------------- 13.9
TOPIC("dj-deploy", "Deployga tayyorlash va joylash", "DEBUG, SECRET_KEY, ALLOWED_HOSTS, statik fayllar va gunicorn", 25, r'''
Sayt kompyuteringizda ishlayapti — endi uni butun dunyoga chiqaramiz! Lekin avval **xavfsizlik** va **sozlamalarni** tartibga keltirish kerak.

## 1. Sozlamalarni muhitdan oʻqish
Maxfiy narsalar koddan emas, **muhit oʻzgaruvchilaridan** olinadi (12.3-mavzuni eslang):

```py norun
# mysite/settings.py
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]                     # yoʻq boʻlsa — ishga tushmaydi
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h]
CSRF_TRUSTED_ORIGINS = ["https://mirae.uz"]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"                            # collectstatic shu yerga yigʻadi
```

Bitta keng tarqalgan tuzoq:

```py
import os

os.environ["DJANGO_DEBUG"] = "False"
print(bool(os.environ["DJANGO_DEBUG"]))       # ⚠ True! Boʻsh boʻlmagan satr — doim True
print(os.environ["DJANGO_DEBUG"] == "1")      # ✅ toʻgʻri tekshiruv
```

## 2. Kuchli SECRET_KEY
```py
import secrets

kalit = secrets.token_urlsafe(50)
print(len(kalit) >= 50, len(set(kalit)) >= 5, kalit.startswith("django-insecure-"))
```

> Django `check --deploy` kalitni zaif deb hisoblaydi, agar u 50 belgidan qisqa boʻlsa, 5 tadan kam turli belgidan iborat boʻlsa yoki `django-insecure-` bilan boshlansa.

## 3. ALLOWED_HOSTS
Django faqat roʻyxatdagi domenlarga javob beradi. `.mirae.uz` (nuqta bilan) — `mirae.uz` va uning barcha subdomenlari:

```py
def ruxsat(host, allowed):
    host = host.split(":")[0].lower()
    for a in allowed:
        if a == "*" or host == a or (a.startswith(".") and (host.endswith(a) or host == a[1:])):
            return True
    return False


for h in ["mirae.uz", "api.mirae.uz", "mirae.uz:8000", "xaker.com"]:
    print(h, ruxsat(h, [".mirae.uz"]))
```

## 4. Tekshiruv roʻyxati
```bash
pip freeze > requirements.txt
python manage.py check --deploy          # xavfsizlik ogohlantirishlari
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn mysite.wsgi:application --workers 3 --bind 0.0.0.0:8000
```

| Qadam | Nima uchun |
|---|---|
| `DEBUG = False` | xato sahifalari kod va sozlamalarni oshkor qilmasin |
| `SECRET_KEY` muhitdan | kalit Git'ga tushmasin |
| `ALLOWED_HOSTS` | begona domenlar orqali hujumdan himoya |
| `collectstatic` | CSS/JS/rasmlar bitta papkada, server ularni tez beradi |
| `gunicorn` | `runserver` oʻrniga ishonchli production server |
| HTTPS | `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE = True` |

## 5. Qayerga joylash mumkin?
- **PythonAnywhere** — boshlovchilar uchun eng oson, bepul tarifi bor (Django Girls qoʻllanmasida qadamma-qadam).
- **Render, Railway, Fly.io** — Git'dan avtomatik deploy.
- **VPS** (DigitalOcean, Hetzner va h.k.) — Nginx + gunicorn + PostgreSQL, toʻliq nazorat.

> Gunicorn ishchilar soni uchun mashhur formula: `2 × CPU + 1`.

!> `DEBUG = True` bilan production'ga chiqmang! 404 yoki 500 xato sahifasi barcha URL lar, sozlamalar va kod qismlarini hammaga koʻrsatadi.
''', [
    P('import os\nos.environ["DJANGO_DEBUG"] = "False"\nprint(bool(os.environ["DJANGO_DEBUG"]))', "False", "Xato", "None", lv=2,
      why="`bool(\"False\")` — `True`, chunki boʻsh boʻlmagan har qanday satr rost. Muhit oʻzgaruvchisini aniq qiymat bilan solishtiring."),
    P('import os\nos.environ["DJANGO_DEBUG"] = "False"\nprint(os.environ["DJANGO_DEBUG"] == "1")', "True", "Xato", "None"),
    P('hosts = "mirae.uz,www.mirae.uz"\nprint(hosts.split(","))', "['mirae.uz,www.mirae.uz']", "('mirae.uz', 'www.mirae.uz')", "Xato"),
    P('print("api.mirae.uz".endswith(".mirae.uz"), "mirae.uz".endswith(".mirae.uz"))', "True True", "False False", "False True"),
    P('import secrets\nprint(len(secrets.token_urlsafe(50)) >= 50)', "False", "50", "Xato"),
    P('from pathlib import PurePosixPath\nprint(PurePosixPath("/srv/loyiha") / "staticfiles")', "/srv/loyihastaticfiles", "staticfiles", "Xato"),
    P('talablar = "Django==5.2\\ngunicorn==23.0\\n"\nprint([q.split("==")[0] for q in talablar.split()])', "['Django==5.2', 'gunicorn==23.0']", "['5.2', '23.0']", "Xato"),
    Q("Production serverda `DEBUG = True` qoldirilsa nima xavf bor?", "Xato sahifalari kod, sozlamalar va maxfiy maʼlumotlarni koʻrsatib qoʻyadi", "Sayt tezlashadi", "Hech qanday xavf yoʻq", "Faqat CSS ishlamay qoladi"),
    Q("`python manage.py collectstatic` nima qiladi?", "Barcha statik fayllarni (CSS, JS, rasm) `STATIC_ROOT` papkasiga yigʻadi", "Bazani tozalaydi", "Migratsiyalarni yaratadi", "Serverni oʻchiradi"),
    F("Sozlamalar muhitdan", "`sozlamalar(muhit)` — `muhit` lugʻatidan: `DEBUG` (`DJANGO_DEBUG` `\"1\"`, `\"true\"` yoki `\"yes\"` boʻlsa — katta-kichik farqsiz — `True`, yoʻq boʻlsa `False`), `SECRET_KEY` (`DJANGO_SECRET_KEY` yoʻq yoki boʻsh boʻlsa `RuntimeError(\"DJANGO_SECRET_KEY berilmagan\")`), `ALLOWED_HOSTS` (`DJANGO_ALLOWED_HOSTS` vergul bilan, boʻsh joylarsiz, boʻshlari tashlanib).",
      "def sozlamalar(muhit):\n    kalit = muhit.get('DJANGO_SECRET_KEY')\n    if not kalit:\n        raise RuntimeError('DJANGO_SECRET_KEY berilmagan')\n    return {\n        'DEBUG': muhit.get('DJANGO_DEBUG', '').lower() in ('1', 'true', 'yes'),\n        'SECRET_KEY': kalit,\n        'ALLOWED_HOSTS': [h.strip() for h in muhit.get('DJANGO_ALLOWED_HOSTS', '').split(',') if h.strip()],\n    }",
      'sozlamalar({"DJANGO_SECRET_KEY": "abc", "DJANGO_DEBUG": "True", "DJANGO_ALLOWED_HOSTS": "mirae.uz, www.mirae.uz,"})', 'sozlamalar({"DJANGO_SECRET_KEY": "x"})', 'sozlamalar({"DJANGO_DEBUG": "1"})', 'sozlamalar({"DJANGO_SECRET_KEY": "k", "DJANGO_DEBUG": "False"})["DEBUG"]', lv=2),
    F("ALLOWED_HOSTS", "`host_ruxsat(host, allowed)` — Django kabi: port olib tashlansin, katta-kichik farqsiz; `\"*\"` — hammasi; `.domen` — domen va barcha subdomenlari; aks holda aniq moslik.",
      "def host_ruxsat(host, allowed):\n    host = host.split(':')[0].lower()\n    for a in allowed:\n        a = a.lower()\n        if a == '*' or host == a:\n            return True\n        if a.startswith('.') and (host.endswith(a) or host == a[1:]):\n            return True\n    return False",
      'host_ruxsat("api.mirae.uz", [".mirae.uz"])', 'host_ruxsat("MIRAE.uz:8000", [".mirae.uz"])', 'host_ruxsat("xaker.com", ["mirae.uz"])', 'host_ruxsat("istalgan.uz", ["*"])', 'host_ruxsat("notmirae.uz", [".mirae.uz"])'),
    F("SECRET_KEY kuchlimi", "`kalit_kuchli(k)` — Django qoidasi: uzunligi ≥ 50, turli belgilar soni ≥ 5 va `django-insecure-` bilan boshlanmasa — `True`.",
      "def kalit_kuchli(k):\n    return len(k) >= 50 and len(set(k)) >= 5 and not k.startswith('django-insecure-')",
      'kalit_kuchli("a" * 60)', 'kalit_kuchli("django-insecure-" + "x1y2z3w4v5" * 5)', 'kalit_kuchli("k3Y_" * 13)', 'kalit_kuchli("qisqa")', 'kalit_kuchli(__import__("secrets").token_urlsafe(50))', lv=1),
    F("check --deploy", "`tekshir(s)` — sozlamalar lugʻatidan ogohlantirishlar roʻyxati (shu tartibda): `DEBUG` rost → `\"DEBUG yoqilgan\"`; `SECRET_KEY` 50 dan qisqa → `\"SECRET_KEY zaif\"`; `ALLOWED_HOSTS` boʻsh → `\"ALLOWED_HOSTS boʻsh\"`; `SECURE_SSL_REDIRECT` yoʻq yoki yolgʻon → `\"HTTPS yoqilmagan\"`.",
      "def tekshir(s):\n    r = []\n    if s.get('DEBUG'):\n        r.append('DEBUG yoqilgan')\n    if len(s.get('SECRET_KEY', '')) < 50:\n        r.append('SECRET_KEY zaif')\n    if not s.get('ALLOWED_HOSTS'):\n        r.append('ALLOWED_HOSTS boʻsh')\n    if not s.get('SECURE_SSL_REDIRECT'):\n        r.append('HTTPS yoqilmagan')\n    return r",
      'tekshir({"DEBUG": True, "SECRET_KEY": "abc", "ALLOWED_HOSTS": []})', 'tekshir({"DEBUG": False, "SECRET_KEY": "x" * 50, "ALLOWED_HOSTS": ["mirae.uz"], "SECURE_SSL_REDIRECT": True})', "tekshir({})", lv=1),
    F("collectstatic", "`yigish(manbalar)` — `manbalar`: `[(ilova, [fayllar])]` (`INSTALLED_APPS` tartibida). Natija `{fayl: ilova}` — bir xil yoʻlli fayl bir nechta ilovada boʻlsa, **birinchisi** olinadi (Django ham shunday qiladi).",
      "def yigish(manbalar):\n    natija = {}\n    for ilova, fayllar in manbalar:\n        for f in fayllar:\n            natija.setdefault(f, ilova)\n    return natija",
      'yigish([("blog", ["css/style.css", "img/logo.png"]), ("dokon", ["css/style.css", "js/savat.js"])])', "yigish([])", 'yigish([("a", ["x"]), ("b", ["x"])])', lv=2),
    F("gunicorn buyrugʻi", "`gunicorn_buyruq(loyiha, cpu=2, port=8000, ishchilar=None)` — `ishchilar` berilmasa `2 × cpu + 1`; natija: `\"gunicorn LOYIHA.wsgi:application --workers N --bind 0.0.0.0:PORT\"`.",
      "def gunicorn_buyruq(loyiha, cpu=2, port=8000, ishchilar=None):\n    n = ishchilar or 2 * cpu + 1\n    return f'gunicorn {loyiha}.wsgi:application --workers {n} --bind 0.0.0.0:{port}'",
      'gunicorn_buyruq("mysite")', 'gunicorn_buyruq("mirae", cpu=4, port=80)', 'gunicorn_buyruq("x", ishchilar=1)', lv=1),
    F("Qolgan qadamlar", "`qolgan(bajarilgan)` — tartibli tekshiruv roʻyxatidan (`requirements`, `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, `migrate`, `collectstatic`, `gunicorn`) hali bajarilmaganlarini tartib bilan qaytarsin; hammasi bajarilgan boʻlsa — `[\"Tayyor! 🚀\"]`.",
      "def qolgan(bajarilgan):\n    tartib = ['requirements', 'DEBUG=False', 'SECRET_KEY', 'ALLOWED_HOSTS', 'migrate', 'collectstatic', 'gunicorn']\n    r = [q for q in tartib if q not in bajarilgan]\n    return r or ['Tayyor! 🚀']",
      'qolgan({"requirements", "migrate"})', 'qolgan(set())', 'qolgan({"requirements", "DEBUG=False", "SECRET_KEY", "ALLOWED_HOSTS", "migrate", "collectstatic", "gunicorn"})', lv=1),
    L("docs", "dj-deployment"),
    L("docs", "dj-checklist"),
    L("docs", "dj-static"),
    L("docs", "djgirls-deploy"),
])
