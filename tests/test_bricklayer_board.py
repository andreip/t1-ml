import unittest

from bricklayer_board import BricklayerBoard

class TestBricklayerBoard(unittest.TestCase):

    def test_parse_board(self):
        boardStr = "|    |    |    |"
        Board = BricklayerBoard(boardStr)
        self.assertEqual(len(Board.board), 3)
        self.assertEqual(len(Board.board[0]), 4)

    def test_get_legal_actions_empty(self):
        boardStr = "|    |    |    |"
        # 'A' is a line brick
        brick = 'A'
        Board = BricklayerBoard(boardStr)
        actions = Board.get_legal_actions(brick)
        # Two board rotated 0 and 180 degrees, 8 for the others.
        self.assertEqual(len(actions), 10)

    def test_get_board_levels(self):
        boardStr = "| #  |  # |   #|"


if __name__ == '__main__':
    unittest.main()
