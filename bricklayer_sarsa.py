#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import random

lengths =\
    {'A':[4,1],'B':[3,2],'C':[3,2],'D':[3, 2],'E':[3,2],'F':[3,2],'G':[2,2]}

class BricklayerSarsa:
    """Bricklayer class which deals with remembering
       SARSA learning specifics like:
       - state-action mappings and their utility
       - parameters like alpha (learning rate).
    """

    def __init__(self, height, length, alpha=0.1, eps=0.1):
        self.height = height
        self.length = length
        # By default return (rotation,left) = (0,0).
        self.maps = defaultdict(lambda: (0,0))

        # Parameters determined empirically.
        self.alpha = alpha
        self.eps = eps

    def get_action(self, line):
        """Get an action based on a line which encodes
        REWARD, STATE, BRICK information.

        This is an ε-greedy policy that based on the
        utilities built it returns an action for a
        state.

        Returns:
            an action of the form (rotation, offset).
        """
        # Increasing epsilon has the effect of making less
        # random choices while times passes, because the SARSA algorithm
        # will learn with time and can make more informed decisions.
        self.eps += 0.01

        if (random.random() <= self.eps):
            return self.__get_action_greedy(line)
        # Else pick a random action from all possible actions
        return self.__get_action_random(line)

    def update_utilities(self, line, action, next_line, next_action):
        """Update the utity self.maps based on the current
        and next move.

        Args:
            line: current state
            next_line: next state arriving from current state
                       by taking an action from get_action(line).
                       It also contains information about reward.
        """
        pass

    def __get_action_greedy(self, line):
        """Compute a list of possible (legal) moves from a given
        state. Choose from that list the one that maximises the
        utility function.
        """
        #legal_moves = __get_legal_actions(line)
        return self.__get_action_random(line)

    def __get_legal_actions(self, line):
        """
        """
        pass

    def __get_action_random(self, line):
        """Simply returns a tuple of legal random
        rotation and left offset.
        """
        rot = random.randint(0, 3)
        max_offset = self.length - lengths[line[-1]][rot % 2]
        offset = random.randint(0, max_offset)
        return (rot, offset)

