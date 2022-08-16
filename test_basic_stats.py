import unittest
import basic_stats as bs

class TestBasicStats(unittest.TestCase):

    def test_10_instance_creation(self) -> None:
        capture = bs.DataCapture()
        expected = (0, [0]*(len(capture)+1))
        actual = capture.get_state()
        self.assertEqual(actual, expected)

    def test_20_add_single_number(self) -> None:
        capture = bs.DataCapture()
        capture.add(1)
        expected = (1, [ 0 if i!=1 else 1 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

    def test_30_add_a_set_of_numbers(self) -> None:
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

        capture.add(5)
        expected = (5, [ [0, 0, 0, 2, 1, 1, 0, 0, 0, 1][i] if i<=9 else 0 for i in range(len(capture)+1) ])
        actual = capture.get_state()
        self.assertEqual(actual, expected)

    def test_40_build_stats(self) -> None:
        capture = bs.DataCapture()
        expected = ( [0, 0, 0], [ [0, 0, 0] for i in range(len(capture)+1) ] )
        stats_by_hand = lambda new_val, prev_stats : \
            ( [ prev_stats[0][0], prev_stats[0][1]+1, prev_stats[0][2] ],
              [ [ prev_stats[1][i][0], prev_stats[1][i][1], prev_stats[1][i][2]+1 ] if i<new_val else
                [ prev_stats[1][i][0], prev_stats[1][i][1]+1, prev_stats[1][i][2] ] if i>new_val else
                [ prev_stats[1][i][0]+1, prev_stats[1][i][1], prev_stats[1][i][2] ]
                for i in range(len(capture)+1) ] )

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

        capture.add(5)
        stats = capture.build_stats()
        expected = stats_by_hand(5, expected)
        actual = stats.get_state()
        self.assertEqual(actual, expected)

    def test_50_less_out_of_left_boundary(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(5)
        stats = capture.build_stats()
        self.assertEqual(stats.less(0), 0)

    def test_60_less_left_boundary(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(5)
        stats = capture.build_stats()
        self.assertEqual(stats.less(1), 0)

    def test_70_between_empty(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(5)
        stats = capture.build_stats()
        self.assertEqual(stats.between(6, 8), 0)

    def test_80_between_non_empty(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(5)
        stats = capture.build_stats()
        self.assertEqual(stats.between(3, 6), 4)

    def test_90_greater_empty(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(5)
        stats = capture.build_stats()
        self.assertEqual(stats.greater(9), 0)

    def test_95_greater_non_empty(self) -> None:
        capture = bs.DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(3)
        capture.add(4)
        capture.add(5)
        stats = capture.build_stats()
        self.assertEqual(stats.greater(4), 2)

if __name__ == '__main__':
    unittest.main()
