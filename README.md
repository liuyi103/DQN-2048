# DQN-2048

This project implements an agent for the game 2048 by deep Q-network (DQN). The current model does not work well.

## Requirements

This project should work on Windows, Mac and Linux. It requires:

+ Python 2.7
+ numpy 1.10.4+
+ tensorflow or theano
+ keras

## Structure

+ DQN_model.py: The implementation of DQN
+ demo.py: A demo plays 2048 automatically.
+ fastplay.py: Run 2048 with optimal policy. (Only called by other programs)
+ game2048.py: The implementation of the game
+ human_play.py: Play 2048. 'w', 's', 'a', 'd' for up, down, left and right
+ main.py: Train the model
+ my_model_weightsXXXX.h5: The weights for the current model. Used by demo
+ test_game2048.py: unittests.
