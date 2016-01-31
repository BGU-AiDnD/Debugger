from Planner.pomcp import MEMORY_POOL, NETWORK_STATE, Utils, SIMULATOR

__author__ = 'amir'

lst=["E_CYCLE","E_3LEGS"]
Enum={}
for x,ind in enumerate(lst):
    Enum[ind]=x

class NETWORK(SIMULATOR.SIMULATOR):
    def __init__(self,numMachines,  ntype):
        super(NETWORK,self).__init__()
        self.NumMachines=numMachines
        self.FailureProb1, self.FailureProb2, self.ObsProb=0.1,0.333,0.95
        self.Neighbours=[]
        self.MemoryPool= MEMORY_POOL.MEMORY_POOL(NETWORK_STATE.Create)
        self.setup(self.NumMachines * 2 + 1,  3,  0.95)
        self.SetRewardRange(self.NumMachines * 2)
        if Enum["E_CYCLE"]==ntype:
            self.MakeRingNeighbours()
        elif Enum["E_3LEGS"]==ntype:
            self.Make3LegsNeighbours()



    def MakeRingNeighbours(self):
        self.Neighbours=[[0] for x in range(self.NumMachines)]
        for i in range(self.NumMachines):
            self.Neighbours[i].append((i + 1) % self.NumMachines)
            self.Neighbours[i].append((i + self.NumMachines - 1) % self.NumMachines)



    def Make3LegsNeighbours(self):
        assert(self.NumMachines >= 4 and self.NumMachines % 3 == 1)
        self.Neighbours=[[0] for x in range(self.NumMachines)]
        self.Neighbours[0].append(1)
        self.Neighbours[0].append(2)
        self.Neighbours[0].append(3)
        for i in range(self.NumMachines):
            if (i < self.NumMachines - 3):
                self.Neighbours[i].append(i + 3)
            if (i <= 4):
                self.Neighbours[i].append(0)
            else:
                self.Neighbours[i].append(i - 3)


    def Copy( self, state):
        nstate = state
        newstate = self.MemoryPool.Allocate() # check!!!!
        newstate = nstate
        return newstate


    def Validate( self, state):
        nstate = state



    def CreateStartState(self):

        nstate = self.MemoryPool.Allocate()
        for  i  in range( self.NumMachines):
            nstate.Machines.push_back(True)
        return nstate


    def FreeState(self,state):
        nstate = state
        self.MemoryPool.Free(nstate)


    def Step(self, state,  action):

        nstate = state
        reward = 0
        observation = 2

        neighbourFailure=[False for x in range(self.NumMachines)]
        for  i  in range( self.NumMachines):
            for j in range(len(self.Neighbours[i])):
                if (not nstate.Machines[self.Neighbours[i][j]]):
                    neighbourFailure[i] = True

        for  i  in range( self.NumMachines):

            if ( not neighbourFailure[i]):
                nstate.Machines[i] = not Utils.Bernoulli(self.FailureProb1)
            else:
                nstate.Machines[i] = not Utils.Bernoulli(self.FailureProb2)


        for  i  in range( self.NumMachines):

            if (nstate.Machines[i]):

                if (self.Neighbours[i].size() > 2): #// server
                    reward += 2
                else:
                    reward += 1

        if (action < self.NumMachines * 2):

            machine = action / 2
            reboot = action % 2

            if (reboot):

                reward -= 2.5
                nstate.Machines[machine] = True
                observation = Utils.Bernoulli(self.ObsProb)

            else: #// ping

                reward -= 0.1
                if (Utils.Bernoulli(self.ObsProb)):
                    observation = nstate.Machines[machine]
                else:
                    observation = not nstate.Machines[machine]
        return False,observation,  reward


    def DisplayBeliefs( self,beliefState):
        pass



    def DisplayState( self, state):

        nstate = state
        for i in  range(self.NumMachines):
            if nstate.Machines[i]:
                print i , ": " , "operational"
            else:
                print i , ": " , "failed"


    def DisplayObservation( self, state, observation):


        if observation==0:
            print "Machine failed" 
        elif observation== 1:
            print "Machine operational" 
        elif observation==2:
            #// Don't say anything
            pass

    def DisplayAction(self, action):
            if (action == self.NumMachines):
                print "No action" 
            machine = action / 2
            reboot = action % 2
            if reboot:
                print "Reboot" , " machine " , machine
            else:
                print "Ping" , " machine " , machine











