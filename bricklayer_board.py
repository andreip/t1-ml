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

    def get_board_levels(self):
        """Returns an array of height difference between addiacent columns.
        It will be used to compute a "hash" for a board and store it in a
        dictionary. This "hash" also has the property of being symetric which
        halves the number of states (significant improvement).
        """
        pass

    def do_move(self, action):
        """Returns a new board based on the action.
        """
        pass
