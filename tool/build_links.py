"""Builds lib/data/links.dart: 15 practice links per level.

Every link comes from a source verified in this session:
- cp-algorithms articles + their practice lists (cloned from GitHub)
- CSES task IDs (read from cses.fi/problemset)
- acmp.ru task IDs (read from the acmp.ru archive)
- LeetCode slugs (checked against kamyu104/LeetCode-Solutions file names)
- Library Checker slugs (checked against yosupo06/library-checker-problems)
- AtCoder Educational DP + Library Practice contests (fixed task ids)
"""
import json, re, sys
from urllib.parse import quote

D = '/home/claude/data/'
cpa = json.load(open(D + 'cpa_links.json'))
cpa_articles = set(cpa.keys())
lc_slugs = set(open(D + 'lc_slugs.txt').read().split())
lc_rows = {r['u'].rstrip('/').split('/')[-1]: r for r in json.load(open(D + 'lc.json'))}
ys_slugs = set(open(D + 'yosupo.txt').read().split())

ATC_DP = dict(a='Frog 1', b='Frog 2', c='Vacation', d='Knapsack 1', e='Knapsack 2', f='LCS',
              g='Longest Path', h='Grid 1', i='Coins', j='Sushi', k='Stones', l='Deque',
              m='Candies', n='Slimes', o='Matching', p='Independent Set', q='Flowers', r='Walk',
              s='Digit Sum', t='Permutation', u='Grouping', v='Subtree', w='Intervals',
              x='Tower', y='Grid 2', z='Frog 3')
ATC_PR = dict(a='Disjoint Set Union', b='Fenwick Tree', c='Floor Sum', d='Maxflow',
              e='MinCostFlow', f='Convolution', g='SCC', h='Two SAT', i='Number of Substrings',
              j='Segment Tree', k='Range Affine Range Sum', l='Lazy Segment Tree')

