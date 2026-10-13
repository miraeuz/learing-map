"""Builds src/data/course.json from the course files and verifies everything.

Every lesson code block and every exercise is executed with real Python:
  - "what does this print" answers are computed, never typed by hand;
  - every reference solution must pass its own tests;
  - every starter template must FAIL the tests (so a blank submission never passes);
  - every online problem must exist in a verified source list.
Run: python3 content/build.py
"""
import contextlib
import hashlib
import html
import importlib
import json
import os
import random
import re
import runpy
import signal
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import dsl  # noqa: E402
from sources.judges import ACMP, CSES  # noqa: E402

COURSE_FILES = [
    "s2_asoslar", "s3_operatorlar", "s4_oqim", "s5_funksiyalar", "s6_tuzilmalar", "s6b_tuzilmalar", "s7_istisnolar",
    "s8_oop", "s9_modullar", "s10_stdlib", "s10b_stdlib", "s11_paketlar", "s12_paketlar", "s13_django",
]
EX_PER_TOPIC = 20

H = runpy.run_path(os.path.join(ROOT, "public", "harness.py"))
EXERCISM = json.load(open(os.path.join(HERE, "sources", "exercism.json"), encoding="utf-8"))
LC = json.load(open(os.path.join(HERE, "sources", "leetcode.json"), encoding="utf-8"))
LC_SLUGS = set(LC["slugs"])
DOCS = json.load(open(os.path.join(HERE, "sources", "docs.json"), encoding="utf-8"))

errors = []


class Timeout(Exception):
    pass


@contextlib.contextmanager
def time_limit(sec):
    def handler(signum, frame):
        raise Timeout()
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(sec)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def run(code, stdin="", files=None):
    with time_limit(5):
        r = json.loads(H["run_program"](code, stdin, json.dumps(files or [])))
    return r["stdout"], r["error"]


def shown_output(code, stdin=""):
    out, err = run(code, stdin)
    if err:
        out = out + ("" if out.endswith("\n") or not out else "\n") + f"⚠ {err['type']}"
    return out.rstrip("\n")


