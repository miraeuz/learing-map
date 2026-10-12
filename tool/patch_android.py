"""Patches the generated AndroidManifest.xml after `flutter create`:
- app label "ICPC yoʻli"
- lets url_launcher open https links in the browser (Android 11+ package visibility)
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'android/app/src/main/AndroidManifest.xml'
s = open(path, encoding='utf-8').read()

s = re.sub(r'android:label="[^"]*"', 'android:label="ICPC yoʻli"', s, count=1)

intent = ('<intent>\n            <action android:name="android.intent.action.VIEW" />\n'
          '            <data android:scheme="https" />\n        </intent>')
if 'android.intent.action.VIEW' not in s:
    if '<queries>' in s:
        s = s.replace('<queries>', '<queries>\n        ' + intent, 1)
    else:
        s = s.replace('</manifest>', '    <queries>\n        ' + intent + '\n    </queries>\n</manifest>', 1)

open(path, 'w', encoding='utf-8').write(s)
print('patched', path)
