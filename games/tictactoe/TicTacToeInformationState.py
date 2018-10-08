from environments import GameState
from environments.InformationState import InformationState
import numpy as np


class TicTacToeInformationState(InformationState):

    def __hash__(self):
        return hash((self.board * (1 if self.current_player == 0 else -1)).tobytes())
        # sum = self.current_player
        # for i in range(9):
        #    sum += 3 ^ (i + 1) + (self.board[i // 3, i % 3] + 1)
        # return int(sum)

    def __eq__(self, other):
        #if isinstance(other, TicTacToeInformationState):
        #    return False
        return np.array_equal(self.board, other.board) and self.current_player == other.current_player

    def __ne__(self, other):
        #if isinstance(other, TicTacToeInformationState):
        #    return False
        return not (np.array_equal(self.board, other.board) and self.current_player == other.current_player)

    def __init__(self, current_player: int, board):
        self.current_player = current_player
        self.board = board

    def __str__(self):
        str_acc = "current player : " + str(self.current_player) + "\n"
        for i in range(0, 3):
            for j in range(0, 3):
                val = self.board[i][j]
                str_acc += "_" if val == 0 else (
                    "0" if val == 1 else
                    "X"
                )
            str_acc += "\n"
        return str_acc

    def create_game_state_from_information_state(self):
        from games.tictactoe.TicTacToeGameState import TicTacToeGameState
        gs = TicTacToeGameState()
        gs.board = self.board.copy()
        gs.current_player = self.current_player
        return gs
