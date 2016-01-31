from Planner.pomcp import STATE

__author__ = 'amir'


class NETWORK_STATE(STATE.STATE):
    def __init__(self):
        super(NETWORK_STATE,self).__init__()
        self.Machines=[]

def Create():
    return NETWORK_STATE()