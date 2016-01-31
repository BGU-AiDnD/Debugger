from django.contrib.sitemaps.views import index

__author__ = 'amir'

import random

class BELIEF_STATE(object):
    def __init__(self):
        self.Samples=[]


    def Free(self,  simulator):

        for i_state in self.Samples:

            simulator.FreeState(i_state)

    # // Creates new state, now owned by caller
    def CreateSample(self,  simulator):
        index = random.randint(0,len(self.Samples)-1)
        return simulator.Copy(self.Samples[index])


    def AddSample(self, state):

        self.Samples.append(state)


    def Copy(self,  beliefs,   simulator):

        for i_state in beliefs.Samples:
            self.AddSample(simulator.Copy(i_state))



    def Move(self, beliefs):

        for i_state in beliefs.Samples:

            self.AddSample(i_state)

        beliefs.Samples=[]
    
    def Empty(self):
        return self.Samples==[]
    def GetNumSamples(self):
        return len(self.Samples)
    def GetSample(self, index):
        return self.Samples[index]

