# Mirae Academy — Python runner and checker. Runs inside Pyodide in a Web Worker.
import builtins
import contextlib
import io
import json
import importlib
import math
import os
import shutil
import sys
import tempfile
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


@contextlib.contextmanager
def _sandbox():
    """Run student code in a fresh, empty folder.

    Files, modules and databases the code creates live only for this run, so
    lessons about files, modules, CSV/JSON/ZIP and SQLite behave the same every
    time — at build time and inside the app.
    """
    base = tempfile.mkdtemp(prefix="mirae-")
    old_cwd = os.getcwd()
    old_path = list(sys.path)
    old_argv = list(sys.argv)
    old_mods = set(sys.modules)
    os.chdir(base)
    sys.path.insert(0, base)
    importlib.invalidate_caches()
    try:
        yield base
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path
        sys.argv[:] = old_argv
        for name in set(sys.modules) - old_mods:
            f = getattr(sys.modules[name], "__file__", None) or ""
            if f.startswith(base) or not f:
                sys.modules.pop(name, None)
        importlib.invalidate_caches()
        shutil.rmtree(base, ignore_errors=True)


def _write_files(files_json):
    """Write helper files (modules, data) into the sandbox folder. Folders are created as needed."""
    for f in json.loads(files_json or "[]"):
        name = f["name"].replace("\\", "/").lstrip("/")
        if ".." in name.split("/"):
            continue
        d = os.path.dirname(name)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(name, "w", encoding="utf-8") as fh:
            fh.write(f["code"])
    importlib.invalidate_caches()


def _exec(code, stdin, ns):
    out = _CappedIO()
    old_in = sys.stdin
    sys.stdin = io.StringIO(stdin or "")
    err = None
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
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


def run_program(code, stdin="", files_json="[]"):
    with _sandbox():
        _write_files(files_json)
        text, err = _exec(code, stdin, {"__name__": "__main__"})
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


def check_function(code, tests_json, files_json="[]"):
    with _sandbox():
        _write_files(files_json)
        return _check_function(code, tests_json)


def _check_function(code, tests_json):
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
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
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


def check_program(code, cases_json, files_json="[]"):
    cases = json.loads(cases_json)
    results = []
    first_out = ""
    for i, c in enumerate(cases):
        with _sandbox():
            _write_files(files_json)
            text, err = _exec(code, c.get("stdin", ""), {"__name__": "__main__"})
        if i == 0:
            first_out = text
        if err:
            results.append({"stdin": c.get("stdin", ""), "ok": False, "got": text, "expect": c["expect"], "error": err})
        else:
            results.append({"stdin": c.get("stdin", ""), "ok": _norm(text) == _norm(c["expect"]), "got": text, "expect": c["expect"]})
    return json.dumps({"stdout": first_out, "error": None, "results": results})
