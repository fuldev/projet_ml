import random

from environments import InformationState
from environments.Agent import Agent


class TabularQLearningAgent(Agent):
    def __init__(self):
        self.Q = dict()
        self.s = None
        self.a = None
        self.r = None
        self.t = None

    def observe(self, reward: float, terminal: bool) -> None:
        self.r = reward
        self.t = terminal

        if (terminal):
            print(reward)
        if terminal:
            self.learn()
            self.s = None
            self.a = None
            self.r = None
            self.t = None


    def act(self, player_index: int, information_state: InformationState, available_actions: 'Iterable[int]') -> int:

        if self.s is not None:
            self.s_next = information_state
            self.learn()

        if not (information_state in self.Q):
            self.Q[information_state] = dict()
            for action in available_actions:
                self.Q[information_state][action] = 0

        best_action = None
        best_action_score = 0
        for action in available_actions:
            if best_action is None or best_action_score < self.Q[information_state][action]:
                best_action = action
                best_action_score = self.Q[information_state][action]

        self.s = information_state
        self.a = best_action

        return best_action

    def learn(self):
        max = -99999999
        if self.t:
            for val in self.Q[self.s_next].values():
                if val > max:
                    max = val

        self.Q[self.s][self.a] += 0.1 * (self.r + (0 if self.t else (0.9 * max)) - self.Q[self.s][self.a])
