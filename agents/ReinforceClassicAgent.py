from keras import Sequential, Input, Model
from keras.activations import tanh, sigmoid
from keras.layers import Dense, concatenate
from keras.optimizers import adam
import numpy as np
from keras.utils import to_categorical

from environments import InformationState
from environments.Agent import Agent
import keras.backend as K


class ReinforceClassicBrain:
    def __init__(self, state_size, num_layers, num_neuron_per_layer, action_size):
        self.state_size = state_size
        self.num_layers = num_layers
        self.num_neuron_per_layer = num_neuron_per_layer
        self.action_size = action_size
        self.model = self.create_model()

    def create_model(self):
        input_state = Input(shape=(self.state_size,))
        input_action = Input(shape=(self.action_size,))

        hidden = concatenate([input_state, input_action])
        for i in range(self.num_layers):
            hidden = Dense(self.num_neuron_per_layer, activation=tanh)(hidden)

        policy = Dense(1, activation=sigmoid)(hidden)

        model = Model([input_state, input_action], policy)
        model.compile(loss=ReinforceClassicBrain.reinforce_loss, optimizer=adam())
        return model

    def predict_policy(self, state, action):
        return self.model.predict([np.array([state]), np.array([action])])[0]

    def predict_policies(self, states, actions):
        return self.model.predict([states, actions])

    def reinforce_loss(y_pred, y_true):
        return -K.log(y_pred) * y_true

    def train_policy(self, state, action, advantage):
        self.model.train_on_batch(
            [np.array([state]), np.array([action])],
            np.array([advantage])
        )

    def train_policies(self, states, actions, advantages):
        self.model.train_on_batch(
            [states, actions],
            advantages
        )


class ReinforceClassicAgent(Agent):

    def __init__(self, state_size, action_size, num_layers=5, num_neuron_per_layer=128):
        self.brain = ReinforceClassicBrain(state_size, num_layers, num_neuron_per_layer, action_size)
        self.action_size = action_size
        self.episode_buffer = []

    def act(self, player_index: int,
            information_state: InformationState,
            available_actions: 'Iterable[int]') -> int:

        vectorized_states = np.array([information_state.vectorize()] * len(available_actions))
        actions_vectorized = np.array([to_categorical(action, self.action_size) for action in available_actions])

        logits = self.brain.predict_policies(vectorized_states, actions_vectorized)

        sum = np.sum(logits)
        probabilities = np.reshape(logits / sum, (len(available_actions),))
        chosen_action = np.random.choice(available_actions, p=probabilities)

        transition = dict()
        transition['s'] = information_state.vectorize()
        transition['a'] = to_categorical(chosen_action, self.action_size)
        transition['r'] = 0.0
        transition['t'] = False

        self.episode_buffer.append(transition)

        return chosen_action

    def observe(self, reward: float, terminal: bool) -> None:
        if not self.episode_buffer:
            return

        self.episode_buffer[len(self.episode_buffer) - 1]['r'] += reward
        self.episode_buffer[len(self.episode_buffer) - 1]['t'] |= terminal

        if terminal:
            states = np.array([transition['s'] for transition in self.episode_buffer])
            actions = np.array([transition['a'] for transition in self.episode_buffer])

            R = 0.0
            for t in reversed(range(len(self.episode_buffer))):
                R = self.episode_buffer[t]['r'] + 0.9 * R
                self.episode_buffer[t]['R'] = R

            advantages = np.array([transition['R'] for transition in self.episode_buffer])

            self.brain.train_policies(states, actions, advantages)
            self.episode_buffer = []


