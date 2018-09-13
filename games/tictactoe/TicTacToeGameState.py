from copy import deepcopy

from environments.GameState import GameState
from games.tictactoe.TicTacToeInformationState import TicTacToeInformationState


class TicTacToeGameState(GameState):
    def __init__(self):
        self.current_player = 0
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def step(self, player_id: int, action_id: int) -> \
            ('GameState', float, bool):
        val = self.board[action_id // 3][action_id % 3]
        if (val != 0):
            raise Exception("Player can't play at specified position !")

        self.board[action_id // 3][action_id % 3] = \
            1 if player_id == 0 else -1

        (score, terminal) = self.compute_current_score_and_end_game()

        self.current_player = (self.current_player + 1) % 2
        return (self, score, terminal)

    def compute_current_score_and_end_game(self):
        board = self.board

        for i in range(3):
            if board[i][0] == 1 and \
                    board[i][1] == 1 and \
                    board[i][2] == 1:
                return (1, True)

            if board[i][0] == -1 and \
                    board[i][1] == -1 and \
                    board[i][2] == -1:
                return (-1, True)

        for i in range(3):
            if board[0][i] == 1 and \
                    board[1][i] == 1 and \
                    board[2][i] == 1:
                return (1, True)

            if board[0][i] == -1 and \
                    board[1][i] == -1 and \
                    board[2][i] == -1:
                return (-1, True)

        if board[0][0] == 1 and \
                    board[1][1] == 1 and \
                    board[2][2] == 1:
                return (1, True)

        if board[0][0] == -1 and \
                    board[1][1] == -1 and \
                    board[2][2] == -1:
                return (-1, True)

        if board[2][0] == 1 and \
                    board[1][1] == 1 and \
                    board[2][0] == 1:
                return (1, True)

        if board[2][0] == -1 and \
                    board[1][1] == -1 and \
                    board[2][0] == -1:
                return (-1, True)

        for i in range(9):
            if board[i//3][i%3] == 0:
                break
            if i == 8:
                return (0, True)

        return (0, False)

    def get_player_count(self) -> int:
        return 2

    def get_current_player_id(self) -> int:
        return self.current_player

    def get_information_state_for_player(self, player_id: int) -> 'InformationState':
        return TicTacToeInformationState(self.current_player,
                                         deepcopy(self.board))

    def get_available_actions_id_for_player(self, player_id: int) -> 'Iterable(int)':
        if player_id != self.current_player:
            return []
        return list(filter(lambda i: self.board[i // 3][i % 3] == 0, range(0, 9)))

    def __str__(self):
        str = ""
        for i in range(0, 3):
            for j in range(0, 3):
                val = self.board[i][j]
                str += "_" if val == 0 else (
                    "0" if val == 1 else
                    "X"
                )
            str += "\n"
        return str


if __name__ == "__main__":
    gs = TicTacToeGameState()
    print(gs.get_available_actions_id_for_player(gs.get_current_player_id()))
    print(gs)
    gs.step(0, 0)
    print(gs)
    gs.step(1, 2)
    print(gs)
    gs.step(0, 2)
