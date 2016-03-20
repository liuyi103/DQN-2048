# This code implementss DQN for the game 2048.
# Unlike the original paper, we directly use the numbers in the grids as inputs.
# The input is consists of 10 frames. The i-th frame is a board for board[i][j] == 2 ** i, which is binary.
# The structure of the network is as follows.
#
#
#
from keras.models import Sequential
import numpy as np
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.core import Activation, Dense, Flatten
from keras.optimizers import RMSprop

# parameters for DQN
nb_filters = 32
img_rows = 4
img_cols = 4
nb_conv = 2
in_channels = 10

# Build deep neuro network.
model = Sequential()
model.add(Convolution2D(nb_filters, nb_conv, nb_conv, dim_ordering = 'th',
                        input_shape = (in_channels, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(4))

model.compile(optimizer=RMSprop(lr=0.001, rho=0.9, epsilon=1e-06), loss = 'mse')