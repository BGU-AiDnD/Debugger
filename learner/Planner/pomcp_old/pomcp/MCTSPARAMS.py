__author__ = 'amir'


class MCTSPARAMS(object):
    def __init__(self):
        self.Verbose=0
        self.MaxDepth=10
        self.NumSimulations=10
        self.NumStartStates=10
        self.UseTransforms=True
        self.NumTransforms=0
        self.MaxAttempts=0
        self.ExpandCount=10
        self.ExplorationConstant=1
        self.UseRave=False
        self.RaveDiscount=1.0
        self.RaveConstant=0.01
        self.DisableTree=False

