import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import '../data/links.dart';
import '../data/practice_link.dart';
import '../data/progress_store.dart';
import '../data/topics.dart';
import '../theme.dart';

/// Opens the level card, growing out of the tapped level point.
/// Returns true ("Ha, bilaman"), false ("Hali yoʻq") or null (closed).
Future<bool?> showLevelPopup({
  required BuildContext context,
  required int index,
  required LevelStatus status,
  required bool locked,
  required Offset from,
  required Set<String> visited,
  required void Function(String url) onVisit,
}) {
  final size = MediaQuery.of(context).size;
  final alignment = Alignment(
    ((from.dx / size.width) * 2 - 1).clamp(-1.0, 1.0),
    ((from.dy / size.height) * 2 - 1).clamp(-1.0, 1.0),
  );
  return showGeneralDialog<bool>(
    context: context,
    barrierDismissible: true,
    barrierLabel: 'Yopish',
    barrierColor: const Color(0x8C06324A),
    transitionDuration: const Duration(milliseconds: 360),
    pageBuilder: (ctx, a1, a2) => LevelCard(
      index: index,
      status: status,
      locked: locked,
      visited: visited,
      onVisit: onVisit,
    ),
    transitionBuilder: (ctx, anim, secondary, child) {
      return FadeTransition(
        opacity: CurvedAnimation(parent: anim, curve: Curves.easeOut),
        child: ScaleTransition(
          alignment: alignment,
          scale: CurvedAnimation(parent: anim, curve: Curves.easeOutBack, reverseCurve: Curves.easeInCubic),
          child: child,
        ),
      );
    },
  );
}

class LevelCard extends StatefulWidget {
  final int index;
  final LevelStatus status;
  final bool locked;
  final Set<String> visited;
  final void Function(String url) onVisit;

  const LevelCard({
    super.key,
    required this.index,
    required this.status,
    required this.locked,
    required this.visited,
    required this.onVisit,
  });

  @override
  State<LevelCard> createState() => _LevelCardState();
}

class _LevelCardState extends State<LevelCard> {
  int _tab = 0;
  late final Set<String> _visited = {...widget.visited};

  List<PracticeLink> get _links => topicLinks[widget.index];

