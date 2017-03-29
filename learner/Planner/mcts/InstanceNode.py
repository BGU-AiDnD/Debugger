__author__ = 'amir'
from math import sqrt, log
import numpy
import Planner.mcts.mcts
import Planner.mcts.actionNode

class InstanceNode(object):

    def __init__(self, parent, action, experimentInstance, approach):
        """
        approach - how to combine tests probabilities to qvalue.
            can be one of the following: "uniform" , "hp", "entropy"
        """
        self.experimentInstance = experimentInstance
        self.approach = approach
        self.parents = {}
        if not parent is None:
            self.parents[action] = parent
        self.children  = {}
        for act in self.experimentInstance.get_optionals_actions():
            self.children[act] = Planner.mcts.actionNode.ActionNode(act, self, self.approach)
        self.visits = dict.fromkeys(self.children.keys(), 0)
        self.value = dict.fromkeys(self.children.keys(), 0)

    @property
    def weight(self):
        """
        The weight of the current node.
        """
        if sum(self.visits.values()) == 0:
            return 0
        return sum(self.value.values()) / float(sum(self.visits.values()))

    def find_childs(self):
        changed = False
        for c in self.children:
            action = self.children[c]
            if not action.fully_expanded():
                action.getStatesIfExists()
                if action.fully_expanded():
                    changed = True
        if changed:
            self.update_from_childs()

    def update_from_childs(self):
        for c in self.children:
            action = self.children[c]
            self.visits[c] = action.visits()
            self.value[c] = action.value()

    def search_weight(self, c):
        """
        Compute the UCT search weight function for this node. Defined as:

            w = Q(v') / N(v') + c * sqrt(2 * ln(N(v)) / N(v'))

        Where v' is the current node and v is the parent of the current node,
        and Q(x) is the total value of node x and N(x) is the number of visits
        to node x.
        """
        weight = self.weight
        for p in self.parents:
            parent = self.parents[p]
            if sum(parent.visits.values()) == 0:
                continue
            weight += c * sqrt(2 * log(sum(parent.visits.values())) / sum(self.visits.values()))
        return weight

    def add_parent(self, parent, action):
        self.parents[action]  = parent

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
            action = filter(lambda c: not c.fully_expanded(),self.children.values())[0]
        except ValueError:
            raise Exception('Node is already fully expanded')
        return action.expand()

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
        return self.children[action].expand()

    def best_action(self, c=1/sqrt(2)):
        """
        Returns the action needed to reach the best child from the current
        node.
        """
        child = self.best_child(c)
        action = filter(lambda parent: parent[1] == self,child.parents.items())[0][0]
        return action, child.weight

    def simulation(self):
        """
        Simulates the game to completion, choosing moves in a uniformly random
        manner. The outcome of the simulation is returns as the state value for
        the given player.
        """
        steps = 1
        ei = self.experimentInstance
        while (not ei.isTerminal()) and ( not ei.AllTestsReached()):
            optionals, probabilities = self.experimentInstance.get_optionals_probabilities_by_approach(self.approach)
            action = numpy.random.choice(optionals, p=probabilities)
            ei = ei.simulate_next_ei(action)[1]
            steps = steps + 1
        if  not ei.isTerminal():
            steps = float('inf')
        return -steps
