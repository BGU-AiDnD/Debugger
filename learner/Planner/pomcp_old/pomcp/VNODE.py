from Planner.pomcp import VALUE, MEMORY_POOL, MEMORY_OBJECT, QNODE, BELIEF_STATE

__author__ = 'amir'

import sys




class VNODE(MEMORY_OBJECT.MEMORY_OBJECT):
    def __init__(self):
        super(VNODE,self).__init__()
        self.Children=[]
        self.BeliefState= BELIEF_STATE.BELIEF_STATE()
        self.Value= VALUE.VALUE(0,0)


    def  Child(self, c):
        return self.Children[c]

    def  Beliefs(self) :
        return self.BeliefState

    def Initialise(self):
        assert(NumChildren!=0)
        self.Children=[QNODE.QNODE() for x in range(NumChildren)]
        for action in range( NumChildren ):
            self.Children[action].Initialise()

    def SetChildren(self, count,  value):
        for action in range( NumChildren ):
            qnode = self.Children[action]
            qnode.Value.Set(count, value)
            qnode.AMAF.Set(count, value)


    def DisplayValue(self, history,  maxDepth) :
        if (history.Size() >= maxDepth):
            return

        for action in range( NumChildren ):
            history.Add(action)
            self.Children[action].DisplayValue(history, maxDepth)
            history.Pop()

    def DisplayPolicy(self, history,  maxDepth) :
        if (history.Size() >= maxDepth):
            return

        bestq = -sys.maxint
        besta = -1
        for action in range( NumChildren ):

            if (self.Children[action].Value.GetValue() > bestq):

                besta = action
                bestq = self.Children[action].Value.GetValue()


        if (besta != -1):

            history.Add(besta)
            self.Children[besta].DisplayPolicy(history, maxDepth)
            history.Pop()

def  Create():
    vnode = VNodePool.Allocate()
    vnode.Initialise()
    return vnode

def constructor():
    return VNODE()

NumChildren = 0
VNodePool = MEMORY_POOL.MEMORY_POOL(constructor)
