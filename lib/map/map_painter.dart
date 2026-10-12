import 'dart:math';

import 'package:flutter/material.dart';

import '../theme.dart';
import 'map_layout.dart';

/// Static scenery: water, swirls, fish, the channel, islands and the beach.
/// Painted once; progress changes never repaint this layer.
class MapPainter extends CustomPainter {
  final MapLayout layout;
  MapPainter(this.layout);

  @override
  void paint(Canvas canvas, Size size) {
    _drawOcean(canvas, size);
    _drawSwirls(canvas, size);
    _drawFish(canvas, size);
    _drawChannel(canvas);
    for (final island in layout.islands) {
      _drawIsland(canvas, island);
    }
    _drawIsland(canvas, IslandSpec(layout.trophy, 90, '🏆', 99));
    _drawBeach(canvas, size);
  }

  void _drawOcean(Canvas canvas, Size size) {
    canvas.drawRect(Offset.zero & size, Paint()..color = AppColors.lagoon);
    final band = Paint()..color = const Color(0x24FFFFFF);
    for (double y = 0; y < size.height; y += 900) {
      final path = Path()
        ..moveTo(0, y + 200)
        ..quadraticBezierTo(size.width * 0.5, y + 80, size.width, y + 260)
        ..lineTo(size.width, y + 420)
        ..quadraticBezierTo(size.width * 0.5, y + 300, 0, y + 460)
        ..close();
      canvas.drawPath(path, band);
    }
  }

  void _drawSwirls(Canvas canvas, Size size) {
    final rnd = Random(11);
    final paint = Paint()
      ..color = const Color(0x4DFFFFFF)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.5
      ..strokeCap = StrokeCap.round;
    final count = (size.height / 120).floor();
    for (var i = 0; i < count; i++) {
      final c = Offset(rnd.nextDouble() * size.width, rnd.nextDouble() * size.height);
      final r = 24 + rnd.nextDouble() * 50;
      final start = rnd.nextDouble() * pi * 2;
      canvas.drawArc(Rect.fromCircle(center: c, radius: r), start, 1.1, false, paint);
      canvas.drawArc(Rect.fromCircle(center: c + const Offset(0, 8), radius: r * 0.7), start + 0.2, 0.8, false, paint);
    }
  }

  void _drawFish(Canvas canvas, Size size) {
    final rnd = Random(5);
    final paint = Paint()..color = const Color(0x2E0B5F86);
    final count = (size.height / 170).floor();
    for (var i = 0; i < count; i++) {
      final c = Offset(rnd.nextDouble() * size.width, rnd.nextDouble() * size.height);
      final s = 0.6 + rnd.nextDouble() * 0.8;
      final dir = rnd.nextBool() ? 1.0 : -1.0;
      canvas.save();
      canvas.translate(c.dx, c.dy);
      canvas.scale(s * dir, s);
      canvas.drawOval(const Rect.fromLTWH(-14, -5, 28, 10), paint);
      final tail = Path()
        ..moveTo(-12, 0)
        ..lineTo(-22, -7)
        ..lineTo(-22, 7)
        ..close();
      canvas.drawPath(tail, paint);
      canvas.restore();
    }
  }

