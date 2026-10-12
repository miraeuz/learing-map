import 'package:flutter/material.dart';

import '../data/progress_store.dart';
import '../data/topics.dart';
import '../map/map_layout.dart';
import '../map/map_painter.dart';
import '../widgets/level_node.dart';
import '../widgets/topic_card.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final _scroll = ScrollController();
  Map<int, LevelStatus> _progress = {};
  bool _loaded = false;
  bool _didInitialScroll = false;
  MapLayout? _layout;
  double _viewportHeight = 0;

  @override
  void initState() {
    super.initState();
    ProgressStore.load().then((p) {
      if (!mounted) return;
      setState(() {
        _progress = p;
        _loaded = true;
      });
    });
  }

  @override
  void dispose() {
    _scroll.dispose();
    super.dispose();
  }

  LevelStatus _status(int i) => _progress[i] ?? LevelStatus.none;

  /// A level is open when the previous one has been answered (Yes or No).
  bool _locked(int i) => i > 0 && _status(i - 1) == LevelStatus.none;

  /// The frontier: first unanswered open level; otherwise the first
  /// "needs practice" level; otherwise the last level.
  int get _currentIndex {
    for (var i = 0; i < topics.length; i++) {
      if (_status(i) == LevelStatus.none && !_locked(i)) return i;
    }
    for (var i = 0; i < topics.length; i++) {
      if (_status(i) == LevelStatus.practice) return i;
    }
    return topics.length - 1;
  }

  int get _doneCount => _progress.values.where((s) => s == LevelStatus.done).length;
  int get _practiceCount => _progress.values.where((s) => s == LevelStatus.practice).length;

  double _offsetFor(int i) {
    final layout = _layout!;
    final fromBottom = layout.height - layout.nodes[i].dy;
    final target = fromBottom - _viewportHeight / 2;
    final max = _scroll.hasClients ? _scroll.position.maxScrollExtent : layout.height;
    return target.clamp(0.0, max).toDouble();
  }

  void _scrollTo(int i, {bool animate = true}) {
    if (!_scroll.hasClients || _layout == null) return;
    final offset = _offsetFor(i);
    if (animate) {
      _scroll.animateTo(offset, duration: const Duration(milliseconds: 700), curve: Curves.easeInOutCubic);
    } else {
      _scroll.jumpTo(offset);
    }
  }

  Future<void> _openLevel(int i, Offset from) async {
    final answer = await showTopicPopup(
      context: context,
      index: i,
      status: _status(i),
      locked: _locked(i),
      from: from,
    );
    if (answer == null || !mounted) return;

    setState(() {
      _progress = Map.of(_progress)..[i] = answer ? LevelStatus.done : LevelStatus.practice;
    });
    await ProgressStore.save(_progress);
    if (!mounted) return;

    final messenger = ScaffoldMessenger.of(context);
    messenger.hideCurrentSnackBar();
    final isLast = i == topics.length - 1;
    messenger.showSnackBar(SnackBar(
      behavior: SnackBarBehavior.floating,
      backgroundColor: answer ? const Color(0xFFEF6C00) : const Color(0xFF00838F),
      duration: const Duration(milliseconds: 1800),
      content: Text(
        answer
            ? (isLast ? '🏆 Roadmap complete! See you at the World Finals!' : '⭐⭐⭐ Level ${i + 1} mastered!')
            : '💪 Marked for practice. Come back when it feels easy.',
        style: const TextStyle(fontWeight: FontWeight.w800),
      ),
    ));

    if (!isLast) {
      Future.delayed(const Duration(milliseconds: 250), () {
        if (mounted) _scrollTo(i + 1);
      });
    }
  }

  Future<void> _confirmReset() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Reset progress?'),
        content: const Text('All levels will go back to the start.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Reset')),
        ],
      ),
    );
    if (ok != true) return;
    await ProgressStore.clear();
    if (!mounted) return;
    setState(() => _progress = {});
    _scrollTo(0);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF3CC8EC),
      body: !_loaded
          ? const Center(child: CircularProgressIndicator(color: Colors.white))
          : LayoutBuilder(builder: (context, constraints) {
              final width = constraints.maxWidth;
              if (_layout == null || _layout!.width != width) {
                _layout = MapLayout(width);
              }
              _viewportHeight = constraints.maxHeight;
              final layout = _layout!;

              if (!_didInitialScroll) {
                _didInitialScroll = true;
                WidgetsBinding.instance.addPostFrameCallback((_) => _scrollTo(_currentIndex, animate: false));
              }

              return Stack(
                children: [
                  SingleChildScrollView(
                    controller: _scroll,
                    reverse: true,
                    child: SizedBox(
                      width: width,
                      height: layout.height,
                      child: Stack(
                        clipBehavior: Clip.none,
                        children: [
                          Positioned.fill(
                            child: RepaintBoundary(
                              child: CustomPaint(painter: MapPainter(layout)),
                            ),
                          ),
                          ..._islandDecorations(layout),
                          ..._stageSigns(layout),
                          ..._levelNodes(layout),
                        ],
                      ),
                    ),
                  ),
                  _TopBar(
                    done: _doneCount,
                    practice: _practiceCount,
                    total: topics.length,
                    stageName: stageOf(topics[_currentIndex]).name,
                    onReset: _confirmReset,
                  ),
                ],
              );
            }),
      floatingActionButton: _loaded
          ? FloatingActionButton.extended(
              backgroundColor: const Color(0xFFFF8F00),
              foregroundColor: Colors.white,
              onPressed: () => _scrollTo(_currentIndex),
              icon: const Icon(Icons.my_location_rounded),
              label: Text('Level ${_currentIndex + 1}', style: const TextStyle(fontWeight: FontWeight.w900)),
            )
          : null,
    );
  }

  List<Widget> _islandDecorations(MapLayout layout) {
    final widgets = <Widget>[];
    for (final island in layout.islands) {
      final s = island.radius * 0.75;
      widgets.add(Positioned(
        left: island.center.dx - s,
        top: island.center.dy - s * 1.25,
        width: s * 2,
        height: s * 2,
        child: IgnorePointer(
          child: Center(child: Text(island.emoji, style: TextStyle(fontSize: s))),
        ),
      ));
    }
    widgets.add(Positioned(
      left: layout.trophy.dx - 50,
      top: layout.trophy.dy - 80,
      width: 100,
      height: 100,
      child: const IgnorePointer(
        child: Center(child: Text('🏆', style: TextStyle(fontSize: 64))),
      ),
    ));
    return widgets;
  }

  List<Widget> _stageSigns(MapLayout layout) {
    return [
      for (final sign in layout.signs)
        Positioned(
          left: sign.center.dx - 82,
          top: sign.center.dy - 30,
          width: 164,
          height: 60,
          child: IgnorePointer(
            child: Transform.rotate(
              angle: sign.tiltLeft ? -0.05 : 0.05,
              child: _WoodSign(stage: sign.stage),
            ),
          ),
        ),
    ];
  }

  List<Widget> _levelNodes(MapLayout layout) {
    final current = _currentIndex;
    const box = 90.0;
    return [
      for (var i = 0; i < topics.length; i++)
        Positioned(
          left: layout.nodes[i].dx - box / 2,
          top: layout.nodes[i].dy - box / 2,
          width: box,
          height: box,
          child: Center(
            child: LevelNode(
              index: i,
              status: _status(i),
              locked: _locked(i),
              current: i == current,
              onTap: (pos) => _openLevel(i, pos),
            ),
          ),
        ),
    ];
  }
}

