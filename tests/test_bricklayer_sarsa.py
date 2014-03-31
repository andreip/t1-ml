import random
import unittest

from bricklayer_sarsa import BricklayerSarsa

class TestBricklayerSarsa(unittest.TestCase):

    def setUp(self):
        length, height = 10, 6
        self.sarsa = BricklayerSarsa(length, height)

    def test_defaultdict(self):
        self.assertEqual(self.sarsa.maps[0], (0))
        self.assertEqual(self.sarsa.maps['a'], (0))

if __name__ == '__main__':
    unittest.main()
