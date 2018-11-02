import numpy as np

from environments import InformationState
from environments.Agent import Agent


class TabularQLearningAgent(Agent):
    def __init__(self):
        self.Q = dict()
        self.s = None
        self.a = None
        self.r = None
        self.t = None
        self.s_next = None
        self.game_count = 0
        self.reward_history = np.array((0, 0, 0))

    def observe(self, reward: float, terminal: bool) -> None:
        if self.s is not None:
            self.r = (self.r if self.r else 0) + reward
            self.t = terminal

            if terminal:
                self.reward_history += (1 if reward == 1 else 0, 1 if reward == -1 else 0, 1 if reward == 0 else 0)
                self.learn()
                self.s = None
                self.a = None
                self.r = None
                self.t = None
                self.game_count += 1
                if (self.game_count % 1000) == 0:
                    print(self.reward_history / 1000)
                    self.reward_history = np.array((0, 0, 0))

    def act(self, player_index: int, information_state: InformationState, available_actions: 'Iterable[int]') -> int:

        if not (information_state in self.Q):
            self.Q[information_state] = dict()
            for action in available_actions:
                self.Q[information_state][action] = 1.1

        if self.s is not None:
            self.s_next = information_state
            self.learn()

        best_action = None
        best_action_score = 0
        for action in available_actions:
            if best_action is None or best_action_score < self.Q[information_state][action]:
                best_action = action
                best_action_score = self.Q[information_state][action]

        self.s = information_state
        self.a = best_action

        return best_action

    def reward_scaler(self, reward):
        if reward == 1:
            return 1.0
        elif reward == 0:
            return 0.0
        return -1.0

    def learn(self):
        self.Q[self.s][self.a] += 0.1 * (
                    self.reward_scaler(self.r) + (0 if self.t else (0.9 * max(self.Q[self.s_next].values()))) -
                    self.Q[self.s][self.a])
