import unittest
from mock import MagicMock, patch, call

from bricklayer import BrickLayer

class TestBricklayer(unittest.TestCase):

    def setUp(self):
        # Mock any socket initialization, we need none.
        with patch.object(BrickLayer, '__init__') as mock:
            mock.return_value = None
            self.bricklayer = BrickLayer()
            # Mock mysend, myreceive to not use sockets.
            self.bricklayer.myreceive = MagicMock()
            self.bricklayer.mysend = MagicMock()

    def test_loop_game_over_update_utilities(self):
        """Test that when we receive a valid line and then
        GAME OVER, that the update_utilities function is still called.
        This is important because SARSA should learn from mistakes too.
        """
        line = "0,|    |    |    |,A"
        game_over = '-20,GAME OVER'
        action = (1,0)

        # Receive should return 'GAME OVER' at 2nd call.
        self.bricklayer.myreceive = MagicMock(side_effect=[line, game_over, ''])
        self.bricklayer.sarsa = MagicMock()
        self.bricklayer.sarsa.get_action = MagicMock(side_effect=[action, None])

        self.bricklayer.loop()
        self.bricklayer.sarsa.update_utilities.assert_called_with(line,
            action, game_over, None)

    def test_loop_continue_after_game_over(self):
        """Test that once we reach a GAME OVER, the GAME OVER
        line is not used as a previous line in the next episode.
        """
        lines = ['0,|#   |    |    |,A',
                 '-20,GAME OVER',
                 '0,|    |    |    |,B',
                 '0,|    |#   |### |,B',
                 '']
        actions = [(1,0), None, (1,0), (1,1)]

        self.bricklayer.myreceive = MagicMock(side_effect=lines)
        self.bricklayer.sarsa = MagicMock()
        self.bricklayer.sarsa.get_action = MagicMock(side_effect=actions)

        self.bricklayer.loop()
        print self.bricklayer.sarsa.update_utilities.call_args_list
        calls = [
            call(lines[0], actions[0], lines[1], actions[1]),
            # This line shold NOT be present in the tests!!
            # That is because GAME OVER should reset the trials, but
            # not be part of a new episode as it would be if this
            # call would be present in the update_utilities call.
            #call(lines[1], actions[1], lines[2], actions[2]),
            call(lines[2], actions[2], lines[3], actions[3])
        ]
        self.assertListEqual(
            self.bricklayer.sarsa.update_utilities.call_args_list,
            calls)

if __name__ == '__main__':
    unittest.main()
