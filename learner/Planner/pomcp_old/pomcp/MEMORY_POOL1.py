from Planner.pomcp import CHUNK

__author__ = 'amir'


class MEMORY_POOL1(object):
    def __init__(self,objectType):
        self.NumAllocated=0
        self.FreeList=[]
        self.Chunks=[]
        self.objectType=objectType

    def   Construct(self):
        obj = self.Allocate()
        return obj

    def Destroy(self,obj):
        self.Free(obj)

    def Allocate(self) :
        if (len(self.FreeList)==0):
            self.NewChunk()
        obj = self.FreeList[0]
        self.FreeList=self.FreeList[1:]
        assert(not obj.IsAllocated())
        obj.SetAllocated()
        self.NumAllocated=self.NumAllocated+1
        return obj

    def Free(self,obj):
        assert(obj.IsAllocated())
        obj.ClearAllocated()
        self.FreeList.append(obj)
        self.NumAllocated-=1

    def DeleteAll(self):

        for i_chunk in self.Chunks:
            del i_chunk
        self.Chunks=[]
        self.FreeList=[]
        self.NumAllocated = 0

    def GetNumAllocated(self):
        return self.NumAllocated

    def NewChunk(self):
            chunk = CHUNK.CHUNK(self.objectType)
            self.Chunks.append(chunk)
            for  i in xrange(CHUNK.Size - 1,0,-1):
                self.FreeList.append(chunk.Objects[i])
                chunk.Objects[i].ClearAllocated()



