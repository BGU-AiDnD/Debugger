from Planner.pomcp import DIAGNOSER_STATE, SIMULATOR

__author__ = 'amir'

#DIAGNOSER


class DIAGNOSER(SIMULATOR.SIMULATOR):
    # treshold define the halt criteria. stop if max(P(diag))>treshold
    def __init__(self,experimentInstance, threshold):
        super(DIAGNOSER,self).__init__()
        self.experimentInstance=experimentInstance
        self.threshold=threshold
        self.setup(len(self.experimentInstance.error),  2)
        #self.MemoryPool=MEMORY_POOL.MEMORY_POOL(DIAGNOSER_STATE.Create)

        #### setup!!!


    def Validate(self,  state):
        pass


    def DisplayBeliefs(self,  beliefState):
        pass

    ## print the state
    def DisplayState(self,  state):
        pass


    def DisplayAction(self,action):
        print "Action " , action


    def DisplayObservation(self,  state, observation):
        print "Observation " , observation


    def CreateStartState(self):
        return DIAGNOSER_STATE.DIAGNOSER_STATE(self.experimentInstance.Copy())

    def FreeState(self,state):
        pass

    def Step(self, state,  action): ##action: next test to execute
        terminal =False
        nstate = state#.clone()
        observation=nstate.addTest(action)
        if observation==-1:
            return True,0,-1
        # assert (len(nstate.experimentInstance.initial_tests) > len(state.experimentInstance.initial_tests))
        reward=-1
        maxP=nstate.getMaxProb()
        # print nstate.experimentInstance.initial_tests ,maxP
        if maxP> self.threshold:
            reward=0
            terminal=True

        return terminal,observation,  reward

    def SimStep( self, state,action, obs):
        terminal =False
        nstate = state#.clone()
        observation=nstate.SimulateADDTest(action,obs)
        if observation==-1:
            return True,0,-1
        # assert (len(nstate.experimentInstance.initial_tests) > len(state.experimentInstance.initial_tests))
        reward=-1
        maxP=nstate.getMaxProb()
        # print nstate.experimentInstance.initial_tests ,maxP
        if maxP> self.threshold:
            reward=0
            terminal=True

        return terminal,observation,  reward

    def Copy( self, state):
        return DIAGNOSER_STATE.DIAGNOSER_STATE(state.experimentInstance.Copy())

