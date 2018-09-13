from environments import InformationState


class Agent:

    # WARNING : Action space must be finite !!!!
    def act(self, player_index: int,
            information_state: InformationState,
            available_actions: 'Iterable[int]') -> int:
        raise NotImplementedError

    def observe(self, reward: float, terminal: bool) -> None:
        raise NotImplementedError

