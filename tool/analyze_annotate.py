"""Turns `flutter analyze --format=machine` output into GitHub annotations.
Exits 1 if there are errors (warnings and infos are reported but don't fail)."""
import sys

errors = 0
raw = open(sys.argv[1], encoding='utf-8', errors='replace').read()
if '|' not in raw:
    print('::warning title=analyzer output::' + raw[-3000:].replace('%', '%25').replace('\n', '%0A'))
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    parts = line.rstrip('\n').split('|')
    if len(parts) < 8:
        continue
    severity, _kind, code, path, ln, col, _length, msg = parts[:8]
    level = {'ERROR': 'error', 'WARNING': 'warning'}.get(severity, 'notice')
    if level == 'error':
        errors += 1
    rel = path.split('/learing-map/learing-map/')[-1] if '/learing-map/' in path else path
    print(f'::{level} file={rel},line={ln},col={col},title={code}::{msg}')
print(f'{errors} error(s)')
sys.exit(1 if errors else 0)
