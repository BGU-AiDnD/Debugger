from Planner.pomcp import RESULTS, MCTS

__author__ = 'amir'


class EXPERIMENT(object):
    def __init__(self,real,simulator,outputFile, expParams,  searchParams):
        self.Real = real
        self.Simulator = simulator
        self.OutputFile= outputFile
        self.ExpParams = expParams
        self.SearchParams = searchParams
        self.Results = RESULTS.RESULTS()
        if (self.ExpParams.AutoExploration):
            self.SearchParams.ExplorationConstant = 1
        MCTS.InitFastUCB(self.SearchParams.ExplorationConstant)

    
    def RunMultiple(self):
        #boost::timer timer
        mcts= MCTS.MCTS(self.Simulator, self.SearchParams)

        undiscountedReturn = 0.0
        discountedReturn = 0.0

        steps=0
        state = self.Real.CreateStartState()#STATE*
        while not state.terminal_or_allReach():
            action = mcts.SelectAction()
            state,terminal,observation, reward = self.Real.RealStep(state, action )
            self.Results.Reward.Add(reward)
            undiscountedReturn += reward
            discountedReturn += reward
            mcts.Update(state)
            steps=steps+1
        # print  "Terminated" ,state.getMaxProb(), len(state.experimentInstance.initial_tests)


        self.Results.Time.Add(-1)
        self.Results.UndiscountedReturn.Add(undiscountedReturn)
        self.Results.DiscountedReturn.Add(discountedReturn)
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

            self.Results.Reward.Add(reward)
            undiscountedReturn += reward
            discountedReturn += reward


            if (terminal):
                print  "Terminated" ,state.getMaxProb(), len(state.experimentInstance.initial_tests)
                break

            mcts.Update(state)

        self.Results.Time.Add(-1)
        self.Results.UndiscountedReturn.Add(undiscountedReturn)
        self.Results.DiscountedReturn.Add(discountedReturn)


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



    def DiscountedReturn(self):

        print  "Main runs"  ,self.OutputFile , "Simulations\tRuns\tUndiscounted return\tUndiscounted error\tDiscounted return\tDiscounted error\tTime\n"
    
        self.SearchParams.MaxDepth = self.ExpParams.UndiscountedHorizon
        self.ExpParams.SimSteps = self.ExpParams.UndiscountedHorizon
        self.ExpParams.NumSteps =  self.ExpParams.UndiscountedHorizon
    
        for i in xrange(self.ExpParams.MinDoubles,self.ExpParams.MaxDoubles,1):
            self.SearchParams.NumSimulations = 1 << i

            self.Results.Clear()
            self.RunOne()

            print  "Simulations = " , self.SearchParams.NumSimulations , "Runs = " , self.Results.Time.GetCount() , "Undiscounted return = " , \
                 self.Results.UndiscountedReturn.GetMean(), " +- " , self.Results.UndiscountedReturn.GetStdErr() , "Discounted return = "\
                 , self.Results.DiscountedReturn.GetMean(), " +- " , self.Results.DiscountedReturn.GetStdErr() , "Time = " \
                 , self.Results.Time.GetMean() , self.OutputFile , self.SearchParams.NumSimulations , "\t" \
                , self.Results.Time.GetCount() , "\t"\
                , self.Results.UndiscountedReturn.GetMean() , "\t"\
                , self.Results.UndiscountedReturn.GetStdErr() , "\t"\
                , self.Results.DiscountedReturn.GetMean() , "\t"\
                , self.Results.DiscountedReturn.GetStdErr() , "\t"\
                , self.Results.Time.GetMean()