# fmt: off
# One spec per topic, in the same order as lib/data/topics.dart.
S = [
 # ---- Stage 0
 dict(cpa=['data_structures/stack_queue_modification'], cses=[(1621,'Distinct Numbers'),(1091,'Concert Tickets'),(1164,'Room Allocation'),(2162,'Josephus Problem I')], acmp=[(82,'Пересечение множеств'),(216,'Коллекционирование этикеток')], lc=['two-sum','top-k-frequent-elements','lru-cache','valid-parentheses'], ys=['associative_array','double_ended_priority_queue'], cf=['data structures']),
 dict(cses=[(1084,'Apartments'),(1090,'Ferris Wheel'),(1074,'Stick Lengths'),(1629,'Movie Festival')], acmp=[(5,'Статистика'),(119,'Сортировка времени'),(41,'Сортировка подсчетом')], lc=['sort-colors','merge-intervals','largest-number','sort-an-array'], cf=['sortings']),
 dict(cpa=['num_methods/binary_search'], cses=[(1091,'Concert Tickets'),(1640,'Sum of Two Values'),(1073,'Towers'),(1163,'Traffic Lights')], acmp=[(267,'Ксерокопии')], lc=['search-insert-position','find-first-and-last-position-of-element-in-sorted-array','time-based-key-value-store'], ys=['predecessor_problem'], cf=['binary search']),
 dict(cses=[(1068,'Weird Algorithm'),(1083,'Missing Number'),(1094,'Increasing Array'),(1071,'Number Spiral')], acmp=[(1,'A+B'),(103,'Снова A+B'),(144,'A*B')], lc=['reverse-integer','string-to-integer-atoi','add-binary'], ys=['many_aplusb','aplusb'], cf=['implementation']),
 dict(cses=[(1069,'Repetitions'),(1092,'Two Sets'),(1617,'Bit Strings'),(1618,'Trailing Zeros')], acmp=[(2,'Сумма'),(147,'Числа Фибоначчи')], lc=['count-primes','power-of-two','climbing-stairs'], cf=['brute force','math']),
 dict(cses=[(1622,'Creating Strings'),(1623,'Apple Division'),(1624,'Chessboard and Queens'),(1625,'Grid Path Description')], acmp=[(16,'Лесенка'),(101,'Магараджа'),(350,'Перестановки')], lc=['permutations','subsets','n-queens','sudoku-solver','combination-sum'], cf=['brute force']),
 dict(cses=[(1629,'Movie Festival'),(1630,'Tasks and Deadlines'),(2183,'Missing Coin Sum'),(1632,'Movie Festival II')], acmp=[(39,'Волосатый бизнес'),(228,'Валютные махинации'),(237,'Головоломка')], lc=['jump-game','gas-station','non-overlapping-intervals','task-scheduler','candy'], cf=['greedy']),
 dict(cpa=['num_methods/binary_search'], cses=[(1620,'Factory Machines'),(1085,'Array Division')], acmp=[(267,'Ксерокопии')], lc=['binary-search','sqrtx','search-in-rotated-sorted-array','find-minimum-in-rotated-sorted-array'], cf=['binary search']),
 dict(cses=[(3151,'Bubble Sort Rounds I'),(1162,'Sorting Methods')], lc=['sort-list','count-of-smaller-numbers-after-self','reverse-pairs','merge-sorted-array'], ys=['static_range_inversions_query'], spoj=[('INVCNT','Inversion Count')], cf=['divide and conquer','sortings']),
 dict(cses=[(1646,'Static Range Sum Queries'),(1661,'Subarray Sums II'),(1662,'Subarray Divisibility'),(1652,'Forest Queries'),(1660,'Subarray Sums I')], acmp=[(284,'Подмассив массива')], lc=['range-sum-query-immutable','subarray-sum-equals-k','product-of-array-except-self','range-sum-query-2d-immutable'], ys=['static_range_sum'], cf=['implementation']),
 dict(cpa=['graph/search-for-connected-components'], cses=[(1666,'Building Roads'),(1192,'Counting Rooms'),(1667,'Message Route')], acmp=[(15,'Дороги'),(124,'Светофорчики'),(125,'Цветной дождь')], lc=['find-the-town-judge','find-center-of-star-graph','clone-graph'], cf=['graphs']),
 dict(cpa=['graph/depth-first-search'], cses=[(1192,'Counting Rooms'),(1666,'Building Roads'),(1669,'Round Trip'),(1674,'Subordinates')], acmp=[(97,'Заповедники'),(137,'Существование пути')], lc=['number-of-islands','max-area-of-island','surrounded-regions','all-paths-from-source-to-target'], cf=['dfs and similar']),
 dict(cpa=['graph/breadth-first-search'], cses=[(1193,'Labyrinth'),(1667,'Message Route'),(1194,'Monsters')], acmp=[(99,'Лабиринт'),(128,'Один конь'),(130,'Два коня')], lc=['rotting-oranges','shortest-path-in-binary-matrix','word-ladder','01-matrix'], cf=['graphs','shortest paths']),
 dict(cpa=['graph/bipartite-check','graph/finding-cycle'], cses=[(1668,'Building Teams'),(1669,'Round Trip'),(1678,'Round Trip II')], lc=['is-graph-bipartite','possible-bipartition','course-schedule','find-eventual-safe-states'], ys=['cycle_detection','cycle_detection_undirected'], cf=['dfs and similar']),
 dict(cpa=['graph/dijkstra'], cses=[(1671,'Shortest Routes I'),(1195,'Flight Discount'),(1196,'Flight Routes'),(1202,'Investigation')], acmp=[(132,'Алгоритм Дейкстры'),(133,'Заправки'),(134,'Автобусы')], lc=['network-delay-time','path-with-minimum-effort','cheapest-flights-within-k-stops'], ys=['shortest_path'], cf=['shortest paths']),
 dict(cpa=['data_structures/disjoint_set_union'], cses=[(1676,'Road Construction'),(1675,'Road Reparation')], lc=['redundant-connection','accounts-merge','satisfiability-of-equality-equations','number-of-operations-to-make-network-connected'], atc=[('practice2','a')], ys=['unionfind','unionfind_with_potential'], cf=['dsu']),
 dict(cpa=['graph/topological-sort'], cses=[(1679,'Course Schedule'),(1680,'Longest Flight Route'),(1681,'Game Routes'),(1757,'Course Schedule II')], lc=['course-schedule-ii','sort-items-by-groups-respecting-dependencies','find-all-possible-recipes-from-given-supplies'], atc=[('dp','g')], cf=['graphs']),
 dict(cpa=['dynamic_programming/knapsack'], cses=[(1158,'Book Shop'),(1745,'Money Sums'),(1093,'Two Sets II')], lc=['partition-equal-subset-sum','target-sum','ones-and-zeroes','last-stone-weight-ii'], atc=[('dp','d'),('dp','e')], cf=['dp']),
 dict(cpa=['dynamic_programming/intro-to-dp'], cses=[(1634,'Minimizing Coins'),(1635,'Coin Combinations I'),(1636,'Coin Combinations II'),(1633,'Dice Combinations')], acmp=[(153,'Монетки - 2')], lc=['coin-change','combination-sum-iv','perfect-squares','minimum-cost-for-tickets'], atc=[('dp','a'),('dp','b')], cf=['dp']),
 dict(cpa=['dynamic_programming/longest_increasing_subsequence'], cses=[(1145,'Increasing Subsequence'),(1748,'Increasing Subsequence II')], acmp=[(122,'Максимальная подпоследовательность')], lc=['longest-increasing-subsequence','russian-doll-envelopes','number-of-longest-increasing-subsequence'], ys=['longest_increasing_subsequence'], cf=['dp']),
 dict(cses=[(1639,'Edit Distance'),(3403,'Longest Common Subsequence')], lc=['longest-common-subsequence','edit-distance','delete-operation-for-two-strings','distinct-subsequences'], atc=[('dp','f')], ys=['longest_common_substring'], cf=['dp','strings']),
 dict(cpa=['others/maximum_average_segment'], cses=[(1643,'Maximum Subarray Sum'),(1644,'Maximum Subarray Sum II')], lc=['maximum-subarray','maximum-sum-circular-subarray','maximum-product-subarray','best-time-to-buy-and-sell-stock'], cf=['dp']),
 dict(cpa=['algebra/sieve-of-eratosthenes','algebra/binary-exp','algebra/euclid-algorithm'], cses=[(1095,'Exponentiation'),(1713,'Counting Divisors'),(1081,'Common Divisors'),(1712,'Exponentiation II')], acmp=[(14,'НОК'),(148,'НОД'),(349,'Простые числа')], lc=['count-primes','powx-n'], cf=['number theory']),
 # ---- Stage 1
 dict(cses=[(1651,'Range Update Queries'),(1652,'Forest Queries'),(1646,'Static Range Sum Queries')], lc=['corporate-flight-bookings','car-pooling','stamping-the-grid'], lcnote=['Difference Array','Prefix Sum'], ys=['static_rectangle_add_rectangle_sum'], cf=['data structures']),
 dict(cpa=['data_structures/stack_queue_modification'], cses=[(1640,'Sum of Two Values'),(1641,'Sum of Three Values'),(1141,'Playlist'),(3221,'Sliding Window Minimum'),(1645,'Nearest Smaller Values')], acmp=[(245,'Сплоченная команда')], lc=['sliding-window-maximum','longest-substring-without-repeating-characters','container-with-most-water','minimum-window-substring','largest-rectangle-in-histogram'], cf=['two pointers']),
 dict(cpa=['num_methods/binary_search'], cses=[(1620,'Factory Machines'),(1085,'Array Division'),(2422,'Multiplication Table')], acmp=[(267,'Ксерокопии')], lc=['koko-eating-bananas','capacity-to-ship-packages-within-d-days','split-array-largest-sum','magnetic-force-between-two-balls'], cf=['binary search']),
 dict(cpa=['num_methods/ternary_search'], cf=['ternary search']),
 dict(cpa=['algebra/bit-manipulation','algebra/all-submasks'], cses=[(1146,'Counting Bits'),(1655,'Maximum Xor Subarray'),(1623,'Apple Division')], lc=['single-number','counting-bits','number-of-1-bits','sum-of-two-integers','maximum-xor-of-two-numbers-in-an-array'], cf=['bitmasks']),
 dict(cses=[(1628,'Meet in the Middle'),(1642,'Sum of Four Values')], lc=['closest-subsequence-sum','partition-array-into-two-arrays-to-minimize-sum-difference','4sum-ii'], cf=['meet-in-the-middle']),
 dict(cses=[(1144,'Salary Queries'),(1619,'Restaurant Customers'),(2169,'Nested Ranges Count')], lc=['count-of-range-sum','count-of-smaller-numbers-after-self'], lcnote=['Coordinate Compression'], cf=['sortings','data structures']),
 # ---- Stage 2
 dict(cpa=['data_structures/segment_tree'], cses=[(1735,'Range Updates and Sums'),(1736,'Polynomial Queries'),(1143,'Hotel Queries'),(2166,'Prefix Sum Queries'),(1190,'Subarray Sum Queries')], atc=[('practice2','j'),('practice2','k'),('practice2','l')], ys=['range_affine_range_sum','point_set_range_composite'], lc=['range-sum-query-mutable','my-calendar-iii','falling-squares'], cf=['data structures']),
 dict(cpa=['data_structures/fenwick'], cses=[(1648,'Dynamic Range Sum Queries'),(1651,'Range Update Queries'),(1739,'Forest Queries II'),(1144,'Salary Queries')], atc=[('practice2','b')], ys=['point_add_range_sum','point_add_rectangle_sum'], lc=['range-sum-query-mutable','create-sorted-array-through-instructions'], cf=['data structures']),
 dict(cpa=['data_structures/sparse-table','sequences/rmq'], cses=[(1647,'Static Range Minimum Queries')], ys=['staticrmq'], cf=['data structures']),
 dict(cpa=['data_structures/deleting_in_log_n'], cses=[(2133,'Dynamic Connectivity'),(2101,'New Roads Queries')], ys=['dynamic_graph_vertex_add_component_sum','persistent_unionfind'], cf=['dsu','divide and conquer']),
 dict(cpa=['data_structures/segment_tree'], cses=[(1737,'Range Queries and Copies')], ys=['range_kth_smallest','persistent_range_affine_range_sum','persistent_queue'], spoj=[('MKTHNUM','K-th Number'),('COT','Count on a tree')], lcnote=['Persistent Segment Tree'], cf=['data structures']),
 dict(cses=[(1144,'Salary Queries'),(3163,'Range Interval Queries')], ys=['range_kth_smallest','static_range_frequency','static_range_count_distinct'], spoj=[('KQUERY','K-query'),('MKTHNUM','K-th Number')], cf=['data structures']),
 dict(cpa=['data_structures/treap'], cses=[(2072,'Cut and Paste'),(2073,'Substring Reversals'),(2074,'Reversals and Sums')], ys=['dynamic_sequence_range_affine_range_sum','range_reverse_range_sum','ordered_set'], cf=['data structures']),
 dict(cpa=['data_structures/sqrt_decomposition'], cses=[(1734,'Distinct Values Queries')], ys=['static_range_mode_query','static_range_inversions_query'], spoj=[('DQUERY','D-query')], lcnote=["Mo's Algorithm", 'Sqrt Decomposition'], cf=['data structures']),
 dict(ys=['range_chmin_chmax_add_range_sum'], cses=[(1735,'Range Updates and Sums')], cf=['data structures']),
 dict(cpa=['geometry/convex_hull_trick'], cses=[(3429,'Lines and Queries I'),(3430,'Lines and Queries II')], ys=['line_add_get_min','segment_add_get_min'], cf=['data structures','geometry']),
 dict(cses=[(2162,'Josephus Problem I'),(2163,'Josephus Problem II'),(1749,'List Removals'),(1076,'Sliding Window Median')], lc=['count-of-smaller-numbers-after-self','sliding-window-median'], ys=['ordered_set'], cf=['data structures']),
 # ---- Stage 3
 dict(cpa=['graph/01_bfs'], lc=['minimum-cost-to-make-at-least-one-valid-path-in-a-grid','minimum-obstacle-removal-to-reach-corner'], cf=['shortest paths']),
 dict(cpa=['graph/all-pair-shortest-path-floyd-warshall','graph/bellman_ford','graph/finding-negative-cycle-in-graph'], cses=[(1672,'Shortest Routes II'),(1673,'High Score'),(1197,'Cycle Finding')], acmp=[(135,'Алгоритм Флойда'),(138,'Алгоритм Форда-Беллмана'),(140,'Цикл отрицательного веса')], lc=['find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance'], cf=['shortest paths']),
 dict(cpa=['graph/strongly-connected-components'], cses=[(1682,'Flight Routes Check'),(1683,'Planets and Kingdoms'),(1686,'Coin Collector')], atc=[('practice2','g')], ys=['scc','incremental_scc'], cf=['graphs','dfs and similar']),
 dict(cpa=['graph/bridge-searching','graph/cutpoints'], cses=[(2076,'Necessary Roads'),(2077,'Necessary Cities')], lc=['critical-connections-in-a-network','minimum-number-of-days-to-disconnect-island'], ys=['two_edge_connected_components','biconnected_components'], cf=['graphs']),
 dict(cpa=['graph/2SAT'], cses=[(1684,'Giant Pizza')], atc=[('practice2','h')], ys=['two_sat'], cf=['2-sat']),
 dict(cpa=['graph/mst_kruskal','graph/mst_prim'], cses=[(1675,'Road Reparation'),(3407,'MST Edge Check'),(3409,'MST Edge Cost')], acmp=[(142,'Минимальный каркас')], lc=['min-cost-to-connect-all-points','find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree'], ys=['minimum_spanning_tree','directedmst'], cf=['graphs','dsu']),
 dict(cpa=['graph/euler_path'], cses=[(1691,'Mail Delivery'),(1693,'Teleporters Path'),(1692,'De Bruijn Sequence')], lc=['reconstruct-itinerary','valid-arrangement-of-pairs','cracking-the-safe'], ys=['eulerian_trail_directed','eulerian_trail_undirected'], cf=['graphs']),
 dict(cpa=['graph/dinic','graph/edmonds_karp'], cses=[(1694,'Download Speed'),(1711,'Distinct Routes')], atc=[('practice2','d')], spoj=[('FASTFLOW','Fast Maximum Flow')], cf=['flows']),
 dict(cpa=['graph/edmonds_karp'], cses=[(1695,'Police Chase'),(1694,'Download Speed')], atc=[('practice2','d')], cf=['flows']),
 dict(cpa=['graph/min_cost_flow','graph/Assignment-problem-min-flow'], cses=[(2129,'Task Assignment'),(2121,'Parcel Delivery'),(2130,'Distinct Routes II')], atc=[('practice2','e')], ys=['min_cost_b_flow'], lcnote=['Min-Cost Max-Flow'], cf=['flows']),
 dict(cpa=['graph/kuhn_maximum_bipartite_matching','graph/hungarian-algorithm'], cses=[(1696,'School Dance'),(2129,'Task Assignment')], ys=['bipartitematching','assignment'], lcnote=['Hungarian Weighted Bipartite Matching'], cf=['graph matchings']),
 dict(cpa=['graph/kuhn_maximum_bipartite_matching'], cses=[(1696,'School Dance')], ys=['bipartitematching','maximum_independent_set'], cf=['graph matchings','flows']),
 dict(cpa=['graph/flow_with_demands'], ys=['min_cost_b_flow'], cf=['flows']),
 # ---- Stage 4
 dict(cpa=['graph/lca','graph/lca_binary_lifting'], cses=[(1688,'Company Queries II'),(1135,'Distance Queries'),(1687,'Company Queries I')], ys=['lca','jump_on_tree'], lc=['lowest-common-ancestor-of-a-binary-tree','kth-ancestor-of-a-tree-node'], cf=['trees']),
 dict(cpa=['graph/lca'], cses=[(1137,'Subtree Queries'),(1138,'Path Queries'),(1674,'Subordinates')], ys=['vertex_add_subtree_sum'], cf=['trees','data structures']),
 dict(cpa=['graph/hld'], cses=[(2134,'Path Queries II'),(1138,'Path Queries')], ys=['vertex_add_path_sum','vertex_set_path_composite'], spoj=[('QTREE','Query on a tree')], lcnote=['Heavy-Light Decomposition','HLD'], cf=['trees']),
 dict(cpa=['graph/centroid_decomposition'], cses=[(2079,'Finding a Centroid'),(2080,'Fixed-Length Paths I'),(2081,'Fixed-Length Paths II')], ys=['frequency_table_of_tree_distance'], cf=['divide and conquer','trees']),
 dict(cses=[(1139,'Distinct Colors')], lcnote=['Small-to-Large Merging'], cf=['trees','dsu']),
 dict(cses=[(1133,'Tree Distances II'),(1132,'Tree Distances I')], lc=['sum-of-distances-in-tree','count-number-of-possible-root-nodes','minimum-edge-reversals-so-every-node-is-reachable'], ys=['tree_diameter'], cf=['trees','dp']),
 dict(cses=[(1135,'Distance Queries')], ys=['lca'], cf=['trees']),
 dict(ys=['dynamic_tree_vertex_add_path_sum','dynamic_tree_vertex_set_path_composite','dynamic_tree_subtree_add_subtree_sum','dynamic_tree_vertex_add_subtree_sum'], cf=['data structures','trees']),
 # ---- Stage 5
 dict(cses=[(1653,'Elevator Rides'),(1690,'Hamiltonian Flights'),(2181,'Counting Tilings')], atc=[('dp','o'),('dp','u')], lc=['partition-to-k-equal-sum-subsets','shortest-path-visiting-all-nodes','find-the-shortest-superstring','smallest-sufficient-team'], cf=['bitmasks','dp']),
 dict(cses=[(2220,'Counting Numbers')], atc=[('dp','s')], lc=['number-of-digit-one','numbers-at-most-n-given-digit-set','count-special-integers','count-of-integers'], cf=['dp']),
 dict(cses=[(1097,'Removal Game'),(1744,'Rectangle Cutting')], atc=[('dp','l'),('dp','n')], acmp=[(123,'Восстановление скобок'),(176,'Скобочки')], lc=['burst-balloons','minimum-cost-to-merge-stones','palindrome-partitioning-ii','strange-printer'], cf=['dp']),
 dict(cses=[(1130,'Tree Matching'),(1131,'Tree Diameter'),(1674,'Subordinates')], atc=[('dp','p'),('dp','v')], lc=['house-robber-iii','binary-tree-maximum-path-sum','binary-tree-cameras','diameter-of-binary-tree'], cf=['trees','dp']),
 dict(cses=[(1654,'SOS Bit Problem'),(3141,'And Subset Count')], ys=['bitwise_and_convolution','subset_convolution'], lcnote=['Fast Subset Transform','FST'], cf=['bitmasks','dp']),
 dict(cpa=['geometry/convex_hull_trick'], cses=[(2084,'Monster Game I'),(2085,'Monster Game II')], atc=[('dp','z')], ys=['line_add_get_min'], lcnote=['Convex Hull Trick'], cf=['dp','geometry']),
 dict(cpa=['dynamic_programming/divide-and-conquer-dp'], cses=[(2086,'Subarray Squares'),(2087,'Houses and Schools')], cf=['divide and conquer','dp']),
 dict(cpa=['dynamic_programming/knuth-optimization'], cses=[(2088,'Knuth Division')], atc=[('dp','n')], cf=['dp']),
 dict(cses=[(2086,'Subarray Squares')], lcnote=['WQS Binary Search','Alien Trick'], cf=['dp','binary search']),
 dict(cpa=['dynamic_programming/profile-dynamics'], cses=[(2181,'Counting Tilings'),(2413,'Counting Towers')], cf=['bitmasks','dp']),
 dict(cpa=['algebra/fibonacci-numbers'], cses=[(1722,'Fibonacci Numbers'),(1096,'Throwing Dice'),(1723,'Graph Paths I'),(1724,'Graph Paths II')], atc=[('dp','r')], ys=['pow_of_matrix','kth_term_of_linearly_recurrent_sequence'], lc=['fibonacci-number','count-vowels-permutation','knight-dialer'], cf=['matrices']),
 # ---- Stage 6
 dict(cpa=['algebra/prime-sieve-linear','algebra/sieve-of-eratosthenes'], cses=[(1713,'Counting Divisors'),(1082,'Sum of Divisors')], acmp=[(349,'Простые числа'),(60,'Сверхпростые числа')], ys=['enumerate_primes','counting_primes'], lc=['count-primes'], cf=['number theory']),
 dict(cpa=['algebra/extended-euclid-algorithm','algebra/chinese-remainder-theorem','algebra/linear-diophantine-equation','algebra/module-inverse'], cf=['chinese remainder theorem','number theory']),
 dict(cpa=['algebra/phi-function'], cses=[(2417,'Counting Coprime Pairs')], ys=['sum_of_totient_function'], lcnote=['Mobius Function'], cf=['number theory']),
 dict(cpa=['combinatorics/binomial-coefficients','combinatorics/catalan-numbers','combinatorics/inclusion-exclusion','combinatorics/stars_and_bars'], cses=[(1079,'Binomial Coefficients'),(1715,'Creating Strings II'),(1716,'Distributing Apples'),(1717,'Christmas Party'),(2064,'Bracket Sequences I')], acmp=[(156,'Шахматы - 2'),(189,'Перестановка по номеру')], ys=['binomial_coefficient'], lc=['unique-paths'], cf=['combinatorics']),
 dict(cpa=['combinatorics/burnside'], cses=[(2209,'Counting Necklaces'),(2210,'Counting Grids')], cf=['combinatorics']),
 dict(cpa=['algebra/primality_tests','algebra/factorization'], cses=[(3396,'Next Prime')], ys=['factorize','primality_test'], cf=['number theory']),
 dict(cpa=['algebra/discrete-log'], ys=['discrete_logarithm_mod','sqrt_mod','kth_root_mod'], cf=['number theory']),
 dict(cpa=['linear_algebra/linear-system-gauss','linear_algebra/determinant-gauss'], cses=[(3154,'System of Linear Equations'),(3191,'Maximum Xor Subset'),(3211,'Number of Subset Xors')], ys=['system_of_linear_equations','matrix_det','system_of_linear_equations_mod_2'], cf=['matrices']),
 dict(cpa=['algebra/fft'], cses=[(2111,'Apples and Bananas'),(2112,'One Bit Positions'),(2113,'Signal Processing')], atc=[('practice2','f')], ys=['convolution_mod','wildcard_pattern_matching'], cf=['fft']),
 dict(cpa=['game_theory/sprague-grundy-nim'], cses=[(1730,'Nim Game I'),(1098,'Nim Game II'),(1099,'Stair Game'),(2207,"Grundy's Game"),(2208,'Another Game')], atc=[('dp','k')], lc=['nim-game','stone-game','can-i-win'], cf=['games']),
 dict(cses=[(1725,'Dice Probability'),(1726,'Moving Robots'),(1727,'Candy Lottery'),(1728,'Inversion Probability')], atc=[('dp','i'),('dp','j')], lc=['new-21-game','knight-probability-in-chessboard','soup-servings'], cf=['probabilities']),
 # ---- Stage 7
 dict(cpa=['string/prefix-function'], cses=[(1753,'String Matching'),(1732,'Finding Borders'),(1112,'Required Substring')], acmp=[(202,'Поиск подстроки')], lc=['shortest-palindrome','longest-happy-prefix','repeated-substring-pattern'], cf=['strings']),
 dict(cpa=['string/z-function'], cses=[(1733,'Finding Periods'),(2107,'String Functions')], ys=['zalgorithm'], lc=['sum-of-scores-of-built-strings'], cf=['strings']),
 dict(cpa=['string/string-hashing','string/rabin-karp'], cses=[(2420,'Palindrome Queries'),(1110,'Minimal Rotation')], lc=['longest-duplicate-substring','repeated-dna-sequences','distinct-echo-substrings'], cf=['hashing']),
 dict(cses=[(1731,'Word Combinations'),(1655,'Maximum Xor Subarray')], lc=['implement-trie-prefix-tree','word-search-ii','replace-words','maximum-xor-of-two-numbers-in-an-array'], ys=['set_xor_min'], cf=['strings','data structures']),
 dict(cpa=['string/aho_corasick'], cses=[(2102,'Finding Patterns'),(2103,'Counting Patterns'),(2104,'Pattern Positions')], ys=['aho_corasick'], lc=['stream-of-characters'], cf=['string suffix structures']),
 dict(cpa=['string/suffix-array'], cses=[(2105,'Distinct Substrings'),(2106,'Repeating Substring'),(3225,'Inverse Suffix Array'),(2108,'Substring Order I')], atc=[('practice2','i')], ys=['suffixarray','number_of_substrings'], cf=['string suffix structures']),
 dict(cpa=['string/suffix-automaton'], cses=[(2109,'Substring Order II'),(2110,'Substring Distribution'),(2105,'Distinct Substrings')], ys=['number_of_substrings','longest_common_substring'], cf=['string suffix structures']),
 dict(cpa=['string/manacher'], cses=[(1111,'Longest Palindrome'),(3138,'All Palindromes')], ys=['enumerate_palindromes'], lc=['longest-palindromic-substring','palindromic-substrings'], cf=['strings']),
 dict(cses=[(3138,'All Palindromes')], ys=['eertree','palindromes_in_deque'], cf=['strings']),
 # ---- Stage 8
 dict(cpa=['geometry/basic-geometry','geometry/oriented-triangle-area'], cses=[(2189,'Point Location Test')], acmp=[(102,'Треугольник и точка')], ys=['sort_points_by_argument'], lc=['check-if-it-is-a-straight-line','valid-boomerang'], cf=['geometry']),
 dict(cpa=['geometry/check-segments-intersection','geometry/point-in-convex-polygon','geometry/segments-intersection'], cses=[(2190,'Line Segment Intersection'),(2192,'Point in Polygon')], acmp=[(348,'Пересечение отрезков'),(319,'Точки отрезка')], ys=['count_points_in_triangle'], cf=['geometry']),
 dict(cpa=['geometry/convex-hull'], cses=[(2195,'Convex Hull')], acmp=[(84,'Выпуклая оболочка')], ys=['static_convex_hull','convex_layers'], lc=['erect-the-fence'], cf=['geometry']),
 dict(cpa=['geometry/convex-hull','geometry/minkowski'], ys=['furthest_pair','all_furthest_neighbors'], cses=[(3410,'Maximum Manhattan Distances')], cf=['geometry']),
 dict(cpa=['geometry/area-of-simple-polygon','geometry/picks-theorem','geometry/lattice-points'], cses=[(2191,'Polygon Area'),(2193,'Polygon Lattice Points')], acmp=[(209,'Целые точки')], lc=['largest-triangle-area'], cf=['geometry']),
 dict(cpa=['geometry/nearest_points'], cses=[(2194,'Minimum Euclidean Distance')], acmp=[(344,'Ближайшие точки')], ys=['closest_pair'], cf=['geometry','divide and conquer']),
 dict(cpa=['geometry/intersecting_segments','geometry/length-of-segments-union'], cses=[(1741,'Area of Rectangles'),(1740,'Intersection Points'),(1619,'Restaurant Customers')], ys=['area_of_union_of_rectangles','rectangle_sum'], lc=['rectangle-area-ii','the-skyline-problem'], cf=['geometry','data structures']),
 dict(cpa=['geometry/halfplane-intersection'], cf=['geometry']),
 dict(cpa=['geometry/circle-circle-intersection','geometry/circle-line-intersection','geometry/tangents-to-two-circles','geometry/enclosing-circle'], acmp=[(26,'Две окружности'),(342,'Вписанная окружность')], ys=['minimum_enclosing_circle'], lc=['maximum-number-of-darts-inside-of-a-circular-dartboard'], cf=['geometry']),
 dict(cpa=['geometry/basic-geometry'], cses=[(1742,'Robot Path')], acmp=[(12,'Дачники'),(117,'Опасная зона')], cf=['geometry']),
 # ---- Stage 9
 dict(cses=[(2101,'New Roads Queries')], spoj=[('METEORS','Meteors')], ys=['static_range_lis_query'], cf=['divide and conquer','binary search']),
 dict(cpa=['data_structures/deleting_in_log_n'], cses=[(2133,'Dynamic Connectivity')], ys=['dynamic_graph_vertex_add_component_sum'], cf=['dsu','divide and conquer']),
 dict(ys=['intersection_of_f2_vector_spaces'], cf=['graphs','flows']),
 dict(ys=['general_matching','general_weighted_matching'], cf=['graph matchings']),
 dict(cses=[(1703,'Critical Cities'),(1203,'Visiting Cities')], ys=['dominatortree'], cf=['graphs']),
 dict(ys=['find_linear_recurrence','kth_term_of_linearly_recurrent_sequence','consecutive_terms_of_linear_recurrent_sequence'], cf=['matrices','math']),
 dict(cf=['math']),
 dict(lc=['random-pick-with-weight','linked-list-random-node','shuffle-an-array','insert-delete-getrandom-o1'], cf=['probabilities','hashing']),
 # ---- Stage 10
 dict(team=True), dict(team=True), dict(team=True), dict(team=True), dict(team=True), dict(team=True),
]
# fmt: on

