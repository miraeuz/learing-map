import 'package:flutter_test/flutter_test.dart';
import 'package:icpc_quest/data/topics.dart';
import 'package:icpc_quest/map/map_layout.dart';

void main() {
  test('every topic belongs to a known stage', () {
    for (final t in topics) {
      expect(t.stage, inInclusiveRange(0, stages.length - 1));
    }
  });

  test('layout places one node per topic', () {
    final layout = MapLayout(400);
    expect(layout.nodes.length, topics.length);
    expect(layout.signs.length, stages.length);
  });
}
