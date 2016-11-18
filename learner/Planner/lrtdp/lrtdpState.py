import LRTDP
import LRTDPModule
import random

__author__ = 'amir'


class LrtdpState(object):
    def __init__(self,experimentInstance, approach):
        """
        experimentInstance - the instance of this state
        approach - how to combine tests probabilities to qvalue.
            can be one of the following: "uniform" , "hp", "entropy"
        """
        self.experimentInstance = experimentInstance
        self.approach = approach
        self.isSolved=self.isTerminal()
        self.value = float('inf')
        if self.isSolved:
            self.value = 0
        self.simulationCount = 0

    def clone(self):
        return LrtdpState(self.experimentInstance.Copy(), self.approach)

    def getMaxProb(self):
        self.experimentInstance.diagnose()
        maxP = max([x.probability for x in self.experimentInstance.diagnoses])
        return maxP

    # do action and return observation
    def addTest(self,ind):
        return self.experimentInstance.addTest(ind)

    def SimulateADDTest(self,ind,observation):
        return self.experimentInstance.SimulateADDTest(ind,observation)

    def greedyAction(self):
        return random.choice(self.getGreedyActions())

    def getGreedyActions(self):
        optionals, probabilities = self.experimentInstance.get_optionals_probabilities_by_approach(self.approach)
        minVal = float('inf')
        result = []
        for action in optionals:
            q = self.qValue(action)
            if q < minVal:
                minVal = q
                result = [action]
            elif q == minVal:
                result.append(action)
        return result

    def getNextStateDist(self,action):
        return LRTDPModule.nextStateDist(self.experimentInstance, action)

    def qValue(self,action):
        q = 1 # cost
        nextStateDist = self.getNextStateDist(action)
        for next,prob in nextStateDist:
            q += prob * next.value
        return q

    def update(self,action):
        if not self.isTerminal():
            self.value = self.qValue(action)

    def isTerminal(self):
        return self.experimentInstance.isTerminal()

    def AllTestsReached(self):
        reached = self.experimentInstance.AllTestsReached()
        return reached

    def terminal_or_allReach(self):
        return self.isTerminal() or self.AllTestsReached()

    # def pickNextState(self):
    #     return  self.simulate_next_state(self.experimentInstance.hp_next())

    def residual(self, action):
        return abs(self.value - self.qValue(action))

    def needsSimulaton(self):
        return self.simulationCount==0

    def simulate_next_state(self,action):
        return LRTDPModule.generateState(self.experimentInstance.simulate_next_ei(action)[1])





