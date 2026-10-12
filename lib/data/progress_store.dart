import 'package:shared_preferences/shared_preferences.dart';

/// Level status: not answered, answered "Hali yoʻq" (practice), answered "Ha" (mastered).
enum LevelStatus { none, practice, done }

class ProgressStore {
  static const _key = 'icpc_progress_v1';
  static const _visitedKey = 'icpc_visited_links_v1';
  static const _onboardedKey = 'icpc_onboarded_v2';

  static Future<Map<int, LevelStatus>> load() async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList(_key) ?? const <String>[];
    final result = <int, LevelStatus>{};
    for (final entry in list) {
      final parts = entry.split(':');
      if (parts.length != 2) continue;
      final index = int.tryParse(parts[0]);
      final value = int.tryParse(parts[1]);
      if (index == null || value == null) continue;
      if (value < 0 || value >= LevelStatus.values.length) continue;
      result[index] = LevelStatus.values[value];
    }
    return result;
  }

  static Future<void> save(Map<int, LevelStatus> progress) async {
    final prefs = await SharedPreferences.getInstance();
    final list = progress.entries
        .where((e) => e.value != LevelStatus.none)
        .map((e) => '${e.key}:${e.value.index}')
        .toList();
    await prefs.setStringList(_key, list);
  }

  static Future<Set<String>> loadVisited() async {
    final prefs = await SharedPreferences.getInstance();
    return (prefs.getStringList(_visitedKey) ?? const <String>[]).toSet();
  }

  static Future<void> saveVisited(Set<String> urls) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(_visitedKey, urls.toList());
  }

  static Future<bool> isOnboarded() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_onboardedKey) ?? false;
  }

  static Future<void> setOnboarded() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_onboardedKey, true);
  }

  static Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
    await prefs.remove(_visitedKey);
  }
}