# ---------- inline + lesson markdown ----------
def inline(text):
    """Escape HTML, then `code` and **bold**. Code spans are protected so `**kwargs` or `2 ** n` stay intact."""
    s = html.escape(text.strip(), quote=False)
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def parse_lesson(body, where):
    blocks = []
    lines = body.strip("\n").split("\n")
    i = 0
    para = []

    pending_files = []

    def flush():
        if para:
            blocks.append({"t": "p", "html": inline(" ".join(x.strip() for x in para))})
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush()
            info = s[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            src = "\n".join(code)
            lang = (info.split() or ["py"])[0]
            mfile = re.search(r"file=(\S+)", info)
            if mfile:
                # A helper file shown as a tab next to the following runnable block.
                pending_files.append({"name": mfile.group(1), "code": src})
                continue
            if lang not in ("py", "python"):
                blocks.append({"t": "code", "code": src, "stdin": "", "norun": True, "lang": lang, "files": []})
                continue
            norun = "norun" in info
            m = re.search(r'input="([^"]*)"', info) or re.search(r"input=(.*)$", info)
            stdin = m.group(1).replace("|", "\n") + "\n" if m else ""
            files, pending_files[:] = list(pending_files), []
            blk = {"t": "code", "code": src, "stdin": stdin, "norun": norun, "lang": "py", "files": files}
            if not norun:
                try:
                    out, err = run(src, stdin, files)
                except Timeout:
                    errors.append(f"{where}: lesson code timed out:\n{src}")
                    out, err = "", None
                blk["out"] = out.rstrip("\n")
                blk["err"] = err
                if err and "xato" not in info:
                    errors.append(f"{where}: lesson code raised {err['type']} (mark ```py xato if intended):\n{src}")
            blocks.append(blk)
            continue
        if not s:
            flush()
        elif s.startswith("## "):
            flush()
            blocks.append({"t": "h", "text": s[3:].strip()})
        elif s.startswith("!> "):
            flush()
            blocks.append({"t": "warn", "html": inline(s[3:])})
        elif s.startswith("> "):
            flush()
            blocks.append({"t": "tip", "html": inline(s[2:])})
        elif s.startswith("- "):
            flush()
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(inline(lines[i].strip()[2:]))
                i += 1
            blocks.append({"t": "ul", "items": items})
            continue
        elif s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append([inline(c) for c in cells])
                i += 1
            blocks.append({"t": "table", "rows": rows})
            continue
        else:
            para.append(s)
        i += 1
    flush()
    if pending_files:
        errors.append(f"{where}: file= block(s) not followed by a runnable code block")
    return blocks


# ---------- exercises ----------
def seeded_shuffle(items, key):
    rnd = random.Random(int(hashlib.sha1(key.encode()).hexdigest()[:12], 16))
    order = list(range(len(items)))
    rnd.shuffle(order)
    return [items[k] for k in order], order.index(0)


def build_predict(e, eid):
    try:
        ans = shown_output(e["code"])
    except Timeout:
        errors.append(f"{eid}: predict code timed out")
        ans = ""
    opts = [ans] + [w.strip("\n") for w in e["wrong"]]
    if len(e["wrong"]) < 2:
        errors.append(f"{eid}: predict needs at least 2 wrong options")
    if len(set(opts)) != len(opts):
        errors.append(f"{eid}: an option equals the real output or repeats ({opts!r})")
    shuffled, answer = seeded_shuffle(opts, eid)
    return {"kind": "quiz", "q": inline(e["q"] or "Bu kod nima chiqaradi?"), "code": e["code"], "options": shuffled,
            "answer": answer, "mono": True, "why": inline(e["why"]) if e["why"] else None, "lv": e["lv"]}


def build_concept(e, eid):
    opts = [e["right"]] + e["wrong"]
    if len(set(opts)) != len(opts) or len(e["wrong"]) < 2:
        errors.append(f"{eid}: concept options invalid {opts!r}")
    shuffled, answer = seeded_shuffle(opts, eid)
    mono = all(len(o) < 40 and re.search(r"[()\[\]=+\-*/%<>'\"]|^\w+$", o) for o in opts)
    return {"kind": "quiz", "q": inline(e["q"]), "code": e["code"], "options": [o for o in shuffled], "answer": answer,
            "mono": bool(mono), "why": inline(e["why"]) if e["why"] else None, "lv": e["lv"]}


def func_name(sol):
    m = re.search(r"^(?:def|class) (\w+)\b", sol, re.M)
    return m.group(1) if m else None


def skeleton(sol):
    """Starter code: keep class/def headers (and decorators), replace every body with a placeholder."""
    lines = sol.split("\n")
    out = []

    def indent(ln):
        return len(ln) - len(ln.lstrip())

    imports = [ln for ln in lines if ln.startswith(("import ", "from "))]
    in_def = None  # indent of the def whose body we are skipping
    for i, ln in enumerate(lines):
        st = ln.lstrip()
        if in_def is not None and st and indent(ln) > in_def:
            continue  # inside a function body: helpers there are the student's job
        if st:
            in_def = None
        is_head = st.startswith(("class ", "def ")) and st.rstrip().endswith(":")
        is_deco = st.startswith("@")
        if not (is_head or is_deco):
            continue
        prev_deco = out and out[-1].lstrip().startswith("@")
        if not prev_deco and out and out[-1].strip() and not out[-1].rstrip().endswith(":"):
            if not indent(ln):
                out.append("")
            out.append("")
        out.append(ln)
        if is_deco:
            continue
        ind = " " * indent(ln)
        if st.startswith("def "):
            out += [ind + "    # Kodingizni shu yerga yozing", ind + "    pass"]
            in_def = indent(ln)
        else:
            body = []
            for l in lines[i + 1:]:
                if l.strip() and indent(l) <= indent(ln):
                    break
                body.append(l)
            if not any(l.lstrip().startswith("def ") for l in body):
                out.append(ind + "    pass")
    if imports:
        out = imports + ["", ""] + out
    return "\n".join(out) + "\n"


def build_func(e, eid):
    sol = e["solution"]
    name = func_name(sol)
    if not name:
        errors.append(f"{eid}: solution has no def/class")
        return None
    tests = []
    # One sequential run so stateful tasks (global counters etc.) get consistent expectations.
    files = json.dumps(e.get("files") or [])
    res = json.loads(H["check_function"](sol, json.dumps([{"call": c, "expect": "None"} for c in e["calls"]]), files))
    if res["error"]:
        errors.append(f"{eid}: solution failed to load: {res['error']}")
        return None
    for call, r in zip(e["calls"], res["results"]):
        if r.get("error"):
            tests.append({"call": call, "raises": r["error"]["type"]})
        else:
            tests.append({"call": call, "expect": r["got"]})
    # Solution must pass its own tests (catches non-determinism).
    chk = json.loads(H["check_function"](sol, json.dumps(tests), files))
    if not all(t["ok"] for t in chk["results"]):
        errors.append(f"{eid}: solution does not pass its own tests: {chk['results']}")
    starter = e["starter"] or skeleton(sol)
    chk2 = json.loads(H["check_function"](starter, json.dumps(tests), files))
    if not chk2["error"] and all(t["ok"] for t in chk2["results"]):
        errors.append(f"{eid}: starter already passes all tests")
    if len(tests) < 3:
        errors.append(f"{eid}: function task needs at least 3 test calls")
    return {"kind": "func", "title": e["title"], "prompt": inline(e["prompt"]), "starter": starter, "tests": tests,
            "solution": sol, "hint": inline(e["hint"]) if e["hint"] else None, "lv": e["lv"], "name": name,
            "files": e.get("files") or []}


def build_prog(e, eid):
    sol = e["solution"]
    tests = []
    for stdin in e["stdins"]:
        stdin_n = stdin + "\n"
        out, err = run(sol, stdin_n, e.get("files"))
        if err:
            errors.append(f"{eid}: solution raised {err} for stdin {stdin!r}")
        if not out.strip():
            errors.append(f"{eid}: solution printed nothing for stdin {stdin!r}")
        tests.append({"stdin": stdin_n, "expect": out})
    starter = e["starter"] if e["starter"] is not None else "# Kodingizni shu yerga yozing\n"
    chk = json.loads(H["check_program"](starter, json.dumps(tests), json.dumps(e.get("files") or [])))
    if all(t["ok"] for t in chk["results"]):
        errors.append(f"{eid}: starter already passes all tests")
    return {"kind": "prog", "title": e["title"], "prompt": inline(e["prompt"]), "starter": starter, "tests": tests,
            "solution": sol, "hint": inline(e["hint"]) if e["hint"] else None, "lv": e["lv"],
            "files": e.get("files") or []}


SITE_NAMES = {"exercism": "Exercism", "lc": "LeetCode", "cses": "CSES", "acmp": "acmp.ru"}


def build_link(e, eid):
    site, ref = e["site"], e["ref"]
    if site == "exercism":
        if ref not in EXERCISM:
            errors.append(f"{eid}: unknown exercism slug {ref}")
        url, title = f"https://exercism.org/tracks/python/exercises/{ref}", e["title"] or EXERCISM.get(ref, ref)
    elif site == "lc":
        if ref not in LC_SLUGS:
            errors.append(f"{eid}: unknown leetcode slug {ref}")
        url = f"https://leetcode.com/problems/{ref}/"
        title = e["title"] or LC["titles"].get(ref) or ref.replace("-", " ").title()
    elif site == "cses":
        if ref not in CSES:
            errors.append(f"{eid}: unknown cses id {ref}")
        url, title = f"https://cses.fi/problemset/task/{ref}", e["title"] or CSES.get(ref, str(ref))
    elif site == "acmp":
        if ref not in ACMP:
            errors.append(f"{eid}: unknown acmp id {ref}")
        url, title = f"https://acmp.ru/index.asp?main=task&id_task={ref}", e["title"] or ACMP.get(ref, str(ref))
    elif site == "docs":
        d = DOCS.get(ref)
        if not d:
            errors.append(f"{eid}: unverified docs page {ref}")
            return None
        url, title = d["url"], e["title"] or d["title"]
        return {"kind": "link", "site": "docs", "siteName": d["site"], "title": title, "url": url,
                "note": inline(e["note"]) if e["note"] else None, "lv": 2}
    else:
        errors.append(f"{eid}: unknown site {site}")
        return None
    return {"kind": "link", "site": site, "siteName": SITE_NAMES[site], "title": title, "url": url,
            "note": inline(e["note"]) if e["note"] else None, "lv": 2}


BUILDERS = {"predict": build_predict, "concept": build_concept, "func": build_func, "prog": build_prog, "link": build_link}


def main():
    for mod in COURSE_FILES:
        if os.path.exists(os.path.join(HERE, mod + ".py")):
            importlib.import_module(mod)
    sections = []
    totals = {"topics": 0, "ex": 0, "quiz": 0, "func": 0, "prog": 0, "link": 0, "lessonCode": 0}
    seen_slugs = set()
    for sec in dsl.SECTIONS:
        out_topics = []
        for ti, t in enumerate(sec["topics"]):
            tid = f"{sec['num']}.{ti + 1}"
            if t["slug"] in seen_slugs:
                errors.append(f"{tid}: duplicate slug {t['slug']}")
            seen_slugs.add(t["slug"])
            blocks = parse_lesson(t["body"], tid)
            totals["lessonCode"] += sum(1 for b in blocks if b["t"] == "code")
            if len(t["ex"]) != EX_PER_TOPIC:
                errors.append(f"{tid} {t['title']}: has {len(t['ex'])} exercises, needs {EX_PER_TOPIC}")
            exs = []
            for ei, e in enumerate(t["ex"]):
                eid = f"{tid}.{ei + 1}"
                try:
                    built = BUILDERS[e["kind"]](e, eid)
                except Timeout:
                    errors.append(f"{eid}: timed out")
                    built = None
                if built:
                    built["id"] = eid
                    exs.append(built)
                    totals["ex"] += 1
                    totals[built["kind"]] += 1
            out_topics.append({"id": tid, "slug": t["slug"], "title": t["title"], "short": t["short"], "mins": t["mins"],
                               "level": t["level"], "blocks": blocks, "ex": exs})
            totals["topics"] += 1
        sections.append({"num": sec["num"], "title": sec["title"], "short": sec["short"], "emoji": sec["emoji"],
                         "topics": out_topics})
    if errors:
        print(f"\n{len(errors)} problem(s):\n")
        print("\n\n".join(errors[:80]))
        sys.exit(1)
    out = os.path.join(ROOT, "src", "data", "course.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"sections": sections, "totals": totals}, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("course.json OK:", json.dumps(totals))
    for s in sections:
        print(f"  {s['num']}. {s['title']}: {len(s['topics'])} topics")


if __name__ == "__main__":
    main()
