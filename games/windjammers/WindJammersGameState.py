import numpy as np

from environments import InformationState
from environments.GameState import GameState
from games.windjammers.WindJammersInformationState import WindJammersInformationState


class WindJammersGameState(GameState):
    action_to_vector = {
        0: np.array([0.0, 0.0]),
        1: np.array([0.0, 1.0]),
        2: np.array([0.707106781186, 0.707106781186]),
        3: np.array([1.0, 0.0]),
        4: np.array([0.707106781186, -0.707106781186]),
        5: np.array([0.0, -1.0]),
        6: np.array([-0.707106781186, -0.707106781186]),
        7: np.array([-1.0, 0.0]),
        8: np.array([-0.707106781186, 0.707106781186]),
        9: np.array([0.0, 0.0]),
        10: np.array([0.0, 0.0]),
        11: np.array([0.0, 0.0]),
    }

    def __init__(self):
        # constants
        self.player_speed_norm = 6.0 / 60.0
        self.frisbee_speed_norm = 3.0 / 60.0
        self.frisbee_radius = 0.05
        self.player_radius = 0.1
        self.three_points_size = 0.2

        # game dynamics
        self.current_player = 0
        self.frames_left = 3600
        self.player1_score = 0
        self.player2_score = 0
        self.reset_after_score()

    def step(self, player_id: int, action_id: int  # 0 : nothing, 1-9 moving directions, 10-12 shooting directions
             ) -> \
            ('GameState', float, bool):
        if self.current_player != player_id:
            raise Exception("This is not this player turn !")
        if action_id < 0 or action_id > 11:
            raise Exception("Not an available action")

        if self.current_player == -1:
            (score, terminal) = self.compute_current_score_and_end_game_more_efficient()
            self.current_player = 0
            return self, score, terminal

        if self.current_player == 0:
            self.player1_intent = action_id
            self.current_player = 1
        elif self.current_player == 1:
            self.player2_intent = action_id
            self.current_player = -1

        return self, 0, False

    def compute_current_score_and_end_game_more_efficient(self):
        if self.frames_left == 0:
            return self.player1_score - self.player2_score, True

        self.frames_left -= 1

        if self.frisbee_state == 0:
            self.frisbee_position += self.frisbee_speed

        if self.player1_state == 0:
            self.player1_position += self.action_to_vector[self.player1_intent] * self.player_speed_norm
            self.player1_position = np.array([
                min(max(self.player1_position[0], -1.0), 0.0),
                min(max(self.player1_position[1], -1.0), 1.0)
            ])

        if self.player2_state == 0:
            self.player2_position += self.action_to_vector[self.player2_intent] * self.player_speed_norm
            self.player2_position = np.array([
                min(max(self.player2_position[0], 0.0), 1.0),
                min(max(self.player2_position[1], -1.0), 1.0)
            ])

        if self.player1_state == 1:
            self.frisbee_state = 0
            self.player1_state = 0
            if self.player1_intent == 9:
                self.frisbee_speed = np.array([0.707106781186, -0.707106781186]) * self.frisbee_speed_norm
            if self.player1_intent == 10:
                self.frisbee_speed = np.array([1.0, 0.0]) * self.frisbee_speed_norm
            if self.player1_intent == 11:
                self.frisbee_speed = np.array([0.707106781186, 0.707106781186]) * self.frisbee_speed_norm

        if self.player2_state == 1:
            self.frisbee_state = 0
            self.player2_state = 0
            if self.player2_intent == 9:
                self.frisbee_speed = np.array([-0.707106781186, -0.707106781186]) * self.frisbee_speed_norm
            if self.player2_intent == 10:
                self.frisbee_speed = np.array([-1.0, 0.0]) * self.frisbee_speed_norm
            if self.player2_intent == 11:
                self.frisbee_speed = np.array([-0.707106781186, 0.707106781186]) * self.frisbee_speed_norm

        if self.frisbee_hit_top_or_bottom():
            self.frisbee_position = np.array([self.frisbee_position[0],
                                             (1.0 - self.frisbee_radius) if self.frisbee_position[1] > 0 else
                                             (-1.0 + self.frisbee_radius)])
            self.frisbee_speed = np.array([self.frisbee_speed[0], -self.frisbee_speed[1]])

        if self.frisbee_hit_player1():
            self.frisbee_state = 1
            self.frisbee_position = self.player1_position
            self.player1_state = 1

        if self.frisbee_hit_player2():
            self.frisbee_state = 1
            self.frisbee_position = self.player2_position
            self.player2_state = 1

        frame_delta = 0.0

        (hit, points) = self.frisbee_hit_left()
        if hit:
            self.player2_score += points
            self.reset_after_score()
            frame_delta = -points

        (hit, points) = self.frisbee_hit_right()
        if hit:
            self.player1_score += points
            self.reset_after_score()
            frame_delta = points

        return frame_delta, False

    def reset_after_score(self):
        self.player1_state = 0  # 0 : standing, 1 : holding frisbee
        self.player2_state = 0  # 0 : standing, 1 : holding frisbee
        self.frisbee_state = 0  # 0: rolling, 1 : held
        self.player1_intent = 0
        self.player2_intent = 0
        self.player1_position = np.array([-0.5, 0.0])
        self.player2_position = np.array([0.5, 0.0])
        self.frisbee_position = np.array([0.0, 0.0])
        self.frisbee_speed = self.action_to_vector[np.random.choice([2, 3, 4, 6, 7, 8])] * self.frisbee_speed_norm

    def frisbee_hit_left(self) -> (bool, int):
        if self.frisbee_position[0] - self.frisbee_radius < -1.0:
            if abs(self.frisbee_position[1]) < self.three_points_size:
                return True, 3.0
            return True, 1.0
        return False, 0.0

    def frisbee_hit_right(self) -> (bool, int):
        if self.frisbee_position[0] + self.frisbee_radius > 1.0:
            if abs(self.frisbee_position[1]) < self.three_points_size:
                return True, 3.0
            return True, 1.0
        return False, 0.0

    def frisbee_hit_top_or_bottom(self) -> bool:
        return abs(self.frisbee_position[1]) + self.frisbee_radius > 1.0

    def frisbee_hit_player1(self) -> bool:
        return np.linalg.norm(self.player1_position - self.frisbee_position) < \
               self.frisbee_radius + self.player_radius and \
               self.frisbee_speed[0] < 0

    def frisbee_hit_player2(self) -> bool:
        return np.linalg.norm(self.player2_position - self.frisbee_position) < \
               self.frisbee_radius + self.player_radius and \
               self.frisbee_speed[0] > 0

    def get_player_count(self) -> int:
        return 2

    def get_current_player_id(self) -> int:
        return self.current_player

    def get_information_state_for_player(self, player_id: int) -> 'InformationState':
        return WindJammersInformationState(self)

    def get_available_actions_id_for_player(self, player_id: int) -> 'Iterable(int)':
        if player_id != self.current_player:
            return []
        if player_id == 0:
            if self.player1_state == 0:
                return [0, 1, 2, 3, 4, 5, 6, 7, 8]
            if self.player1_state == 1:
                return [9, 10, 11]

        if player_id == 1:
            if self.player2_state == 0:
                return [0, 1, 2, 3, 4, 5, 6, 7, 8]
            if self.player2_state == 1:
                return [9, 10, 11]

    def __str__(self):
        str_acc = ""
        for j in reversed(range(-10, 11)):
            for i in range(-10, 11):
                c = " "
                if i == -10 or j == -10 or i == 10 or j == 10:
                    c = "¤"
                if i == round(self.frisbee_position[0] * 10.0) and j == round(self.frisbee_position[1] * 10.0):
                    c = "O"
                if i == round(self.player1_position[0] * 10.0) and j == round(self.player1_position[1] * 10.0):
                    c = "1"
                if i == round(self.player2_position[0] * 10.0) and j == round(self.player2_position[1] * 10.0):
                    c = "2"
                str_acc += c
            str_acc += "\n"
        return str_acc

    def copy_game_state(self):
        gs = WindJammersGameState()
        gs.player1_position = self.player1_position.copy()
        gs.player1_state = self.player1_state
        gs.player1_score = self.player1_score
        gs.player1_intent = self.player1_intent
        gs.player2_position = self.player2_position.copy()
        gs.player2_state = self.player2_state
        gs.player2_score = self.player2_score
        gs.player2_intent = self.player2_intent
        gs.frisbee_position = self.frisbee_position.copy()
        gs.frisbee_state = self.frisbee_state
        gs.frisbee_speed = self.frisbee_speed.copy()
        gs.frisbee_radius = self.frisbee_radius
        gs.frisbee_speed_norm = self.frisbee_speed_norm
        gs.player_speed_norm = self.player_speed_norm
        gs.player_radius = self.player_radius
        gs.three_points_size = self.three_points_size
        gs.frames_left = self.frames_left
        gs.current_player = self.current_player
        return gs


if __name__ == "__main__":
    gs = WindJammersGameState()
    print(gs.get_available_actions_id_for_player(gs.get_current_player_id()))
    print(gs)
