import os
from time import sleep


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from agents.CommandLineAgent import CommandLineAgent
from agents.RandomAgent import RandomAgent
from environments import Agent
from environments.GameRunner import GameRunner
from games.windjammers.WindJammersGameState import WindJammersGameState
import numpy as np


class BasicWindJammersRunner(GameRunner):

    def __init__(self, agent1: Agent, agent2: Agent,
                 print_and_reset_score_history_threshold=None,
                 replace_player1_with_commandline_after_similar_results=None):
        self.agents = (agent1, agent2)
        self.stuck_on_same_score = 0
        self.prev_history = None
        self.print_and_reset_score_history_threshold = print_and_reset_score_history_threshold
        self.replace_player1_with_commandline_after_similar_results = replace_player1_with_commandline_after_similar_results

    def run(self, max_rounds: int = -1,
            initial_game_state: WindJammersGameState = WindJammersGameState()) -> 'Tuple[float]':
        round_id = 0

        score_history = np.array((0, 0, 0.0))
        while round_id < max_rounds or round_id == -1:
            gs = initial_game_state.copy_game_state()
            terminal = False
            while not terminal:
                sleep(0.016)
                print(gs)
                current_player = gs.get_current_player_id()
                action = 0
                if current_player != -1:
                    action_ids = gs.get_available_actions_id_for_player(current_player)
                    info_state = gs.get_information_state_for_player(current_player)
                    action = self.agents[current_player].act(current_player,
                                                            info_state,
                                                            action_ids)

                # WARNING : Two Players Zero Sum Game Hypothesis
                (gs, score, terminal) = gs.step(current_player, action)
                self.agents[0].observe(score, terminal)
                self.agents[1].observe(-score, terminal)

                if not terminal:
                    score_history += (score if score > 0 else 0.0, -score if score < 0 else 0.0, 0)

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
                    score_history = np.array((0, 0, 0.0))
        return tuple(score_history)


if __name__ == "__main__":

    print("Rdm vs Rdm")
    print(BasicWindJammersRunner(RandomAgent(),
                               RandomAgent(),
                               print_and_reset_score_history_threshold=10).run(10000))

    # print("CommandLine vs CommandLine")
    # print(BasicWindJammersRunner(CommandLineAgent(),
    #                              CommandLineAgent(),
    #                             print_and_reset_score_history_threshold=100).run(100))
