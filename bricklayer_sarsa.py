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

    def __init__(self, height, length, alpha=0.1):
        self.height = height
        self.length = length
        self.alpha = alpha
        # By default return (rotation,left) = (0,0).
        self.maps = defaultdict(lambda: (0,0))
        # Initially set a big random polict, and decrease it over time.
        self.eps = 0.1

    def get_action(self, line):
        """Get an action based on a line which encodes
        REWARD, STATE, BRICK information.

        This is an ε-greedy policy that based on the
        utilities built it returns an action for a
        state.

        Returns an action of the form:
            (rotation, offset) of a brick of type (int,int).
        """
        self.eps += 0.01
        if (random.random() <= eps):
            return __get_action_greedy(line)
        # Else pick a random action from all possible actions
        return __get_action_random(line)

    def __get_action_greedy(self, line):
        """Compute a list of possible (legal) moves from a given
        state. Choose from that list the one that maximises the
        utility function.
        """
        #legal_moves = __get_legal_actions(line)
        pass

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

