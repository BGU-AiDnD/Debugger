from Planner.pomcp import STATE, SIMULATOR

__author__ = 'amir'

import random


class TEST_STATE(STATE.STATE):
    def __init__(self):
        super(STATE.STATE, self).__init__()
        self.Depth=0


class TEST_SIMULATOR(SIMULATOR.SIMULATOR):
    def __init__(self,actions, observations, maxDepth):
        super(TEST_SIMULATOR, self)
        super(TEST_SIMULATOR, self).__init__()
        super(TEST_SIMULATOR, self).setup(actions, observations)
        self.MaxDepth=maxDepth

    def Copy(self, state):
        tstate = state
        newstate = TEST_STATE()
        newstate.Depth = tstate.Depth
        return newstate

    def CreateStartState(self):
        return TEST_STATE()

    def FreeState(self, state):
        pass

    def Step(self, state,  action):

        #Up to MaxDepth action 0 is good independent of observations
        tstate = state
        if (tstate.Depth < self.MaxDepth and action == 0):
            reward = 1.0
        else:
            reward = 0.0
        observation = random.randint(0, self.GetNumObservations())
        tstate.Depth=tstate.Depth+1
        return False,observation,  reward

    def OptimalValue(self):
        discount = 1.0
        totalReward = 0.0
        for i in range( self.MaxDepth):
            totalReward += discount
            discount = self.GetDiscount()
        return totalReward

    def MeanValue(self):
        discount = 1.0
        totalReward = 0.0
        for i in range( self.MaxDepth):
            totalReward += discount / self.GetNumActions()
            discount = self.GetDiscount()
        return totalReward

