import 'dart:math';

import 'package:flutter/material.dart';

import '../data/progress_store.dart';
import '../data/topics.dart';

/// Opens the level popup, growing out of the tapped point.
/// Returns true (Yes), false (No) or null (closed).
Future<bool?> showTopicPopup({
  required BuildContext context,
  required int index,
  required LevelStatus status,
  required bool locked,
  required Offset from,
}) {
  final size = MediaQuery.of(context).size;
  final alignment = Alignment(
    (from.dx / size.width) * 2 - 1,
    (from.dy / size.height) * 2 - 1,
  );
  return showGeneralDialog<bool>(
    context: context,
    barrierDismissible: true,
    barrierLabel: 'Close',
    barrierColor: const Color(0x99001F3F),
    transitionDuration: const Duration(milliseconds: 380),
    pageBuilder: (ctx, a1, a2) => TopicCard(index: index, status: status, locked: locked),
    transitionBuilder: (ctx, anim, secondary, child) {
      return FadeTransition(
        opacity: CurvedAnimation(parent: anim, curve: Curves.easeOut),
        child: ScaleTransition(
          alignment: alignment,
          scale: CurvedAnimation(parent: anim, curve: Curves.easeOutBack, reverseCurve: Curves.easeIn),
          child: child,
        ),
      );
    },
  );
}

class TopicCard extends StatelessWidget {
  final int index;
  final LevelStatus status;
  final bool locked;

  const TopicCard({super.key, required this.index, required this.status, required this.locked});

  @override
  Widget build(BuildContext context) {
    final topic = topics[index];
    final stage = stageOf(topic);
    final width = min(MediaQuery.of(context).size.width * 0.9, 440.0);
    final maxHeight = MediaQuery.of(context).size.height * 0.82;

    return Center(
      child: Material(
        color: Colors.transparent,
        child: Container(
          width: width,
          constraints: BoxConstraints(maxHeight: maxHeight),
          decoration: BoxDecoration(
            color: const Color(0xFFFFFBF2),
            borderRadius: BorderRadius.circular(28),
            border: Border.all(color: Colors.white, width: 4),
            boxShadow: const [
              BoxShadow(color: Color(0x55000000), blurRadius: 24, offset: Offset(0, 10)),
            ],
          ),
          clipBehavior: Clip.antiAlias,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _Header(stage: stage, index: index, onClose: () => Navigator.of(context).pop()),
              Flexible(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.fromLTRB(20, 18, 20, 8),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        topic.name,
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.w900,
                          color: Color(0xFF3E2723),
                          height: 1.15,
                        ),
                      ),
                      const SizedBox(height: 8),
                      _StatusChip(status: status, locked: locked),
                      const SizedBox(height: 16),
                      _Section(
                        icon: '📘',
                        title: 'What to learn',
                        body: topic.info,
                        color: stage.color,
                      ),
                      const SizedBox(height: 12),
                      _Section(
                        icon: '🎯',
                        title: 'Where to practice',
                        body: stage.practice,
                        color: const Color(0xFF00897B),
                      ),
                      const SizedBox(height: 12),
                      _Section(
                        icon: '🔎',
                        title: 'Search for',
                        body: '"${topic.name} cp-algorithms"  •  "${topic.name} codeforces"',
                        color: const Color(0xFF5E35B1),
                      ),
                    ],
                  ),
                ),
              ),
              _QuestionArea(topic: topic, locked: locked, index: index),
            ],
          ),
        ),
      ),
    );
  }
}

