from environments import GameState


class InformationState:

    def __hash__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def create_game_state_from_information_state(self):
        raise NotImplementedError
