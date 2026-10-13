from dsl import TOPIC, P, Q, F, PR, L

# Section 10 continues (SECTION is declared in s10_stdlib.py).

# ---------------------------------------------------------------- 10.9
TOPIC("random", "Tasodifiy qiymatlar (random, secrets)", "Oʻyinlar, test maʼlumotlari va xavfsiz kodlar", 20, r'''
Zar tashlash, viktorina savollarini aralashtirish, test uchun maʼlumot yasash — bularning hammasi **tasodifiy** qiymatlarni talab qiladi.

## Asosiy funksiyalar
```py
import random

random.seed(2026)                     # natija har safar bir xil boʻlishi uchun
print(random.randint(1, 6))           # 1..6 (ikkalasi ham kiradi)
print(random.random())                # 0.0 ≤ x < 1.0
print(random.uniform(10, 20))         # 10..20 orasidagi kasr
print(random.choice(["tosh", "qaychi", "qogʻoz"]))
```

> `random.seed(n)` — "urugʻ". Bir xil urugʻ → bir xil ketma-ketlik. Testlar va oʻyin qayta koʻrish (replay) uchun juda foydali.

## Roʻyxatlar bilan
```py
import random

random.seed(7)
savollar = ["Q1", "Q2", "Q3", "Q4", "Q5"]
random.shuffle(savollar)              # joyida aralashtiradi
print(savollar)
print(random.sample(range(1, 50), 6))         # 6 ta takrorlanmas son
print(random.choices(["A", "B"], weights=[9, 1], k=10))   # ogʻirlik bilan
```

| Funksiya | Nima qiladi |
|---|---|
| `randint(a, b)` | a..b butun son |
| `choice(seq)` | bitta element |
| `choices(seq, k=n)` | n ta (takrorlanishi mumkin) |
| `sample(seq, n)` | n ta takrorlanmas |
| `shuffle(lst)` | joyida aralashtirish |

## Amaliy: parol generatori
```py
import random
import string

random.seed(1)
belgilar = string.ascii_letters + string.digits
parol = "".join(random.choice(belgilar) for _ in range(10))
print(parol, len(parol))
```

## Xavfsizlik uchun — secrets
!> `random` — oʻyin va simulyatsiya uchun. **Parol, token, tasdiqlash kodi** uchun `secrets` modulini ishlating: uning natijasini oldindan taxmin qilib boʻlmaydi.

```py
import secrets

kod = "".join(secrets.choice("0123456789") for _ in range(6))
print(len(kod), kod.isdigit())
token = secrets.token_hex(16)
print(len(token))
```

> Mirae Academy faollashtirish kodi ham aynan shunday — kriptografik xavfsiz tasodif bilan yaratiladi.

## Esda tuting
- `random.seed()` — takrorlanadigan natija.
- Pul, parol, kod — faqat `secrets`.
''', [
    P('import random\nrandom.seed(5)\na = random.random()\nrandom.seed(5)\nprint(a == random.random())', "False", "0.5", "Xato"),
    P('import random\nx = random.randint(1, 1)\nprint(x)', "0", "Xato", "2"),
    P('import random\nr = [1, 2, 3]\nprint(random.shuffle(r))', "[3, 1, 2]", "[1, 2, 3]", "Xato", lv=2,
      why="`shuffle` roʻyxatni joyida aralashtiradi va `None` qaytaradi."),
    P('import random\nprint(len(random.sample(range(100), 5)), len(set(random.sample(range(10), 10))))', "5 5", "10 10", "5 1"),
    P('import random\nprint(random.sample([1, 2], 3))', "[1, 2, 1]", "[1, 2]", "[]"),
    P('import secrets\nprint(len(secrets.token_hex(8)))', "8", "4", "32"),
    P('import random\nrandom.seed(0)\nprint(all(0 <= random.random() < 1 for _ in range(1000)))', "False", "1000", "Xato"),
    Q("Parol yoki tasdiqlash kodi uchun qaysi modul toʻgʻri?", "secrets", "random", "math", "time"),
    Q("`random.sample(royxat, k)` ning `random.choices` dan farqi?", "sample elementlarni takrorlamaydi", "sample tezroq", "choices faqat bitta element beradi", "Farqi yoʻq"),
    F("Zar", "`zarlar(n, urug)` — urugʻ bilan n ta zar tashlab (1..6), yigʻindisini qaytarsin.",
      "import random\n\n\ndef zarlar(n, urug):\n    random.seed(urug)\n    return sum(random.randint(1, 6) for _ in range(n))",
      "zarlar(3, 1) == zarlar(3, 1)", "zarlar(0, 5)", "3 <= zarlar(3, 42) <= 18", "zarlar(100, 7) == zarlar(100, 7)", lv=1),
    F("Viktorina", "`aralash(savollar, urug)` — roʻyxat nusxasini urugʻ bilan aralashtirib qaytarsin (asl roʻyxat oʻzgarmasin).",
      "import random\n\n\ndef aralash(savollar, urug):\n    r = list(savollar)\n    random.Random(urug).shuffle(r)\n    return r",
      "sorted(aralash([3, 1, 2], 9))", "aralash([], 1)", "(a := [1, 2, 3, 4], aralash(a, 5), a)[-1]", "aralash([1, 2, 3, 4, 5], 3) == aralash([1, 2, 3, 4, 5], 3)"),
    F("Lotereya", "`lotereya(urug)` — 1..49 orasidan 6 ta takrorlanmas sonni (`sample`) saralangan holda qaytarsin.",
      "import random\n\n\ndef lotereya(urug):\n    return sorted(random.Random(urug).sample(range(1, 50), 6))",
      "len(lotereya(1))", "len(set(lotereya(2)))", "all(1 <= x <= 49 for x in lotereya(3))", "lotereya(4) == sorted(lotereya(4))"),
    F("Parol", "`parol(uzunlik)` — `secrets` bilan harf va raqamlardan iborat parol yasasin; unda kamida bitta raqam va bitta harf boʻlsin (boʻlmasa qayta yasang).",
      "import secrets\nimport string\n\n\ndef parol(uzunlik):\n    belgilar = string.ascii_letters + string.digits\n    while True:\n        p = ''.join(secrets.choice(belgilar) for _ in range(uzunlik))\n        if any(c.isdigit() for c in p) and any(c.isalpha() for c in p):\n            return p",
      "len(parol(12))", "parol(8).isalnum()", "any(c.isdigit() for c in parol(6))", "parol(10) != parol(10)", lv=2),
    F("Monte-Karlo", "`pi_taxmin(n, urug)` — kvadratga n ta tasodifiy nuqta tashlab, aylana ichiga tushganlar ulushi orqali π ni taxmin qilsin: `4 * ichida / n` (2 xona).",
      "import random\n\n\ndef pi_taxmin(n, urug):\n    r = random.Random(urug)\n    ichida = sum(1 for _ in range(n) if r.random() ** 2 + r.random() ** 2 <= 1)\n    return round(4 * ichida / n, 2)",
      "3.0 < pi_taxmin(20000, 1) < 3.3", "pi_taxmin(1000, 5) == pi_taxmin(1000, 5)", "type(pi_taxmin(10, 1)).__name__", lv=3),
    F("Ogʻirlikli tanlov", "`sovga(urug, n)` — `choices` bilan n ta sovgʻa tanlansin: `\"konfet\"` (70), `\"kitob\"` (25), `\"planshet\"` (5). Har biri necha marta tushganini lugʻatda qaytarsin (faqat tushganlari, alifbo boʻyicha).",
      "import random\n\n\ndef sovga(urug, n):\n    r = random.Random(urug)\n    t = r.choices(['konfet', 'kitob', 'planshet'], weights=[70, 25, 5], k=n)\n    return {k: t.count(k) for k in sorted(set(t))}",
      "sum(sovga(1, 100).values())", "sovga(2, 1000)['konfet'] > sovga(2, 1000)['kitob']", "sovga(3, 0)", lv=2),
    F("Tasdiqlash kodi", "`kod(n)` — `secrets` bilan n xonali raqamli kod (nollardan boshlanishi mumkin) satr qaytarsin.",
      "import secrets\n\n\ndef kod(n):\n    return ''.join(secrets.choice('0123456789') for _ in range(n))",
      "len(kod(6))", "kod(6).isdigit()", "kod(0)"),
    L("docs", "py-random"),
    L("docs", "py-secrets"),
    L("exercism", "robot-name"),
    L("lc", "shuffle-an-array"),
])

