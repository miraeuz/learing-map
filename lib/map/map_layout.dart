import 'dart:math';

import 'package:flutter/material.dart';

import '../data/topics.dart';

class IslandSpec {
  final Offset center;
  final double radius;
  final String emoji;
  final int seed;
  const IslandSpec(this.center, this.radius, this.emoji, this.seed);
}

class StageSign {
  final Offset center;
  final Stage stage;
  final bool tiltLeft;
  const StageSign(this.center, this.stage, this.tiltLeft);
}

/// Computes where every level point, island and stage sign sits on the map.
/// Level 1 is at the bottom; the path winds upward like in match-3 games.
class MapLayout {
  static const double spacing = 125;
  static const double padBottom = 190;
  static const double padTop = 260;
  static const double nodeSize = 66;

  static const _islandEmojis = [
    '🏰', '🏴‍☠️', '🐚', '⛵', '🗼', '💎', '🦜', '🗺️', '⚓', '🦀', '🐙', '🛖'
  ];

  final double width;
  late final double height;
  late final List<Offset> nodes;
  late final List<IslandSpec> islands;
  late final List<StageSign> signs;
  late final Offset trophy;

  MapLayout(this.width) {
    final n = topics.length;
    height = padBottom + padTop + (n - 1) * spacing;
    final amp = min(width * 0.26, 150.0);

    nodes = List.generate(n, (i) {
      final x = width / 2 + amp * sin(i * 0.62);
      final y = height - padBottom - i * spacing;
      return Offset(x, y);
    });

    // Stage signs at each stage start.
    final signIndices = <int>{};
    final signList = <StageSign>[];
    for (var i = 0; i < n; i++) {
      if (i == 0 || topics[i].stage != topics[i - 1].stage) {
        signIndices.add(i);
        final node = nodes[i];
        final below = i == 0
            ? node + const Offset(0, 70)
            : Offset((node.dx + nodes[i - 1].dx) / 2, node.dy + spacing / 2);
        final x = below.dx > width / 2 ? width * 0.25 : width * 0.75;
        signList.add(StageSign(Offset(x, below.dy), stages[topics[i].stage], x < width / 2));
      }
    }
    signs = signList;

    // Islands beside the path, away from signs.
    final islandList = <IslandSpec>[];
    var k = 0;
    for (var i = 1; i < n; i += 3) {
      if (signIndices.contains(i) || signIndices.contains(i + 1)) continue;
      final node = nodes[i];
      final left = node.dx > width / 2;
      final double r = (width * 0.2).clamp(60.0, 140.0).toDouble();
      final cx = left ? width * 0.14 : width * 0.86;
      islandList.add(IslandSpec(
        Offset(cx, node.dy),
        r,
        _islandEmojis[k % _islandEmojis.length],
        i * 7 + 3,
      ));
      k++;
    }
    islands = islandList;

    trophy = Offset(width / 2, nodes.last.dy - 150);
  }

  /// Point on the smooth path between node [i] and node [i+1], t in [0,1].
  Offset pathPoint(int i, double t) {
    final p0 = nodes[i];
    final p3 = nodes[i + 1];
    final midY = (p0.dy + p3.dy) / 2;
    final p1 = Offset(p0.dx, midY);
    final p2 = Offset(p3.dx, midY);
    final u = 1 - t;
    return p0 * (u * u * u) +
        p1 * (3 * u * u * t) +
        p2 * (3 * u * t * t) +
        p3 * (t * t * t);
  }
}
