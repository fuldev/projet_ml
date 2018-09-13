from environments.InformationState import InformationState
import numpy as np


class TicTacToeInformationState(InformationState):
    def __hash__(self):
         return hash(np.array(self.board).tobytes())

    def __eq__(self, other):
        if isinstance(other, TicTacToeInformationState):
            return False
        for i in range(9):
            if self.board[i//3][i%3] != \
                    other.board[i // 3][i % 3]:
                return False
        return self.current_player == other.current_player

    def __init__(self, current_player: int, board):
        self.current_player = current_player
        self.board = board

    def __str__(self):
        str = "current player : \n"
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

    i = 1
    elt = 2
    print(((elt) * 3) ^ (i + 1))