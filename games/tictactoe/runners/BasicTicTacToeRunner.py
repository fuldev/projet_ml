import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from agents.CommandLineAgent import CommandLineAgent
from agents.DQNLearningAgentCheatSheet import DQNLearningAgent
from agents.RandomAgent import RandomAgent
from agents.TabularQLearningAgent import TabularQLearningAgent
from environments import Agent
from environments.GameRunner import GameRunner
from environments.GameState import GameState
from games.tictactoe.TicTacToeGameState import TicTacToeGameState
import numpy as np


class BasicTicTacToeRunner(GameRunner):

    def __init__(self, agent1: Agent, agent2: Agent):
        self.agents = (agent1, agent2)
        self.stuck_on_same_score = 0
        self.prev_history = None

    def run(self, max_rounds: int = -1) -> 'Tuple[float]':
        round_id = 0

        score_history = np.array((0, 0, 0))
        while round_id < max_rounds or round_id == -1:
            gs = TicTacToeGameState()
            terminal = False
            while not terminal:
                current_player = gs.get_current_player_id()
                action_ids = gs.get_available_actions_id_for_player(current_player)
                info_state = gs.get_information_state_for_player(current_player)
                action = self.agents[current_player].act(current_player,
                                                         info_state,
                                                         action_ids)

                # WARNING : Two Players Zero Sum Game Hypothesis
                (gs, score, terminal) = gs.step(current_player, action)
                self.agents[current_player].observe(
                    (1 if current_player == 0 else -1) * score,
                    terminal)

                if terminal:
                    score_history += (1 if score == 1 else 0,1 if score == -1 else 0,1 if score == 0 else 0)
                    other_player = (current_player + 1) % 2
                    self.agents[other_player].observe(
                        (1 if other_player == 0 else -1) * score,
                        terminal)

            if round_id != -1:
                round_id += 1
                if round_id % 1000 == 0:
                    print(score_history / 1000)
                    if self.prev_history is not None and \
                        score_history[0] == self.prev_history[0] and \
                        score_history[1] == self.prev_history[1] and \
                        score_history[2] == self.prev_history[2] :
                        self.stuck_on_same_score += 1
                    else:
                        self.prev_history = score_history
                        self.stuck_on_same_score = 0
                    if (self.stuck_on_same_score >= 5):
                        self.agents = (CommandLineAgent(), self.agents[1])
                        self.stuck_on_same_score = 0
                    score_history = np.array((0, 0, 0))


if __name__ == "__main__":
    BasicTicTacToeRunner(TabularQLearningAgent(),TabularQLearningAgent()).run(100000000)
