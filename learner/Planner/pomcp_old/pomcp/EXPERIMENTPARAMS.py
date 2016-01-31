__author__ = 'amir'

class EXPERIMENTPARAMS(object):
    def __init__ (self):
        self.NumRuns = 10
        self.NumSteps = 100000
        self.SimSteps = 1000
        self.TimeOut = 3600
        self.MinDoubles = 0
        self.MaxDoubles = 20
        self.TransformDoubles = -4
        self.TransformAttempts = 1000
        self.Accuracy = 0.01
        self.UndiscountedHorizon = 100
        self.AutoExploration = True
