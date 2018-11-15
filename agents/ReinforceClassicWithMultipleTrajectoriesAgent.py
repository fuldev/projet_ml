import numpy as np
from keras.utils import to_categorical

from agents.ReinforceClassicAgent import ReinforceClassicBrain
from environments import InformationState
from environments.Agent import Agent


class ReinforceClassicWithMultipleTrajectoriesAgent(Agent):

    def __init__(self, state_size, action_size, num_layers=5,
                 num_neuron_per_layer=128,
                 train_every_X_trajectories=16):
        self.brain = ReinforceClassicBrain(state_size, num_layers, num_neuron_per_layer, action_size)
        self.action_size = action_size
        self.trajectories = []
        self.current_trajectory_buffer = []
        self.train_every_X_trajectory = train_every_X_trajectories

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

        self.current_trajectory_buffer.append(transition)

        return chosen_action

    def observe(self, reward: float, terminal: bool) -> None:
        if not self.current_trajectory_buffer:
            return

        self.current_trajectory_buffer[len(self.current_trajectory_buffer) - 1]['r'] += reward
        self.current_trajectory_buffer[len(self.current_trajectory_buffer) - 1]['t'] |= terminal

        if terminal:

            R = 0.0
            for t in reversed(range(len(self.current_trajectory_buffer))):
                R = self.current_trajectory_buffer[t]['r'] + 0.9 * R
                self.current_trajectory_buffer[t]['R'] = R

            self.trajectories.append(self.current_trajectory_buffer)
            self.current_trajectory_buffer = []

            if len(self.trajectories) == self.train_every_X_trajectory:
                states = np.array([transition['s'] for trajectory in self.trajectories for transition in trajectory])
                actions = np.array([transition['a'] for trajectory in self.trajectories for transition in trajectory])
                advantages = np.array([transition['R'] for trajectory in self.trajectories for transition in trajectory])

                self.brain.train_policies(states, actions, advantages)
                self.trajectories = []
