import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'screens/map_screen.dart';
import 'theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.dark,
  ));
  runApp(const IcpcQuestApp());
}

class IcpcQuestApp extends StatelessWidget {
  const IcpcQuestApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ICPC yoʻli',
      debugShowCheckedModeBanner: false,
      theme: buildTheme(),
      home: const MapScreen(),
    );
  }
}
