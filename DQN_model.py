from keras.models import Graph, Sequential, model_from_json
import numpy as np
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.core import Activation, Dense, Flatten
from keras.optimizers import RMSprop
import time

class Model:
    def __init__(self):
        # parameters for Q-learning
        self.discount_rate = 0.99

        # parameters for CNN
        nb_filters = 32
        img_rows = 4
        img_cols = 4
        nb_conv = 2
        in_channels = 10
        nb_actions = 4

        # Build deep neuro network.
        model = Graph()
        model.add_input(name = 'state', input_shape = (in_channels, img_rows, img_cols))
        model.add_input(name = 'action', input_shape = (nb_actions,))
        model.add_node(Flatten(), name='action_', input='action')
        model.add_node(Convolution2D(nb_filters, nb_conv, nb_conv, dim_ordering='th'), name = 'con1', input = 'state')
        model.add_node(Activation('relu'), name = 'act1', input = 'con1')
        model.add_node(Convolution2D(nb_filters, nb_conv, nb_conv, dim_ordering='th'), name = 'con2', input = 'act1')
        model.add_node(Activation('relu'), name = 'act2', input = 'con2')
        model.add_node(Flatten(), name = 'flat', input = 'act2')
        model.add_node(Dense(128), name = 'den1', input = 'flat')
        model.add_node(Activation('relu'), name = 'act3', input = 'den1')
        model.add_node(Dense(nb_actions), name = 'den2', input = 'act3')
        model.add_output(name = 'out', inputs = ['den2', 'action_'], merge_mode = 'mul')
        model.compile(optimizer=RMSprop(lr=0.001, rho=0.9, epsilon=1e-06), loss={'out':'mse'})

        self.model = model
        self.max_memory = 10000
        self.memory = [[], [], []]  # record all the experiences, when the size reach max_memory, train the model.

    def get_q(self, state):
        return self.model.predict(data = {'state': [state], 'action':[[1, 1, 1, 1]]})[0]

    def add_transfer(self, state1, action, state2, reward):
        # Add the current transfer into memory
        action_map = {'w':[1, 0, 0, 0], 's': [0, 1, 0, 0], 'a': [0, 0, 1, 0], 'd': [0, 0, 0, 1]}
        action = action_map[action]
        best_q = max(self.model.predict(data = {'state': [state2], 'action':[[1, 1, 1, 1]]})[0])
        self.memory[0].append(state1)
        self.memory[1].append(action)
        self.memory[2].append(reward + self.discount_rate * best_q)

        # When the memory is full, train!
        if len(self.memory[0]) >= self.max_memory:
            self.model.fit({'state': self.memory[0], 'action': self.memory[1], 'out': self.memory[2]}, batch_size = 32,
                           nb_epoch = 10)
            self.memory = [[], [], []]

    def dumps(self):
        f = file('model%d.txt' % time.time(), 'w')
        f.write(str(self.model.to_json()))
        f.close()

    def loads(self, filename):
        f = file(filename, 'r')
        self.model = model_from_json(''.join(f.readlines()))
