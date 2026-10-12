"""Exports the roadmap (stages, topics, practice links) from the Flutter sources
to desktop/src/data/roadmap.json so both apps share one source of truth."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dart_strings(s):
    """Decode a Dart single-quoted string literal body."""
    return s.replace("\\'", "'").replace('\\$', '$').replace('\\\\', '\\')


STR = r"'((?:\\.|[^'\\])*)'"

topics_src = open(os.path.join(ROOT, 'lib/data/topics.dart'), encoding='utf-8').read()
links_src = open(os.path.join(ROOT, 'lib/data/links.dart'), encoding='utf-8').read()

stages = []
for m in re.finditer(r"Stage\((\d+), " + STR + ", " + STR + ", " + STR + r", Color\(0xFF([0-9A-Fa-f]{6})\)\)", topics_src):
    stages.append(dict(id=int(m.group(1)), name=dart_strings(m.group(2)), emoji=dart_strings(m.group(3)),
                       tagline=dart_strings(m.group(4)), color='#' + m.group(5).upper()))

topics = []
for m in re.finditer(r"Topic\((\d+), " + STR + r",\s*" + STR + r"\)", topics_src):
    topics.append(dict(stage=int(m.group(1)), name=dart_strings(m.group(2)), info=dart_strings(m.group(3))))

levels = []
for block in re.split(r"\n  // \d+\n", links_src)[1:]:
    items = re.findall(r"PracticeLink\(" + STR + ", " + STR + ", " + STR + r"\)", block)
    levels.append([dict(site=dart_strings(a), title=dart_strings(b), url=dart_strings(c)) for a, b, c in items])

assert len(stages) == 11, len(stages)
assert len(topics) == 117, len(topics)
assert len(levels) == 117 and all(len(l) == 15 for l in levels), [len(l) for l in levels]
for t, l in zip(topics, levels):
    t['links'] = l

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'desktop/src/data/roadmap.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(dict(stages=stages, topics=topics), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', out, len(topics), 'topics', sum(len(t['links']) for t in topics), 'links')
