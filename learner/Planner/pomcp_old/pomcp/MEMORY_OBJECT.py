__author__ = 'amir'


class MEMORY_OBJECT(object):
    def __init__(self):
        self.Allocated=False

    def SetAllocated(self):
        self.Allocated = True
    def ClearAllocated(self):
        self.Allocated = False
    def IsAllocated(self):
         return self.Allocated

