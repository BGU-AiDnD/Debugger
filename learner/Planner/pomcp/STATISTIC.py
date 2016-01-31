__author__ = 'amir'


import sys
import math



class STATISTIC(object):
    def __init__(self):
        self.Count=0
        self.Mean=0.0
        self.Variance=0.0
        self.Min=1.0*-sys.maxint
        self.Max=sys.maxint*1.0


    def Initialise(self,val, count):
        self.Count = count
        self.Mean = val

    def Add(self, val):
        MeanOld = self.Mean
        CountOld = self.Count
        self.Count=self.Count+1
        assert(self.Count > 0) #// overflow
        self.Mean += (val - self.Mean) / self.Count
        self.Variance = (CountOld * (self.Variance + MeanOld * MeanOld)
                      + val * val) / self.Count - self.Mean * self.Mean
        if (val > self.Max):
            self.Max = val
        if (val < self.Min):
            self.Min = val

    def Clear(self):
        self.Count=0
        self.Mean=0.0
        self.Variance=0.0
        self.Min=1.0*(-sys.maxint)
        self.Max=sys.maxint*1.0

    def GetTotal(self):
        return self.Mean * self.Count

    def  GetCount(self):

        return self.Count

    def GetMean(self):

        return self.Mean

    def GetStdDev(self):
        return math.sqrt(self.Variance)

    def GetStdErr(self):

        return math.sqrt(self.Variance / self.Count)

    def GetMax(self):

        return self.Max


    def GetMin(self):

        return self.Min

    def Print(self,  name):

        print name , ": " , self.Mean , " [" , self.Min , ", " , self.Max , "]"


    def __str__(self):

        return  repr([ ": " , self.Mean , " [" , self.Min , ", " , self.Max , "]"])











