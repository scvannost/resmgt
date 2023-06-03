import unittest

from resmgt import Game


class TestGame(unittest.TestCase):
    def test_init(self):
        game = Game()
        assert game.surface is not None
