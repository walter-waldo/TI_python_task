"""Unit testing for the Basic Statistics module.
"""

import unittest
import basic_stats as bs

class TestBasicStats(unittest.TestCase):

    def test_00_instance_creation(self) -> None:
        capture = bs.DataCapture()
        expected = (0, [0]*(len(capture)+1))
        actual = capture.get_state()
        self.assertEqual(actual, expected)

    def test_10_add_single_value(self) -> None:
        capture = bs.DataCapture()
        capture.add(1)
        expected = (1, [ 0 if i!=1 else 1 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

    def test_20_add_a_set_of_value(self) -> None:
        capture = bs.DataCapture()

        capture.add(3)
        expected = (1, [ [0, 0, 0, 1, 0, 0, 0, 0, 0, 0][i] if i<=9 else 0 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

        capture.add(9)
        expected = (2, [ [0, 0, 0, 1, 0, 0, 0, 0, 0, 1][i] if i<=9 else 0 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

        capture.add(3)
        expected = (3, [ [0, 0, 0, 2, 0, 0, 0, 0, 0, 1][i] if i<=9 else 0 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

        capture.add(4)
        expected = (4, [ [0, 0, 0, 2, 1, 0, 0, 0, 0, 1][i] if i<=9 else 0 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

        capture.add(6)
        expected = (5, [ [0, 0, 0, 2, 1, 0, 1, 0, 0, 1][i] if i<=9 else 0 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

    def test_30_build_stats_with_values(self) -> None:
        capture = bs.DataCapture()
        expected = ( [0, 0, 0], [ [0, 0, 0] for i in range(len(capture)+1+1) ] )
        stats_by_hand = lambda new_val, prev_stats : \
            ( [ prev_stats[0][0], prev_stats[0][1]+1, prev_stats[0][2] ],
              [ [ prev_stats[1][i][0], prev_stats[1][i][1], prev_stats[1][i][2]+1 ] if i < new_val else
                [ prev_stats[1][i][0], prev_stats[1][i][1]+1, prev_stats[1][i][2] ] if i > new_val else
                [ prev_stats[1][i][0]+1, prev_stats[1][i][1], prev_stats[1][i][2] ]
                for i in range(len(capture)+1+1) ] )

        capture.add(3)
        stats = capture.build_stats()
        expected = stats_by_hand(3, expected)
        actual = stats.get_state()
        self.assertEqual(actual, expected)

        capture.add(9)
        stats = capture.build_stats()
        expected = stats_by_hand(9, expected)
        actual = stats.get_state()
        self.assertEqual(actual, expected)

        capture.add(3)
        stats = capture.build_stats()
        expected = stats_by_hand(3, expected)
        actual = stats.get_state()
        self.assertEqual(actual, expected)

        capture.add(4)
        stats = capture.build_stats()
        expected = stats_by_hand(4, expected)
        actual = stats.get_state()
        self.assertEqual(actual, expected)

        capture.add(6)
        stats = capture.build_stats()
        expected = stats_by_hand(6, expected)
        actual = stats.get_state()
        self.assertEqual(actual, expected)

    def test_40_query_less_than_val_beyond_left_boundary(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()
        self.assertEqual(stats.less(0), 0)

    def test_50_query_less_than_val_at_left_boundary(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()
        self.assertEqual(stats.less(1), 0)

    def test_60_query_empty_range(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()
        self.assertEqual(stats.between(7, 8), 0)

    def test_70_query_non_empty_range(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()
        self.assertEqual(stats.between(3, 6), 4)

    def test_80_query_greater_than_greatest_val(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()
        self.assertEqual(stats.greater(9), 0)
        self.assertEqual(stats.greater(len(capture)+1), 0)

    def test_90x1_query_greater_than_non_greatest_val(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()
        self.assertEqual(stats.greater(4), 2)

    def test_90x2_query_stats_no_having_values(self) -> None:
        capture = bs.DataCapture()
        stats = capture.build_stats()
        self.assertEqual(stats.less(0), 0)
        self.assertEqual(stats.less(10), 0)
        self.assertEqual(stats.greater(0), 0)
        self.assertEqual(stats.greater(10), 0)
        self.assertEqual(stats.between(0, 10), 0)

    def test_90x3_value_out_of_allowed_domain(self) -> None:
        capture = bs.DataCapture()
        try:
            capture.add(0)
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to validate minimum allowed value')
        try:
            capture.add(len(capture)+1)
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to validate maximum allowed value')
        try:
            capture.add('quinientos')                               # type: ignore
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to validate value type domain')

    def test_90x4_query_range_with_not_int_borders(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        stats = capture.build_stats()
        try:
            self.assertEqual(stats.between('minus one', 4), 3)      # type: ignore
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to query range with not int left border')
        try:
            self.assertEqual(stats.between(-1, 'four'), 3)          # type: ignore
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to query range with not int roght border')
        try:
            self.assertEqual(stats.between('minus one', 'four'), 3) # type: ignore
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to query range with not int borders')

    def test_90x5_query_range_with_one_side_beyond_border(self) -> None:
        try:
            capture = bs.DataCapture()
            capture.add(3)
            capture.add(9)
            capture.add(3)
            capture.add(4)
            capture.add(6)
            stats = capture.build_stats()
            self.assertEqual(stats.between(-1, 4), 3)
            self.assertEqual(stats.between(1, 11), 5)
            self.assertEqual(stats.between(1, len(capture)+1), 5)
        except Exception as e:
            self.fail(e.args)

    def test_90x6_query_range_with_both_sides_beyond_borders(self) -> None:
        try:
            capture = bs.DataCapture()
            capture.add(3)
            capture.add(9)
            capture.add(3)
            capture.add(4)
            capture.add(6)
            stats = capture.build_stats()
            self.assertEqual(stats.between(-1, 11), 5)
        except Exception as e:
            self.fail(e.args)


    def test_90x7_query_range_with_both_sides_swapped(self) -> None:
        try:
            capture = bs.DataCapture()
            capture.add(3)
            stats = capture.build_stats()
            self.assertEqual(stats.between(11, 5), 1)
        except Exception as e:
            self.assertTrue(True, e.args)
        else:
            self.fail('Failed to validate query range with both sides swapped')

if __name__ == '__main__':
    unittest.main()
