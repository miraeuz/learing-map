import 'package:flutter/material.dart';

/// Voyage palette: lagoon water, deep channel, sand, coral for "where you are",
/// gold for "mastered". Ink and paper for reading surfaces.
class AppColors {
  static const lagoon = Color(0xFF2BB3D9);
  static const lagoonLight = Color(0xFF5FCDEB);
  static const deep = Color(0xFF0B5F86);
  static const sand = Color(0xFFF6DFA6);
  static const sandDark = Color(0xFFDDB46A);
  static const coral = Color(0xFFFF6B4A);
  static const coralDark = Color(0xFFD9472A);
  static const gold = Color(0xFFFFC233);
  static const goldDark = Color(0xFFE08A00);
  static const teal = Color(0xFF14A38B);
  static const tealDark = Color(0xFF0B7A67);
  static const ink = Color(0xFF1D2B3A);
  static const inkSoft = Color(0xFF55657A);
  static const paper = Color(0xFFFFF8EA);
  static const stone = Color(0xFFB9C3CC);
  static const stoneDark = Color(0xFF8494A3);
}

ThemeData buildTheme() {
  const base = TextStyle(fontFamily: 'Nunito', color: AppColors.ink);
  return ThemeData(
    useMaterial3: true,
    fontFamily: 'Nunito',
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.lagoon,
      primary: AppColors.deep,
      secondary: AppColors.coral,
      surface: AppColors.paper,
    ),
    scaffoldBackgroundColor: AppColors.lagoon,
    textTheme: TextTheme(
      headlineSmall: base.copyWith(fontSize: 24, fontWeight: FontWeight.w900, height: 1.15),
      titleLarge: base.copyWith(fontSize: 20, fontWeight: FontWeight.w900),
      titleMedium: base.copyWith(fontSize: 16, fontWeight: FontWeight.w800),
      bodyLarge: base.copyWith(fontSize: 16, fontWeight: FontWeight.w600, height: 1.5),
      bodyMedium: base.copyWith(fontSize: 14, fontWeight: FontWeight.w600, height: 1.45),
      labelLarge: base.copyWith(fontSize: 15, fontWeight: FontWeight.w800),
      labelMedium: base.copyWith(fontSize: 12, fontWeight: FontWeight.w700),
    ),
    snackBarTheme: const SnackBarThemeData(
      behavior: SnackBarBehavior.floating,
      contentTextStyle: TextStyle(fontFamily: 'Nunito', fontWeight: FontWeight.w800, fontSize: 15),
    ),
  );
}