# ---------------------------------------------------------------- 10.10
TOPIC("brauzer-email", "Brauzerni ochish va email yuborish", "webbrowser, smtplib va email.message", 20, r'''
Python boshqa dasturlar va xizmatlar bilan ham ishlay oladi: brauzerda sahifa ochish, email yuborish.

## Brauzerni ochish
```py norun
import webbrowser

webbrowser.open("https://docs.python.org/3/")          # standart brauzerda
webbrowser.open_new_tab("https://mirae.uz")
```

> Bu funksiya sizning kompyuteringizdagi brauzerni ishga tushiradi, shuning uchun bu yerda (ilova ichida) emas, oʻz kompyuteringizdagi Python'da sinab koʻring.

URL ni toʻgʻri yasash uchun `urllib.parse` qulay:

```py
from urllib.parse import urlencode, quote

soz = "python darslari oʻzbekcha"
url = "https://www.google.com/search?" + urlencode({"q": soz})
print(url)
print(quote("salom dunyo"))
```

## Email xabar yasash
`email.message.EmailMessage` — xabarning toʻgʻri formatini (sarlavhalar, kodlash, ilovalar) oʻzi tuzadi:

```py
from email.message import EmailMessage

xabar = EmailMessage()
xabar["From"] = "ustoz@mirae.uz"
xabar["To"] = "madina@example.com"
xabar["Subject"] = "Imtihon natijasi"
xabar.set_content("Salom, Madina!\n\nSiz 2-boʻlim imtihonidan 92% oldingiz. Tabriklaymiz!")

print(xabar["Subject"])
print(xabar["To"])
print(xabar.get_content().splitlines()[0])
```

## Fayl ilova qilish
```py
from email.message import EmailMessage

x = EmailMessage()
x["Subject"] = "Hisobot"
x.set_content("Hisobot ilova qilindi.")
x.add_attachment("ism,ball\nAli,85\n".encode(), maintype="text", subtype="csv", filename="baholar.csv")

print(x.is_multipart())
print([q.get_filename() for q in x.iter_attachments()])
```

## smtplib bilan yuborish
```py norun
import smtplib
import os
from email.message import EmailMessage

x = EmailMessage()
x["From"] = "siz@gmail.com"
x["To"] = "dost@example.com"
x["Subject"] = "Salom"
x.set_content("Python orqali yuborildi!")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()                                   # shifrlash
    server.login("siz@gmail.com", os.environ["EMAIL_PAROL"])
    server.send_message(x)
```

!> Parolni hech qachon kod ichiga yozmang! Uni **muhit oʻzgaruvchisi**da saqlang (12-boʻlim: API kalitlarini yashirish). Gmail uchun oddiy parol emas, "App password" kerak boʻladi.

| Port | Usul |
|---|---|
| 587 | `SMTP` + `starttls()` |
| 465 | `SMTP_SSL` |

## Esda tuting
- `webbrowser.open(url)` — sahifani foydalanuvchi brauzerida ochadi.
- Email: `EmailMessage` bilan yasang, `smtplib` bilan yuboring, parolni koddan tashqarida saqlang.
''', [
    P('from urllib.parse import urlencode\nprint(urlencode({"q": "a b", "n": 2}))', "q=a b&n=2", "{'q': 'a b'}", "q=a%20b&n=2"),
    P('from urllib.parse import quote\nprint(quote("a/b c"))', "a%2Fb%20c", "a/b c", "a/b+c"),
    P('from email.message import EmailMessage\nx = EmailMessage()\nx["Subject"] = "Salom"\nprint(x["Subject"], x["To"])', "Salom", "Salom ''", "Xato"),
    P('from email.message import EmailMessage\nx = EmailMessage()\nx.set_content("Bir\\nIkki")\nprint(x.get_content().count("\\n"))', "1", "0", "Xato"),
    P('from email.message import EmailMessage\nx = EmailMessage()\nx.set_content("a")\nprint(x.is_multipart())', "True", "a", "Xato"),
    P('from urllib.parse import urlparse\nu = urlparse("https://mirae.uz/darslar?id=5")\nprint(u.netloc, u.path, u.query)', "https mirae.uz id=5", "mirae.uz darslar 5", "Xato"),
    P('from urllib.parse import parse_qs\nprint(parse_qs("a=1&b=2&a=3"))', "{'a': '3', 'b': '2'}", "{'a': 1, 'b': 2}", "[('a', '1'), ('b', '2'), ('a', '3')]", lv=2),
    Q("Email parolini qayerda saqlash kerak?", "Muhit oʻzgaruvchisida (yoki maxfiy sozlamalar faylida), kod ichida emas", "Kodning birinchi qatorida", "GitHub'dagi README faylida", "Fayl nomida"),
    Q("587-port bilan ishlaganda ulanishni shifrlash uchun qaysi metod chaqiriladi?", "starttls()", "encrypt()", "secure()", "ssl()"),
    F("Qidiruv havolasi", "`qidiruv(soz)` — `https://www.google.com/search?q=...` havolasini `urlencode` bilan yasasin.",
      "from urllib.parse import urlencode\n\n\ndef qidiruv(soz):\n    return 'https://www.google.com/search?' + urlencode({'q': soz})",
      'qidiruv("python")', 'qidiruv("oʻzbek tili")', 'qidiruv("a&b=c")', lv=1),
    F("Havolani tahlil", "`tahlil(url)` — `(domen, yoʻl, {parametr: qiymat})` qaytarsin (parametr qiymatlari — oxirgi uchragan).",
      "from urllib.parse import urlparse, parse_qsl\n\n\ndef tahlil(url):\n    u = urlparse(url)\n    return (u.netloc, u.path, dict(parse_qsl(u.query)))",
      'tahlil("https://mirae.uz/dars?id=5&til=uz")', 'tahlil("http://localhost:8000/")', 'tahlil("https://a.uz/x?k=1&k=2")'),
    F("Xabar yasash", "`xabar(kimga, mavzu, matn)` — `EmailMessage` yasab, `(To, Subject, birinchi_qator)` kortejini qaytarsin.",
      "from email.message import EmailMessage\n\n\ndef xabar(kimga, mavzu, matn):\n    x = EmailMessage()\n    x['To'] = kimga\n    x['Subject'] = mavzu\n    x.set_content(matn)\n    return (x['To'], x['Subject'], x.get_content().splitlines()[0])",
      'xabar("a@b.uz", "Salom", "Birinchi\\nIkkinchi")', 'xabar("x@y.z", "Imtihon", "Natija: 92%")'
      , 'xabar("m@m.uz", "", ".")'),
    F("Ommaviy xat", "`xatlar(talabalar)` — `[(ism, email, ball)]` uchun shaxsiy xabarlar yasab, har biri uchun `\"EMAIL: Salom, ISM! Ballingiz: BALL\"` satrini (xabarning `To` va matnidan) qaytarsin.",
      "from email.message import EmailMessage\n\n\ndef xatlar(talabalar):\n    natija = []\n    for ism, email, ball in talabalar:\n        x = EmailMessage()\n        x['To'] = email\n        x.set_content(f'Salom, {ism}! Ballingiz: {ball}')\n        natija.append(f\"{x['To']}: {x.get_content().strip()}\")\n    return natija",
      'xatlar([("Ali", "ali@m.uz", 85), ("Madina", "madina@m.uz", 92)])', "xatlar([])", 'xatlar([("X", "x@x", 0)])', lv=2),
    F("Ilova", "`ilovali(fayl_nomi, matn)` — xabarga matnni `text/plain` ilova qilib, ilovalar nomlari roʻyxati va `is_multipart()` ni kortejda qaytarsin.",
      "from email.message import EmailMessage\n\n\ndef ilovali(fayl_nomi, matn):\n    x = EmailMessage()\n    x.set_content('Ilova bor')\n    x.add_attachment(matn.encode(), maintype='text', subtype='plain', filename=fayl_nomi)\n    return ([a.get_filename() for a in x.iter_attachments()], x.is_multipart())",
      'ilovali("hisobot.txt", "salom")', 'ilovali("a.txt", "")', 'ilovali("b.txt", "x")[0]', lv=2),
    F("Email tekshiruvi", "`togri_email(s)` — `email.utils.parseaddr` bilan manzilni ajratib, unda bitta `@` va nuqtali domen boʻlsa `True`.",
      "from email.utils import parseaddr\n\n\ndef togri_email(s):\n    _, manzil = parseaddr(s)\n    if manzil.count('@') != 1:\n        return False\n    nom, domen = manzil.split('@')\n    return bool(nom) and '.' in domen and not domen.startswith('.') and not domen.endswith('.')",
      'togri_email("ali@mirae.uz")', 'togri_email("Ali Valiyev <ali@mirae.uz>")', 'togri_email("ali@mirae")', 'togri_email("@mirae.uz")', 'togri_email("a@b@c.uz")', lv=3),
    F("SMTP sozlamasi", "`smtp_sozlama(xizmat)` — `{\"gmail\": (\"smtp.gmail.com\", 587), \"yandex\": (\"smtp.yandex.ru\", 465), \"mail\": (\"smtp.mail.ru\", 465)}` dan qaytarsin; nomaʼlum xizmat — `ValueError`.",
      "def smtp_sozlama(xizmat):\n    s = {'gmail': ('smtp.gmail.com', 587), 'yandex': ('smtp.yandex.ru', 465), 'mail': ('smtp.mail.ru', 465)}\n    if xizmat not in s:\n        raise ValueError('nomaʼlum xizmat')\n    return s[xizmat]",
      'smtp_sozlama("gmail")', 'smtp_sozlama("yandex")', 'smtp_sozlama("x")', lv=1),
    L("docs", "py-webbrowser"),
    L("docs", "py-email-examples"),
    L("docs", "py-smtplib"),
    L("docs", "py-urllib-parse"),
])

