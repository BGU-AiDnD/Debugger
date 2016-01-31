from Planner.pomcp import STATUS

__author__ = 'amir'

lst=["PURE","LEGAL","SMART","NUM_LEVELS"]
Enum={}
for x,ind in enumerate(lst):
    Enum[ind]=x

class KNOWLEDGE(object):
    def __init__(self):
        self.TreeLevel=Enum["LEGAL"]
        self.RolloutLevel=Enum["LEGAL"]
        self.SmartTreeCount=10
        self.SmartTreeValue=1.0

    def Level(self,phase):
        assert(phase < STATUS.NUM_PHASES)
        if (phase == STATUS.TREE):
                return self.TreeLevel
        else:
                return self.RolloutLevel





