"""
A collection of classes and functions for playing certain types of
games. Specifically, an implementation of the MCTS algorithm.
"""
import random, Queue
from math import sqrt, log
from random import sample
import InstanceNode

def mcts_uct(ei, iterations, approach):
    """
    Implementation of the UCT variant of the MCTS algorithm.
    """
    root = InstanceNode.InstanceNode(None, None, ei, approach)
    for i in xrange(iterations):
        child = root
        while not child.terminal() and (not child.experimentInstance.AllTestsReached()):
            if not child.fully_expanded():
                child = child.expand()
                break
            else:
                child = child.best_child()
        delta = child.simulation()
        while not child is None:
            child.visits += 1
            child.value += delta
            # delta -= 1
            child = child.parent

    return root.best_action(c=0)