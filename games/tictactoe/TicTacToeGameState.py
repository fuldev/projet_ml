from environments.GameState import GameState


class TicTacToeGameState(GameState):
    def step(self, player_id: int, action_id: int) -> \
            ('GameState', float, bool):
        pass

    def get_player_count(self) -> int:
        pass

    def get_current_player_id(self) -> int:
        pass

    def get_information_state_for_player(self, player_id: int) -> 'InformationState':
        pass

    def get_available_actions_id_for_player(self, player_id: int) -> 'Iterable(int)':
        pass

    def __str__(self):
        pass