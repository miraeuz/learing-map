"""Writes desktop/src/data/details.json from the three study-guide parts."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from details_a import A  # noqa: E402
from details_b import B  # noqa: E402
from details_c import C  # noqa: E402
from details_w import W  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
items = A + B + C
assert len(A) == 41 and len(B) == 32 and len(C) == 44, (len(A), len(B), len(C))
assert len(W) == len(items), len(W)
for i, d in enumerate(items):
    assert set(d) == {'k', 'c', 'p'}, i
    d['h'], d['w'] = W[i]
    assert 3 <= len(d['k']) <= 6 and 1 <= len(d['p']) <= 3, i
out = os.path.join(ROOT, 'desktop/src/data/details.json')
json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', out, len(items))
