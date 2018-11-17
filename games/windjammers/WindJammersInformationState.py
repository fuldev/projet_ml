import numpy as np

from environments.InformationState import InformationState


class WindJammersInformationState(InformationState):

    def __hash__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return \
            np.array_equal(self.player1_position, other.player1_position) and \
            self.player1_state == other.player1_state and \
            self.player1_score == other.player1_score and \
            self.player1_intent == other.player1_intent and \
            np.array_equal(self.player2_position, other.player2_position) and \
            self.player2_state == other.player2_state and \
            self.player2_score == other.player2_score and \
            self.player2_intent == other.player2_intent and \
            np.array_equal(self.frisbee_position, other.frisbee_position) and \
            self.frisbee_state == other.frisbee_state and \
            np.array_equal(self.frisbee_speed, other.frisbee_speed) and \
            self.frisbee_radius == other.frisbee_radius and \
            self.frisbee_speed_norm == other.frisbee_speed_norm and \
            self.player_speed_norm == other.player_speed_norm and \
            self.player_radius == other.player_radius and \
            self.three_points_size == other.three_points_size and \
            self.frames_left == other.frames_left and \
            self.current_player == other.current_player

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, game_state):
        self.player1_position = game_state.player1_position.copy()
        self.player1_state = game_state.player1_state
        self.player1_score = game_state.player1_score
        self.player1_intent = game_state.player1_intent
        self.player2_position = game_state.player2_position.copy()
        self.player2_state = game_state.player2_state
        self.player2_score = game_state.player2_score
        self.player2_intent = game_state.player2_intent
        self.frisbee_position = game_state.frisbee_position.copy()
        self.frisbee_state = game_state.frisbee_state
        self.frisbee_speed = game_state.frisbee_speed.copy()
        self.frisbee_radius = game_state.frisbee_radius
        self.frisbee_speed_norm = game_state.frisbee_speed_norm
        self.player_speed_norm = game_state.player_speed_norm
        self.player_radius = game_state.player_radius
        self.three_points_size = game_state.three_points_size
        self.frames_left = game_state.frames_left
        self.current_player = game_state.current_player

    def __str__(self):
        str_acc = "current player : " + str(self.current_player) + "\n"
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

    def vectorize(self):
        return np.array([
            self.player1_position[0],
            self.player1_position[1],
            self.player2_position[0],
            self.player2_position[1],
            self.frisbee_position[0],
            self.frisbee_position[1],
            self.frisbee_speed[0],
            self.frisbee_speed[1]
        ])

    def create_game_state_from_information_state(self):
        from games.windjammers.WindJammersGameState import WindJammersGameState
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