TEAM = [
    ('github', 'KACTL - KTH team notebook', 'https://github.com/kth-competitive-programming/kactl'),
    ('cf', 'Codeforces Gym - ICPC regionals', 'https://codeforces.com/gyms'),
    ('cf', 'Codeforces contests archive', 'https://codeforces.com/contests'),
    ('icpc', 'ICPC Global - official site', 'https://icpc.global/'),
    ('kattis', 'Kattis - ICPC problems', 'https://open.kattis.com/problems'),
    ('atcoder', 'AtCoder contest archive', 'https://atcoder.jp/contests/archive'),
    ('vjudge', 'Virtual Judge - team contests', 'https://vjudge.net/contest'),
    ('cses', 'CSES Problem Set', 'https://cses.fi/problemset/'),
    ('cses', "Competitive Programmer's Handbook (PDF)", 'https://cses.fi/book/book.pdf'),
    ('usaco', 'USACO Guide', 'https://usaco.guide/'),
    ('cpa', 'cp-algorithms', 'https://cp-algorithms.com/'),
    ('clist', 'CLIST - contest calendar', 'https://clist.by/'),
    ('acmp', 'acmp.ru - problem archive', 'https://acmp.ru/index.asp?main=tasks'),
    ('robo', 'RoboContest - olympiads & problems', 'https://robocontest.uz/'),
    ('lc', 'LeetCode weekly contests', 'https://leetcode.com/contest/'),
]

