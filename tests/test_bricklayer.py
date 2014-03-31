import unittest
from mock import MagicMock, patch

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

if __name__ == '__main__':
    unittest.main()
