#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import random

from bricklayer_board import BricklayerBoard

class BricklayerSarsa:
    """Bricklayer class which deals with remembering SARSA learning specifics
    like:
       - state-action mappings and their utility
       - parameters like alpha (learning rate).

    For more detailed information about how we represent Tetris states,
    check the README file.
    """

    def __init__(self, height, length, alpha=0.1, eps=0.1, gamma=0.8,
                 maps=defaultdict(int)):
        self.height = height
        self.length = length
        # By default return a score of 0 for unknown.
        self.maps = maps

        # Parameters determined empirically.
        self.alpha = alpha
        self.eps = eps
        self.gamma = gamma

    def get_action(self, line):
        """Get an action based on a line which encodes
        REWARD, STATE, BRICK information.

        This is an ε-greedy policy that based on the
        utilities built it returns an action for a
        state.

        Returns:
            an action of the form (rotation, offset).
        """
        if 'GAME OVER' in line:
            return None

        # Increasing epsilon has the effect of making less
        # random choices while times passes, because the SARSA algorithm
        # will learn with time and can make more informed decisions.
        self.eps += 0.01

        # Compute all the legal actions one can don from a
        # position. Next choose among them with a stragey.
        [_, boardStr, brick] = line.split(',')
        board = BricklayerBoard(boardStr)
        legal_actions = board.get_legal_actions(brick)
        board_state = board.get_board_diff_levels()

        if (random.random() <= self.eps):
            return self.__get_action_greedy(board_state, legal_actions)
        # Else pick a random action from all possible actions
        return self.__get_action_random(legal_actions)

    def update_utilities(self, line, action, next_line, next_action):
        """Update the utity self.maps based on the current
        and next move.

        Args:
            line: current state
            next_line: next state arriving from current state
                       by taking an action from get_action(line).
                       It also contains information about reward.
        """
        state_key = self.get_state_key_from_line(line, action)
        next_state_key = self.get_state_key_from_line(next_line, next_action)
        reward = int(next_line.split(',')[0])

        # Update the utilities based from state_key based on next_state_key.
        self.maps[state_key] = (1-self.alpha) * self.maps[state_key] +\
            self.alpha * (reward + self.gamma * self.maps[next_state_key])

    def get_state_key_from_line(self, line, action):
        if 'GAME OVER' in line:
            [rewardStr, boardStr] = line.split(',')
            return (boardStr, action)
        else:
            [_, boardStr, _] = line.split(',')
            board_state = BricklayerBoard(boardStr).get_board_diff_levels()
            return (board_state, action)

    def __get_action_greedy(self, board_state, legal_actions):
        """Compute a list of possible (legal) moves from a given
        state. Choose from that list the one that maximises the
        utility function.
        """
        max_action = legal_actions[0]
        max_score = self.maps[(board_state, max_action)]

        for action in legal_actions[1:]:
            score = self.maps[(board_state, action)]
            if score > max_score:
                max_score = score
                max_action = action
        return max_action

    def __get_action_random(self, legal_actions):
        """Simply returns a tuple of legal random
        rotation and left offset.
        """
        return random.choice(legal_actions)

