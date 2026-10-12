import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../data/progress_store.dart';
import '../data/topics.dart';
import '../map/map_layout.dart';
import '../map/map_painter.dart';
import '../theme.dart';
import '../widgets/confetti.dart';
import '../widgets/hud.dart';
import '../widgets/level_node.dart';
import '../widgets/level_sheet.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final _scroll = ScrollController();
  final _confetti = GlobalKey<ConfettiOverlayState>();
  Map<int, LevelStatus> _progress = {};
  Set<String> _visited = {};
  bool _loaded = false;
  bool _didInitialScroll = false;
  MapLayout? _layout;
  double _viewportHeight = 0;

  static const _nodeBoxW = 90.0;
  static const _nodeBoxH = 100.0;
  static const _nodeFaceCenterY = 52.0;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final p = await ProgressStore.load();
    final v = await ProgressStore.loadVisited();
    final onboarded = await ProgressStore.isOnboarded();
    if (!mounted) return;
    setState(() {
      _progress = p;
      _visited = v;
      _loaded = true;
    });
    if (!onboarded) {
      WidgetsBinding.instance.addPostFrameCallback((_) async {
        if (!mounted) return;
        await showWelcome(context);
        await ProgressStore.setOnboarded();
      });
    }
  }

  @override
  void dispose() {
    _scroll.dispose();
    super.dispose();
  }

  LevelStatus _status(int i) => _progress[i] ?? LevelStatus.none;

  /// A level is open when the previous one has been answered.
  bool _locked(int i) => i > 0 && _status(i - 1) == LevelStatus.none;

  /// First unanswered open level; otherwise the first "practice" level; otherwise the last.
  int get _currentIndex {
    for (var i = 0; i < topics.length; i++) {
      if (_status(i) == LevelStatus.none && !_locked(i)) return i;
    }
    for (var i = 0; i < topics.length; i++) {
      if (_status(i) == LevelStatus.practice) return i;
    }
    return topics.length - 1;
  }

  /// How far the gold wake reaches: the first unanswered level.
  int get _frontier {
    for (var i = 0; i < topics.length; i++) {
      if (_status(i) == LevelStatus.none) return i;
    }
    return topics.length;
  }

  double _offsetFor(int i) {
    final layout = _layout!;
    final fromBottom = layout.height - layout.nodes[i].dy;
    final target = fromBottom - _viewportHeight * 0.42;
    final max = _scroll.hasClients ? _scroll.position.maxScrollExtent : layout.height;
    return target.clamp(0.0, max).toDouble();
  }

  void _scrollTo(int i, {bool animate = true}) {
    if (!_scroll.hasClients || _layout == null) return;
    final offset = _offsetFor(i);
    if (animate && !MediaQuery.of(context).disableAnimations) {
      _scroll.animateTo(offset, duration: const Duration(milliseconds: 750), curve: Curves.easeInOutCubic);
    } else {
      _scroll.jumpTo(offset);
    }
  }

  void _scrollToStage(int stageId) {
    final idx = topics.indexWhere((t) => t.stage == stageId);
    if (idx >= 0) _scrollTo(idx);
  }

  void _markVisited(String url) {
    _visited = {..._visited, url};
    ProgressStore.saveVisited(_visited);
  }

  Future<void> _openLevel(int i, Offset from) async {
    HapticFeedback.lightImpact();
    final answer = await showLevelPopup(
      context: context,
      index: i,
      status: _status(i),
      locked: _locked(i),
      from: from,
      visited: _visited,
      onVisit: _markVisited,
    );
    if (!mounted) return;
    setState(() {}); // refresh visited counts
    if (answer == null) return;

    setState(() {
      _progress = Map.of(_progress)..[i] = answer ? LevelStatus.done : LevelStatus.practice;
    });
    await ProgressStore.save(_progress);
    if (!mounted) return;

    final isLast = i == topics.length - 1;
    final stageDone = answer &&
        [for (var k = 0; k < topics.length; k++) if (topics[k].stage == topics[i].stage) k]
            .every((k) => _status(k) == LevelStatus.done);

    if (answer) _confetti.currentState?.burst(from);

    final messenger = ScaffoldMessenger.of(context);
    messenger.hideCurrentSnackBar();
    messenger.showSnackBar(SnackBar(
      backgroundColor: answer ? AppColors.goldDark : AppColors.tealDark,
      duration: const Duration(milliseconds: 2200),
      content: Text(
        isLast && answer
            ? 'Yoʻl xaritasi tugadi! Endi World Finals 🏆'
            : stageDone
                ? '${stageOf(topics[i]).name} bosqichi toʻliq oʻzlashtirildi ⭐'
                : answer
                    ? '${i + 1}-daraja oʻzlashtirildi'
                    : '${i + 1}-daraja mashq roʻyxatiga qoʻshildi. Oson tuyulganda qayting.',
      ),
    ));

    if (!isLast) {
      Future.delayed(const Duration(milliseconds: 350), () {
        if (mounted) _scrollTo(_currentIndex);
      });
    }
  }

  Future<void> _confirmReset() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.paper,
        title: const Text('Natijalarni tozalaysizmi?', style: TextStyle(fontWeight: FontWeight.w900)),
        content: const Text('Barcha darajalar boshlangʻich holatga qaytadi.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Bekor qilish')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: AppColors.coral),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Tozalash'),
          ),
        ],
      ),
    );
    if (ok != true) return;
    await ProgressStore.clear();
    if (!mounted) return;
    setState(() {
      _progress = {};
      _visited = {};
    });
    _scrollTo(0);
  }

  @override
  Widget build(BuildContext context) {
    if (!_loaded) {
      return const Scaffold(
        backgroundColor: AppColors.lagoon,
        body: Center(child: CircularProgressIndicator(color: Colors.white)),
      );
    }
    final current = _currentIndex;
    return Scaffold(
      backgroundColor: AppColors.lagoon,
      body: LayoutBuilder(builder: (context, constraints) {
        final width = constraints.maxWidth;
        if (_layout == null || _layout!.width != width) {
          _layout = MapLayout(width);
        }
        _viewportHeight = constraints.maxHeight;
        final layout = _layout!;

        if (!_didInitialScroll) {
          _didInitialScroll = true;
          WidgetsBinding.instance.addPostFrameCallback((_) => _scrollTo(current, animate: false));
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
                      child: RepaintBoundary(child: CustomPaint(painter: MapPainter(layout))),
                    ),
                    Positioned.fill(
                      child: RepaintBoundary(child: CustomPaint(painter: RoutePainter(layout, _frontier))),
                    ),
                    ..._islandDecorations(layout),
                    ..._stageSigns(layout),
                    ..._levelNodes(layout, current),
                    _ship(layout, current),
                  ],
                ),
              ),
            ),
            Positioned(
              left: 0,
              right: 0,
              top: 0,
              child: Hud(
                progress: _progress,
                currentStage: topics[current].stage,
                onStageTap: _scrollToStage,
                onReset: _confirmReset,
                onHelp: () => showWelcome(context),
              ),
            ),
            Positioned.fill(child: ConfettiOverlay(key: _confetti)),
          ],
        );
      }),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppColors.deep,
        foregroundColor: Colors.white,
        onPressed: () => _scrollTo(current),
        icon: const Text('⛵', style: TextStyle(fontSize: 20)),
        label: Text('${current + 1}-darajaga',
            style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15)),
      ),
    );
  }

  List<Widget> _islandDecorations(MapLayout layout) {
    final widgets = <Widget>[];
    for (final island in layout.islands) {
      final s = island.radius * 0.72;
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
      top: layout.trophy.dy - 84,
      width: 100,
      height: 100,
      child: const IgnorePointer(
        child: Center(child: Text('🏆', style: TextStyle(fontSize: 62))),
      ),
    ));
    return widgets;
  }

  List<Widget> _stageSigns(MapLayout layout) {
    return [
      for (final sign in layout.signs)
        Positioned(
          left: sign.center.dx - 84,
          top: sign.center.dy - 30,
          width: 168,
          height: 60,
          child: GestureDetector(
            onTap: () => _scrollToStage(sign.stage.id),
            child: Transform.rotate(
              angle: sign.tiltLeft ? -0.04 : 0.04,
              child: _StageSign(stage: sign.stage),
            ),
          ),
        ),
    ];
  }

  List<Widget> _levelNodes(MapLayout layout, int current) {
    return [
      for (var i = 0; i < topics.length; i++)
        Positioned(
          left: layout.nodes[i].dx - _nodeBoxW / 2,
          top: layout.nodes[i].dy - _nodeFaceCenterY,
          width: _nodeBoxW,
          height: _nodeBoxH,
          child: LevelNode(
            key: ValueKey('node$i'),
            index: i,
            status: _status(i),
            locked: _locked(i),
            current: i == current,
            onTap: (pos) => _openLevel(i, pos),
          ),
        ),
    ];
  }

  Widget _ship(MapLayout layout, int current) {
    final node = layout.nodes[current];
    final onLeft = node.dx > layout.width / 2;
    final x = onLeft ? node.dx - 88 : node.dx + 42;
    return AnimatedPositioned(
      duration: const Duration(milliseconds: 900),
      curve: Curves.easeInOutCubic,
      left: x,
      top: node.dy - 30,
      width: 48,
      height: 52,
      child: IgnorePointer(child: ShipMarker(facingLeft: !onLeft)),
    );
  }
}

class _StageSign extends StatelessWidget {
  final Stage stage;
  const _StageSign({required this.stage});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(10, 6, 12, 6),
      decoration: BoxDecoration(
        color: const Color(0xFFB57A45),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFF7A4A22), width: 2.5),
        boxShadow: const [BoxShadow(color: Color(0x4006324A), blurRadius: 6, offset: Offset(0, 4))],
      ),
      child: Row(
        children: [
          Text(stage.emoji, style: const TextStyle(fontSize: 22)),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${stage.id}-bosqich',
                    style: const TextStyle(color: Color(0xFFFFE3BF), fontSize: 11.5, fontWeight: FontWeight.w800)),
                Text(
                  stage.name,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w900),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