GENERIC = [
    ('usaco', 'USACO Guide', 'https://usaco.guide/'),
    ('cses', "Competitive Programmer's Handbook (PDF)", 'https://cses.fi/book/book.pdf'),
    ('cpa', 'cp-algorithms', 'https://cp-algorithms.com/'),
    ('acmp', 'acmp.ru - problem archive', 'https://acmp.ru/index.asp?main=tasks'),
    ('cses', 'CSES Problem Set', 'https://cses.fi/problemset/'),
    ('cf', 'Codeforces EDU kurslari', 'https://codeforces.com/edu/courses'),
    ('ys', 'Library Checker - barcha masalalar', 'https://judge.yosupo.jp/'),
    ('atcoder', 'AtCoder Problems - mashq jadvali', 'https://kenkoooo.com/atcoder/'),
    ('spoj', 'SPOJ classical masalalar', 'https://www.spoj.com/problems/classical/'),
    ('kattis', 'Kattis masalalar arxivi', 'https://open.kattis.com/problems'),
]

YS_NAMES = {'suffixarray': 'Suffix Array', 'staticrmq': 'Static RMQ', 'unionfind': 'Union Find',
            'bipartitematching': 'Bipartite Matching', 'dominatortree': 'Dominator Tree',
            'directedmst': 'Directed MST', 'zalgorithm': 'Z Algorithm', 'aplusb': 'A + B',
            'scc': 'Strongly Connected Components', 'lca': 'Lowest Common Ancestor', 'eertree': 'Eertree'}


