# __author__ = 'daybreaklee'
from random import *

class MarkovChainGraph(object):
    def __init__(self):
        self.chain = {}

    def add_node(self, value, token):
        self.chain[value] = MarkovChainNode(value, token)

    def __getitem__(self, value):
        return self.chain[value]

class MarkovChainNode(object):
    def __init__(self,  value, token = None,):
        self.state = token
        self.next_states = []
        self.value = value

    def add_next_state(self, node, probability):
        self.next_states.append((node, probability))
        self.next_states.sort(key = lambda ele: ele[1], reverse=True)

    def get_next_state(self):
        # Randomly select a next node from the chain
        probability = random()
        for ele in self.next_states:
            if probability <= ele[1]:
                return ele[0]
            else:
                probability -= ele[1]