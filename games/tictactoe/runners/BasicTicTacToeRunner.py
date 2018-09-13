from agents.RandomAgent import RandomAgent
from environments import Agent
from environments.GameRunner import GameRunner
from environments.GameState import GameState
from games.tictactoe.TicTacToeGameState import TicTacToeGameState


class BasicTicTacToeRunner(GameRunner):

    def __init__(self, agent1: Agent, agent2: Agent):
        self.agents = (agent1, agent2)

    def run(self, max_rounds: int = -1) -> 'Tuple[float]':
        round_id = 0

        while round_id < max_rounds or round_id == -1:
            gs = TicTacToeGameState()
            print(gs)
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
                    other_player = (current_player + 1) % 2
                    self.agents[other_player].observe(
                        (1 if other_player == 0 else -1) * score,
                        terminal)

                print(gs)

            if round_id != -1:
                round_id += 1


if __name__ == "__main__":
    BasicTicTacToeRunner(RandomAgent(), RandomAgent()).run(10)