def ys_title(s):
    return YS_NAMES.get(s, s.replace('_', ' ').title())


def site_of(url):
    for key, code in [('codeforces', 'cf'), ('spoj.com', 'spoj'), ('onlinejudge.org', 'uva'), ('uva.', 'uva'),
                      ('timus', 'timus'), ('leetcode', 'lc'), ('cses.fi', 'cses'), ('atcoder', 'atcoder'),
                      ('kattis', 'kattis'), ('hackerrank', 'hackerrank'), ('codechef', 'codechef'),
                      ('acmicpc', 'baekjoon'), ('eolymp', 'eolymp'), ('e-olymp', 'eolymp'),
                      ('lightoj', 'lightoj'), ('hackerearth', 'hackerearth'), ('csacademy', 'csacademy'),
                      ('usaco', 'usaco'), ('dmoj', 'dmoj'), ('yosupo', 'ys'), ('acmp.ru', 'acmp'),
                      ('toph', 'toph'), ('topcoder', 'topcoder'), ('poj.org', 'poj'), ('hdu', 'hdu'),
                      ('vjudge', 'vjudge'), ('luogu', 'luogu'), ('loj.ac', 'loj'), ('oj.uz', 'ojuz'),
                      ('szkopul', 'szkopul'), ('projecteuler', 'euler'), ('informatics', 'informatics')]:
        if key in url:
            return code
    return 'web'


