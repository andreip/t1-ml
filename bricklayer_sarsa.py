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

    def get_action(self, line):
        rot = random.randint(0, 3)
        max_offset = self.length - lengths[line[-1]][rot % 2]
        offset = random.randint(0, max_offset)
        return [rot, offset]
