# Mirae Academy — Python runner and checker. Runs inside Pyodide in a Web Worker.
import builtins
import contextlib
import io
import json
import math
import sys
import traceback

OUT_LIMIT = 20000
FILENAME = "<kod>"


class _CappedIO(io.StringIO):
    def write(self, s):
        if self.tell() > OUT_LIMIT:
            return len(s)
        return super().write(s)


def _err_info(exc):
    line = None
    for fr in traceback.extract_tb(exc.__traceback__):
        if fr.filename == FILENAME:
            line = fr.lineno
    if isinstance(exc, SyntaxError) and exc.filename == FILENAME:
        line = exc.lineno
    msg = str(exc)
    if isinstance(exc, SyntaxError):
        msg = exc.msg
    return {"type": type(exc).__name__, "msg": msg, "line": line}


def _exec(code, stdin, ns):
    out = _CappedIO()
    old_in = sys.stdin
    sys.stdin = io.StringIO(stdin or "")
    err = None
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(code, FILENAME, "exec"), ns)
    except SystemExit:
        pass
    except EOFError as e:
        err = {"type": "EOFError", "msg": "input() uchun kirish maʼlumoti tugadi", "line": _err_info(e)["line"]}
    except BaseException as e:  # noqa: BLE001 — report every student error
        err = _err_info(e)
    finally:
        sys.stdin = old_in
    text = out.getvalue()
    if len(text) > OUT_LIMIT:
        text = text[:OUT_LIMIT] + "\n… (chiqish juda uzun, qisqartirildi)"
    return text, err


def _norm(s):
    lines = [ln.rstrip() for ln in s.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run_program(code, stdin=""):
    ns = {"__name__": "__main__"}
    text, err = _exec(code, stdin, ns)
    return json.dumps({"stdout": text, "error": err})


def _same(got, exp):
    if isinstance(exp, float) or isinstance(got, float):
        try:
            return math.isclose(float(got), float(exp), rel_tol=1e-9, abs_tol=1e-9)
        except (TypeError, ValueError):
            return False
    if isinstance(exp, bool) != isinstance(got, bool):
        return False
    if isinstance(exp, (list, tuple)) and isinstance(got, (list, tuple)):
        return type(exp) is type(got) and len(exp) == len(got) and all(_same(a, b) for a, b in zip(got, exp))
    return got == exp


def check_function(code, tests_json):
    tests = json.loads(tests_json)
    ns = {"__name__": "__main__"}
    text, err = _exec(code, "", ns)
    if err:
        return json.dumps({"stdout": text, "error": err, "results": []})
    results = []
    for t in tests:
        call = t["call"]
        out = _CappedIO()
        try:
            with contextlib.redirect_stdout(out):
                got = eval(call, ns)
            if "raises" in t:
                results.append({"call": call, "ok": False, "got": repr(got), "expect": t["raises"] + " xatosi"})
            else:
                exp = eval(t["expect"])
                results.append({"call": call, "ok": _same(got, exp), "got": repr(got), "expect": t["expect"]})
        except BaseException as e:  # noqa: BLE001
            info = _err_info(e)
            if "raises" in t:
                ok = info["type"] == t["raises"]
                results.append({"call": call, "ok": ok, "got": info["type"] + " xatosi", "expect": t["raises"] + " xatosi"})
            else:
                results.append({"call": call, "ok": False, "got": f"{info['type']}: {info['msg']}", "expect": t["expect"], "error": info})
    return json.dumps({"stdout": text, "error": None, "results": results})


def check_program(code, cases_json):
    cases = json.loads(cases_json)
    results = []
    first_out = ""
    for i, c in enumerate(cases):
        text, err = _exec(code, c.get("stdin", ""), {"__name__": "__main__"})
        if i == 0:
            first_out = text
        if err:
            results.append({"stdin": c.get("stdin", ""), "ok": False, "got": text, "expect": c["expect"], "error": err})
        else:
            results.append({"stdin": c.get("stdin", ""), "ok": _norm(text) == _norm(c["expect"]), "got": text, "expect": c["expect"]})
    return json.dumps({"stdout": first_out, "error": None, "results": results})
