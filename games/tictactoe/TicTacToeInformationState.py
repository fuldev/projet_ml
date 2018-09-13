from environments.InformationState import InformationState


class TicTacToeInformationState(InformationState):
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