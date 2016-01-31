__author__ = 'amir'


class VALUE(object):
    def __init__(self, count,  value):
        self.Count = count
        self.Total = value * count
        
    def Set(self, count,  value):
        self.Count = count
        self.Total = value * count
    

    def Add(self, totalReward):
        self.Count += 1
        self.Total += totalReward
    

    def Addweight(self, totalReward, weight):
        self.Count += weight
        self.Total += totalReward * weight

    def GetValue(self) :
        if self.Count==0:
            return self.Total
        else:
            return self.Total / self.Count
    

    def GetCount(self) :
        return self.Count