def clean_title(t):
    t = re.sub(r'^\s*(CF|Codeforces|SPOJ|UVA|UVa|Timus|LeetCode|CSES|AtCoder|Kattis|Hackerrank|HackerRank|CodeChef|Codechef|e-olymp|E-olymp|LightOJ|Light OJ|Hackerearth|HackerEarth|CSAcademy|CS Academy|USACO|DMOJ|LOJ|POJ|HDU|TopCoder|Library Checker|GYM|Gym|acm\.timus|Baekjoon|ACMICPC|Toph|AIZU|Aizu|SGU)\s*[-:#]?\s*', '', t).strip()
    t = t.replace('**', '').replace('`', '')
    return t or 'Problem'


def lc_title(slug):
    if slug in lc_rows:
        return lc_rows[slug]['t']
    small = {'a', 'an', 'the', 'of', 'in', 'to', 'and', 'or', 'with', 'by', 'for', 'at', 'on', 'from'}
    words = slug.split('-')
    return ' '.join(w if (i and w in small) else (w.upper() if w in ('ii', 'iii', 'iv', 'lru', 'atoi', 'dna', 'o1') else w.capitalize()) for i, w in enumerate(words))


errors = []


def build(spec, idx):
    links = []
    seen = set()

    def add(site, title, url):
        if url in seen:
            return
        seen.add(url)
        links.append((site, title, url))

    if spec.get('team'):
        start = (idx * 5) % len(TEAM)
        for k in range(len(TEAM)):
            add(*TEAM[(start + k) % len(TEAM)])
        return links[:15]

    arts = spec.get('cpa', [])
    for a in arts:
        if a not in cpa_articles:
            errors.append(f'{idx}: missing cpa article {a}')
    for a in arts[:2]:
        name = a.split('/')[-1].replace('_', ' ').replace('-', ' ').title()
        add('cpa', f'Nazariya: {name}', f'https://cp-algorithms.com/{a}.html')

    for tid, name in spec.get('cses', [])[:4]:
        add('cses', name, f'https://cses.fi/problemset/task/{tid}')

    lcs = [s for s in spec.get('lc', []) if s in lc_slugs]
    for s in spec.get('lc', []):
        if s not in lc_slugs:
            errors.append(f'{idx}: missing lc slug {s}')
    for kw in spec.get('lcnote', []):
        for slug, r in lc_rows.items():
            if r['locked'] or '🔒' in r['note']:
                continue
            notes = [n.strip().strip('`').strip() for n in re.split(r',', r['note'])]
            if kw in notes and slug not in lcs and slug in lc_slugs:
                lcs.append(slug)
    for s in lcs[:3]:
        add('lc', lc_title(s), f'https://leetcode.com/problems/{s}/')

    for tid, name in spec.get('acmp', [])[:2]:
        add('acmp', name, f'https://acmp.ru/index.asp?main=task&id_task={tid}')

    for c, t in spec.get('atc', [])[:2]:
        name = ATC_DP[t] if c == 'dp' else ATC_PR[t]
        add('atcoder', name, f'https://atcoder.jp/contests/{c}/tasks/{c}_{t}')

    for s in spec.get('ys', []):
        if s not in ys_slugs:
            errors.append(f'{idx}: missing ys slug {s}')
    for s in [s for s in spec.get('ys', []) if s in ys_slugs][:2]:
        add('ys', ys_title(s), f'https://judge.yosupo.jp/problem/{s}')

    for code, name in spec.get('spoj', []):
        add('spoj', name, f'https://www.spoj.com/problems/{code}/')

    # Reserve the last two slots for the Codeforces tag list and RoboContest archive.
    reserve = 2
    pool = []
    for a in arts:
        pool.extend(cpa.get(a, []))
    # Prefer a mix of judges: round-robin by site.
    by_site = {}
    for t, u in pool:
        by_site.setdefault(site_of(u), []).append((t, u))
    order = sorted(by_site.keys(), key=lambda s: {'cf': 0, 'spoj': 1, 'cses': 2, 'atcoder': 3, 'kattis': 4, 'lc': 5}.get(s, 9))
    rr = True
    while rr and len(links) < 15 - reserve:
        rr = False
        for s in order:
            if by_site[s] and len(links) < 15 - reserve:
                t, u = by_site[s].pop(0)
                add(s, clean_title(t), u)
                rr = True

    # Extra leftovers from the spec lists if still short.
    for tid, name in spec.get('cses', [])[4:]:
        if len(links) < 15 - reserve:
            add('cses', name, f'https://cses.fi/problemset/task/{tid}')
    for s in lcs[3:]:
        if len(links) < 15 - reserve:
            add('lc', lc_title(s), f'https://leetcode.com/problems/{s}/')
    for tid, name in spec.get('acmp', [])[2:]:
        if len(links) < 15 - reserve:
            add('acmp', name, f'https://acmp.ru/index.asp?main=task&id_task={tid}')
    for c, t in spec.get('atc', [])[2:]:
        if len(links) < 15 - reserve:
            add('atcoder', ATC_DP[t] if c == 'dp' else ATC_PR[t], f'https://atcoder.jp/contests/{c}/tasks/{c}_{t}')
    for s in [s for s in spec.get('ys', []) if s in ys_slugs][2:]:
        if len(links) < 15 - reserve:
            add('ys', ys_title(s), f'https://judge.yosupo.jp/problem/{s}')

    tags = spec.get('cf', [])
    # Codeforces difficulty ladders for the main tag fill remaining space.
    if tags:
        main = quote(tags[0])
        for lo, hi in [(1200, 1600), (1600, 2000), (2000, 2400), (2400, 3000)]:
            if len(links) < 15 - reserve:
                add('cf', f'Codeforces: "{tags[0]}" {lo}–{hi}', f'https://codeforces.com/problemset?tags={main},{lo}-{hi}')
        for t in tags[1:]:
            if len(links) < 15 - reserve:
                add('cf', f'Codeforces: "{t}" masalalari', f'https://codeforces.com/problemset?tags={quote(t)}')
    for g in GENERIC:
        if len(links) < 15 - reserve:
            add(*g)

    if tags:
        add('cf', f'Codeforces: barcha "{tags[0]}" masalalari', f'https://codeforces.com/problemset?tags={quote(tags[0])}')
    add('robo', 'RoboContest masalalar arxivi', 'https://robocontest.uz/tasks')
    for g in GENERIC:
        if len(links) < 15:
            add(*g)
    return links[:15]


def dart_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'").replace('$', '\\$') + "'"


def main(n_topics, out):
    if len(S) != n_topics:
        sys.exit(f'spec count {len(S)} != topics {n_topics}')
    all_links = [build(s, i) for i, s in enumerate(S)]
    if errors:
        print('\n'.join(errors))
        sys.exit('errors above')
    lines = ["// GENERATED by build_links.py - do not edit by hand.", "import 'practice_link.dart';", '',
             'const topicLinks = <List<PracticeLink>>[']
    for i, links in enumerate(all_links):
        lines.append(f'  // {i + 1}')
        lines.append('  [')
        for site, title, url in links:
            lines.append(f'    PracticeLink({dart_str(site)}, {dart_str(title)}, {dart_str(url)}),')
        lines.append('  ],')
    lines.append('];')
    open(out, 'w').write('\n'.join(lines) + '\n')
    counts = [len(l) for l in all_links]
    print('levels', len(all_links), 'min', min(counts), 'max', max(counts), 'total', sum(counts))
    from collections import Counter
    print(Counter(s for l in all_links for s, _, _ in l).most_common())
    json.dump(all_links, open(D + 'links_preview.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
