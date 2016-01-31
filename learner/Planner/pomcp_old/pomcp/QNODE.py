from Planner.pomcp import VALUE, ALPHA

__author__ = 'amir'

NumChildren = 0


class QNODE(object):
    def __init__(self):
        self.Children=[]
        self.AlphaData= ALPHA.ALPHA()
        self.Value= VALUE.VALUE(0.0,0.0)
        self.AMAF= VALUE.VALUE(0.0,0.0)


    def  Child(self, c):
        return self.Children[c]
    def  Alpha(self) :
        return self.AlphaData

    def Initialise(self):
        assert(NumChildren!=0)
        self.Children=[None for x in range(NumChildren)]
        for observation in range( NumChildren):
            self.Children[observation] =None
        self.AlphaData.AlphaSum=[]


    def DisplayValue(self, history,  maxDepth) :
        history.Display()
        print  ": " ,  self.Value.GetValue() ,  " (" ,  self.Value.GetCount() ,  ")\n"
        if (history.Size() >= maxDepth):
            return

        for observation in range( NumChildren ):
            if (self.Children[observation]):

                history.Back().Observation = observation
                self.Children[observation].DisplayValue(history, maxDepth)




    def DisplayPolicy(self, history,  maxDepth) :
        history.Display()
        print  ": " ,  self.Value.GetValue() ,  " (" , self.Value.GetCount() ,  ")\n"
        if (history.Size() >= maxDepth):
            return

        for observation in range( NumChildren ):
            if (self.Children[observation]):

                history.Back().Observation = observation
                self.Children[observation].DisplayPolicy(history, maxDepth)

