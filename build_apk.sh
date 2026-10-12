#!/usr/bin/env bash
# ICPC yoʻli APK ni oʻz kompyuteringizda yigʻish (Flutter + Android SDK kerak).
set -e
cd "$(dirname "$0")"
flutter create --platforms=android --project-name icpc_quest --org com.icpcquest .
python3 tool/patch_android.py android/app/src/main/AndroidManifest.xml
flutter pub get
dart run flutter_launcher_icons
flutter build apk --release
echo
echo "APK tayyor: build/app/outputs/flutter-apk/app-release.apk"
