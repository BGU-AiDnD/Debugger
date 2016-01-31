from Planner.pomcp import STATE

__author__ = 'amir'


class DIAGNOSER_STATE(STATE.STATE):
    def __init__(self,experimentInstance):
        super(DIAGNOSER_STATE,self).__init__()
        self.experimentInstance=experimentInstance

    def clone(self):
        return DIAGNOSER_STATE(self.experimentInstance.Copy())

    def getMaxProb(self):
        self.experimentInstance.diagnose()
        maxP=max([x.probability for x in self.experimentInstance.diagnoses])
        return maxP

    # do action and return observation
    def addTest(self,ind):
        return self.experimentInstance.addTest(ind)

    def SimulateADDTest(self,ind,observation):
        return self.experimentInstance.SimulateADDTest(ind,observation)


def Create():
    return DIAGNOSER_STATE()
