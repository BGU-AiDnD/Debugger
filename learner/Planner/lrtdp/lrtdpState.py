import LRTDP
import LRTDPModule
import random

__author__ = 'amir'


class LrtdpState(object):
    def __init__(self,experimentInstance):
        self.experimentInstance = experimentInstance
        self.isSolved=self.isTerminal()
        self.value = 1
        if self.isSolved:
            self.value = 0
        self.simulationCount = 0

    def clone(self):
        return LrtdpState(self.experimentInstance.Copy())

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
        # optionals = self.experimentInstance.next_tests_by_hp()
        optionals = self.experimentInstance.get_optionals_actions()
        minVal = float('inf') #big number
        result = []
        if len(optionals)==0:
            print "len(optionals)==0:"
        for action in optionals:
            q = self.qValue(action)
            if q < minVal:
                minVal = q
                result = [action]
            elif q == minVal:
                result.append(action)
        return result

    def getNextStateDist(self,action):
        #return LRTDP.LRTDP(1,2,3,4).nextStateDist(self.experimentInstance,action)
        return LRTDPModule.nextStateDist(self.experimentInstance, action)

    def qValue(self,action):
        q = 1
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

    def residual(self):
        return abs(self.value - self.qValue(self.greedyAction()))

    def needsSimulaton(self):
        return self.simulationCount==0

    def simulate_next_state(self,action):
        #return LRTDP.LRTDP(1,2,3,4).generateState(self.experimentInstance.simulate_next_ei(action))
        return LRTDPModule.generateState(self.experimentInstance.simulate_next_ei(action)[1])





