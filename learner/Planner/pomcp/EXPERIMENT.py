from Planner.pomcp import  MCTS

__author__ = 'amir'


class EXPERIMENT(object):
    def __init__(self,real,simulator, expParams,  searchParams):
        self.Real = real
        self.Simulator = simulator
        self.ExpParams = expParams
        self.SearchParams = searchParams
        if (self.ExpParams.AutoExploration):
            self.SearchParams.ExplorationConstant = 1
        MCTS.InitFastUCB(self.SearchParams.ExplorationConstant)

    
    def RunMultiple(self):
        #boost::timer timer
        mcts= MCTS.MCTS(self.Simulator, self.SearchParams)


        steps=0
        state = self.Real.CreateStartState()#STATE*
        terminal=False
        while not (state.terminal_or_allReach() or terminal):
            action = mcts.SelectAction()
            ei=state.experimentInstance
            # print "ei-repr" , repr(ei), ei.calc_precision_recall()
            # print "selected action" , action ,"HP" , ei.next_tests_by_hp()
            state,terminal,observation, reward = self.Real.RealStep(state, action )
            mcts.Update(state)
            steps=steps+1
        # print  "Terminated" ,state.getMaxProb(), len(state.experimentInstance.initial_tests)


        ei=state.experimentInstance
        precision, recall=ei.calc_precision_recall()
        return precision, recall, steps

    def RunSim(self,mcts):
        #boost::timer timer
        # mcts= MCTS.MCTS(self.Simulator, self.SearchParams)

        undiscountedReturn = 0.0
        discountedReturn = 0.0

        state = self.Simulator.CreateStartState()#STATE*

        for t in range(int(self.ExpParams.NumSteps)):
            action = mcts.SelectAction()
            state,terminal,observation, reward = self.Simulator.Step(state, action )

            undiscountedReturn += reward
            discountedReturn += reward


            if (terminal):
                print  "Terminated" ,state.getMaxProb(), len(state.experimentInstance.initial_tests)
                break

            mcts.Update(state)


    def RunOne(self,tries):
        mcts= MCTS.MCTS(self.Simulator, self.SearchParams)
        for x in range(tries):
            self.RunSim(mcts)
        state = self.Real.CreateStartState()
        ei=state.experimentInstance
        steps=0
        while not state.terminal_or_allReach():
            steps=steps+1
            action = mcts.GreedyUCB(state,False)
            state,terminal,observation, reward = self.Real.RealStep(state, action )
            ei=state.experimentInstance

        print "Terminated"

        precision, recall=ei.calc_precision_recall()
        print "end",repr(ei)
        print precision, recall, steps

