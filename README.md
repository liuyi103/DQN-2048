# DQN-2048

This project implements an agent for the game 2048 by deep Q-network (DQN). The current model does not work well.

## Requirements

This project should work on Windows, Mac and Linux. It requires:

+ Python 2.7
+ numpy
+ tensorflow or Theano
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

## Current performance

When lucky, the agent can get 5000+ points. Usually, it gets 1000 ~ 5000 points.
It is significantly better than random agent.
For a human player, one can usually get ~20000 points and win the game when he or she knows the "corner trick".
Otherwise, maybe just like this agent.

## Help needed

I am not experienced in deep learning.
So, I am almost sure that there should be many improvements to be done.
I would like to see others' improvements.
The licence? Do whatever you want on it.