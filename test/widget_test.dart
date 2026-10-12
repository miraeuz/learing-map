import 'package:flutter_test/flutter_test.dart';
import 'package:icpc_quest/data/links.dart';
import 'package:icpc_quest/data/practice_link.dart';
import 'package:icpc_quest/data/topics.dart';
import 'package:icpc_quest/map/map_layout.dart';

void main() {
  test('every topic belongs to a known stage', () {
    for (final t in topics) {
      expect(t.stage, inInclusiveRange(0, stages.length - 1));
    }
  });

  test('every level has 15 practice links with known sites', () {
    expect(topicLinks.length, topics.length);
    for (final links in topicLinks) {
      expect(links.length, 15);
      for (final l in links) {
        expect(siteStyles.containsKey(l.site), isTrue, reason: l.site);
        expect(l.url.startsWith('http'), isTrue);
      }
    }
  });

  test('layout places one node per topic', () {
    final layout = MapLayout(400);
    expect(layout.nodes.length, topics.length);
    expect(layout.signs.length, stages.length);
  });
}
