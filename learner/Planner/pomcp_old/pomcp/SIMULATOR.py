from Planner.pomcp import KNOWLEDGE

__author__ = 'amir'

import random
import sys
import scipy



class SIMULATOR(object):
    def __init__(self):
        self.NumActions=0
        self.NumObservations=0
        self.Discount=1.0
        self.RewardRange=1.0

        self.Knowledge= KNOWLEDGE.KNOWLEDGE()


    def setup(self, numActions,  numObservations,  discount=1.0):
        self.NumActions=numActions
        self.NumObservations=numObservations
        self.Discount=discount
        self.RewardRange=1.0

        self.Knowledge= KNOWLEDGE.KNOWLEDGE()

        assert(discount > 0 and discount <= 1)

    def Validate(self,  state):
        pass



    def LocalMove(self, state,   history,
        stepObs,   status):
        return True


    def GenerateLegal(self,  state,   history,   status):
        actions=[]
        for a in range(self.NumActions):
            actions.append(a)
        return actions


    def GeneratePreferred(self,  state,   history,
        actions,   status):
        pass


    def SelectRandom(self,  state,   history,
          status):
        actions=[]

        if (self.Knowledge.RolloutLevel >= KNOWLEDGE.Enum["SMART"]):
            actions=[]
            self.GeneratePreferred(state, history, actions, status)
            if (len(actions)>0):
                return actions[random.randint(0,len(actions)-1)]


        if (self.Knowledge.RolloutLevel >= KNOWLEDGE.Enum["LEGAL"]):

            actions=self.GenerateLegal(state, history,  status)
            if (len(actions)>0):
                return random.choice(actions)


        return random.randint(0,self.NumActions)

    # // Use domain knowledge to assign prior value and confidence to actions
    # // Should only use fully observable state variables
    def Prior(self,  state,   history,
        vnode,   status):
        actions=[]

        if (self.Knowledge.TreeLevel == KNOWLEDGE.Enum["PURE"] or state == None):
            vnode.SetChildren(0, 0)
            return

        else:
            vnode.SetChildren(sys.maxint, -sys.maxint)

        if (self.Knowledge.TreeLevel >= KNOWLEDGE.Enum["LEGAL"]):
            actions=self.GenerateLegal(state, history,  status)
            for a in actions:
                qnode = vnode.Child(a)
                qnode.Value.Set(0, 0)
                qnode.AMAF.Set(0, 0)

        if (self.Knowledge.TreeLevel >= KNOWLEDGE.Enum["SMART"]):
            actions=[]
            self.GeneratePreferred(state, history, actions, status)
            for a in actions:
                qnode = vnode.Child(a)
                qnode.Value.Set(self.Knowledge.SmartTreeCount, self.Knowledge.SmartTreeValue)
                qnode.AMAF.Set(self.Knowledge.SmartTreeCount, self.Knowledge.SmartTreeValue)




    def HasAlpha(self):
        return False


    def AlphaValue(self,  qnode,  q,  n):
        pass


    def UpdateAlpha(self, qnode,   state):
        pass


    def DisplayBeliefs(self,  beliefState,):
        pass


    def DisplayState(self,  state):
        pass


    def DisplayAction(self,action):
        print "Action " , action 


    def DisplayObservation(self,  state, observation):
        print "Observation " , observation 


    def DisplayReward(self,reward):
        print "Reward " , reward 


    def GetHorizon(self,accuracy, DiscountedHorizon):
        if (self.Discount == 1):
            return DiscountedHorizon
        return float(scipy.log(accuracy) / scipy.log(self.Discount))


    def SetKnowledge(self, knowledge):
        self.Knowledge = knowledge 
    def  GetNumActions(self):
        return self.NumActions 
    def  GetNumObservations(self):
        return self.NumObservations 
    def  IsEpisodic(self):
        return False
    def  GetDiscount(self):
        return self.Discount 
    def  GetRewardRange(self):
        return self.RewardRange

    def  SetRewardRange(self,reward):
        self.RewardRange=reward


    # virtuals

    def CreateStartState(self):
        pass

    def FreeState(self,state):
        pass

    def Step(self, state,  action):
        pass

    def Copy( self, state):
        pass

    def SimStep( self, state,action, observation):
        pass