class _Header extends StatelessWidget {
  final Stage stage;
  final int index;
  final VoidCallback onClose;
  const _Header({required this.stage, required this.index, required this.onClose});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(18, 14, 8, 14),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [stage.color, Color.lerp(stage.color, Colors.black, 0.25)!],
        ),
      ),
      child: Row(
        children: [
          Text(stage.emoji, style: const TextStyle(fontSize: 26)),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'STAGE ${stage.id}  •  LEVEL ${index + 1}',
                  style: const TextStyle(
                    color: Color(0xDDFFFFFF),
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 1.2,
                  ),
                ),
                Text(
                  stage.name,
                  style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w900),
                ),
              ],
            ),
          ),
          IconButton(
            onPressed: onClose,
            icon: const Icon(Icons.close_rounded, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _StatusChip extends StatelessWidget {
  final LevelStatus status;
  final bool locked;
  const _StatusChip({required this.status, required this.locked});

  @override
  Widget build(BuildContext context) {
    late final String text;
    late final Color color;
    if (locked) {
      text = '🔒 Locked';
      color = const Color(0xFF757575);
    } else {
      switch (status) {
        case LevelStatus.done:
          text = '⭐ Mastered';
          color = const Color(0xFFEF6C00);
          break;
        case LevelStatus.practice:
          text = '↻ Needs practice';
          color = const Color(0xFF00838F);
          break;
        case LevelStatus.none:
          text = '✨ New';
          color = const Color(0xFFC2185B);
          break;
      }
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withAlpha(30),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withAlpha(120)),
      ),
      child: Text(text, style: TextStyle(color: color, fontWeight: FontWeight.w800, fontSize: 12)),
    );
  }
}

class _Section extends StatelessWidget {
  final String icon;
  final String title;
  final String body;
  final Color color;
  const _Section({required this.icon, required this.title, required this.body, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withAlpha(22),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withAlpha(60)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('$icon  $title',
              style: TextStyle(fontWeight: FontWeight.w900, color: color, fontSize: 14)),
          const SizedBox(height: 6),
          Text(body, style: const TextStyle(fontSize: 15, height: 1.4, color: Color(0xFF37474F))),
        ],
      ),
    );
  }
}

class _QuestionArea extends StatelessWidget {
  final Topic topic;
  final bool locked;
  final int index;
  const _QuestionArea({required this.topic, required this.locked, required this.index});

  @override
  Widget build(BuildContext context) {
    if (locked) {
      return Container(
        padding: const EdgeInsets.all(18),
        color: const Color(0xFFF1F1F1),
        child: Text(
          'Answer level $index first to unlock this one.',
          textAlign: TextAlign.center,
          style: const TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF616161)),
        ),
      );
    }
    return Container(
      padding: const EdgeInsets.fromLTRB(18, 14, 18, 18),
      decoration: const BoxDecoration(
        color: Color(0xFFFFF3E0),
        border: Border(top: BorderSide(color: Color(0xFFFFE0B2), width: 2)),
      ),
      child: Column(
        children: [
          Text(
            'Can you write or apply "${topic.name}" from memory, bug-free, under contest pressure?',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: Color(0xFF4E342E)),
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: _GameButton(
                  label: 'No, not yet',
                  colors: const [Color(0xFF4DD0E1), Color(0xFF00838F)],
                  onTap: () => Navigator.of(context).pop(false),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _GameButton(
                  label: 'Yes! ⭐',
                  colors: const [Color(0xFFFFCA28), Color(0xFFFF6F00)],
                  onTap: () => Navigator.of(context).pop(true),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _GameButton extends StatelessWidget {
  final String label;
  final List<Color> colors;
  final VoidCallback onTap;
  const _GameButton({required this.label, required this.colors, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 52,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: colors),
          borderRadius: BorderRadius.circular(26),
          border: Border.all(color: Colors.white, width: 3),
          boxShadow: [BoxShadow(color: colors.last.withAlpha(120), blurRadius: 8, offset: const Offset(0, 4))],
        ),
        child: Text(
          label,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 17,
            fontWeight: FontWeight.w900,
            shadows: [Shadow(color: Color(0x55000000), offset: Offset(0, 2), blurRadius: 2)],
          ),
        ),
      ),
    );
  }
}