# ---------------------------------------------------------------- 10.11
TOPIC("shablonlar", "Shablonlar (Template)", "Matn qoliplari: string.Template, format va f-satr", 15, r'''
Sertifikat, chek, SMS xabar, email — hammasi **shablon** asosida yasaladi: matnning bir qismi oʻzgarmas, bir qismi har safar boshqacha.

## string.Template
```py
from string import Template

t = Template("Hurmatli $ism! Siz $kurs kursini ${ball}% natija bilan tugatdingiz.")
print(t.substitute(ism="Madina", kurs="Python", ball=92))
```

- `$nom` yoki `${nom}` — oʻrin egallovchi;
- `$$` — oddiy `$` belgisi.

## substitute va safe_substitute
```py
from string import Template

t = Template("Narx: $narx soʻm, chegirma: $chegirma")
print(t.safe_substitute(narx=12000))        # yoʻq qiymat oʻz holicha qoladi
try:
    t.substitute(narx=12000)
except KeyError as e:
    print("KeyError:", e)
```

## Nega Template, f-satr emas?
| Usul | Qachon |
|---|---|
| f-satr `f"{ism}"` | kod ichida, qiymatlar shu yerda maʼlum |
| `"{ism}".format(...)` | shablon oldindan tayyor, keyin toʻldiriladi |
| `Template("$ism")` | shablonni **foydalanuvchi** yoki fayl beradi — xavfsiz |

!> Foydalanuvchi yozgan shablonga `.format()` yoki `eval` ishlatmang — u obyekt atributlariga kirib, maxfiy maʼlumotni chiqarishi mumkin. `Template` faqat oddiy almashtirish qiladi.

## Fayldan shablon
```py
from string import Template
from pathlib import Path

Path("sertifikat.txt").write_text(
    "SERTIFIKAT\n$ism\n«$kurs» kursini muvaffaqiyatli tugatdi.\nSana: $sana\n", encoding="utf-8")

shablon = Template(Path("sertifikat.txt").read_text(encoding="utf-8"))
for ism in ["Ali Valiyev", "Madina Karimova"]:
    print(shablon.substitute(ism=ism, kurs="Python asoslari", sana="13.10.2026"))
```

## format bilan jadval-shablon
```py
qator = "{nom:<10}{soni:>4}{narx:>10,}"
for n, s, p in [("Non", 2, 8000), ("Sut", 1, 12000), ("Choy", 3, 75000)]:
    print(qator.format(nom=n, soni=s, narx=p))
```

## Esda tuting
- `Template("$x").substitute(x=1)` — xavfsiz, oddiy shablon.
- `safe_substitute` — yetishmagan qiymatda xato bermaydi.
''', [
    P('from string import Template\nprint(Template("$a+$b").substitute(a=1, b=2))', "3", "$a+$b", "a+b"),
    P('from string import Template\nprint(Template("${x}yz").substitute(x="ab"))', "${x}yz", "x yz", "Xato"),
    P('from string import Template\nprint(Template("$x va $y").safe_substitute(x=1))', "1 va", "1 va None", "⚠ KeyError"),
    P('from string import Template\nprint(Template("Narx: $$5").substitute())', "Narx: $$5", "Narx: 5", "⚠ KeyError"),
    P('from string import Template\nTemplate("$ism").substitute(nom="Ali")', "Ali", "$ism", "⚠ ValueError"),
    P('print("{0}-{1}-{0}".format("a", "b"))', "a-b-c", "{0}-{1}-{0}", "Xato"),
    P('print("{x:>5}|".format(x=42))', "42   |", "42|", "Xato", lv=2),
    Q("Foydalanuvchi bergan shablon uchun eng xavfsiz usul?", "string.Template", "eval", "f-satr ichida input()", "exec"),
    Q("`safe_substitute` ning `substitute` dan farqi?", "Yetishmagan qiymat boʻlsa xato bermaydi, oʻrin egallovchini qoldiradi", "Tezroq ishlaydi", "Raqamlarni formatlaydi", "Farqi yoʻq"),
    F("Salomlashuv", "`salom(ism, soat)` — `Template(\"$salom, $ism!\")` bilan: soat < 12 → `Xayrli tong`, < 18 → `Xayrli kun`, aks holda `Xayrli kech`.",
      "from string import Template\n\n\ndef salom(ism, soat):\n    s = 'Xayrli tong' if soat < 12 else 'Xayrli kun' if soat < 18 else 'Xayrli kech'\n    return Template('$salom, $ism!').substitute(salom=s, ism=ism)",
      'salom("Ali", 9)', 'salom("Madina", 15)', 'salom("Bek", 21)', lv=1),
    F("Sertifikatlar", "`sertifikatlar(shablon, odamlar)` — har bir `{\"ism\":…, \"ball\":…}` uchun shablonni toʻldirib roʻyxat qaytarsin.",
      "from string import Template\n\n\ndef sertifikatlar(shablon, odamlar):\n    t = Template(shablon)\n    return [t.substitute(o) for o in odamlar]",
      'sertifikatlar("$ism — $ball ball", [{"ism": "Ali", "ball": 85}, {"ism": "Vali", "ball": 90}])', 'sertifikatlar("x", [])', 'sertifikatlar("${ism}ga", [{"ism": "Madina", "ball": 1}])'),
    F("Xavfsiz toʻldirish", "`toldir(shablon, qiymatlar)` — `safe_substitute` bilan toʻldirib, natijada qolgan `$nom` oʻrinlar sonini ham qaytarsin: `(matn, qolgan)`.",
      "import re\nfrom string import Template\n\n\ndef toldir(shablon, qiymatlar):\n    m = Template(shablon).safe_substitute(qiymatlar)\n    return (m, len(re.findall(r'\\$\\{?[A-Za-z_]\\w*\\}?', m)))",
      'toldir("$a va $b", {"a": 1})', 'toldir("$a", {"a": "x"})', 'toldir("${x}${y}${z}", {})', lv=2),
    F("Chek", "`chek(narsalar)` — `[(nom, soni, narx)]` dan `\"{:<8}{:>3}{:>9}\"` formatidagi qatorlar va oxirida `JAMI` qatori (`\"{:<11}{:>9}\"`) — hammasini `\\n` bilan birlashtirgan satr.",
      "def chek(narsalar):\n    q = ['{:<8}{:>3}{:>9}'.format(n, s, s * p) for n, s, p in narsalar]\n    q.append('{:<11}{:>9}'.format('JAMI', sum(s * p for _, s, p in narsalar)))\n    return '\\n'.join(q)",
      'chek([("Non", 2, 4000), ("Sut", 1, 12000)])', "chek([])", 'chek([("Choy", 3, 25000)])', lv=2),
    F("SMS shablon", "`sms(shablon, **q)` — `Template` bilan toʻldirsin, natija 160 belgidan oshsa, 157 belgigacha qisqartirib `\"...\"` qoʻshsin.",
      "from string import Template\n\n\ndef sms(shablon, **q):\n    m = Template(shablon).substitute(**q)\n    return m if len(m) <= 160 else m[:157] + '...'",
      'sms("Kodingiz: $kod", kod="482913")', 'len(sms("$x", x="a" * 200))', 'sms("$x", x="a" * 200)[-3:]', 'sms("Salom $ism", ism="Ali")'),
    F("Oʻzgaruvchilar roʻyxati", "`kalitlar(shablon)` — `Template(...).get_identifiers()` bilan shablondagi oʻrin egallovchilar nomlarini (takrorsiz, kelish tartibida) qaytarsin.",
      "from string import Template\n\n\ndef kalitlar(shablon):\n    return Template(shablon).get_identifiers()",
      'kalitlar("$ism, $yosh, ${ism}")', 'kalitlar("oddiy matn")', 'kalitlar("$$5 va $narx")', lv=2),
    F("HTML kartochka", "`kartochka(ism, kasb)` — `Template` bilan `<div class=\"karta\"><h3>$ism</h3><p>$kasb</p></div>` ni toʻldirsin; qiymatlardagi `<`, `>`, `&` larni `html.escape` bilan xavfsiz qilsin.",
      "import html\nfrom string import Template\n\n\ndef kartochka(ism, kasb):\n    t = Template('<div class=\"karta\"><h3>$ism</h3><p>$kasb</p></div>')\n    return t.substitute(ism=html.escape(ism), kasb=html.escape(kasb))",
      'kartochka("Ali", "Dasturchi")', 'kartochka("<script>", "A & B")', 'kartochka("", "")', lv=3),
    L("docs", "py-string"),
    L("exercism", "two-fer"),
    L("exercism", "proverb"),
    L("exercism", "twelve-days", note="Takrorlanuvchi qoʻshiq — shablon bilan juda qisqa yechiladi."),
])

