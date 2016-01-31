from Planner.pomcp import ENTRY

__author__ = 'amir'


class HISTORY(object):
    def __init__(self):
        self.History=[]

    def Add(self, action,  obs = -1):
        self.History.append(ENTRY.ENTRY(action, obs))


    def Pop(self):
        self.History=self.History[:-1]


    def Truncate(self, t):
        self.History=self.History[:t]


    def Clear(self):
        self.History=[]


    def Size(self):
        return len(self.History)

    def Back(self):
        assert(len(self.History) > 0)
        return self.History[-1]

    def Display(self):

        for t in range(len(self.History)):
            print  "a=" , self.History[t].Action ,  " "
            if (self.History[t].Observation >= 0):
                print "o=" , self.History[t].Observation , " "

    def __getitem__(self, item):
        return self.History[item]




