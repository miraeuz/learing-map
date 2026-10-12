# ICPC Quest 🏝️

Your ICPC roadmap as a mobile-game island map: 117 levels across 11 stages
(Fundamentals → Data Structures → Graphs → Trees → DP → Math → Strings →
Geometry → Elite → Team skills).

- Tap a level point → a popup grows out of it with **what to learn**, **where to practice**, and **what to search**.
- Answer **Yes** → level gets 3 stars (mastered). Answer **No** → marked "needs practice" (↻ badge).
- Either answer unlocks the next level. Progress is saved on the phone.

## Get the APK without installing anything (GitHub, free)

1. Create a new repository on github.com and upload all files in this folder (keep the `.github` folder).
2. Open the **Actions** tab. The "Build APK" workflow runs automatically (about 5–8 minutes).
3. Open the finished run → **Artifacts** → download `icpc-quest-apk` → unzip → `app-release.apk`.
4. Copy it to your phone and install it (allow "Install unknown apps").

## Build on your own computer

Requires Flutter (stable) and the Android SDK.

```bash
./build_apk.sh
```

The APK will be at `build/app/outputs/flutter-apk/app-release.apk`.

## Customize

- Topics and explanations: `lib/data/topics.dart`
- Map drawing (ocean, islands, palms): `lib/map/map_painter.dart`
- Level popup: `lib/widgets/topic_card.dart`