# ---------------------------------------------------------------- 10.12
TOPIC("argparse", "Buyruq satri argumentlari", "sys.argv va argparse bilan CLI dasturlar", 20, r'''
Professional dasturlar koʻpincha terminaldan parametrlar bilan ishga tushiriladi:

```bash
python hisob.py --summa 1000000 --foiz 18 --yil 3
python resize.py rasm.jpg --kenglik 800
git commit -m "xabar"
```

## sys.argv
Eng oddiy usul — `sys.argv` roʻyxati: `[0]` — dastur nomi, keyingilari — argumentlar (hammasi satr):

```py
import sys

sys.argv = ["salom.py", "Madina", "3"]     # terminaldagi: python salom.py Madina 3
ism = sys.argv[1]
marta = int(sys.argv[2])
for _ in range(marta):
    print(f"Salom, {ism}!")
```

> Bu ilova ichida terminal yoʻq, shuning uchun `sys.argv` ni qoʻlda beramiz. Oʻz kompyuteringizda shunchaki `python salom.py Madina 3` yozasiz.

## argparse — qulay va professional
```py
import argparse

parser = argparse.ArgumentParser(description="Kredit kalkulyatori")
parser.add_argument("summa", type=int, help="kredit summasi (soʻm)")
parser.add_argument("--foiz", type=float, default=20, help="yillik foiz")
parser.add_argument("--oy", type=int, default=12)
parser.add_argument("-v", "--batafsil", action="store_true")

args = parser.parse_args(["12000000", "--foiz", "24", "-v"])
print(args)
jami = args.summa * (1 + args.foiz / 100)
print(f"Oylik toʻlov: {jami / args.oy:,.0f} soʻm")
if args.batafsil:
    print(f"Jami: {jami:,.0f}")
```

| Yozuv | Turi |
|---|---|
| `add_argument("nom")` | majburiy (pozitsion) |
| `add_argument("--nom")` | ixtiyoriy (bayroqli) |
| `type=int` | turni avtomatik aylantirish |
| `default=...` | standart qiymat |
| `action="store_true"` | bayroq: bor/yoʻq |
| `choices=[...]` | ruxsat etilgan qiymatlar |

## Avtomatik yordam (--help)
```py
import argparse

p = argparse.ArgumentParser(prog="rasm", description="Rasm oʻlchamini oʻzgartiradi")
p.add_argument("fayl")
p.add_argument("--kenglik", type=int, default=800)
p.print_help()
```

## Notoʻgʻri kiritish
```py
import argparse

p = argparse.ArgumentParser(prog="hisob")
p.add_argument("--yil", type=int, choices=[1, 2, 3])
try:
    p.parse_args(["--yil", "besh"])
except SystemExit:
    print("argparse xato xabarini chiqarib, dasturni toʻxtatdi")
```

## Esda tuting
- `sys.argv` — xom roʻyxat; `argparse` — turlar, standartlar, yordam va xatolar avtomatik.
- `--help` hech qanday qoʻshimcha koddan bepul keladi.
''', [
    P('import sys\nsys.argv = ["a.py", "5", "7"]\nprint(sys.argv[1] + sys.argv[2])', "12", "a.py57", "Xato"),
    P('import sys\nsys.argv = ["a.py"]\nprint(len(sys.argv) - 1)', "1", "0 a.py", "Xato"),
    P('import argparse\np = argparse.ArgumentParser()\np.add_argument("n", type=int)\nprint(p.parse_args(["5"]).n * 2)', "55", "n", "Xato"),
    P('import argparse\np = argparse.ArgumentParser()\np.add_argument("--rang", default="qizil")\nprint(p.parse_args([]).rang)', "None", "--rang", "Xato"),
    P('import argparse\np = argparse.ArgumentParser()\np.add_argument("-v", action="store_true")\nprint(p.parse_args([]).v, p.parse_args(["-v"]).v)', "None True", "True True", "Xato"),
    P('import argparse\np = argparse.ArgumentParser()\np.add_argument("--tez-rejim", action="store_true")\nprint(p.parse_args(["--tez-rejim"]).tez_rejim)', "⚠ AttributeError", "tez-rejim", "None", lv=2,
      why="Argument nomidagi `-` atributda `_` ga aylanadi: `--tez-rejim` → `args.tez_rejim`."),
    P('import argparse\np = argparse.ArgumentParser()\np.add_argument("sonlar", type=int, nargs="+")\nprint(sum(p.parse_args(["1", "2", "3"]).sonlar))', "123", "['1', '2', '3']", "Xato"),
    Q("`action=\"store_true\"` nima qiladi?", "Bayroq berilsa True, berilmasa False", "Qiymatni faylga saqlaydi", "Argumentni majburiy qiladi", "Qiymatni satrga aylantiradi"),
    Q("`sys.argv[0]` da nima boʻladi?", "Ishga tushirilgan dastur (skript) nomi", "Birinchi argument", "Python versiyasi", "Argumentlar soni"),
    F("Oddiy CLI", "`hisobla(argv)` — `argv` roʻyxatida `[dastur, a, amal, b]`; amal `+ - x /` boʻlishi mumkin. Natijani qaytarsin.",
      "def hisobla(argv):\n    a, amal, b = float(argv[1]), argv[2], float(argv[3])\n    return {'+': a + b, '-': a - b, 'x': a * b, '/': a / b}[amal]",
      'hisobla(["k.py", "6", "x", "7"])', 'hisobla(["k.py", "10", "/", "4"])', 'hisobla(["k.py", "1", "-", "5"])', lv=1),
    F("argparse bilan", "`parse(argv)` — `ism` (majburiy), `--yosh` (int, standart 18), `--katta` (store_true) argumentlarini tahlil qilib, `(ism, yosh, katta)` qaytarsin.",
      "import argparse\n\n\ndef parse(argv):\n    p = argparse.ArgumentParser()\n    p.add_argument('ism')\n    p.add_argument('--yosh', type=int, default=18)\n    p.add_argument('--katta', action='store_true')\n    a = p.parse_args(argv)\n    return (a.ism, a.yosh, a.katta)",
      'parse(["Ali"])', 'parse(["Madina", "--yosh", "16", "--katta"])', 'parse(["--katta", "Bek"])'),
    F("Bir nechta qiymat", "`statistika(argv)` — `sonlar` (int, `nargs=\"+\"`) va `--amal` (`choices=[\"yigindi\", \"ortacha\", \"maks\"]`, standart `yigindi`).",
      "import argparse\n\n\ndef statistika(argv):\n    p = argparse.ArgumentParser()\n    p.add_argument('sonlar', type=int, nargs='+')\n    p.add_argument('--amal', choices=['yigindi', 'ortacha', 'maks'], default='yigindi')\n    a = p.parse_args(argv)\n    if a.amal == 'yigindi':\n        return sum(a.sonlar)\n    if a.amal == 'ortacha':\n        return sum(a.sonlar) / len(a.sonlar)\n    return max(a.sonlar)",
      'statistika(["1", "2", "3"])', 'statistika(["4", "8", "--amal", "ortacha"])', 'statistika(["--amal", "maks", "5", "9", "2"])', lv=2),
    F("Xato ushlash", "`xavfsiz(argv)` — `--yil` (int, `choices=[1, 2, 3]`) ni tahlil qilsin; notoʻgʻri boʻlsa (`SystemExit`) `\"xato\"` qaytarsin, aks holda yilni. argparse xato matnini chiqarmasin (`io.StringIO` + `contextlib.redirect_stderr`).",
      "import argparse\nimport contextlib\nimport io\n\n\ndef xavfsiz(argv):\n    p = argparse.ArgumentParser()\n    p.add_argument('--yil', type=int, choices=[1, 2, 3])\n    try:\n        with contextlib.redirect_stderr(io.StringIO()):\n            return p.parse_args(argv).yil\n    except SystemExit:\n        return 'xato'",
      'xavfsiz(["--yil", "2"])', 'xavfsiz(["--yil", "5"])', 'xavfsiz(["--yil", "bir"])', "xavfsiz([])", lv=3),
    F("Yordam matni", "`yordam()` — `prog=\"rasm\"`, `fayl` va `--kenglik` (int) argumentli parser yasab, `format_usage()` natijasini (oxirgi `\\n` siz) qaytarsin.",
      "import argparse\n\n\ndef yordam():\n    p = argparse.ArgumentParser(prog='rasm')\n    p.add_argument('fayl')\n    p.add_argument('--kenglik', type=int)\n    return p.format_usage().strip()",
      "yordam()", "yordam().startswith('usage')", "'fayl' in yordam()"),
    F("Kalit=qiymat", "`kv(argv)` — `[\"til=uz\", \"tema=dark\"]` kabi argumentlardan lugʻat yasasin; `=` siz argument boʻlsa `ValueError`.",
      "def kv(argv):\n    d = {}\n    for a in argv:\n        if '=' not in a:\n            raise ValueError(a)\n        k, v = a.split('=', 1)\n        d[k] = v\n    return d",
      'kv(["til=uz", "tema=dark"])', "kv([])", 'kv(["url=a=b"])', 'kv(["xato"])'),
    F("Kichik komanda", "`ishlat(argv)` — `argparse` subparsers bilan ikki buyruq: `qosh a b` → yigʻindi, `salom ism [--marta N]` → `\"Salom, ISM!\"` N marta boʻsh joy bilan (standart 1).",
      "import argparse\n\n\ndef ishlat(argv):\n    p = argparse.ArgumentParser()\n    sub = p.add_subparsers(dest='buyruq', required=True)\n    q = sub.add_parser('qosh')\n    q.add_argument('a', type=int)\n    q.add_argument('b', type=int)\n    s = sub.add_parser('salom')\n    s.add_argument('ism')\n    s.add_argument('--marta', type=int, default=1)\n    a = p.parse_args(argv)\n    if a.buyruq == 'qosh':\n        return a.a + a.b\n    return ' '.join([f'Salom, {a.ism}!'] * a.marta)",
      'ishlat(["qosh", "2", "3"])', 'ishlat(["salom", "Ali"])', 'ishlat(["salom", "Vali", "--marta", "2"])', lv=3),
    L("docs", "py-argparse-howto"),
    L("docs", "py-argparse"),
    L("docs", "py-sys"),
    L("exercism", "grep", note="Haqiqiy CLI bayroqlari (-n, -i, -l…) bilan ishlash."),
])

