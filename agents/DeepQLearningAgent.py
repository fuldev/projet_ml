import random

import keras
import numpy as np
from keras import Sequential, Input, Model
from keras.activations import relu, linear
from keras.constraints import maxnorm
from keras.layers import Dense, Flatten, Concatenate, BatchNormalization
from keras.losses import mse
from keras.optimizers import sgd, rmsprop

from environments import InformationState
from environments.Agent import Agent


class DeepQLearningAgent(Agent):
    def __init__(self, input_size, action_size, num_layers=3, num_hidden_per_layer=256, epsilon=0.01, lr=0.01,
                 gamma=0.9, use_target=True, target_update_every=100, print_error=True, print_error_every=100):
        self.lr = lr
        self.use_target = use_target
        self.target_update_every = target_update_every
        self.print_error = print_error
        self.print_error_every = print_error_every
        self.Q = self.create_net(input_size, action_size, num_layers, num_hidden_per_layer)
        self.QTarget = self.create_net(input_size, action_size, num_layers, num_hidden_per_layer)
        self.QTarget.set_weights(self.Q.get_weights())
        self.s = None
        self.a = None
        self.r = None
        self.t = None
        self.s_next_duplicated = None
        self.s_next_available_actions = None
        self.game_count = 0
        self.epsilon = epsilon
        self.gamma = gamma
        self.input_size = input_size
        self.action_size = action_size
        self.reward_history = np.array((0, 0, 0))
        self.accumulated_error = 0.0
        self.learn_steps = 0

    def create_net(self, input_size, action_size, num_layers, num_hidden_per_layer):
        input_state = Input(shape=(input_size,))
        input_action = Input(shape=(action_size,))
        inputs = Concatenate()([input_state, input_action])
        hidden = inputs
        for i in range(num_layers):
            hidden = Dense(num_hidden_per_layer, activation=relu, kernel_constraint=maxnorm(), bias_constraint=maxnorm())(hidden)
        q = Dense(1, activation=linear)(hidden)
        model = Model([input_state, input_action], q)
        model.compile(optimizer=rmsprop(self.lr), loss=keras.losses.mse)
        return model

    def observe(self, reward: float, terminal: bool) -> None:
        if self.s is not None:
            self.r = (self.r if self.r else 0.0) + reward
            self.t = terminal

            if terminal:
                self.reward_history += (1 if reward == 1 else 0, 1 if reward == -1 else 0, 1 if reward == 0 else 0)
                self.learn()
                self.game_count += 1
                if (self.use_target and self.game_count % self.target_update_every) == 0:
                    print('Updating Target Network')
                    self.QTarget.set_weights(self.Q.get_weights())

    def act(self, player_index: int, information_state: InformationState, available_actions: 'Iterable[int]') -> int:

        available_actions_list = list(available_actions)

        inputs_states = np.array([information_state.vectorize()] * len(available_actions_list))
        actions_vectorized = np.array(
            [keras.utils.to_categorical(action_id, self.action_size) for action_id in available_actions_list])

        if self.s is not None:
            self.s_next_duplicated = inputs_states
            self.s_next_available_actions = actions_vectorized
            self.t = False
            self.learn()

        if random.random() > self.epsilon:
            q_values = self.Q.predict([inputs_states, actions_vectorized]).flatten()
            best_id = q_values.argmax()
        else:
            best_id = random.randint(0, len(available_actions_list) - 1)

        self.s = inputs_states[best_id]
        self.a = actions_vectorized[best_id]

        return available_actions_list[best_id]

    def reward_scaler(self, reward):
        if reward == 1:
            return 1.0
        elif reward == 0:
            return 0.0
        return -1.0

    def learn(self):
        self.learn_steps += 1
        target = self.r + 0 if self.t else (
                self.gamma *
                (self.QTarget if self.use_target else self.Q)
                .predict([self.s_next_duplicated,
                          self.s_next_available_actions])
                .flatten().max()
        )

        loss = self.Q.train_on_batch([np.array([self.s]), np.array([self.a])], np.array([target]))
        self.accumulated_error += loss

        self.s = None
        self.a = None
        self.r = None
        self.t = None
        self.s_next_duplicated = None
        self.s_next_available_actions = None

        if self.print_error and self.learn_steps % self.print_error_every == 0:
            print(self.accumulated_error / self.learn_steps)
            self.accumulated_error = 0
