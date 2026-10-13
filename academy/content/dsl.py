"""Authoring helpers for Mirae Academy lessons.

A course file calls SECTION(...) once and then TOPIC(...) for every lesson.
Exercises (20 per topic):

  P(code, *wrong, why=None, q=None, lv=1)
      "What does this print?" — the correct answer is computed by running `code`.
  Q(question, right, *wrong, why=None, code=None, lv=1)
      A concept question with one right answer.
  F(title, prompt, solution, *calls, hint=None, starter=None, lv=2)
      Write a function. `calls` are expressions like "yig(2, 3)"; the expected
      results are computed from `solution`.
  PR(title, prompt, solution, *stdins, hint=None, starter=None, lv=1)
      Write a whole program. Each stdin case is fed to input(); expected output
      is computed from `solution`.
  L(site, ref, title=None, note=None)
      An online problem: site is 'exercism', 'lc' (LeetCode), 'cses' or 'acmp'.

Lesson bodies use a tiny Markdown: '## heading', paragraphs, '- bullets',
'> tip', '!> warning', '| table | rows |', and ```py code blocks. Code blocks are
executed at build time and their output is shown under them. Use ```py norun to
skip running and ```py input=Ali|25 to feed input() (| separates lines).
"""

SECTIONS = []


def SECTION(num, title, short, emoji):
    SECTIONS.append({"num": num, "title": title, "short": short, "emoji": emoji, "topics": []})


def TOPIC(slug, title, short, mins, body, ex, level=1):
    assert SECTIONS, "SECTION() must come first"
    SECTIONS[-1]["topics"].append(
        {"slug": slug, "title": title, "short": short, "mins": mins, "level": level, "body": body, "ex": ex}
    )


def P(code, *wrong, why=None, q=None, lv=1):
    return {"kind": "predict", "code": code.strip("\n"), "wrong": list(wrong), "why": why, "q": q, "lv": lv}


def Q(question, right, *wrong, why=None, code=None, lv=1):
    return {"kind": "concept", "q": question, "right": right, "wrong": list(wrong), "why": why,
            "code": code.strip("\n") if code else None, "lv": lv}


def F(title, prompt, solution, *calls, hint=None, starter=None, lv=2):
    return {"kind": "func", "title": title, "prompt": prompt, "solution": solution.strip("\n"),
            "calls": list(calls), "hint": hint, "starter": starter, "lv": lv}


def PR(title, prompt, solution, *stdins, hint=None, starter=None, lv=1):
    return {"kind": "prog", "title": title, "prompt": prompt, "solution": solution.strip("\n"),
            "stdins": list(stdins) or [""], "hint": hint, "starter": starter, "lv": lv}


def L(site, ref, title=None, note=None):
    return {"kind": "link", "site": site, "ref": ref, "title": title, "note": note}