# ---------------------------------------------------------------- 10.13
TOPIC("subprocess", "Tashqi dasturlarni ishga tushirish", "subprocess, shlex va os.environ", 15, r'''
Python boshqa dasturlarni ham boshqara oladi: `git`, `ffmpeg`, `ping`, boshqa skriptlar. Buning uchun **`subprocess`** moduli ishlatiladi.

```py norun
import subprocess

natija = subprocess.run(["python", "--version"], capture_output=True, text=True)
print(natija.returncode)       # 0 — muvaffaqiyatli
print(natija.stdout.strip())   # Python 3.14.2

r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd="loyiha")
for qator in r.stdout.splitlines():
    print(qator)
```

> Bu ilova ichida tashqi dasturlar yoʻq (Python brauzer muhitida ishlaydi), shuning uchun yuqoridagi kodni oʻz kompyuteringizda sinang. Quyidagi misollar esa shu yerda ishlaydi.

## Muhim parametrlar
| Parametr | Maʼnosi |
|---|---|
| `capture_output=True` | chiqishni ushlash (`stdout`, `stderr`) |
| `text=True` | baytlar emas, satrlar |
| `check=True` | xato kodi boʻlsa `CalledProcessError` |
| `timeout=10` | 10 soniyadan oshsa toʻxtatish |
| `cwd="papka"` | qaysi papkada ishga tushirish |

## Buyruqni roʻyxat qilib bering
!> `subprocess.run("rm -rf " + papka, shell=True)` — **xavfli**: `papka` ichida `; boshqa_buyruq` boʻlsa, u ham bajariladi (command injection). Buyruqni **roʻyxat** qilib bering va `shell=True` dan qoching.

Satrni xavfsiz roʻyxatga ajratish — `shlex.split`:

```py
import shlex

buyruq = 'ffmpeg -i "mening video.mp4" -vf scale=640:-1 natija.mp4'
print(shlex.split(buyruq))
print(shlex.quote("fayl; rm -rf /"))      # xavfsiz qoʻshtirnoq
print(shlex.join(["echo", "salom dunyo"]))
```

## Muhit oʻzgaruvchilari
Tashqi dasturlar sozlamalarni koʻpincha **muhit oʻzgaruvchilari**dan oladi:

```py
import os

os.environ["MIRAE_REJIM"] = "test"
print(os.environ.get("MIRAE_REJIM"))
print(os.environ.get("YOQ_OZGARUVCHI", "standart"))
print(os.getenv("MIRAE_REJIM") == "test")
```

## Qaytish kodi (return code)
```py norun
import subprocess

try:
    subprocess.run(["git", "push"], check=True, timeout=60)
except subprocess.CalledProcessError as e:
    print("Buyruq xato bilan tugadi, kod:", e.returncode)
except subprocess.TimeoutExpired:
    print("Juda uzoq davom etdi")
```

> `0` — muvaffaqiyat, boshqa son — xato. Bu qoida deyarli barcha buyruqlar uchun bir xil.

## Esda tuting
- `subprocess.run([...], capture_output=True, text=True)` — eng koʻp ishlatiladigan shakl.
- `shell=True` va satr birlashtirish — xavfli; roʻyxat + `shlex`.
''', [
    P('import shlex\nprint(shlex.split("a b c"))', "a b c", "('a', 'b', 'c')", "['a b c']"),
    P('import shlex\nprint(shlex.split(\'cp "mening fayl.txt" zaxira/\'))', "['cp', '\"mening', 'fayl.txt\"', 'zaxira/']", "['cp \"mening fayl.txt\" zaxira/']", "Xato"),
    P('import shlex\nprint(shlex.join(["echo", "a b"]))', "echo a b", 'echo "a b"', "['echo', 'a b']"),
    P('import shlex\nprint(shlex.quote("salom"))', "'salom'", '"salom"', "Xato"),
    P('import os\nos.environ["X_TEST"] = "5"\nprint(os.environ["X_TEST"] * 2)', "10", "5", "Xato"),
    P('import os\nprint(os.getenv("YOQ_MIRAE_123", "yoʻq"))', "None", "⚠ KeyError", "YOQ_MIRAE_123"),
    P('import os\nos.environ["N"] = 5', "5", "None", "⚠ ValueError", lv=2),
    Q("Nega `shell=True` va satrlarni qoʻshib buyruq yasash xavfli?", "Foydalanuvchi kiritgan matn orqali qoʻshimcha buyruq bajarilishi mumkin (command injection)", "Buyruq sekin ishlaydi", "Natija chiqmaydi", "Python ruxsat bermaydi"),
    Q("Tashqi buyruqning qaytish kodi `0` boʻlsa bu nimani bildiradi?", "Muvaffaqiyatli tugadi", "Xato yuz berdi", "Buyruq topilmadi", "Vaqt tugadi"),
    F("Buyruqni ajratish", "`ajrat(buyruq)` — `shlex.split` bilan satrni roʻyxatga ajratsin.",
      "import shlex\n\n\ndef ajrat(buyruq):\n    return shlex.split(buyruq)",
      'ajrat("git commit -m \\"birinchi commit\\"")', 'ajrat("ls")', "ajrat(\"echo 'a b' c\")", lv=1),
    F("Xavfsiz buyruq", "`xavfsiz(fayl)` — `[\"cat\", fayl]` ni `shlex.join` bilan bitta xavfsiz satrga aylantirsin.",
      "import shlex\n\n\ndef xavfsiz(fayl):\n    return shlex.join(['cat', fayl])",
      'xavfsiz("eslatma.txt")', 'xavfsiz("mening fayl.txt")', 'xavfsiz("x; rm -rf /")'),
    F("Muhitdan sozlama", "`sozlama(nom, standart)` — `os.environ` dan qiymat olsin; qiymat `\"1\"`, `\"true\"`, `\"ha\"` (katta-kichik farqsiz) boʻlsa `True`, `\"0\"`, `\"false\"`, `\"yoq\"` boʻlsa `False`, boshqa qiymat — oʻzi, yoʻq boʻlsa — standart.",
      "import os\n\n\ndef sozlama(nom, standart):\n    v = os.environ.get(nom)\n    if v is None:\n        return standart\n    if v.lower() in ('1', 'true', 'ha'):\n        return True\n    if v.lower() in ('0', 'false', 'yoq'):\n        return False\n    return v",
      '(__import__("os").environ.__setitem__("MIRAE_DEBUG", "TRUE"), sozlama("MIRAE_DEBUG", False))[-1]',
      '(__import__("os").environ.__setitem__("MIRAE_TIL", "uz"), sozlama("MIRAE_TIL", "en"))[-1]',
      'sozlama("MIRAE_YOQ_456", 42)', '(__import__("os").environ.__setitem__("MIRAE_X", "yoq"), sozlama("MIRAE_X", True))[-1]', lv=2),
    F("Natija tahlili", "`tahlil(returncode, stdout)` — tashqi buyruq natijasidan `{\"ok\": bool, \"qatorlar\": N, \"birinchi\": birinchi qator yoki None}` qaytarsin.",
      "def tahlil(returncode, stdout):\n    q = stdout.splitlines()\n    return {'ok': returncode == 0, 'qatorlar': len(q), 'birinchi': q[0] if q else None}",
      'tahlil(0, "Python 3.14.2\\n")', 'tahlil(1, "")', 'tahlil(0, " M main.py\\n?? yangi.py\\n")'),
    F("git status", "`ozgarishlar(chiqish)` — `git status --short` chiqishidan `{\"M\": [...], \"??\": [...], ...}` lugʻatini (holat kodi → fayllar, kelish tartibida) yasasin.",
      "def ozgarishlar(chiqish):\n    d = {}\n    for q in chiqish.splitlines():\n        if q.strip():\n            kod, fayl = q[:2].strip(), q[3:]\n            d.setdefault(kod, []).append(fayl)\n    return d",
      'ozgarishlar(" M main.py\\n?? yangi.py\\n M util.py\\nA  qoshildi.py\\n")', 'ozgarishlar("")', 'ozgarishlar("?? a b.txt\\n")', lv=3),
    F("Injeksiyani aniqlash", "`shubhali(argument)` — argumentda `;`, `&&`, `|`, `` ` ``, `$(` dan biri boʻlsa `True`.",
      "def shubhali(argument):\n    return any(x in argument for x in [';', '&&', '|', '`', '$('])",
      'shubhali("rasm.jpg")', 'shubhali("a.txt; rm -rf /")', 'shubhali("$(whoami)")', 'shubhali("x | y")'),
    F("Buyruq yasovchi", "`ffmpeg_buyruq(kirish, kenglik, chiqish)` — `[\"ffmpeg\", \"-i\", kirish, \"-vf\", f\"scale={kenglik}:-1\", chiqish]` roʻyxatini qaytarsin; kenglik musbat butun son boʻlmasa `ValueError`.",
      "def ffmpeg_buyruq(kirish, kenglik, chiqish):\n    if not isinstance(kenglik, int) or kenglik <= 0:\n        raise ValueError('kenglik notoʻgʻri')\n    return ['ffmpeg', '-i', kirish, '-vf', f'scale={kenglik}:-1', chiqish]",
      'ffmpeg_buyruq("video.mp4", 640, "kichik.mp4")', 'ffmpeg_buyruq("a b.mov", 1280, "c.mp4")[2]', 'ffmpeg_buyruq("x", -5, "y")', lv=1),
    L("docs", "py-subprocess"),
    L("docs", "py-os", title="os.environ — muhit oʻzgaruvchilari"),
    L("exercism", "grep"),
    L("lc", "simplify-path"),
])

