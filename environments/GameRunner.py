from environments import GameState

class GameRunner:
    def run(self, initial_game_state: GameState, max_rounds: int = -1) -> 'Tuple[float]':
        raise NotImplementedError


