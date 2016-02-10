from Planner.pomcp import MCTSPARAMS, STATISTIC
__author__ = 'amir'

import random
import math
import sys

UCB_N = 10000
UCB_n = 100
UCB=[[0.0 for x in range(UCB_n)] for y in range(UCB_N)]# static [UCB_N][UCB_n]
InitialisedFastUCB=True# static bool


class MCTS(object):
    def __init__(self,simulator,params):
        self.Simulator=simulator
        self.SimulatorStatus=None
        self.Params=params
        self.TreeDepth=0
        self.PeakTreeDepth=0


        self.StatTreeDepth= STATISTIC.STATISTIC()
        self.StatRolloutDepth= STATISTIC.STATISTIC()
        self.StatTotalReward= STATISTIC.STATISTIC()


        self.Root=self.Simulator.CreateStartState()

        self.start_state=self.Simulator.CreateStartState()


    def Update(self,state):
        self.Root = self.Simulator.generateState(state.experimentInstance)


    def SelectAction(self):
        self.UCTSearch()
        return self.GreedyUCB(self.Root, False)

    def RolloutSearch(self):

        legal=self.Simulator.GenerateLegal(self.Root)
        ##### optionals
        random.shuffle(legal)

        for i in self.Params.NumSimulations:
            action = legal[i % len(legal)]
            state = self.Root.clone()
            immediateReward, delayedReward, totalReward=0.0,0.0,0.0
            state,terminal,observation, immediateReward = self.Simulator.Step(state, action )


            delayedReward = self.Rollout(state)
            totalReward = immediateReward +  delayedReward
            state.Value.Add(totalReward)



    def UCTSearch(self):

        self.ClearStatistics()
        for n in range(self.Params.NumSimulations):
            #print type( self.Root),type( self.Root.Beliefs)
            state = self.Root.clone()

            self.TreeDepth=0
            self.PeakTreeDepth=0

            totalReward = self.SimulateV(state)
            self.StatTotalReward.Add(totalReward)
            self.StatTreeDepth.Add(self.PeakTreeDepth)


    def SimulateV(self,state):

        action = self.GreedyUCB(state, True)

        self.PeakTreeDepth = self.TreeDepth
        if (self.TreeDepth >= self.Params.MaxDepth): #// search horizon reached
            return 0

        nstate,terminal,observation, immediateReward = self.Simulator.Step(state, action )
        totalReward = self.SimulateQ(state,nstate)
        state.Value.Add(totalReward)
        # print "SimulateV reward", totalReward
        return totalReward


    def SimulateQ(self,state, nstate):

        immediateReward, delayedReward = 0.0,0.0
        totalReward=0.0

        if (nstate.terminal_or_allReach() and nstate.Value.GetCount() < self.Params.ExpandCount):
            return 0

        if (False==nstate.isTerminal()):
            self.TreeDepth=self.TreeDepth+1
            delayedReward = self.SimulateV(nstate)
            self.TreeDepth=self.TreeDepth-1

        totalReward =totalReward+ immediateReward + delayedReward
        state.Value.Add(totalReward)
        return totalReward


    def GreedyUCB(self, state, ucb):

        besta=[]
        bestq = -sys.maxint
        N = state.Value.GetCount()
        logN = math.log(N + 1)

        for action in state.getOptionalsActions():

            nstate,terminal,observation, immediateReward = self.Simulator.Step(state, action )
            q = 0.0+nstate.Value.GetValue()
            n = nstate.Value.GetCount()

            if n>0 and besta==[]:
                amir_amir=""
            if (ucb):
                q += self.FastUCB(N, n, logN)

            if (q >= bestq):

                if (q > bestq):
                    besta=[]
                bestq = q
                besta.append(action)
        if besta==[]:
            op=state.getOptionalsActions()
            print op
            amir_amir=""
        assert(len(besta)>0)
        return random.choice(besta)

    def Rollout(self,state):

        totalReward = 0.0
        discount = 1.0
        terminal = False
        numSteps=0
        for  numSteps in range(self.Params.MaxDepth-self.TreeDepth):
            if terminal==True:
                break
            observation=0
            reward=0.0
    
            action = self.Simulator.SelectRandom(state) ###random
            state,terminal,observation, reward = self.Simulator.Step(state, action )

            totalReward += reward * discount
            discount *= self.Simulator.GetDiscount()
    
        self.StatRolloutDepth.Add(numSteps)
        return totalReward


    def FastUCB(self,N,  n, logN):

        if (InitialisedFastUCB and N < UCB_N and n < UCB_n):
            return UCB[N][n]

        if (n == 0):
            return sys.maxint
        else:
            return self.Params.ExplorationConstant * math.sqrt(logN / n)

    def ClearStatistics(self):

        self.StatTreeDepth.Clear()
        self.StatRolloutDepth.Clear()
        self.StatTotalReward.Clear()

def InitFastUCB( exploration):

    print "Initialising fast UCB table... "
    for  N in  range(UCB_N):
        for n in range( UCB_n):
            if (n == 0):
                UCB[N][n] = sys.maxint
            else:
                UCB[N][n] = exploration * math.sqrt(math.log(N + 1) / n)
    print "done"
    InitialisedFastUCB = True



#UnitTest()
        
        
        
        
