from environments import InformationState


class GameState:

    # WARNING : Action space must be finite !!!!
    def step(self,
             player_id: int,
             action_id: int) -> \
            ('GameState', float, bool):
        raise NotImplementedError

    def get_player_count(self) -> int:
        raise NotImplementedError

    def get_current_player_id(self) -> int:
        raise NotImplementedError

    def get_information_state_for_player(self, player_id: int) -> 'InformationState':
        raise NotImplementedError

    def get_available_actions_id_for_player(self, player_id: int) -> 'Iterable(int)':
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
