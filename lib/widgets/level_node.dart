import 'dart:math';

import 'package:flutter/material.dart';

import '../data/progress_store.dart';
import '../theme.dart';

/// A pressable 3D level button on the map.
class LevelNode extends StatefulWidget {
  final int index;
  final LevelStatus status;
  final bool locked;
  final bool current;
  final void Function(Offset globalPosition) onTap;

  const LevelNode({
    super.key,
    required this.index,
    required this.status,
    required this.locked,
    required this.current,
    required this.onTap,
  });

  @override
  State<LevelNode> createState() => _LevelNodeState();
}

class _LevelNodeState extends State<LevelNode> {
  bool _pressed = false;

  (Color, Color, Color) get _colors {
    if (widget.locked) return (const Color(0xFFD5DCE2), AppColors.stone, AppColors.stoneDark);
    switch (widget.status) {
      case LevelStatus.done:
        return (const Color(0xFFFFDC7A), AppColors.gold, AppColors.goldDark);
      case LevelStatus.practice:
        return (const Color(0xFF5ED3BE), AppColors.teal, AppColors.tealDark);
      case LevelStatus.none:
        return (const Color(0xFFFF9A80), AppColors.coral, AppColors.coralDark);
    }
  }

  @override
  Widget build(BuildContext context) {
    final (light, face, rim) = _colors;
    final label = '${widget.index + 1}';
    const size = 60.0;
    const depth = 6.0;
    final press = _pressed ? depth - 1 : 0.0;

    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTapDown: (_) => setState(() => _pressed = true),
      onTapCancel: () => setState(() => _pressed = false),
      onTapUp: (d) {
        setState(() => _pressed = false);
        widget.onTap(d.globalPosition);
      },
      child: SizedBox(
        width: size + 30,
        height: size + depth + 34,
        child: Stack(
          clipBehavior: Clip.none,
          alignment: Alignment.topCenter,
          children: [
            // Soft shadow on the water.
            Positioned(
              top: size + depth - 8,
              child: Container(
                width: size * 0.95,
                height: 16,
                decoration: BoxDecoration(
                  color: const Color(0x330B5F86),
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
            ),
            // Rim (the button's side).
            Positioned(
              top: 22 + depth,
              child: Container(
                width: size,
                height: size,
                decoration: BoxDecoration(shape: BoxShape.circle, color: rim),
              ),
            ),
            // Face.
            AnimatedPositioned(
              duration: const Duration(milliseconds: 70),
              top: 22 + press,
              child: Container(
                width: size,
                height: size,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    center: const Alignment(-0.35, -0.45),
                    radius: 0.95,
                    colors: [light, face],
                  ),
                  border: Border.all(color: Colors.white, width: 3),
                ),
                alignment: Alignment.center,
                child: widget.locked
                    ? const Icon(Icons.lock_rounded, color: Colors.white, size: 24)
                    : Text(
                        label,
                        style: TextStyle(
                          fontFamily: 'Nunito',
                          color: Colors.white,
                          fontWeight: FontWeight.w900,
                          fontSize: label.length > 2 ? 19 : 23,
                          shadows: [Shadow(color: rim, offset: const Offset(0, 2))],
                        ),
                      ),
              ),
            ),
            if (widget.status == LevelStatus.done && !widget.locked)
              const Positioned(top: 0, child: _Stars()),
            if (widget.status == LevelStatus.practice && !widget.locked)
              const Positioned(top: 12, right: 6, child: _PracticeBadge()),
            if (widget.current && !widget.locked)
              const Positioned(top: 22, child: IgnorePointer(child: _Ripple(size: size))),
          ],
        ),
      ),
    );
  }
}

class _Stars extends StatelessWidget {
  const _Stars();

  @override
  Widget build(BuildContext context) {
    Widget star(double size, double dy, double angle) => Transform.translate(
          offset: Offset(0, dy),
          child: Transform.rotate(
            angle: angle,
            child: Icon(Icons.star_rounded, size: size, color: AppColors.gold, shadows: const [
              Shadow(color: Color(0x99B36200), blurRadius: 2, offset: Offset(0, 1.5)),
            ]),
          ),
        );
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [star(22, 8, -0.25), star(28, 0, 0), star(22, 8, 0.25)],
    );
  }
}

class _PracticeBadge extends StatelessWidget {
  const _PracticeBadge();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 24,
      height: 24,
      decoration: BoxDecoration(
        color: AppColors.coral,
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 2),
      ),
      child: const Icon(Icons.replay_rounded, size: 14, color: Colors.white),
    );
  }
}

/// Expanding rings around the current level: "you are here".
class _Ripple extends StatefulWidget {
  final double size;
  const _Ripple({required this.size});

  @override
  State<_Ripple> createState() => _RippleState();
}

class _RippleState extends State<_Ripple> with SingleTickerProviderStateMixin {
  late final AnimationController _c =
      AnimationController(vsync: this, duration: const Duration(milliseconds: 1800))..repeat();

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (MediaQuery.of(context).disableAnimations) return const SizedBox.shrink();
    return AnimatedBuilder(
      animation: _c,
      builder: (context, _) {
        return CustomPaint(
          size: Size(widget.size, widget.size),
          painter: _RipplePainter(_c.value),
        );
      },
    );
  }
}

class _RipplePainter extends CustomPainter {
  final double t;
  _RipplePainter(this.t);

  @override
  void paint(Canvas canvas, Size size) {
    final c = size.center(Offset.zero);
    for (final shift in const [0.0, 0.5]) {
      final v = (t + shift) % 1.0;
      final r = size.width / 2 + 4 + v * 26;
      final paint = Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3
        ..color = Colors.white.withAlpha((180 * (1 - v)).round());
      canvas.drawCircle(c, r, paint);
    }
  }

  @override
  bool shouldRepaint(covariant _RipplePainter old) => old.t != t;
}

/// The little ship moored next to the current level.
class ShipMarker extends StatefulWidget {
  final bool facingLeft;
  const ShipMarker({super.key, required this.facingLeft});

  @override
  State<ShipMarker> createState() => _ShipMarkerState();
}

class _ShipMarkerState extends State<ShipMarker> with SingleTickerProviderStateMixin {
  late final AnimationController _c =
      AnimationController(vsync: this, duration: const Duration(milliseconds: 2400))..repeat();

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final still = MediaQuery.of(context).disableAnimations;
    final ship = Transform(
      alignment: Alignment.center,
      transform: Matrix4.diagonal3Values(widget.facingLeft ? -1 : 1, 1, 1),
      child: const Text('⛵', style: TextStyle(fontSize: 38)),
    );
    if (still) return ship;
    return AnimatedBuilder(
      animation: _c,
      child: ship,
      builder: (context, child) {
        final a = _c.value * 2 * pi;
        return Transform.translate(
          offset: Offset(0, sin(a) * 4),
          child: Transform.rotate(angle: sin(a + 0.8) * 0.06, child: child),
        );
      },
    );
  }
}
