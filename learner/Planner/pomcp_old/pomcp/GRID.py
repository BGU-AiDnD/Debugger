from Planner.pomcp import COORD

__author__ = 'amir'


class GRID(object):
    def __init__(self,XSize,YSize):
        self.XSize=XSize
        self.YSize=YSize
        self.Grid=[]
        self.Grid.resize(self.XSize * self.YSize)

    def Resize(self,XSize,YSize):
        self.XSize=XSize
        self.YSize=YSize
        self.Grid=[]
        self.Grid.resize(self.XSize * self.YSize)

    def GetXSize(self):
        return self.XSize
    def GetYSize(self):
        return self.YSize

    def IndexCoord(self,  coord):
        return self.XSize * coord.Y + coord.X

    def Index(self, x,  y):
        assert(self.Inside(COORD.COORD(x, y)))
        return self.XSize * y + x

    def Inside(self,  coord):
        return coord.X >= 0 and coord.Y >= 0 and coord.X < self.XSize and coord.Y < self.YSize

    def SetAllValues(self,  value):
        for x in range(self.XSize):
            for  y in range(self.YSize):
                self.Grid[self.Index(x, y)] = value


    def SetRow(self, y,  values):
        for x in range(self.XSize):
            self.Grid[self.Index(x, y)] = values[x]


    def SetCol(self, x,  values):
        for  y in range(self.YSize):
            self.Grid[self.Index(x, y)] = values[y]


    def Coord(self, index):
        assert(index >= 0 and index < self.XSize * self.YSize)
        return COORD.COORD(index % self.XSize, index / self.XSize)



    def DistToEdge(self,  coord,  direction):
        assert(self.Inside(coord))
        if direction== COORD.Enum["E_NORTH"]:
            return self.YSize - 1 - coord.Y
        elif direction== COORD.Enum["E_EAST"]:
            return self.XSize - 1 - coord.X
        elif direction== COORD.Enum["E_SOUTH"]:
            return coord.Y
        elif direction== COORD.Enum["E_WEST"]:
            return coord.X






