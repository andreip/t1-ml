from collections import defaultdict
import random
import unittest

from bricklayer_sarsa import BricklayerSarsa
from bricklayer_board import BricklayerBoard

class TestBricklayerSarsa(unittest.TestCase):

    def setUp(self):
        length, height = 10, 6
        self.sarsa = BricklayerSarsa(height, length)

    def test_defaultdict(self):
        self.assertEqual(self.sarsa.maps[0], (0))
        self.assertEqual(self.sarsa.maps['a'], (0))

    def test_update_utilities(self):
        """Test that updating does not produce any errors."""
        line = '0,|    | #  |  # |   #|,A'
        board = BricklayerBoard(line.split(',')[1])
        length, height = len(board.board[0]), len(board.board)
        sarsa = BricklayerSarsa(height, length)

        action = (1,0)
        next_line = '0,|#   |##  |# # |#  #|,B'
        next_action = (2,1)

        self.sarsa.update_utilities(line, action, next_line, next_action)

    def test_get_action_greedy(self):
        line = '0,|    | #  |  # |   #|,A'
        board = BricklayerBoard(line.split(',')[1])
        length, height = len(board.board[0]), len(board.board)

        # Update utility map so that a specific action is
        # chosen a = (1,0).
        board_state = board.get_board_diff_levels()
        max_action = (1,0)
        action = (0,0)

        # Make the utility map favour the max_action.
        maps = defaultdict(int)
        maps[(board_state, max_action)] = 10
        maps[(board_state, action)] = 1

        # We don't want any randomness here, eps=1 will assure
        # policy will be greedy.
        sarsa = BricklayerSarsa(height, length, eps=1, maps=maps)
        self.assertEqual(sarsa.get_action(line), max_action)

if __name__ == '__main__':
    unittest.main()
