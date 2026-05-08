import unittest

from matrix_graph_BFS import BFS


class TestMatrixGraphBFS(unittest.TestCase):
    def test_reaches_snack_basic_path(self):
        matrix = [
            "D...",
            ".#..",
            "..S.",
        ]
        self.assertTrue(BFS(matrix))

    def test_blocked_by_walls_and_boss(self):
        matrix = [
            "D#B",
            "###",
            "..S",
        ]
        self.assertFalse(BFS(matrix))

    def test_no_desk_returns_false(self):
        matrix = [
            "...",
            ".S.",
            "...",
        ]
        self.assertFalse(BFS(matrix))

    def test_multiple_desks_one_can_reach_snack(self):
        matrix = [
            "D###",
            "D..S",
            "####",
        ]
        self.assertTrue(BFS(matrix))

    def test_diagonal_only_path_is_allowed(self):
        matrix = [
            "D#.",
            "#.S",
            "...",
        ]
        self.assertTrue(BFS(matrix))

    def test_hash_wall_should_block_path_per_prompt(self):
        matrix = [
            "D##",
            "###",
            "..S",
        ]
        self.assertFalse(BFS(matrix))

    def test_empty_matrix_should_return_false_not_crash(self):
        self.assertFalse(BFS([]))

    def test_legacy_w_wall_is_still_blocked(self):
        matrix = [
            "DWW",
            "WWW",
            "..S",
        ]
        self.assertFalse(BFS(matrix))

    def test_cannot_move_left_or_up(self):
        matrix = [
            "..S",
            "...",
            "D..",
        ]
        self.assertFalse(BFS(matrix))


if __name__ == "__main__":
    unittest.main()
