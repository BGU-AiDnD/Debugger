__author__ = 'amir'
import random
import Planner.mcts.mcts
import Planner.mcts.InstanceNode

class ActionNode(object):
    def __init__(self, action, parent, approach):
        self.action = action
        self.parent = parent
        self.approach = approach
        self.pass_probability = self.parent.experimentInstance.compute_pass_prob(self.action)
        next_ei = self.parent.experimentInstance.next_state_distribution(self.action)
        self.f_ei = next_ei[0][0]
        self.p_ei = next_ei[1][0]
        self.f_child = None
        self.p_child = None
        self.getStatesIfExists()

    def getStatesIfExists(self):
        if not self.p_child:
            self.p_child = Planner.mcts.mcts.getStateIfExists(self.parent, self.action, self.p_ei)
        if not self.f_child:
            self.f_child = Planner.mcts.mcts.getStateIfExists(self.parent, self.action, self.f_ei)

    def weight(self):
        self.getStatesIfExists()
        weight = 0
        if self.p_child:
            weight += self.pass_probability * self.p_child.weight
        if self.f_child:
            weight += (1 - self.pass_probability) * self.f_child.weight
        return weight

    def value(self):
        self.getStatesIfExists()
        value = 0
        if self.p_child:
            value += self.pass_probability * sum(self.p_child.value.values())
        if self.f_child:
            value += (1 - self.pass_probability) * sum(self.f_child.value.values())
        return value

    def visits(self):
        self.getStatesIfExists()
        visits = 0
        if self.p_child:
            visits += sum(self.p_child.visits.values())
        if self.f_child:
            visits += sum(self.f_child.visits.values())
        return visits

    def search_weight(self, c):
        self.getStatesIfExists()
        weight = 0
        if self.p_child and sum(self.p_child.visits.values()) > 0:
            weight += self.pass_probability * self.p_child.search_weight(c)
        if self.f_child and sum(self.f_child.visits.values()) > 0:
            weight += (1 - self.pass_probability) * self.f_child.search_weight(c)
        return weight

    def expand(self):
        if random.random() <= self.pass_probability:
            if not self.p_child:
                self.p_child = Planner.mcts.mcts.generateState(self.parent, self.action, self.p_ei, self.approach)
            return self.p_child
        else:
            if not self.f_child:
                self.f_child = Planner.mcts.mcts.generateState(self.parent, self.action, self.f_ei, self.approach)
            return self.f_child

    def fully_expanded(self):
        return None is [self.p_child ,self.f_child]
