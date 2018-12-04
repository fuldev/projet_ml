import unittest

from games.tictactoe.TicTacToeGameState import TicTacToeGameState


class TicTacToeGameStateTests(unittest.TestCase):

    def setUp(self):
        self.gs = TicTacToeGameState()

    def test_lines_wins_for_player_0(self):
        gs = self.gs
        for i in range(3):
            gs = TicTacToeGameState()
            gs.step(0, i * 3 + 0)
            gs.step(1, ((i + 1) % 3) * 3 + 0)
            gs.step(0, i * 3 + 1)
            gs.step(1, ((i + 1) % 3) * 3 + 1)
            _, rew, term = gs.step(0, i * 3 + 2)
            assert (rew, term) == (1, True)

    def test_columns_wins_for_player_0(self):
        gs = self.gs
        for i in range(3):
            gs = TicTacToeGameState()
            gs.step(0, i + 0)
            gs.step(1, ((i + 1) % 3) + 0)
            gs.step(0, i + 1 * 3)
            gs.step(1, ((i + 1) % 3) + 1 * 3)
            _, rew, term = gs.step(0, i + 2 * 3)
            assert (rew, term) == (1, True)

    def test_lines_wins_for_player_1(self):
        gs = self.gs
        for i in range(3):
            gs = TicTacToeGameState()
            gs.step(0, i * 3 + 0)
            gs.step(1, ((i + 1) % 3) * 3 + 0)
            gs.step(0, i * 3 + 1)
            gs.step(1, ((i + 1) % 3) * 3 + 1)
            gs.step(0, ((i + 2) % 3) * 3 + 0)
            _, rew, term = gs.step(1, ((i + 1) % 3) * 3 + 2)
            assert (rew, term) == (-1, True)

    def test_columns_wins_for_player_1(self):
        gs = self.gs
        for i in range(3):
            gs = TicTacToeGameState()
            gs.step(0, i + 0)
            gs.step(1, ((i + 1) % 3) + 0)
            gs.step(0, i + 1 * 3)
            gs.step(1, ((i + 1) % 3) + 1 * 3)
            gs.step(0, (i + 2) % 3 + 0)
            _, rew, term = gs.step(1, ((i + 1) % 3) + 2 * 3)
            assert (rew, term) == (-1, True)

    def test_diagonal_wins_for_player_0(self):
        gs = self.gs
        gs.step(0, 0)
        gs.step(1, 1)
        gs.step(0, 4)
        gs.step(1, 5)
        _, rew, term = gs.step(0, 8)

        gs = TicTacToeGameState()
        gs.step(0, 2)
        gs.step(1, 1)
        gs.step(0, 4)
        gs.step(1, 5)
        _, rew, term = gs.step(0, 6)
        assert (rew, term) == (1, True)

    def test_diagonal_wins_for_player_1(self):
        gs = self.gs
        gs.step(0, 1)
        gs.step(1, 0)
        gs.step(0, 2)
        gs.step(1, 4)
        gs.step(0, 5)
        _, rew, term = gs.step(1, 8)
        assert (rew, term) == (-1, True)

        gs = TicTacToeGameState()
        gs.step(0, 0)
        gs.step(1, 2)
        gs.step(0, 1)
        gs.step(1, 4)
        gs.step(0, 5)
        _, rew, term = gs.step(1, 6)
        assert (rew, term) == (-1, True)

    @unittest.expectedFailure
    def test_player_1_cannot_play_first(self):
        gs = self.gs
        gs.step(1, 0)

    def test_draw_game(self):
        gs = self.gs
        gs.step(0, 0)
        gs.step(1, 4)
        gs.step(0, 2)
        gs.step(1, 1)
        gs.step(0, 7)
        gs.step(1, 3)
        gs.step(0, 5)
        gs.step(1, 8)
        _, rew, term = gs.step(0, 6)
        assert (rew, term) == (0, True)


if __name__ == "__main__":
    unittest.main()