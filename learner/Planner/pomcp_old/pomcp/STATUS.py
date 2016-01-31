__author__ = 'amir'


NUM_PHASES=0
TREE=0

lst=["TREE","ROLLOUT","NUM_PHASES"]
Enum1={}
for x,ind in enumerate(lst):
    Enum1[ind]=x

lst=["CONSISTENT","INCONSISTENT","RESAMPLED","OUT_OF_PARTICLES"]
Enum2={}
for x,ind in enumerate(lst):
    Enum2[ind]=x

class STATUS(object):
    def __init__(self):
        self.Phase=Enum1["TREE"]
        self.Particles=Enum2["CONSISTENT"]
