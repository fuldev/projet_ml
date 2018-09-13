import random

from environments import InformationState
from environments.Agent import Agent


class CommandLineAgent(Agent):
    def observe(self, reward: float, terminal: bool) -> None:
        if terminal:
            print("Draw" if reward == 0 else ("You Win" if reward == 1 else "You Lose"))

    def act(self, player_index: int, information_state: InformationState, available_actions: 'Iterable[int]') -> int:
        action_count = len(available_actions)

        while True:
            print(information_state)
            print("Choose action from : " + str(list(available_actions)))
            str_action = input()
            action_id = int(str_action)
            if action_id in available_actions:
                break

        return action_id

