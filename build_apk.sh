#!/usr/bin/env bash
# Build the ICPC Quest APK on your own computer (needs Flutter + Android SDK).
set -e
cd "$(dirname "$0")"
flutter create --platforms=android --project-name icpc_quest --org com.icpcquest .
sed -i.bak 's/android:label="icpc_quest"/android:label="ICPC Quest"/' android/app/src/main/AndroidManifest.xml
rm -f android/app/src/main/AndroidManifest.xml.bak
flutter pub get
flutter build apk --release
echo
echo "APK ready: build/app/outputs/flutter-apk/app-release.apk"
