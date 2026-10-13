"""Verify docs links against their source files on GitHub; writes docs.json.

Usage: for each repo, `git clone --depth 1 --filter=blob:none --no-checkout` and save
`git ls-tree -r --name-only HEAD` to <TREES>/<owner>_<repo>.txt, then run
`python3 verify_docs.py <TREES>`.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docs_candidates import DOCS

TREES = sys.argv[1] if len(sys.argv) > 1 else "trees"
_cache = {}


def exists(repo, path):
    """True if `path` is in the repo's file list (git ls-tree output saved as <owner>_<repo>.txt)."""
    if repo not in _cache:
        _cache[repo] = set(open(os.path.join(TREES, repo.replace("/", "_") + ".txt")).read().split("\n"))
    return path in _cache[repo]

out, bad = {}, []
for key, ((repo, src, url, site), page, title) in DOCS.items():
    base, ext = os.path.splitext(src.format(page))
    found = None
    for e in [ext, ".rst", ".md", ".txt"]:
        if exists(repo, base + e):
            found = base + e
            break
    if not found:
        bad.append((key, repo, src.format(page)))
        continue
    out[key] = {"url": url.format(page) if "{}" in url else url, "title": title, "site": site, "source": f"{repo}/{found}"}
json.dump(out, open(os.path.join(os.path.dirname(__file__), "docs.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "verified")
for b in bad: print("MISSING", b)
