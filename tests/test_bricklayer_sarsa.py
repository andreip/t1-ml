import random
import unittest

from bricklayer_sarsa import BricklayerSarsa
from bricklayer_board import BricklayerBoard

class TestBricklayerSarsa(unittest.TestCase):

    def setUp(self):
        length, height = 10, 6
        self.sarsa = BricklayerSarsa(length, height)

    def test_defaultdict(self):
        self.assertEqual(self.sarsa.maps[0], (0))
        self.assertEqual(self.sarsa.maps['a'], (0))

    def test_update_utilities(self):
        """Test that updating does not produce any errors."""
        line = '0,|    | #  |  # |   #|,A'
        board = BricklayerBoard(line.split(',')[1])
        length, height = len(board.board[0]), len(board.board)
        sarsa = BricklayerSarsa(length, height)

        action = (1,0)
        next_line = '0,|#   |##  |# # |#  #|,B'
        next_action = (2,1)

        self.sarsa.update_utilities(line, action, next_line, next_action)

if __name__ == '__main__':
    unittest.main()
