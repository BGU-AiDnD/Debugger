__author__ = 'amir'

class EXPERIMENTPARAMS(object):
    def __init__ (self):
        self.NumRuns = 10
        self.NumSteps = 10
        self.SimSteps = 1000
        self.MinDoubles = 0
        self.MaxDoubles = 2
        self.Accuracy = 0.01
        self.UndiscountedHorizon = 10
        self.AutoExploration = True
