import 'package:flutter/material.dart';

/// One practice link shown in a level's "Masalalar" tab.
class PracticeLink {
  final String site;
  final String title;
  final String url;
  const PracticeLink(this.site, this.title, this.url);

  SiteStyle get style => siteStyles[site] ?? const SiteStyle('WEB', 'Veb-sahifa', Color(0xFF607D8B));
}

class SiteStyle {
  final String badge;
  final String name;
  final Color color;
  const SiteStyle(this.badge, this.name, this.color);
}

const siteStyles = <String, SiteStyle>{
  'cf': SiteStyle('CF', 'Codeforces', Color(0xFF1F8ACB)),
  'lc': SiteStyle('LC', 'LeetCode', Color(0xFFF89F1B)),
  'cses': SiteStyle('CSES', 'CSES', Color(0xFF3F4A5A)),
  'acmp': SiteStyle('ACMP', 'acmp.ru', Color(0xFFD84315)),
  'robo': SiteStyle('ROBO', 'RoboContest', Color(0xFF2E7D32)),
  'atcoder': SiteStyle('AC', 'AtCoder', Color(0xFF222222)),
  'ys': SiteStyle('LIB', 'Library Checker', Color(0xFF6A1B9A)),
  'cpa': SiteStyle('CPA', 'cp-algorithms', Color(0xFF00897B)),
  'spoj': SiteStyle('SPOJ', 'SPOJ', Color(0xFF3B5998)),
  'uva': SiteStyle('UVa', 'UVa Online Judge', Color(0xFF8D6E63)),
  'timus': SiteStyle('TIM', 'Timus', Color(0xFF5D4037)),
  'kattis': SiteStyle('KAT', 'Kattis', Color(0xFFE53935)),
  'codechef': SiteStyle('CC', 'CodeChef', Color(0xFF5B4638)),
  'hackerrank': SiteStyle('HR', 'HackerRank', Color(0xFF2EC866)),
  'usaco': SiteStyle('USA', 'USACO', Color(0xFF1565C0)),
  'vjudge': SiteStyle('VJ', 'Virtual Judge', Color(0xFF455A64)),
  'poj': SiteStyle('POJ', 'POJ', Color(0xFF546E7A)),
  'github': SiteStyle('GH', 'GitHub', Color(0xFF24292F)),
  'icpc': SiteStyle('ICPC', 'ICPC', Color(0xFF0D47A1)),
  'clist': SiteStyle('CL', 'CLIST', Color(0xFF00695C)),
  'topcoder': SiteStyle('TC', 'TopCoder', Color(0xFF29A8E0)),
  'lightoj': SiteStyle('LOJ', 'LightOJ', Color(0xFFFF7043)),
  'szkopul': SiteStyle('SZK', 'Szkopuł', Color(0xFFC62828)),
  'dmoj': SiteStyle('DMOJ', 'DMOJ', Color(0xFFFBC02D)),
  'ojuz': SiteStyle('OJ', 'oj.uz', Color(0xFF7B1FA2)),
  'csacademy': SiteStyle('CSA', 'CS Academy', Color(0xFF0097A7)),
  'euler': SiteStyle('PE', 'Project Euler', Color(0xFF424242)),
  'eolymp': SiteStyle('EO', 'E-olymp', Color(0xFF1976D2)),
  'toph': SiteStyle('TPH', 'Toph', Color(0xFF26A69A)),
  'hackerearth': SiteStyle('HE', 'HackerEarth', Color(0xFF323754)),
  'hdu': SiteStyle('HDU', 'HDU', Color(0xFF6D4C41)),
  'baekjoon': SiteStyle('BOJ', 'Baekjoon', Color(0xFF0076C0)),
};
