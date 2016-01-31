from Planner.pomcp import MCTSPARAMS, STATISTIC, VNODE, TEST_SIMULATOR, HISTORY, QNODE, BELIEF_STATE, STATUS

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
        self.History= HISTORY.HISTORY()
        self.Status= STATUS.STATUS()

        VNODE.NumChildren = self.Simulator.GetNumActions()
        QNODE.NumChildren = self.Simulator.GetNumObservations()

        self.StatTreeDepth= STATISTIC.STATISTIC()
        self.StatRolloutDepth= STATISTIC.STATISTIC()
        self.StatTotalReward= STATISTIC.STATISTIC()


        self.Root=self.ExpandNode(self.Simulator.CreateStartState())

        for  i in range(self.Params.NumStartStates):
            self.Root.Beliefs().AddSample(self.Simulator.CreateStartState())



    def BeliefState(self):
        return self.Root.Beliefs()

    def GetHistory(self):
        return self.History


    def GetStatus(self):
        return self.SimulatorStatus



    def Update(self,action, observation, reward):
        self.History.Add(action, observation)
        beliefs= BELIEF_STATE.BELIEF_STATE()

        # Find matching vnode from the rest of the tree
        qnode = self.Root.Child(action)
        vnode = qnode.Child(observation)
        if (vnode!=None):
            if (self.Params.Verbose >= 1):
                print "Matched " , vnode.Beliefs().GetNumSamples() , " states"
            beliefs.Copy(vnode.Beliefs(), self.Simulator)
        else:

            if (self.Params.Verbose >= 1):
                print"No matching node found"


        # Generate transformed states to avoid particle deprivation
        if (self.Params.UseTransforms):
            self.AddTransforms(self.Root, beliefs)

        # If we still have no particles, fail
        if (beliefs.Empty() and (vnode==None or vnode.Beliefs().Empty())):
            return False

        if (self.Params.Verbose >= 1):
            self.Simulator.DisplayBeliefs(beliefs)

        # Find a state to initialise prior (only requires fully observed state)
        state = None
        if (vnode and not vnode.Beliefs().Empty()):
            state = vnode.Beliefs().GetSample(0)
        else:
            state = beliefs.GetSample(0)

        # Delete old tree and create new root

        newRoot = self.ExpandNode(state)
        newRoot.BeliefState=beliefs
        self.Root = newRoot
        return True


    def SelectAction(self):
        if (self.Params.DisableTree):
            self.RolloutSearch()
        else:
            self.UCTSearch()
        return self.GreedyUCB(self.Root, False)

    def RolloutSearch(self):
        totals=[0.0 for x in self.Simulator.GetNumActions()]
        historyDepth = self.History.Size()
        assert(self.BeliefState().GetNumSamples() > 0)
        legal=self.Simulator.GenerateLegal(self.BeliefState().GetSample(0), self.GetHistory(),  self.GetStatus())
        random.shuffle(legal)

        for i in self.Params.NumSimulations:
            action = legal[i % len(legal)]
            state = self.Root.Beliefs().CreateSample(self.Simulator)
            self.Simulator.Validate(state)

            immediateReward, delayedReward, totalReward=0.0,0.0,0.0
            terminal,observation, immediateReward = self.Simulator.Step(state, action )

            vnode = self.Root.Child(action).Child(observation)
            if (vnode==None and False==terminal):
                vnode = self.ExpandNode(state)
                self.AddSample(vnode, state)

            self.History.Add(action, observation)

            delayedReward = self.Rollout(state)
            totalReward = immediateReward + self.Simulator.GetDiscount() * delayedReward
            self.Root.Child(action).Value.Add(totalReward)
            self.Simulator.FreeState(state)
            self.History.Truncate(historyDepth)

    def UCTSearch(self):

        self.ClearStatistics()
        historyDepth = self.History.Size()

        for n in range(self.Params.NumSimulations):


            #print type( self.Root),type( self.Root.Beliefs)
            state = self.Root.BeliefState.CreateSample(self.Simulator)
            self.Simulator.Validate(state)
            self.Status.Phase = STATUS.Enum1["TREE"] #SIMULATOR::STATUS::TREE
            if (self.Params.Verbose >= 2):
                print"Starting simulation"
                self.Simulator.DisplayState(state)


            self.TreeDepth=0
            self.PeakTreeDepth=0
            totalReward = self.SimulateV(state, self.Root)
            self.StatTotalReward.Add(totalReward)
            self.StatTreeDepth.Add(self.PeakTreeDepth)

            if (self.Params.Verbose >= 2):
                print"Total reward = " ,  totalReward
            if (self.Params.Verbose >= 3):
                self.DisplayValue(4)

            self.Simulator.FreeState(state)
            self.History.Truncate(historyDepth)

        self.DisplayStatistics()

    def SimulateV(self,state, vnode):

        action = self.GreedyUCB(vnode, True)

        self.PeakTreeDepth = self.TreeDepth
        if (self.TreeDepth >= self.Params.MaxDepth): #// search horizon reached
            return 0

        if (self.TreeDepth == 1):
            self.AddSample(vnode, state)

        qnode = vnode.Child(action)
        totalReward = self.SimulateQ(state, qnode, action)
        vnode.Value.Add(totalReward)
        self.AddRave(vnode, totalReward)
        # print "SimulateV reward", totalReward
        return totalReward


    def SimulateQ(self,state, qnode, action):

        immediateReward, delayedReward = 0.0,0.0
        totalReward=0.0

        if (self.Simulator.HasAlpha()):
            self.Simulator.UpdateAlpha(qnode, state)

        for obs in range(self.Simulator.GetNumObservations()):
            nstate=state.clone()
            terminal,observation, immediateReward=self.Simulator.SimStep(nstate, action,obs)
            assert(observation >= 0 and observation < self.Simulator.GetNumObservations())
            self.History.Add(action, observation)

            if (self.Params.Verbose >= 3):
                self.Simulator.DisplayAction(action)
                self.Simulator.DisplayObservation(nstate, observation)
                self.Simulator.DisplayReward(immediateReward)
                self.Simulator.DisplayState(nstate)


            vnode = qnode.Child(observation)
            if (vnode==None and False==terminal and qnode.Value.GetCount() >= self.Params.ExpandCount):
                vnode = self.ExpandNode(nstate)

            if (False==terminal):

                self.TreeDepth=self.TreeDepth+1
                if (vnode!=None):
                    delayedReward = self.SimulateV(nstate, vnode)
                else:
                    delayedReward = self.Rollout(nstate)
                self.TreeDepth=self.TreeDepth-1


            totalReward =totalReward+ immediateReward + self.Simulator.GetDiscount() * delayedReward
            qnode.Value.Add(totalReward)
        return totalReward

    #
    # def SimulateQ(self,state, qnode, action):
    #
    #     immediateReward, delayedReward = 0.0,0.0
    #
    #     if (self.Simulator.HasAlpha()):
    #         self.Simulator.UpdateAlpha(qnode, state)
    #
    #     for obs in range(self.Simulator.GetNumObservations()):
    #         terminal,observation, immediateReward=self.Simulator.SimStep(state, action,obs)
    #     terminal,observation, immediateReward = self.Simulator.Step(state, action )
    #     assert(observation >= 0 and observation < self.Simulator.GetNumObservations())
    #     self.History.Add(action, observation)
    #
    #     if (self.Params.Verbose >= 3):
    #
    #         self.Simulator.DisplayAction(action)
    #         self.Simulator.DisplayObservation(state, observation)
    #         self.Simulator.DisplayReward(immediateReward)
    #         self.Simulator.DisplayState(state)
    #
    #
    #     vnode = qnode.Child(observation)
    #     if (vnode==None and False==terminal and qnode.Value.GetCount() >= self.Params.ExpandCount):
    #         vnode = self.ExpandNode(state)
    #
    #     if (False==terminal):
    #
    #         self.TreeDepth=self.TreeDepth+1
    #         if (vnode!=None):
    #             delayedReward = self.SimulateV(state, vnode)
    #         else:
    #             delayedReward = self.Rollout(state)
    #         self.TreeDepth=self.TreeDepth-1
    #
    #
    #     totalReward = immediateReward + self.Simulator.GetDiscount() * delayedReward
    #     qnode.Value.Add(totalReward)
    #     return totalReward
    #

    def AddRave(self,vnode, totalReward):

        totalDiscount = 1.0
        for t in xrange(self.TreeDepth,self.History.Size()):
            qnode = vnode.Child(self.History[t].Action)
            qnode.AMAF.Addweight(totalReward, totalDiscount)
            totalDiscount = totalDiscount* self.Params.RaveDiscount


    def ExpandNode(self, state):

        vnode = VNODE.Create()
        vnode.Value.Set(0, 0)
        self.Simulator.Prior(state, self.History, vnode, self.SimulatorStatus)
        if (self.Params.Verbose >= 2):
            print"Expanding node: " , \
            self.History.Display()
    
        return vnode

    def AddSample(self, node, state):
        sample = self.Simulator.Copy(state)
        node.Beliefs().AddSample(sample)
        if (self.Params.Verbose >= 2):
            print"Adding sample:"
            self.Simulator.DisplayState(sample)

    def GreedyUCB(self, vnode, ucb):

        besta=[]
        bestq = -sys.maxint
        N = vnode.Value.GetCount()
        logN = math.log(N + 1)
        hasalpha = self.Simulator.HasAlpha()

        for action in range(self.Simulator.GetNumActions()):
            q, alphaq=0.0,0.0
            n, alphan=0,0

            qnode = vnode.Child(action)
            q = qnode.Value.GetValue()
            n = qnode.Value.GetCount()

            if (self.Params.UseRave and qnode.AMAF.GetCount() > 0):

                n2 = qnode.AMAF.GetCount()
                beta = n2 / (n + n2 + self.Params.RaveConstant * n * n2)
                q = (1.0 - beta) * q + beta * qnode.AMAF.GetValue()


            if (hasalpha and n > 0):

                self.Simulator.AlphaValue(qnode, alphaq, alphan)
                q = (n * q + alphan * alphaq) / (n + alphan)
                #// , "N = " , n , ", alphaN = " , alphan , endl
                #// , "Q = " , q , ", alphaQ = " , alphaq , endl


            if (ucb):
                q += self.FastUCB(N, n, logN)

            if (q >= bestq):

                if (q > bestq):
                    besta=[]
                bestq = q
                besta.append(action)


        assert(len(besta)>0)
        return random.choice(besta)

    def Rollout(self,state):
    
        self.Status.Phase = STATUS.Enum1["ROLLOUT"]
        if (self.Params.Verbose >= 3):
            print "Starting rollout"
    
        totalReward = 0.0
        discount = 1.0
        terminal = False
        numSteps=0
        for  numSteps in range(   self.Params.MaxDepth-self.TreeDepth):
            if terminal==True:
                break
            observation=0
            reward=0.0
    
            action = self.Simulator.SelectRandom(state, self.History, self.Status)
            terminal,observation, reward = self.Simulator.Step(state, action )
            self.History.Add(action, observation)
    
            if (self.Params.Verbose >= 4):
                self.Simulator.DisplayAction(action)
                self.Simulator.DisplayObservation(state, observation)
                self.Simulator.DisplayReward(reward)
                self.Simulator.DisplayState(state)
    
            totalReward += reward * discount
            discount *= self.Simulator.GetDiscount()
    
        self.StatRolloutDepth.Add(numSteps)
        if (self.Params.Verbose >= 3):
            print "Ending rollout after " , numSteps ,\
                 " steps, with total reward " , totalReward 
        return totalReward

    def AddTransforms(self, root, beliefs):

        attempts, added = 0,0
    
        #// Local transformations of state that are consistent with history
        while (added < self.Params.NumTransforms and attempts < self.Params.MaxAttempts):
            transform = self.CreateTransform()
            if (transform):
            
                beliefs.AddSample(transform)
                added=added+1
            
            attempts=attempts+1
        
    
        if (self.Params.Verbose >= 1):
            print "Created " , added , " local transformations out of " \
                , attempts , " attempts"
        
    def CreateTransform(self):
        stepObs=0
        stepReward=0.0

        state = self.Root.Beliefs().CreateSample(self.Simulator)
        terminal,stepObs, stepReward=self.Simulator.Step(state, self.History.Back().Action)
        if (self.Simulator.LocalMove(state, self.History, stepObs, self.SimulatorStatus)):
            return state
        self.Simulator.FreeState(state)
        return 0



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

    def DisplayStatistics(self):

        if (self.Params.Verbose >= 1):
        
            self.StatTreeDepth.Print("Tree depth")
            self.StatRolloutDepth.Print("Rollout depth")
            self.StatTotalReward.Print("Total reward")
    
        if (self.Params.Verbose >= 2):

            print  "Policy after " , self.Params.NumSimulations , " simulations"
            self.DisplayPolicy(6)
            print "Values after " , self.Params.NumSimulations , " simulations"
            self.DisplayValue(6)

    def DisplayValue(self,depth):
        history=None
        print "MCTS Values:"
        self.Root.DisplayValue(history, depth)


    def DisplayPolicy(self,depth):
        history=None
        print "MCTS Policy:"
        self.Root.DisplayPolicy(history, depth)


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