# ---------------------------------------------------------------- 10.14
TOPIC("math", "Math moduli", "Ildiz, daraja, yaxlitlash, trigonometriya va statistika", 15, r'''
Oddiy `+ - * /` dan tashqari hisoblar uchun `math` moduli bor.

## Asosiy funksiyalar
```py
import math

print(math.sqrt(144), math.isqrt(150))      # ildiz va butun ildiz
print(math.pow(2, 10), 2 ** 10)
print(math.floor(3.7), math.ceil(3.2), math.trunc(-3.7))
print(math.fabs(-5), abs(-5))
print(math.pi, math.e)
```

## Yaxlitlash turlari
| Funksiya | 3.7 | -3.7 |
|---|---|---|
| `math.floor` (pastga) | 3 | -4 |
| `math.ceil` (yuqoriga) | 4 | -3 |
| `math.trunc` (nolga) | 3 | -3 |
| `round` (eng yaqin) | 4 | -4 |

> `round(2.5)` → `2`, `round(3.5)` → `4`: Python "bank yaxlitlash"ini ishlatadi — teng holatda juft songa.

## Butun sonlar
```py
import math

print(math.gcd(48, 18), math.lcm(4, 6))
print(math.factorial(10))
print(math.comb(5, 2), math.perm(5, 2))     # kombinatsiya va oʻrinlashtirish
print(math.prod([1, 2, 3, 4]))
```

## Trigonometriya va logarifm
```py
import math

print(round(math.sin(math.pi / 6), 4))
print(math.degrees(math.pi), math.radians(180))
print(math.log10(1000), math.log2(1024), round(math.log(math.e), 2))
print(math.hypot(3, 4))                     # gipotenuza
print(math.dist((0, 0), (6, 8)))            # ikki nuqta masofasi
```

## Float bilan ehtiyot
```py
import math

print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.inf > 10 ** 100, math.isnan(float("nan")))
```

## statistics moduli
```py
import statistics as st

ballar = [85, 92, 78, 92, 60, 74]
print(st.mean(ballar), st.median(ballar), st.mode(ballar))
print(round(st.stdev(ballar), 2))
```

## Esda tuting
- `floor`/`ceil`/`trunc`/`round` — har xil yaxlitlash.
- Kasrlarni solishtirishda `==` emas, `math.isclose`.
''', [
    P('import math\nprint(math.floor(-2.5), math.ceil(-2.5))', "-2 -3", "-2.5 -2.5", "-3 -3"),
    P('print(round(2.5), round(3.5))', "3 4", "2 3", "3 3", lv=2, why="Python teng holatda juft songa yaxlitlaydi (banker's rounding)."),
    P('import math\nprint(math.isqrt(99))', "9.9498", "10", "99"),
    P('import math\nprint(math.comb(4, 2))', "12", "8", "24"),
    P('import math\nprint(math.gcd(0, 7), math.lcm(3, 5))', "0 15", "1 8", "7 8"),
    P('import math\nprint(math.sqrt(-1))', "1j", "-1", "nan"),
    P('import math\nprint(math.hypot(5, 12), math.dist((1, 1), (4, 5)))', "13 5", "17.0 7.0", "Xato"),
    Q("Kasr sonlarni solishtirishning toʻgʻri usuli?", "math.isclose(a, b)", "a == b", "a is b", "round(a) == round(b)"),
    Q("Avtobuslar sonini hisoblashda (100 yoʻlovchi, 30 oʻrin) qaysi funksiya mos?", "math.ceil(100 / 30)", "math.floor(100 / 30)", "round(100 / 30)", "math.trunc(100 / 30)"),
    F("Avtobuslar", "`avtobus(yolovchi, sigim)` — kerakli avtobuslar soni (`math.ceil`).",
      "import math\n\n\ndef avtobus(yolovchi, sigim):\n    return math.ceil(yolovchi / sigim)",
      "avtobus(100, 30)", "avtobus(60, 30)", "avtobus(0, 30)", "avtobus(1, 50)", lv=1),
    F("Kombinatorika", "`jamoalar(n, k)` — n kishidan k kishilik jamoa necha xil usulda tuzilishi mumkin (`math.comb`)? `tartibli(n, k)` — tartib muhim boʻlsa (`math.perm`).",
      "import math\n\n\ndef jamoalar(n, k):\n    return math.comb(n, k)\n\n\ndef tartibli(n, k):\n    return math.perm(n, k)",
      "jamoalar(5, 2)", "tartibli(5, 2)", "jamoalar(30, 3)", "tartibli(3, 3)"),
    F("Uchburchak", "`uchburchak(a, b, c)` — Geron formulasi bilan yuzani 2 xonagacha yaxlitlab qaytarsin; uchburchak mavjud boʻlmasa `ValueError`.",
      "import math\n\n\ndef uchburchak(a, b, c):\n    if a + b <= c or a + c <= b or b + c <= a:\n        raise ValueError('uchburchak emas')\n    p = (a + b + c) / 2\n    return round(math.sqrt(p * (p - a) * (p - b) * (p - c)), 2)",
      "uchburchak(3, 4, 5)", "uchburchak(5, 5, 5)", "uchburchak(1, 2, 3)", lv=2),
    F("Burchak", "`burchak(x, y)` — nuqtaning OX oʻqiga nisbatan burchagini gradusda (`math.atan2`, `math.degrees`, 1 xona) qaytarsin.",
      "import math\n\n\ndef burchak(x, y):\n    return round(math.degrees(math.atan2(y, x)), 1)",
      "burchak(1, 1)", "burchak(0, 5)", "burchak(-1, 0)", "burchak(3, -3)", lv=2),
    F("Statistika", "`tahlil(sonlar)` — `{\"ortacha\", \"mediana\", \"moda\", \"stdev\"}` (ortacha va stdev 2 xona) — `statistics` moduli bilan.",
      "import statistics as st\n\n\ndef tahlil(sonlar):\n    return {'ortacha': round(st.mean(sonlar), 2), 'mediana': st.median(sonlar), 'moda': st.mode(sonlar), 'stdev': round(st.stdev(sonlar), 2)}",
      "tahlil([85, 92, 78, 92, 60, 74])", "tahlil([1, 1, 2])", "tahlil([5, 5])['stdev']", lv=2,
      hint="`statistics.mean`, `median`, `mode`, `stdev`."),
    F("Murakkab foiz", "`omonat(summa, foiz, yil)` — har yili foiz qoʻshiladigan omonat: `summa * (1 + foiz/100) ** yil`, `math.floor` bilan butun soʻmgacha.",
      "import math\n\n\ndef omonat(summa, foiz, yil):\n    return math.floor(summa * (1 + foiz / 100) ** yil)",
      "omonat(1000000, 20, 3)", "omonat(5000000, 0, 10)", "omonat(100, 100, 5)"),
    F("Tub sonlar", "`tublar(n)` — n gacha (n kiradi) tub sonlar roʻyxati; tekshiruvda `math.isqrt` dan foydalaning.",
      "import math\n\n\ndef tublar(n):\n    return [x for x in range(2, n + 1) if all(x % d for d in range(2, math.isqrt(x) + 1))]",
      "tublar(30)", "tublar(1)", "len(tublar(1000))", lv=2),
    L("docs", "py-math"),
    L("exercism", "armstrong-numbers"),
    L("lc", "sqrtx"),
    L("exercism", "perfect-numbers"),
])

