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
            if (self.SearchParams.UseRave):
                self.SearchParams.ExplorationConstant = 0
            else:
                self.SearchParams.ExplorationConstant = simulator.GetRewardRange()
        MCTS.InitFastUCB(self.SearchParams.ExplorationConstant)

    
    def Run(self):
        #boost::timer timer
        mcts= MCTS.MCTS(self.Simulator, self.SearchParams)

        undiscountedReturn = 0.0
        discountedReturn = 0.0
        discount = 1.0
        terminal = False
        outOfParticles = False
        t=0

        state = self.Real.CreateStartState()#STATE*

        for t in range(int(self.ExpParams.NumSteps)):
            action = mcts.SelectAction()
            # print "action", action, state.experimentInstance.initial_tests, state.getMaxProb(), state.experimentInstance.error
            terminal,observation, reward = self.Real.Step(state, action )
            # print "state.getMaxProb",  state.getMaxProb()

            self.Results.Reward.Add(reward)
            undiscountedReturn += reward
            discountedReturn += reward * discount
            discount *= self.Real.GetDiscount()


            if (terminal):
                print  "Terminated" ,state.getMaxProb(), len(state.experimentInstance.initial_tests)#, str(mcts.StatTreeDepth) , str(mcts.StatRolloutDepth) , str(mcts.StatTotalReward)
                break

            outOfParticles = not mcts.Update(action, observation, reward)
            if (outOfParticles):
                break

           # if (timer.elapsed() > self.ExpParams.TimeOut):

            #    print  "Timed out after ", t , " steps in ", self.results.Time.GetTotal() , "seconds"
             #   break

        if (outOfParticles):

            print "Out of particles, finishing episode with SelectRandom"
            history = mcts.GetHistory()#HISTORY
            while (++t < self.ExpParams.NumSteps):

                observation=0
                reward=0.0

                # This passes real state into simulator!
                # SelectRandom must only use fully observable state
                # to avoid "cheating"
                action = self.Simulator.SelectRandom(state, history, mcts.GetStatus())
                terminal,observation, reward = self.Real.Step(state, action )

                self.Results.Reward.Add(reward)
                undiscountedReturn += reward
                discountedReturn += reward * discount
                discount *= self.Real.GetDiscount()

                if (terminal):

                    print  "Terminated"#, str(mcts.StatTreeDepth) , str(mcts.StatRolloutDepth) , str(mcts.StatTotalReward)
                    break


                history.Add(action, observation)

        #self.results.Time.Add(timer.elapsed())
        self.Results.Time.Add(-1)
        self.Results.UndiscountedReturn.Add(undiscountedReturn)
        self.Results.DiscountedReturn.Add(discountedReturn)
        # print  "Discounted return = " , discountedReturn, ", average = " , self.Results.DiscountedReturn.GetMean()
        # print  "Undiscounted return = " , undiscountedReturn, ", average = " , self.Results.UndiscountedReturn.GetMean()

    def MultiRun(self):
        for n in range(self.ExpParams.NumRuns):
            print  "Starting run " , n + 1 , " with " , self.SearchParams.NumSimulations , " simulations... "
            self.Run()
            if (self.Results.Time.GetTotal() >self.ExpParams.TimeOut):
                #print "Timed out after " , n , " runs in ", self.Results.Time.GetTotal() , "seconds"
                break

    def DiscountedReturn(self):

        print  "Main runs"  ,self.OutputFile , "Simulations\tRuns\tUndiscounted return\tUndiscounted error\tDiscounted return\tDiscounted error\tTime\n"
    
        self.SearchParams.MaxDepth = self.Simulator.GetHorizon(self.ExpParams.Accuracy, self.ExpParams.UndiscountedHorizon)
        self.ExpParams.SimSteps = self.Simulator.GetHorizon(self.ExpParams.Accuracy, self.ExpParams.UndiscountedHorizon)
        self.ExpParams.NumSteps = self.Real.GetHorizon(self.ExpParams.Accuracy, self.ExpParams.UndiscountedHorizon)
    
        #for (int i = ExpParams.MinDoubles i <= ExpParams.MaxDoubles i++)
        for i in xrange(self.ExpParams.MinDoubles,self.ExpParams.MaxDoubles,1):
        
            self.SearchParams.NumSimulations = 1 << i
            self.SearchParams.NumStartStates = 1 << i
            if (i + self.ExpParams.TransformDoubles >= 0):
                self.SearchParams.NumTransforms = 1 << (i + self.ExpParams.TransformDoubles)
            else:
                self.SearchParams.NumTransforms = 1
            self.SearchParams.MaxAttempts = self.SearchParams.NumTransforms * self.ExpParams.TransformAttempts
    
            self.Results.Clear()
            # self.MultiRun()
            self.Run()

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


                
        
    def AverageReward(self):

        print  "Main runs" , self.OutputFile , "Simulations\tSteps\tAverage reward\tAverage time\n"

        self.SearchParams.MaxDepth = self.Simulator.GetHorizon(self.ExpParams.Accuracy, self.ExpParams.UndiscountedHorizon)
        self.ExpParams.SimSteps = self.Simulator.GetHorizon(self.ExpParams.Accuracy, self.ExpParams.UndiscountedHorizon)

        for  i in xrange( self.ExpParams.MinDoubles  , self.ExpParams.MaxDoubles ):

            self.SearchParams.NumSimulations = 2**i
            self.SearchParams.NumStartStates = 2**i
            if (i + self.ExpParams.TransformDoubles >= 0):
                 self.SearchParams.NumTransforms = 1 , (i + self.ExpParams.TransformDoubles)
            else:
                 self.SearchParams.NumTransforms = 1
            self.SearchParams.MaxAttempts =  self.SearchParams.NumTransforms * self.ExpParams.TransformAttempts

            self.Results.Clear()
            self.Run()

            print  "Simulations = " ,  self.SearchParams.NumSimulations ,  \
                 "Steps = " , self.Results.Reward.GetCount() ,  \
                 "Average reward = " , self.Results.Reward.GetMean()\
                , " +- " , self.Results.Reward.GetStdErr() ,  \
                 "Average time = " , self.Results.Time.GetMean() / self.Results.Reward.GetCount() ,\
            self.OutputFile ,  self.SearchParams.NumSimulations , "\t"\
                , self.Results.Reward.GetCount() , "\t"\
                , self.Results.Reward.GetMean() , "\t"\
                , self.Results.Reward.GetStdErr() , "\t"\
                , self.Results.Time.GetMean() / self.Results.Reward.GetCount()