  Future<void> _open(PracticeLink link) async {
    HapticFeedback.selectionClick();
    final ok = await launchUrl(Uri.parse(link.url), mode: LaunchMode.externalApplication);
    if (!mounted) return;
    if (ok) {
      setState(() => _visited.add(link.url));
      widget.onVisit(link.url);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Havolani ochib boʻlmadi: ${link.url}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final topic = topics[widget.index];
    final stage = stageOf(topic);
    final mq = MediaQuery.of(context);
    final width = min(mq.size.width - 24, 460.0);
    final opened = _links.where((l) => _visited.contains(l.url)).length;

    return SafeArea(
      child: Center(
        child: Material(
          color: Colors.transparent,
          child: Container(
            width: width,
            constraints: BoxConstraints(maxHeight: mq.size.height * 0.86),
            decoration: BoxDecoration(
              color: AppColors.paper,
              borderRadius: BorderRadius.circular(30),
              boxShadow: const [
                BoxShadow(color: Color(0x5506324A), blurRadius: 30, offset: Offset(0, 14)),
              ],
            ),
            clipBehavior: Clip.antiAlias,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _Header(stage: stage, index: widget.index, title: topic.name, status: widget.status, locked: widget.locked),
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 14, 16, 4),
                  child: _Tabs(
                    selected: _tab,
                    labels: ['Oʻrganish', 'Masalalar  $opened/${_links.length}'],
                    color: stage.color,
                    onChanged: (i) => setState(() => _tab = i),
                  ),
                ),
                Flexible(
                  child: AnimatedSwitcher(
                    duration: const Duration(milliseconds: 180),
                    child: _tab == 0
                        ? _LearnTab(
                            key: const ValueKey('learn'),
                            info: topic.info,
                            stage: stage,
                            first: _links.first,
                            onOpenFirst: () => _open(_links.first),
                            onShowProblems: () => setState(() => _tab = 1),
                          )
                        : _ProblemsTab(
                            key: const ValueKey('problems'),
                            links: _links,
                            visited: _visited,
                            onOpen: _open,
                          ),
                  ),
                ),
                _AnswerBar(locked: widget.locked, index: widget.index),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _Header extends StatelessWidget {
  final Stage stage;
  final int index;
  final String title;
  final LevelStatus status;
  final bool locked;
  const _Header({required this.stage, required this.index, required this.title, required this.status, required this.locked});

  @override
  Widget build(BuildContext context) {
    final (statusText, statusColor) = switch ((locked, status)) {
      (true, _) => ('Yopiq', AppColors.stoneDark),
      (false, LevelStatus.done) => ('Oʻzlashtirilgan', AppColors.goldDark),
      (false, LevelStatus.practice) => ('Mashq kerak', AppColors.tealDark),
      (false, LevelStatus.none) => ('Yangi', AppColors.coralDark),
    };
    return Container(
      padding: const EdgeInsets.fromLTRB(18, 16, 8, 18),
      color: stage.color,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 52,
            height: 52,
            decoration: const BoxDecoration(color: Color(0x33FFFFFF), shape: BoxShape.circle),
            alignment: Alignment.center,
            child: Text(stage.emoji, style: const TextStyle(fontSize: 26)),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${stage.id}-bosqich: ${stage.name}',
                  style: const TextStyle(color: Color(0xE6FFFFFF), fontSize: 13, fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 2),
                Text(
                  title,
                  style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.w900, height: 1.15),
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    _Chip(text: '${index + 1}-daraja', fg: stage.color, bg: Colors.white),
                    const SizedBox(width: 6),
                    _Chip(text: statusText, fg: Colors.white, bg: statusColor),
                  ],
                ),
              ],
            ),
          ),
          IconButton(
            tooltip: 'Yopish',
            onPressed: () => Navigator.of(context).pop(),
            icon: const Icon(Icons.close_rounded, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _Chip extends StatelessWidget {
  final String text;
  final Color fg;
  final Color bg;
  const _Chip({required this.text, required this.fg, required this.bg});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(20)),
      child: Text(text, style: TextStyle(color: fg, fontSize: 12, fontWeight: FontWeight.w800)),
    );
  }
}

class _Tabs extends StatelessWidget {
  final int selected;
  final List<String> labels;
  final Color color;
  final ValueChanged<int> onChanged;
  const _Tabs({required this.selected, required this.labels, required this.color, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 44,
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: const Color(0xFFF1E6CC),
        borderRadius: BorderRadius.circular(22),
      ),
      child: Row(
        children: [
          for (var i = 0; i < labels.length; i++)
            Expanded(
              child: GestureDetector(
                onTap: () => onChanged(i),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 180),
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: selected == i ? Colors.white : Colors.transparent,
                    borderRadius: BorderRadius.circular(18),
                    boxShadow: selected == i
                        ? const [BoxShadow(color: Color(0x1F5D4A1F), blurRadius: 6, offset: Offset(0, 2))]
                        : null,
                  ),
                  child: Text(
                    labels[i],
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w800,
                      color: selected == i ? color : AppColors.inkSoft,
                    ),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class _LearnTab extends StatelessWidget {
  final String info;
  final Stage stage;
  final PracticeLink first;
  final VoidCallback onOpenFirst;
  final VoidCallback onShowProblems;
  const _LearnTab({
    super.key,
    required this.info,
    required this.stage,
    required this.first,
    required this.onOpenFirst,
    required this.onShowProblems,
  });

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(20, 14, 20, 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Nimani oʻrganish kerak', style: text.titleMedium),
          const SizedBox(height: 6),
          Text(info, style: text.bodyLarge),
          const SizedBox(height: 16),
          _LinkTile(link: first, visited: false, onTap: onOpenFirst, highlight: stage.color),
          const SizedBox(height: 14),
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFFF7EDD6),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('🎯', style: TextStyle(fontSize: 20)),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Masalalar boʻlimidan kamida 5 tasini yechib koʻring. Hammasi oson tuyulsa, "Ha, bilaman" ni bosing.',
                        style: text.bodyMedium,
                      ),
                      const SizedBox(height: 6),
                      GestureDetector(
                        onTap: onShowProblems,
                        child: Text(
                          'Masalalarni koʻrish',
                          style: TextStyle(color: stage.color, fontWeight: FontWeight.w900, fontSize: 14),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ProblemsTab extends StatelessWidget {
  final List<PracticeLink> links;
  final Set<String> visited;
  final void Function(PracticeLink) onOpen;
  const _ProblemsTab({super.key, required this.links, required this.visited, required this.onOpen});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 12),
      shrinkWrap: true,
      itemCount: links.length,
      separatorBuilder: (_, __) => const SizedBox(height: 8),
      itemBuilder: (context, i) {
        final link = links[i];
        return _LinkTile(link: link, visited: visited.contains(link.url), onTap: () => onOpen(link));
      },
    );
  }
}

class _LinkTile extends StatelessWidget {
  final PracticeLink link;
  final bool visited;
  final VoidCallback onTap;
  final Color? highlight;
  const _LinkTile({required this.link, required this.visited, required this.onTap, this.highlight});

  @override
  Widget build(BuildContext context) {
    final style = link.style;
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(16),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.fromLTRB(10, 10, 12, 10),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: highlight ?? const Color(0xFFEFE3C6), width: highlight == null ? 1.5 : 2),
          ),
          child: Row(
            children: [
              Container(
                width: 46,
                height: 36,
                alignment: Alignment.center,
                decoration: BoxDecoration(color: style.color, borderRadius: BorderRadius.circular(10)),
                child: Text(
                  style.badge,
                  style: const TextStyle(color: Colors.white, fontSize: 11.5, fontWeight: FontWeight.w900),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      link.title,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: visited ? AppColors.inkSoft : AppColors.ink,
                        height: 1.2,
                      ),
                    ),
                    Text(
                      style.name,
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: AppColors.inkSoft),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              visited
                  ? const Icon(Icons.check_circle_rounded, color: AppColors.teal, size: 22)
                  : const Icon(Icons.open_in_new_rounded, color: AppColors.stoneDark, size: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class _AnswerBar extends StatelessWidget {
  final bool locked;
  final int index;
  const _AnswerBar({required this.locked, required this.index});

  @override
  Widget build(BuildContext context) {
    if (locked) {
      return Container(
        padding: const EdgeInsets.fromLTRB(20, 16, 20, 18),
        color: const Color(0xFFF1E6CC),
        child: Text(
          'Bu darajani ochish uchun avval $index-darajaga javob bering.',
          textAlign: TextAlign.center,
          style: const TextStyle(fontWeight: FontWeight.w800, color: AppColors.inkSoft, fontSize: 14),
        ),
      );
    }
    return Container(
      padding: const EdgeInsets.fromLTRB(16, 14, 16, 16),
      decoration: const BoxDecoration(
        color: Color(0xFFF7EDD6),
        border: Border(top: BorderSide(color: Color(0xFFEBDDBA), width: 1.5)),
      ),
      child: Column(
        children: [
          const Text(
            'Buni kontestda yoddan, xatosiz yoza olasizmi?',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 15, fontWeight: FontWeight.w900, color: AppColors.ink),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _PushButton(
                  label: 'Hali yoʻq',
                  face: Colors.white,
                  rim: const Color(0xFFD9CBA6),
                  textColor: AppColors.tealDark,
                  onTap: () => Navigator.of(context).pop(false),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _PushButton(
                  label: 'Ha, bilaman',
                  face: AppColors.coral,
                  rim: AppColors.coralDark,
                  textColor: Colors.white,
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

/// A chunky 3D button that sinks when pressed, matching the level buttons.
class _PushButton extends StatefulWidget {
  final String label;
  final Color face;
  final Color rim;
  final Color textColor;
  final VoidCallback onTap;
  const _PushButton({required this.label, required this.face, required this.rim, required this.textColor, required this.onTap});

  @override
  State<_PushButton> createState() => _PushButtonState();
}

class _PushButtonState extends State<_PushButton> {
  bool _down = false;

  @override
  Widget build(BuildContext context) {
    const depth = 5.0;
    return Semantics(
      button: true,
      label: widget.label,
      child: GestureDetector(
        onTapDown: (_) => setState(() => _down = true),
        onTapCancel: () => setState(() => _down = false),
        onTapUp: (_) {
          setState(() => _down = false);
          HapticFeedback.mediumImpact();
          widget.onTap();
        },
        child: SizedBox(
          height: 52 + depth,
          child: Stack(
            children: [
              Positioned(
                left: 0,
                right: 0,
                bottom: 0,
                height: 52,
                child: DecoratedBox(
                  decoration: BoxDecoration(color: widget.rim, borderRadius: BorderRadius.circular(18)),
                ),
              ),
              AnimatedPositioned(
                duration: const Duration(milliseconds: 60),
                left: 0,
                right: 0,
                top: _down ? depth - 1 : 0,
                height: 52,
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(color: widget.face, borderRadius: BorderRadius.circular(18)),
                  child: Text(
                    widget.label,
                    style: TextStyle(color: widget.textColor, fontSize: 17, fontWeight: FontWeight.w900),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