  void _drawChannel(Canvas canvas) {
    final path = routePath(layout);
    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0x330B5F86)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 124
        ..strokeCap = StrokeCap.round
        ..strokeJoin = StrokeJoin.round,
    );
    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0x260B5F86)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 72
        ..strokeCap = StrokeCap.round
        ..strokeJoin = StrokeJoin.round,
    );
  }

  Path _blob(Offset c, double r, int seed, double scale) {
    const pts = 16;
    final points = <Offset>[];
    for (var k = 0; k < pts; k++) {
      final a = k / pts * pi * 2;
      final wobble = 0.86 + 0.14 * sin(a * 3 + seed) + 0.06 * cos(a * 5 + seed * 2);
      points.add(Offset(
        c.dx + cos(a) * r * 1.2 * wobble * scale,
        c.dy + sin(a) * r * 0.78 * wobble * scale,
      ));
    }
    final path = Path();
    final first = Offset.lerp(points.last, points.first, 0.5)!;
    path.moveTo(first.dx, first.dy);
    for (var k = 0; k < pts; k++) {
      final p = points[k];
      final next = points[(k + 1) % pts];
      final mid = Offset.lerp(p, next, 0.5)!;
      path.quadraticBezierTo(p.dx, p.dy, mid.dx, mid.dy);
    }
    path.close();
    return path;
  }

  void _drawIsland(Canvas canvas, IslandSpec s) {
    final c = s.center;
    final r = s.radius;
    canvas.drawPath(_blob(c, r, s.seed, 1.2), Paint()..color = const Color(0x5580E3F2));
    canvas.drawPath(
      _blob(c, r, s.seed, 1.05),
      Paint()
        ..color = const Color(0xD9FFFFFF)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 5,
    );
    canvas.drawPath(_blob(c + const Offset(0, 9), r, s.seed, 1.0), Paint()..color = AppColors.sandDark);
    canvas.drawPath(_blob(c, r, s.seed, 1.0), Paint()..color = AppColors.sand);
    canvas.drawPath(_blob(c - Offset(0, r * 0.08), r, s.seed + 1, 0.62), Paint()..color = const Color(0xFF8CC152));
    canvas.drawPath(_blob(c - Offset(0, r * 0.12), r, s.seed + 2, 0.45), Paint()..color = const Color(0xFFA0D468));
    _drawPalm(canvas, c + Offset(-r * 0.75, r * 0.15), r * 0.75, -12);
    _drawPalm(canvas, c + Offset(r * 0.7, r * 0.1), r * 0.65, 14);
    final shell = Paint()..color = const Color(0xFFE8C9A8);
    canvas.drawOval(Rect.fromCenter(center: c + Offset(r * 0.3, r * 0.55), width: 12, height: 9), shell);
    canvas.drawOval(Rect.fromCenter(center: c + Offset(-r * 0.25, r * 0.6), width: 9, height: 7), shell);
  }

  void _drawPalm(Canvas canvas, Offset base, double h, double lean) {
    final top = base + Offset(lean, -h);
    final trunk = Path()
      ..moveTo(base.dx, base.dy)
      ..quadraticBezierTo(base.dx + lean * 0.1, base.dy - h * 0.6, top.dx, top.dy);
    canvas.drawPath(
      trunk,
      Paint()
        ..color = const Color(0xFF9C6B3C)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 7
        ..strokeCap = StrokeCap.round,
    );
    final leafDark = Paint()..color = const Color(0xFF2E7D32);
    final leaf = Paint()..color = const Color(0xFF5CB85C);
    const angles = [-160.0, -125.0, -90.0, -55.0, -20.0, 20.0, 160.0];
    final len = h * 0.55;
    for (final deg in angles) {
      final a = deg * pi / 180;
      final tip = top + Offset(cos(a) * len, sin(a) * len + len * 0.35);
      final normal = Offset(-sin(a), cos(a)) * (len * 0.22);
      final mid = Offset.lerp(top, tip, 0.5)!;
      final p = Path()
        ..moveTo(top.dx, top.dy)
        ..quadraticBezierTo(mid.dx + normal.dx, mid.dy + normal.dy - len * 0.15, tip.dx, tip.dy)
        ..quadraticBezierTo(mid.dx - normal.dx * 0.3, mid.dy - normal.dy * 0.3, top.dx, top.dy)
        ..close();
      canvas.drawPath(p.shift(const Offset(0, 2)), leafDark);
      canvas.drawPath(p, leaf);
    }
    final coco = Paint()..color = const Color(0xFF8D6E2F);
    canvas.drawCircle(top + const Offset(-4, 4), 4, coco);
    canvas.drawCircle(top + const Offset(4, 5), 4, coco);
    canvas.drawCircle(top + const Offset(0, 8), 4, coco);
  }

  void _drawBeach(Canvas canvas, Size size) {
    final top = size.height - 95;
    final path = Path()..moveTo(0, top);
    const waves = 6;
    final w = size.width / waves;
    for (var i = 0; i < waves; i++) {
      path.quadraticBezierTo(w * i + w / 2, top + (i.isEven ? -18 : 14), w * (i + 1), top);
    }
    path
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();
    canvas.drawPath(path.shift(const Offset(0, -10)), Paint()..color = const Color(0xD9FFFFFF));
    canvas.drawPath(path, Paint()..color = AppColors.sand);
  }

  @override
  bool shouldRepaint(covariant MapPainter oldDelegate) => oldDelegate.layout != layout;
}

Path routePath(MapLayout layout) {
  final nodes = layout.nodes;
  final path = Path()..moveTo(nodes[0].dx, nodes[0].dy + 160);
  path.lineTo(nodes[0].dx, nodes[0].dy);
  for (var i = 0; i < nodes.length - 1; i++) {
    final p0 = nodes[i];
    final p3 = nodes[i + 1];
    final midY = (p0.dy + p3.dy) / 2;
    path.cubicTo(p0.dx, midY, p3.dx, midY, p3.dx, p3.dy);
  }
  path.lineTo(layout.trophy.dx, layout.trophy.dy);
  return path;
}

/// The route between levels: a gold wake behind the ship (answered levels)
/// and white bubbles ahead of it.
class RoutePainter extends CustomPainter {
  final MapLayout layout;
  final int frontier; // index of the current level
  RoutePainter(this.layout, this.frontier);

  @override
  void paint(Canvas canvas, Size size) {
    final wakeGlow = Paint()
      ..color = const Color(0x66FFE08A)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 14
      ..strokeCap = StrokeCap.round;
    final wake = Paint()
      ..color = AppColors.gold
      ..style = PaintingStyle.stroke
      ..strokeWidth = 6
      ..strokeCap = StrokeCap.round;
    final bubbleFill = Paint()..color = Colors.white;
    final bubbleRing = Paint()
      ..color = const Color(0xFF7FD3EE)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    for (var i = 0; i < layout.nodes.length - 1; i++) {
      if (i < frontier) {
        // Dashed gold wake along this segment.
        Offset? prev;
        const steps = 14;
        for (var k = 0; k <= steps; k++) {
          final t = 0.18 + 0.64 * k / steps;
          final p = layout.pathPoint(i, t);
          if (prev != null && k.isOdd) {
            canvas.drawLine(prev, p, wakeGlow);
            canvas.drawLine(prev, p, wake);
          }
          prev = p;
        }
      } else {
        for (final t in const [0.33, 0.5, 0.67]) {
          final p = layout.pathPoint(i, t);
          canvas.drawCircle(p, 5, bubbleFill);
          canvas.drawCircle(p, 5, bubbleRing);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant RoutePainter old) => old.frontier != frontier || old.layout != layout;
}
