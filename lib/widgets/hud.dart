import 'dart:math';

import 'package:flutter/material.dart';

import '../data/progress_store.dart';
import '../data/topics.dart';
import '../theme.dart';

/// Top "logbook": overall progress ring plus one chip per stage.
class Hud extends StatefulWidget {
  final Map<int, LevelStatus> progress;
  final int currentStage;
  final ValueChanged<int> onStageTap;
  final VoidCallback onReset;
  final VoidCallback onHelp;

  const Hud({
    super.key,
    required this.progress,
    required this.currentStage,
    required this.onStageTap,
    required this.onReset,
    required this.onHelp,
  });

  @override
  State<Hud> createState() => _HudState();
}

class _HudState extends State<Hud> {
  final _chips = ScrollController();
  final _keys = List.generate(stages.length, (_) => GlobalKey());

  @override
  void didUpdateWidget(covariant Hud old) {
    super.didUpdateWidget(old);
    if (old.currentStage != widget.currentStage) {
      WidgetsBinding.instance.addPostFrameCallback((_) => _revealChip(widget.currentStage));
    }
  }

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _revealChip(widget.currentStage));
  }

  void _revealChip(int stage) {
    final ctx = _keys[stage].currentContext;
    if (ctx == null) return;
    Scrollable.ensureVisible(ctx, duration: const Duration(milliseconds: 400), alignment: 0.3);
  }

  @override
  void dispose() {
    _chips.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final total = topics.length;
    final done = widget.progress.values.where((s) => s == LevelStatus.done).length;
    final practice = widget.progress.values.where((s) => s == LevelStatus.practice).length;
    final stage = stages[widget.currentStage];

    final perStageTotal = List.filled(stages.length, 0);
    final perStageDone = List.filled(stages.length, 0);
    for (var i = 0; i < total; i++) {
      perStageTotal[topics[i].stage]++;
      if (widget.progress[i] == LevelStatus.done) perStageDone[topics[i].stage]++;
    }

    return SafeArea(
      bottom: false,
      child: Container(
        margin: const EdgeInsets.fromLTRB(12, 8, 12, 0),
        padding: const EdgeInsets.fromLTRB(12, 12, 4, 10),
        decoration: BoxDecoration(
          color: AppColors.paper,
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: AppColors.sand, width: 2),
          boxShadow: const [BoxShadow(color: Color(0x4006324A), blurRadius: 16, offset: Offset(0, 6))],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                _ProgressRing(value: total == 0 ? 0 : done / total, color: AppColors.gold),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'ICPC yoʻli',
                        style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: AppColors.ink, height: 1.1),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '$done ta oʻzlashtirildi, $practice ta mashqda',
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.inkSoft),
                      ),
                      Text(
                        'Hozir: ${stage.name}',
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: stage.color),
                      ),
                    ],
                  ),
                ),
                PopupMenuButton<String>(
                  tooltip: 'Menyu',
                  icon: const Icon(Icons.more_vert_rounded, color: AppColors.inkSoft),
                  onSelected: (v) {
                    if (v == 'reset') widget.onReset();
                    if (v == 'help') widget.onHelp();
                  },
                  itemBuilder: (_) => const [
                    PopupMenuItem(value: 'help', child: Text('Qanday ishlaydi')),
                    PopupMenuItem(value: 'reset', child: Text('Natijalarni tozalash')),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 10),
            SizedBox(
              height: 46,
              child: ListView.separated(
                controller: _chips,
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.only(right: 8),
                itemCount: stages.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (context, i) {
                  final s = stages[i];
                  final active = i == widget.currentStage;
                  final complete = perStageDone[i] == perStageTotal[i];
                  return GestureDetector(
                    key: _keys[i],
                    onTap: () => widget.onStageTap(i),
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      padding: const EdgeInsets.fromLTRB(8, 4, 12, 4),
                      decoration: BoxDecoration(
                        color: active ? s.color : Colors.white,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: active ? s.color : const Color(0xFFEFE3C6), width: 1.5),
                      ),
                      child: Row(
                        children: [
                          Text(complete ? '⭐' : s.emoji, style: const TextStyle(fontSize: 18)),
                          const SizedBox(width: 6),
                          Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                s.name,
                                style: TextStyle(
                                  fontSize: 12.5,
                                  fontWeight: FontWeight.w800,
                                  color: active ? Colors.white : AppColors.ink,
                                ),
                              ),
                              const SizedBox(height: 3),
                              SizedBox(
                                width: 64,
                                child: ClipRRect(
                                  borderRadius: BorderRadius.circular(4),
                                  child: LinearProgressIndicator(
                                    value: perStageDone[i] / perStageTotal[i],
                                    minHeight: 5,
                                    backgroundColor: active ? const Color(0x55FFFFFF) : const Color(0xFFF1E6CC),
                                    valueColor: AlwaysStoppedAnimation(active ? Colors.white : s.color),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ProgressRing extends StatelessWidget {
  final double value;
  final Color color;
  const _ProgressRing({required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 58,
      height: 58,
      child: TweenAnimationBuilder<double>(
        tween: Tween(begin: 0, end: value),
        duration: const Duration(milliseconds: 700),
        curve: Curves.easeOutCubic,
        builder: (context, v, _) => CustomPaint(
          painter: _RingPainter(v, color),
          child: Center(
            child: Text(
              '${(v * 100).round()}%',
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w900, color: AppColors.ink),
            ),
          ),
        ),
      ),
    );
  }
}

class _RingPainter extends CustomPainter {
  final double value;
  final Color color;
  _RingPainter(this.value, this.color);

  @override
  void paint(Canvas canvas, Size size) {
    final rect = (Offset.zero & size).deflate(4);
    canvas.drawArc(rect, 0, 2 * pi, false,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 7
          ..color = const Color(0xFFF1E6CC));
    canvas.drawArc(rect, -pi / 2, 2 * pi * value, false,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 7
          ..strokeCap = StrokeCap.round
          ..color = color);
  }

  @override
  bool shouldRepaint(covariant _RingPainter old) => old.value != value;
}

/// First-launch explanation of how the map works.
Future<void> showWelcome(BuildContext context) {
  return showDialog<void>(
    context: context,
    builder: (ctx) => Dialog(
      backgroundColor: AppColors.paper,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(22, 24, 22, 18),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(child: Text('⛵', style: TextStyle(fontSize: 48))),
            const SizedBox(height: 8),
            const Center(
              child: Text('ICPC yoʻliga xush kelibsiz',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 21, fontWeight: FontWeight.w900, color: AppColors.ink)),
            ),
            const SizedBox(height: 14),
            const _HowRow(emoji: '🗺️', text: '117 ta daraja — ICPC uchun kerak boʻlgan har bir mavzu, asoslardan finalgacha.'),
            const _HowRow(emoji: '👆', text: 'Darajani bosing: nimani oʻrganish kerakligi va 15 ta mashq havolasi ochiladi.'),
            const _HowRow(emoji: '⭐', text: '"Ha, bilaman" — daraja oʻzlashtirildi. "Hali yoʻq" — mashq roʻyxatiga tushadi.'),
            const _HowRow(emoji: '🔓', text: 'Har qanday javob keyingi darajani ochadi. Natijalar telefoningizda saqlanadi.'),
            const SizedBox(height: 10),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: FilledButton(
                style: FilledButton.styleFrom(
                  backgroundColor: AppColors.coral,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
                ),
                onPressed: () => Navigator.of(ctx).pop(),
                child: const Text('Yoʻlga chiqish', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900)),
              ),
            ),
          ],
        ),
      ),
    ),
  );
}

class _HowRow extends StatelessWidget {
  final String emoji;
  final String text;
  const _HowRow({required this.emoji, required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(emoji, style: const TextStyle(fontSize: 20)),
          const SizedBox(width: 10),
          Expanded(
            child: Text(text, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w700, color: AppColors.ink, height: 1.4)),
          ),
        ],
      ),
    );
  }
}
