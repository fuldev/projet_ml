import random
import numpy as np

from environments import InformationState, GameRunner
from environments.Agent import Agent


class RandomRolloutAgent(Agent):

    def __init__(self, num_rollouts_per_available_action, runner: GameRunner):
        self.num_rollouts_per_available_action = num_rollouts_per_available_action
        self.runner = runner

    def observe(self, reward: float, terminal: bool) -> None:
        pass

    def act(self, player_index: int, information_state: InformationState, available_actions: 'Iterable[int]') -> int:
        actions = tuple(available_actions)
        action_count = len(actions)
        action_scores = np.zeros(action_count)
        for i in range(action_count):
            gs = information_state.create_game_state_from_information_state()
            (result_gs, score, terminal) = gs.step(player_index, actions[i])

            # Two player zero sum game hypothesis
            player_score = (1 if player_index == 0 else -1) * score
            if not terminal:
                history = self.runner.run(self.num_rollouts_per_available_action, gs)
                player_score += history[player_index] - history[(player_index + 1) % 2]
            player_score = player_score / (1.0 if terminal else self.num_rollouts_per_available_action)
            action_scores[i] = player_score
        return actions[np.argmax(action_scores)]

