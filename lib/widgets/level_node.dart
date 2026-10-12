import 'package:flutter/material.dart';

import '../data/progress_store.dart';

/// One round level button on the map, styled like a match-3 level point.
class LevelNode extends StatelessWidget {
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

  List<Color> get _colors {
    if (locked) return const [Color(0xFFE0E0E0), Color(0xFF9E9E9E)];
    switch (status) {
      case LevelStatus.done:
        return const [Color(0xFFFFE082), Color(0xFFFF8F00)];
      case LevelStatus.practice:
        return const [Color(0xFF80DEEA), Color(0xFF00838F)];
      case LevelStatus.none:
        return const [Color(0xFFF48FB1), Color(0xFFC2185B)];
    }
  }

  @override
  Widget build(BuildContext context) {
    final colors = _colors;
    final label = (index + 1).toString().padLeft(2, '0');

    Widget button = GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTapUp: (d) => onTap(d.globalPosition),
      child: Stack(
        clipBehavior: Clip.none,
        alignment: Alignment.center,
        children: [
          // Pedestal under the button.
          Positioned(
            bottom: -6,
            child: Container(
              width: 62,
              height: 24,
              decoration: BoxDecoration(
                color: const Color(0x99E1F5FE),
                borderRadius: BorderRadius.circular(30),
              ),
            ),
          ),
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: colors,
              ),
              border: Border.all(color: Colors.white, width: 3),
              boxShadow: [
                BoxShadow(
                  color: colors.last.withAlpha(140),
                  blurRadius: 10,
                  offset: const Offset(0, 5),
                ),
              ],
            ),
            alignment: Alignment.center,
            child: locked
                ? const Icon(Icons.lock_rounded, color: Colors.white, size: 26)
                : Text(
                    label,
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      fontSize: label.length > 2 ? 17 : 21,
                      shadows: const [
                        Shadow(color: Color(0x66000000), offset: Offset(0, 2), blurRadius: 2),
                      ],
                    ),
                  ),
          ),
          // Shine.
          Positioned(
            top: 9,
            left: 16,
            child: IgnorePointer(
              child: Container(
                width: 16,
                height: 8,
                decoration: BoxDecoration(
                  color: const Color(0x80FFFFFF),
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
          ),
          if (status == LevelStatus.done && !locked)
            const Positioned(top: -26, child: _Stars()),
          if (status == LevelStatus.practice && !locked)
            const Positioned(top: -10, right: -10, child: _PracticeBadge()),
        ],
      ),
    );

    if (current && !locked) {
      button = _Pulse(child: button);
    }
    return button;
  }
}

class _Stars extends StatelessWidget {
  const _Stars();

  @override
  Widget build(BuildContext context) {
    Widget star(double size, double dy) => Transform.translate(
          offset: Offset(0, dy),
          child: Icon(Icons.star_rounded, size: size, color: const Color(0xFFFFD600),
              shadows: const [Shadow(color: Color(0x88E65100), blurRadius: 3, offset: Offset(0, 1))]),
        );
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [star(24, 8), star(28, 0), star(24, 8)],
    );
  }
}

class _PracticeBadge extends StatelessWidget {
  const _PracticeBadge();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 26,
      height: 26,
      decoration: BoxDecoration(
        color: const Color(0xFFFF7043),
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 2),
      ),
      child: const Icon(Icons.replay_rounded, size: 15, color: Colors.white),
    );
  }
}

/// Gentle bounce on the current level so the player knows where to go.
class _Pulse extends StatefulWidget {
  final Widget child;
  const _Pulse({required this.child});

  @override
  State<_Pulse> createState() => _PulseState();
}

class _PulseState extends State<_Pulse> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 900),
  )..repeat(reverse: true);

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _c,
      builder: (context, child) {
        final t = Curves.easeInOut.transform(_c.value);
        return Transform.translate(
          offset: Offset(0, -6 * t),
          child: Transform.scale(scale: 1.0 + 0.06 * t, child: child),
        );
      },
      child: widget.child,
    );
  }
}
