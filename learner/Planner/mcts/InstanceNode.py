__author__ = 'amir'


import random, Queue
from math import sqrt, log
from random import sample

class InstanceNode(object):

    def __init__(self, parent, action, experimentInstance, approach):
        """
        approach - how to combine tests probabilities to qvalue.
            can be one of the following: "uniform" , "hp", "entropy"
        """

        self.experimentInstance = experimentInstance
        self.approach = approach
        self.parent    = parent
        self.children  = dict.fromkeys(self.experimentInstance.get_optionals_actions())
        if not self.experimentInstance.AllTestsReached() and not self.experimentInstance.isTerminal():
            optionals, probabilities = self.experimentInstance.get_optionals_probabilities_by_approach(approach)
            self.children_probability = dict(zip(optionals, probabilities))
        else:
            self.children_probability = {}
        # Tree data
        self.action    = action
         # Search meta data
        self.visits    = 0
        self.value     = 0.0

    @property
    def weight(self):
        """
        The weight of the current node.
        """
        if self.visits == 0:
            return 0
        return self.value / float(self.visits)

    def search_weight(self, c):
        """
        Compute the UCT search weight function for this node. Defined as:

            w = Q(v') / N(v') + c * sqrt(2 * ln(N(v)) / N(v'))

        Where v' is the current node and v is the parent of the current node,
        and Q(x) is the total value of node x and N(x) is the number of visits
        to node x.
        """
        return self.weight + c * sqrt(2 * log(self.parent.visits) / self.visits)

    def actions(self):
        """
        The valid actions for the current node state.
        """
        return self.experimentInstance.get_optionals_actions()

    def result(self, action):
        """
        The state resulting from the given action taken on the current node
        state by the node player.
        """
        return self.experimentInstance.simulate_next_ei(action)[1]

    def terminal(self):
        """
        Whether the current node state is terminal.
        """
        return self.experimentInstance.isTerminal()

    def fully_expanded(self):
        """
        Whether all child nodes have been expanded (instantiated). Essentially
        this just checks to see if any of its children are set to None.
        """
        return not None in self.children.values()

    def expand(self):
        """
        Instantiates one of the unexpanded children (if there are any,
        otherwise raises an exception) and returns it.
        """
        try:
            action = self.children.keys()[self.children.values().index(None)]
        except ValueError:
            raise Exception('Node is already fully expanded')
        ei = self.result(action)
        child = InstanceNode(self, action, ei, self.approach)
        self.children[action] = child
        return child

    def best_child(self, c=1/sqrt(2)):
        """
        return the action with max search_weight + hp. in case that action not expanded weight = 0 .
        """
        if not self.fully_expanded():
            raise Exception('Node is not fully expanded')
        values = []
        for action in self.children:
            weight = self.children[action].search_weight(c)
            values.append((action, weight))
        action = max(values, key=lambda x: x[1])[0]
        # in case that child not expanded - expand
        # if self.children[action] == None:
        #     ei = self.result(action)
        #     child = InstanceNode(self, action, ei, self.approach)
        #     self.children[action] = child
        return self.children[action]

    def best_action(self, c=1/sqrt(2)):
        """
        Returns the action needed to reach the best child from the current
        node.
        """
        child = self.best_child(c)
        return child.action, child.weight

    def max_child(self):
        """
        Returns the child with the highest value.
        """
        return max(self.children.values(), key=lambda x: x.weight)

    def simulation(self):
        """
        Simulates the game to completion, choosing moves in a uniformly random
        manner. The outcome of the simulation is returns as the state value for
        the given player.
        """
        steps = 1
        ei = self.experimentInstance
        while (not ei.isTerminal()) and ( not ei.AllTestsReached()):
            action = sample(ei.get_optionals_actions(), 1)[0]
            ei = ei.simulate_next_ei(action)[1]
            steps = steps + 1
        if  not ei.isTerminal():
            steps = steps + 1
        return -steps
