from Planner.pomcp import DIAGNOSER_STATE
import random

__author__ = 'amir'

#DIAGNOSER


class DIAGNOSER(object):
    # treshold define the halt criteria. stop if max(P(diag))>treshold
    def __init__(self,experimentInstance, threshold):
        self.experimentInstance=experimentInstance
        self.threshold=threshold
        self.states={}
        self.NumActions=len(self.experimentInstance.error)
        self.NumObservations=2
        self.Discount=1
        self.RewardRange=1.0

        #self.MemoryPool=MEMORY_POOL.MEMORY_POOL(DIAGNOSER_STATE.Create)

        #### setup!!!


    def GenerateLegal(self,  state):
        return state.getOptionalsActions()

        # actions=[]
        # for a in range(self.NumActions):
        #     actions.append(a)
        # return actions

        ##return possible actions


    def SelectRandom(self,  state):
        actions=self.GenerateLegal(state)
        if (len(actions)>0):
            return random.choice(actions)
        return random.randint(0,self.NumActions)


    def CreateStartState(self):
        return self.generateState(self.experimentInstance.Copy())


    def generateState(self,experimentInstance):
        key=repr(experimentInstance)
        # print "Add key",key
        if key not in self.states:
            # print "new key",key
            state = DIAGNOSER_STATE.DIAGNOSER_STATE(experimentInstance.Copy())
            self.states[key]= state
        # else:
            #saved key
            # print "saved key",self.states[key].Value.GetCount()
        return self.states[key]


    def Step(self, state,  action): ##action: next test to execute
        terminal =False
        nstate,observation=state.addTest(action,self)
        if observation==-1:
            return nstate,True,0,-1
        reward=-1
        maxP=nstate.getMaxProb()
        if maxP> self.threshold:
            reward=0
            terminal=True

        return nstate,terminal,observation,  reward

    def RealStep(self, state,  action): ##action: next test to execute
        terminal =False
        nstate,observation=state.addRealTest(action,self)
        if observation==-1:
            return nstate,True,0,-1
        reward=-1
        maxP=nstate.getMaxProb()
        if maxP> self.threshold:
            reward=0
            terminal=True

        return nstate,terminal,observation,  reward

    def SimStep( self, state,action, obs):
        terminal =False
        nstate,observation=state.SimulateADDTest(action,obs,self)
        if observation==-1:
            return nstate,True,0,-1
        # assert (len(nstate.experimentInstance.initial_tests) > len(state.experimentInstance.initial_tests))
        reward=-1
        maxP=nstate.getMaxProb()
        # print nstate.experimentInstance.initial_tests ,maxP
        if maxP> self.threshold:
            reward=0
            terminal=True

        return nstate,terminal,observation,  reward

    def Copy( self, state):
        return DIAGNOSER_STATE.DIAGNOSER_STATE(state.experimentInstance.Copy())