# ---------------------------------------------------------------- 10.15
TOPIC("regex", "Muntazam ifodalar (RegEx)", "re moduli: qidirish, ajratib olish va almashtirish", 30, r'''
**Muntazam ifoda** (regular expression, regex) — matndagi **naqshni** tasvirlash tili. Telefon raqamlarini topish, email tekshirish, loglardan sanalarni ajratib olish — regex bilan bir qatorda.

```py
import re

matn = "Ali: +998 90 123 45 67, Vali: +998 91 765 43 21"
print(re.findall(r"\+998 \d{2} \d{3} \d{2} \d{2}", matn))
```

> Regex naqshlarini doim **r"..."** (raw string) ichida yozing — teskari chiziqlar oʻz holicha qoladi.

## Asosiy belgilar
| Naqsh | Maʼnosi |
|---|---|
| `\d` | raqam (0–9) |
| `\w` | harf, raqam yoki `_` |
| `\s` | boʻsh joy |
| `.` | istalgan belgi (yangi qatordan tashqari) |
| `[abc]`, `[a-z]` | toʻplamdagi bitta belgi |
| `^`, `$` | satr boshi, oxiri |
| `*`, `+`, `?` | 0+, 1+, 0 yoki 1 marta |
| `{3}`, `{2,4}` | aniq 3, 2 dan 4 gacha |
| `( )` | guruh — ajratib olish |
| `\|` | yoki |

## Asosiy funksiyalar
```py
import re

print(re.search(r"\d+", "Narx: 12500 soʻm").group())     # birinchi moslik
print(re.findall(r"\d+", "3 olma, 12 nok, 7 uzum"))       # hammasi
print(re.fullmatch(r"\d{4}", "2026") is not None)          # butun satr mosmi
print(re.sub(r"\s+", " ", "juda    koʻp     boʻsh   joy"))  # almashtirish
print(re.split(r"[,;]\s*", "olma, nok;uzum;  anor"))      # ajratish
```

## Guruhlar — maʼlumotni ajratib olish
```py
import re

log = "2026-10-13 09:15:02 ERROR Toʻlov tizimi javob bermadi"
m = re.match(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.*)", log)
yil, oy, kun, vaqt, daraja, xabar = m.groups()
print(kun, oy, yil, "|", daraja, "|", xabar)
```

Nomli guruhlar yanada aniq:

```py
import re

m = re.search(r"(?P<ism>\w+)@(?P<domen>[\w.]+)", "Murojaat: info@mirae.uz")
print(m.group("ism"), m.group("domen"))
print(m.groupdict())
```

## Amaliy: email va telefon tekshiruvi
```py
import re

EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
for e in ["ali@mirae.uz", "ali@mirae", "ali.valiyev+kurs@gmail.com", "@x.uz"]:
    print(f"{e:<28}", bool(EMAIL.match(e)))
```

> `re.compile` — naqsh koʻp marta ishlatilsa, uni bir marta kompilyatsiya qilish samaraliroq.

## Bayroqlar
```py
import re

print(re.findall(r"python", "Python PYTHON python", flags=re.IGNORECASE))
print(re.findall(r"^\w+", "birinchi qator\nikkinchi qator", flags=re.MULTILINE))
```

## Esda tuting
- `search` — birinchi moslik, `findall` — hammasi, `fullmatch` — butun satr, `sub` — almashtirish.
- Guruhlar `( )` va nomli guruhlar `(?P<nom>...)` — maʼlumotni ajratib olish uchun.
''', [
    P('import re\nprint(re.findall(r"\\d", "a1b22c333"))', "['1', '22', '333']", "['122333']", "6"),
    P('import re\nprint(re.findall(r"\\d+", "a1b22c333"))', "['1', '2', '2', '3', '3', '3']", "[1, 22, 333]", "3"),
    P('import re\nprint(re.sub(r"[aeiou]", "*", "salom"))', "s*l*m*", "*a*o*", "salom"),
    P('import re\nm = re.search(r"(\\w+)@(\\w+)", "x: ali@mirae")\nprint(m.group(2), m.group(0))', "ali mirae", "mirae mirae", "Xato"),
    P('import re\nprint(bool(re.match(r"\\d+", "abc123")), bool(re.search(r"\\d+", "abc123")))', "True True", "False False", "True False"),
    P('import re\nprint(re.fullmatch(r"\\d{3}", "1234"))', "123", "True", "⚠ ValueError"),
    P('import re\nprint(re.split(r"\\s*,\\s*", "a , b,c ,  d"))', "['a , b,c ,  d']", "['a', ' b', 'c ', '  d']", "['a', 'b', 'c']"),
    Q("`re.search` va `re.match` farqi?", "match faqat satr boshidan tekshiradi, search istalgan joydan", "Farqi yoʻq", "search faqat raqamlarni topadi", "match barcha mosliklarni qaytaradi"),
    Q("Regex naqshlarini nega `r\"...\"` ichida yozish kerak?", "Teskari chiziqlar (\\d, \\w) Python tomonidan oʻzgartirilmasligi uchun", "Tezroq ishlashi uchun", "Faqat r bilan regex ishlaydi", "Katta-kichik harf farqlanmasligi uchun"),
    F("Raqamlar", "`sonlar(matn)` — matndagi barcha butun sonlarni (manfiylari bilan) `int` roʻyxat qilib qaytarsin.",
      "import re\n\n\ndef sonlar(matn):\n    return [int(x) for x in re.findall(r'-?\\d+', matn)]",
      'sonlar("Harorat -5, ertaga 12, keyin 0")', 'sonlar("raqam yoʻq")', 'sonlar("a1b22c-333")', lv=1),
    F("Email", "`email_togri(s)` — `^[\\w.+-]+@[\\w-]+(\\.[\\w-]+)+$` naqshi bilan tekshirsin.",
      "import re\n\n\ndef email_togri(s):\n    return re.fullmatch(r'[\\w.+-]+@[\\w-]+(\\.[\\w-]+)+', s) is not None",
      'email_togri("ali@mirae.uz")', 'email_togri("ali@mirae")', 'email_togri("ali.v+kurs@gmail.com")', 'email_togri("a b@c.uz")', lv=1),
    F("Telefon", "`telefonlar(matn)` — `+998 XX XXX XX XX` (boʻsh joylar yoki tirelar bilan yoki ularsiz) raqamlarni topib, `+998XXXXXXXXX` koʻrinishiga keltirib qaytarsin.",
      "import re\n\n\ndef telefonlar(matn):\n    t = re.findall(r'\\+998[\\s-]?\\d{2}[\\s-]?\\d{3}[\\s-]?\\d{2}[\\s-]?\\d{2}', matn)\n    return [re.sub(r'[\\s-]', '', x) for x in t]",
      'telefonlar("Ali: +998 90 123 45 67, Vali: +998-91-765-43-21, Bek: +998935554433")', 'telefonlar("raqam yoʻq")', 'telefonlar("+998 90 12")', lv=2),
    F("Log tahlili", "`xatolar(log)` — har qatori `YYYY-MM-DD HH:MM:SS DARAJA xabar` boʻlgan logdan `ERROR` qatorlarining `(vaqt, xabar)` juftliklarini qaytarsin.",
      "import re\n\n\ndef xatolar(log):\n    return re.findall(r'^\\d{4}-\\d{2}-\\d{2} (\\d{2}:\\d{2}:\\d{2}) ERROR (.*)$', log, flags=re.M)",
      'xatolar("2026-10-13 09:15:02 ERROR Toʻlov xatosi\\n2026-10-13 09:16:00 INFO ok\\n2026-10-13 10:00:00 ERROR Baza uzildi")', 'xatolar("")', 'xatolar("2026-01-01 00:00:00 WARN x")', lv=2),
    F("Sanalarni almashtirish", "`formatla(matn)` — matndagi barcha `YYYY-MM-DD` sanalarni `DD.MM.YYYY` ga almashtirsin (`re.sub` va guruhlar).",
      "import re\n\n\ndef formatla(matn):\n    return re.sub(r'(\\d{4})-(\\d{2})-(\\d{2})', r'\\3.\\2.\\1', matn)",
      'formatla("Imtihon 2026-12-25 da, natija 2027-01-05 da")', 'formatla("sana yoʻq")', 'formatla("2026-10-13")'),
    F("Kuchli parol", "`kuchli(p)` — kamida 8 belgi, kamida bitta katta harf, kichik harf, raqam va maxsus belgi (`[^\\w\\s]`) boʻlsa `True` (har bir shart uchun alohida `re.search`).",
      "import re\n\n\ndef kuchli(p):\n    return (len(p) >= 8 and re.search(r'[A-Z]', p) is not None and re.search(r'[a-z]', p) is not None\n            and re.search(r'\\d', p) is not None and re.search(r'[^\\w\\s]', p) is not None)",
      'kuchli("Mirae2026!")', 'kuchli("mirae2026")', 'kuchli("M!r4e")', 'kuchli("SALOM123#")', lv=2),
    F("Nomli guruhlar", "`chek_tahlili(qator)` — `\"Non x2 = 8000\"` koʻrinishidagi qatordan `{\"nom\": ..., \"soni\": int, \"summa\": int}` ni nomli guruhlar bilan qaytarsin; mos kelmasa `None`.",
      "import re\n\n\ndef chek_tahlili(qator):\n    m = re.fullmatch(r'(?P<nom>\\w+) x(?P<soni>\\d+) = (?P<summa>\\d+)', qator.strip())\n    if not m:\n        return None\n    d = m.groupdict()\n    return {'nom': d['nom'], 'soni': int(d['soni']), 'summa': int(d['summa'])}",
      'chek_tahlili("Non x2 = 8000")', 'chek_tahlili("  Sut x1 = 12000 ")', 'chek_tahlili("notoʻgʻri qator")', lv=3),
    L("docs", "py-regex-howto"),
    L("exercism", "acronym"),
    L("exercism", "phone-number"),
    L("lc", "validate-ip-address"),
])
