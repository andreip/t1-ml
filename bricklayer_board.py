class BricklayerBoard:
    BRICK = '#'
    EMPTY = ' '

    def __init__(self, boardStr):
        self.lengths =\
            {'A':[4,1],'B':[3,2],'C':[3,2],'D':[3, 2],'E':[3,2],'F':[3,2],'G':[2,2]}
        self.board = filter(lambda(x): len(x) > 0, boardStr.split('|'))

    def get_legal_actions(self, brick):
        """Returns a list of legal actions based on the board and
        the next brick.

        Returns:
            [(rot, offset), (rot2, offset2), ... ].
        """
        legal_actions = []
        # For each rotation
        for rot in range(0,4):
            max_offset = len(self.board[0]) - self.lengths[brick][rot % 2]
            for offset in range(0, max_offset + 1):
                legal_actions.append((rot, offset))
        return legal_actions

    def get_board_diff_levels(self):
        """Returns an array of height _differences_ between addiacent columns.
        It will be used to compute a "hash" for a board and store it in a
        dictionary. This "hash" also has the property of being symetric which
        halves the number of states (significant improvement).
        """
        levels = self.get_board_levels()
        diff = []
        for i in range(1, len(levels)):
            diff.append(abs(levels[i-1] - levels[i]))
        return tuple(diff)

    def get_board_levels(self):
        """Returns an array of all columns' levels.

        w = 4, h = 3
        |#   |
        |  # |
        |   #|
        *----*
        This should return [3, 0, 2, 1].

        Returns:
            an array [h1, h2, ... ].
        """
        width, height = len(self.board[0]), len(self.board)
        levels = [0 for i in range(width)]
        for l, line in enumerate(self.board):
            level = height - l
            for c, cell in enumerate(line):
                if cell == BricklayerBoard.BRICK and levels[c] < level:
                    levels[c] = level
        return tuple(levels)