class _WoodSign extends StatelessWidget {
  final Stage stage;
  const _WoodSign({required this.stage});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFFC98B4E), Color(0xFF8D5A2B)],
        ),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF5D3A1A), width: 2.5),
        boxShadow: const [BoxShadow(color: Color(0x55000000), blurRadius: 6, offset: Offset(0, 3))],
      ),
      child: Row(
        children: [
          Text(stage.emoji, style: const TextStyle(fontSize: 22)),
          const SizedBox(width: 6),
          Expanded(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('STAGE ${stage.id}',
                    style: const TextStyle(
                        color: Color(0xFFFFE0B2), fontSize: 10, fontWeight: FontWeight.w900, letterSpacing: 1)),
                Text(
                  stage.name,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w900),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _TopBar extends StatelessWidget {
  final int done;
  final int practice;
  final int total;
  final String stageName;
  final VoidCallback onReset;

  const _TopBar({
    required this.done,
    required this.practice,
    required this.total,
    required this.stageName,
    required this.onReset,
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Container(
        margin: const EdgeInsets.fromLTRB(12, 8, 12, 0),
        padding: const EdgeInsets.fromLTRB(16, 10, 6, 12),
        decoration: BoxDecoration(
          color: const Color(0xEEFFFBF2),
          borderRadius: BorderRadius.circular(22),
          border: Border.all(color: Colors.white, width: 3),
          boxShadow: const [BoxShadow(color: Color(0x33000000), blurRadius: 12, offset: Offset(0, 4))],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                const Text('🏝️', style: TextStyle(fontSize: 24)),
                const SizedBox(width: 8),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('ICPC Quest',
                          style: TextStyle(fontSize: 19, fontWeight: FontWeight.w900, color: Color(0xFF3E2723))),
                      Text('Now: $stageName',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: Color(0xFF8D6E63))),
                    ],
                  ),
                ),
                _Pill(text: '⭐ $done', color: const Color(0xFFEF6C00)),
                const SizedBox(width: 6),
                _Pill(text: '↻ $practice', color: const Color(0xFF00838F)),
                PopupMenuButton<String>(
                  icon: const Icon(Icons.more_vert_rounded, color: Color(0xFF5D4037)),
                  onSelected: (v) {
                    if (v == 'reset') onReset();
                  },
                  itemBuilder: (_) => const [
                    PopupMenuItem(value: 'reset', child: Text('Reset progress')),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 8),
            Padding(
              padding: const EdgeInsets.only(right: 10),
              child: Row(
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: LinearProgressIndicator(
                        value: total == 0 ? 0 : done / total,
                        minHeight: 12,
                        backgroundColor: const Color(0xFFFFE0B2),
                        valueColor: const AlwaysStoppedAnimation(Color(0xFFFF8F00)),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Text('$done / $total',
                      style: const TextStyle(fontWeight: FontWeight.w900, color: Color(0xFF5D4037))),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Pill extends StatelessWidget {
  final String text;
  final Color color;
  const _Pill({required this.text, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withAlpha(30),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Text(text, style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 13)),
    );
  }
}
