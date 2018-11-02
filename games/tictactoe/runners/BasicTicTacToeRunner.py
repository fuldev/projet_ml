import os

from keras.engine.saving import load_model
from tensorflow import keras

from agents.DeepQLearningAgent import DeepQLearningAgent
from agents.RandomRolloutAgent import RandomRolloutAgent

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from agents.CommandLineAgent import CommandLineAgent
from agents.RandomAgent import RandomAgent
from agents.TabularQLearningAgent import TabularQLearningAgent
from environments import Agent
from environments.GameRunner import GameRunner
from environments.GameState import GameState
from games.tictactoe.TicTacToeGameState import TicTacToeGameState
import numpy as np


class BasicTicTacToeRunner(GameRunner):

    def __init__(self, agent1: Agent, agent2: Agent,
                 print_and_reset_score_history_threshold=None,
                 replace_player1_with_commandline_after_similar_results=None):
        self.agents = (agent1, agent2)
        self.stuck_on_same_score = 0
        self.prev_history = None
        self.print_and_reset_score_history_threshold = print_and_reset_score_history_threshold
        self.replace_player1_with_commandline_after_similar_results = replace_player1_with_commandline_after_similar_results

    def run(self, max_rounds: int = -1,
            initial_game_state: TicTacToeGameState = TicTacToeGameState()) -> 'Tuple[float]':
        round_id = 0

        score_history = np.array((0, 0, 0))
        while round_id < max_rounds or round_id == -1:
            gs = initial_game_state.copy_game_state()
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
                    score_history += (1 if score == 1 else 0, 1 if score == -1 else 0, 1 if score == 0 else 0)
                    other_player = (current_player + 1) % 2
                    self.agents[other_player].observe(
                        (1 if other_player == 0 else -1) * score,
                        terminal)

            if round_id != -1:
                round_id += 1
                if self.print_and_reset_score_history_threshold is not None and \
                        round_id % self.print_and_reset_score_history_threshold == 0:
                    print(score_history / self.print_and_reset_score_history_threshold)
                    if self.prev_history is not None and \
                            score_history[0] == self.prev_history[0] and \
                            score_history[1] == self.prev_history[1] and \
                            score_history[2] == self.prev_history[2]:
                        self.stuck_on_same_score += 1
                    else:
                        self.prev_history = score_history
                        self.stuck_on_same_score = 0
                    if (self.replace_player1_with_commandline_after_similar_results is not None and
                            self.stuck_on_same_score >= self.replace_player1_with_commandline_after_similar_results):
                        self.agents = (CommandLineAgent(), self.agents[1])
                        self.stuck_on_same_score = 0
                    score_history = np.array((0, 0, 0))
        return tuple(score_history)


if __name__ == "__main__":
    # print("Rdm vs Rdm")
    # print(BasicTicTacToeRunner(RandomAgent(),
    #                            RandomAgent(),
    #                            print_and_reset_score_history_threshold=100).run(1000000))

    print("Rdm vs DeepQLearning (should be around 80% wins for player 2)")
    print(BasicTicTacToeRunner(RandomAgent(),
                               DeepQLearningAgent(9, 9, lr=0.001, gamma=0.9, num_layers=5,
                                                  num_hidden_per_layer=64,
                                                  target_update_every=1000),
                               print_and_reset_score_history_threshold=100).run(10000))

    print("DeepQLearning vs Rdm (should be around 90/95% wins for player 1)")
    print(BasicTicTacToeRunner(DeepQLearningAgent(9, 9, lr=0.001, gamma=0.9, num_layers=5,
                                                  num_hidden_per_layer=64,
                                                  target_update_every=1000),
                               RandomAgent(),
                               print_and_reset_score_history_threshold=100).run(10000))

    print("DeepQLearning vs DeepQLearning (should oscillate between 95% win for player 1 and 95% " +
          "draw if we let it run for a long time)")
    print(BasicTicTacToeRunner(DeepQLearningAgent(9, 9, lr=0.001, gamma=0.9, num_layers=5,
                                                  num_hidden_per_layer=64,
                                                  target_update_every=1000),
                               DeepQLearningAgent(9, 9, lr=0.001, gamma=0.9, num_layers=5,
                                                  num_hidden_per_layer=64,
                                                  target_update_every=1000),
                               print_and_reset_score_history_threshold=100).run(100000))
    # print(BasicTicTacToeRunner(RandomAgent(), RandomRolloutAgent(100,
    #                                                              BasicTicTacToeRunner(RandomAgent(), RandomAgent())),
    #                            print_and_reset_score_history_threshold=100).run(1000000))
