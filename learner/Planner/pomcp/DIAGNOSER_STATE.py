import VALUE


__author__ = 'amir'


class DIAGNOSER_STATE(object):
    def __init__(self,experimentInstance):
        super(DIAGNOSER_STATE,self).__init__()
        self.experimentInstance=experimentInstance
        self.Value= VALUE.VALUE(0,0)

    def clone(self):
        return DIAGNOSER_STATE(self.experimentInstance.Copy())

    def getMaxProb(self):
        self.experimentInstance.diagnose()
        maxP=max([x.probability for x in self.experimentInstance.diagnoses])
        return maxP

    # do action and return observation
    def addTest(self,ind,simulator):
        obs,new_ei=self.experimentInstance.simulate_next_ei(ind)
        new_state=simulator.generateState(new_ei)
        return new_state,obs

    def addRealTest(self,ind,simulator):
        new_ei=self.experimentInstance.Copy()
        obs=new_ei.addTest(ind)
        new_state=simulator.generateState(new_ei)
        return new_state,obs

    def next_state_distribution(self):
        return self.experimentInstance.next_state_distribution()

    def SimulateADDTest(self,ind,observation,simulator):
        new_ei=self.experimentInstance.Copy()
        obs=new_ei.SimulateADDTest(ind,observation)
        new_state=simulator.generateState(new_ei)
        return new_state,obs

    def getOptionalsActions(self):
        return self.experimentInstance.next_tests_by_hp()
        # return self.experimentInstance.get_optionals_actions()

    def isTerminal(self):
        return self.experimentInstance.isTerminal()

    def AllTestsReached(self):
        reached = self.experimentInstance.AllTestsReached()
        return reached

    def terminal_or_allReach(self):
        return self.isTerminal() or self.AllTestsReached()

