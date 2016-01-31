__author__ = 'amir'


class MEMORY_POOL(object):
    def __init__(self,objectType):
        self.NumAllocated=0
        self.FreeList=[]
        self.Chunks=[]
        self.objectType=objectType

    def   Construct(self):

        return self.objectType()

    def Destroy(self,obj):
        pass

    def Allocate(self) :

        return self.objectType()

    def Free(self,obj):
        pass

    def DeleteAll(self):
        pass
    def GetNumAllocated(self):
        return 0

    def NewChunk(self):
            pass