def UnitTest():
    UnitTestGreedy()
    UnitTestUCB()
    UnitTestRollout()
    for depth in range(4):
        UnitTestSearch(depth)

def UnitTestGreedy():

    testSimulator= TEST_SIMULATOR.TEST_SIMULATOR(5, 5, 0)
    params= MCTSPARAMS.MCTSPARAMS()
    mcts=MCTS(testSimulator, params)
    numAct = testSimulator.GetNumActions()
    numObs = testSimulator.GetNumObservations()


    vnode = mcts.ExpandNode(testSimulator.CreateStartState())
    vnode.Value.Set(1, 0)
    vnode.Child(0).Value.Set(0, 1)
    for action in xrange(1, numAct):
        vnode.Child(action).Value.Set(0, 0)
    x= mcts.GreedyUCB(vnode, False)
    print "x:",x
    assert(mcts.GreedyUCB(vnode, False) == 0)

def UnitTestUCB():

    testSimulator= TEST_SIMULATOR.TEST_SIMULATOR(5, 5, 0)
    params= MCTSPARAMS.MCTSPARAMS()
    mcts=MCTS(testSimulator, params)
    numAct = testSimulator.GetNumActions()
    numObs = testSimulator.GetNumObservations()

    #// With equal value, action with lowest count is selected
    vnode1 = mcts.ExpandNode(testSimulator.CreateStartState())
    vnode1.Value.Set(1, 0)
    for action in range( numAct):
        if (action == 3):
            vnode1.Child(action).Value.Set(99, 0)
        else:
            vnode1.Child(action).Value.Set(100 + action, 0)
    assert(mcts.GreedyUCB(vnode1, True) == 3)

    #// With high counts, action with highest value is selected
    vnode2 = mcts.ExpandNode(testSimulator.CreateStartState())
    vnode2.Value.Set(1, 0)
    for action in range( numAct):
        if (action == 3):
            vnode2.Child(action).Value.Set(99 + numObs, 1)
        else:
            vnode2.Child(action).Value.Set(100 + numAct - action, 0)
    assert(mcts.GreedyUCB(vnode2, True) == 3)

    #// Action with low value and low count beats actions with high counts
    vnode3 = mcts.ExpandNode(testSimulator.CreateStartState())
    vnode3.Value.Set(1, 0)
    for action in range( numAct):
        if (action == 3):
            vnode3.Child(action).Value.Set(1, 1)
        else:
            vnode3.Child(action).Value.Set(100 + action, 1)
    assert(mcts.GreedyUCB(vnode3, True) == 3)

    #// Actions with zero count is always selected
    vnode4 = mcts.ExpandNode(testSimulator.CreateStartState())
    vnode4.Value.Set(1, 0)
    for action in range( numAct):
        if (action == 3):
            vnode4.Child(action).Value.Set(0, 0)
        else:
            vnode4.Child(action).Value.Set(1, 1)
    assert(mcts.GreedyUCB(vnode4, True) == 3)

def UnitTestRollout():
    testSimulator= TEST_SIMULATOR.TEST_SIMULATOR(2, 2, 0)
    params= MCTSPARAMS.MCTSPARAMS()
    params.NumSimulations = 1000
    params.MaxDepth = 10
    mcts=MCTS(testSimulator, params)
    totalReward=0.0
    for n in range( mcts.Params.NumSimulations):
        state = testSimulator.CreateStartState()
        mcts.TreeDepth = 0
        totalReward += mcts.Rollout(state)
    rootValue = totalReward / mcts.Params.NumSimulations
    meanValue = testSimulator.MeanValue()
    assert(abs(meanValue - rootValue) < 0.1)


def UnitTestSearch(depth):
    testSimulator= TEST_SIMULATOR.TEST_SIMULATOR(3, 2, depth)
    params= MCTSPARAMS.MCTSPARAMS()
    params.MaxDepth = depth + 1
    params.NumSimulations = pow(10, depth + 1)
    mcts=MCTS(testSimulator, params)
    mcts.UCTSearch()
    rootValue = mcts.Root.Value.GetValue()
    optimalValue = testSimulator.OptimalValue()
    assert(abs(optimalValue - rootValue) < 0.1)


#UnitTest()
        
        
        
        
