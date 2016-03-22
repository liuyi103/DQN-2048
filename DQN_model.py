from keras.models import Graph, Sequential, model_from_json
import numpy as np
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.core import Activation, Dense, Flatten, Dropout
from keras.optimizers import RMSprop
import time
from fastplay import fast_play
import json
from game2048 import Game2048

def build_CNN():
    '''
    :return: A CNN model for the game
    '''
    # parameters for CNN
    nb_filters = 128
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
    # model.add_node(Dropout(0.5), name = 'dro1', input = 'act3')
    model.add_node(Dense(nb_actions), name = 'den2', input = 'act3')
    model.add_output(name = 'out', inputs = ['den2', 'action_'], merge_mode = 'mul')
    model.compile(optimizer=RMSprop(lr=0.001, rho=0.9, epsilon=1e-06), loss={'out':'mse'})
    return model

class Model:
    def __init__(self, model_name = 'cnn'):
        # parameters for Q-learning
        self.discount_rate = 0.99

        # build the model according to model_name
        name_func = {'cnn':build_CNN}
        self.model = name_func[model_name]()
        self.max_memory = 10000
        self.memory = [[], [], []]  # record all the experiences, when the size reach max_memory, train the model.

    def get_q(self, state):
        return self.model.predict_on_batch(data = {'state': [state], 'action': [np.array([1, 1, 1, 1])]})['out'][0]

    def add_transfer(self, state1, action, state2, reward):
        # Add the current transfer into memory
        action_map = {'w':[1, 0, 0, 0], 's': [0, 1, 0, 0], 'a': [0, 0, 1, 0], 'd': [0, 0, 0, 1]}
        action = np.array(action_map[action])
        best_q = max(self.model.predict_on_batch(data = {'state': [state2], 'action':[np.ones(4)]})['out'][0])
        self.memory[0].append(state1)
        self.memory[1].append(action)
        self.memory[2].append((reward + self.discount_rate * best_q) * action)

        if len(self.memory[0]) >= self.max_memory:
            self.model.fit({'state': np.array(self.memory[0]), 'action': np.array(self.memory[1]),
                            'out': np.array(self.memory[2])}, batch_size = 32, nb_epoch = 10, verbose=0)
            self.memory = [[], [], []]
            print '---------------------'
            for k in range(20):
                print fast_play(self)

    def dumps(self):
        json_string = self.model.to_json()
        open('my_model_architecture.json', 'w').write(json_string)
        self.model.save_weights('my_model_weights%d.h5'%time.time())

    def loads(self, model, weights):
        f = file(model, 'r')
        self.model = model_from_json(''.join(f.readlines()))
        f.close()
        self.model.load_weights(weights)

    @staticmethod
    def board_to_state(board):
        board = np.array(board)
        return np.array([board == 2 ** (i+1) for i in range(10)])
