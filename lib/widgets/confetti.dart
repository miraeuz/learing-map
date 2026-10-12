import 'dart:math';

import 'package:flutter/material.dart';

import '../theme.dart';

/// A one-shot confetti burst drawn over the whole screen.
class ConfettiOverlay extends StatefulWidget {
  const ConfettiOverlay({super.key});

  @override
  State<ConfettiOverlay> createState() => ConfettiOverlayState();
}

class _Particle {
  Offset pos;
  Offset vel;
  final Color color;
  final double size;
  double angle;
  final double spin;
  _Particle(this.pos, this.vel, this.color, this.size, this.angle, this.spin);
}

class ConfettiOverlayState extends State<ConfettiOverlay> with SingleTickerProviderStateMixin {
  late final AnimationController _c =
      AnimationController(vsync: this, duration: const Duration(milliseconds: 1700))
        ..addListener(_tick);
  final _particles = <_Particle>[];
  final _rnd = Random();
  Duration _last = Duration.zero;

  static const _colors = [AppColors.gold, AppColors.coral, AppColors.teal, Colors.white, AppColors.lagoonLight];

  void burst(Offset origin) {
    if (MediaQuery.of(context).disableAnimations) return;
    _particles.clear();
    for (var i = 0; i < 70; i++) {
      final a = -pi / 2 + (_rnd.nextDouble() - 0.5) * pi * 1.1;
      final speed = 380 + _rnd.nextDouble() * 520;
      _particles.add(_Particle(
        origin,
        Offset(cos(a) * speed, sin(a) * speed),
        _colors[_rnd.nextInt(_colors.length)],
        6 + _rnd.nextDouble() * 6,
        _rnd.nextDouble() * pi,
        (_rnd.nextDouble() - 0.5) * 12,
      ));
    }
    _last = Duration.zero;
    _c.forward(from: 0);
  }

  void _tick() {
    final now = _c.lastElapsedDuration ?? Duration.zero;
    final dt = (now - _last).inMicroseconds / 1e6;
    _last = now;
    for (final p in _particles) {
      p.vel = Offset(p.vel.dx * 0.985, p.vel.dy * 0.985 + 900 * dt);
      p.pos += p.vel * dt;
      p.angle += p.spin * dt;
    }
    setState(() {});
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_c.isAnimating) return const SizedBox.shrink();
    return IgnorePointer(
      child: CustomPaint(
        size: Size.infinite,
        painter: _ConfettiPainter(_particles, 1 - _c.value),
      ),
    );
  }
}

class _ConfettiPainter extends CustomPainter {
  final List<_Particle> particles;
  final double opacity;
  _ConfettiPainter(this.particles, this.opacity);

  @override
  void paint(Canvas canvas, Size size) {
    for (final p in particles) {
      canvas.save();
      canvas.translate(p.pos.dx, p.pos.dy);
      canvas.rotate(p.angle);
      final paint = Paint()..color = p.color.withAlpha((255 * opacity.clamp(0.0, 1.0)).round());
      canvas.drawRRect(
        RRect.fromRectAndRadius(Rect.fromCenter(center: Offset.zero, width: p.size, height: p.size * 0.55), const Radius.circular(2)),
        paint,
      );
      canvas.restore();
    }
  }

  @override
  bool shouldRepaint(covariant _ConfettiPainter old) => true;
}
