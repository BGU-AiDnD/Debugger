__author__ = 'amir'

import math


lst=["E_NORTH","E_EAST","E_SOUTH","E_WEST","E_NORTHEAST","E_SOUTHEAST","E_SOUTHWEST","E_NORTHWEST"]
Enum={}
for x,ind in enumerate(lst):
    Enum[ind]=x




class COORD(object):
    def __init__(self,x, y):
        self.X=x
        self.Y=y

    def Valid(self):
        return self.X >= 0 and self.Y >= 0


    def equal(self, rhs):
        return self.X == rhs.X and self.Y == rhs.Y


    def isDif(self,rhs):
        return self.X != rhs.X or self.Y != rhs.Y


    def AddOffset(self, offset):
        self.X += offset.X
        self.Y += offset.Y


    def Add(self, rhs):
        return COORD(self.X + rhs.X, self.Y + rhs.Y)


    def multyply(self,mul):
        return COORD(self.X * mul, self.Y * mul)

def Clockwise( dir):
    return (dir + 1) % 4
def Opposite( dir):
    return (dir + 2) % 4
def Anticlockwise( dir):
    return (dir + 3) % 4


def EuclideanDistance( lhs,  rhs):

    return math.sqrt((lhs.X - rhs.X) * (lhs.X - rhs.X)
              + (lhs.Y - rhs.Y) * (lhs.Y - rhs.Y))


def ManhattanDistance( lhs,  rhs):

    return abs(lhs.X - rhs.X) + abs(lhs.Y - rhs.Y)


def DirectionalDistance( lhs,  rhs, direction):
    if direction==Enum["E_NORTH"]:
        return rhs.Y - lhs.Y
    elif direction==Enum["E_EAST"]:
        return rhs.X - lhs.X
    elif direction==Enum["E_SOUTH"]:
        return lhs.Y - rhs.Y
    elif direction==Enum["E_WEST"]:
        return lhs.X - rhs.X


def printCoord(coord):
    print "(" , coord.X , ", " , coord.Y , ")"


Null=COORD(-1,-1)
North, East, South, West=COORD(0,1),COORD(1,0),COORD(0,-1),COORD(-1,0)
NorthEast, SouthEast, SouthWest, NorthWest=COORD(1,1),COORD(1,-1),COORD(-1,-1),COORD(-1,1)
Compass=[North, East, South, West, NorthEast,SouthEast,SouthWest,NorthWest]
CompassString=["N", "E","S","W","NE","SE","SW","NW"]

def UnitTest():

    assert(COORD(3, 3).Add( COORD(2, 2)).equal( COORD(5, 5)))
    coord =COORD(5, 2)
    coord .AddOffset(COORD(2, 5))
    assert(coord .equal(COORD(7, 7)))
    assert(COORD(2, 2) .Add(  North ).equal( COORD(2, 3)))
    assert(COORD(2, 2) .Add(  East ).equal( COORD(3, 2)))
    assert(COORD(2, 2) .Add(  South).equal( COORD(2, 1)))
    assert(COORD(2, 2) .Add(  West) .equal( COORD(1, 2)))
    assert(Compass[Enum["E_NORTH"]] == North)
    assert(Compass[Enum["E_EAST"]] == East)
    assert(Compass[Enum["E_WEST"]] == West)
    assert(Compass[Enum["E_SOUTH"]] == South)
    assert(Clockwise(Enum["E_NORTH"]) == Enum["E_EAST"])
    assert(Clockwise(Enum["E_EAST"]) == Enum["E_SOUTH"])
    assert(Clockwise(Enum["E_SOUTH"]) == Enum["E_WEST"])
    assert(Clockwise(Enum["E_WEST"]) == Enum["E_NORTH"])
    assert(Opposite(Enum["E_NORTH"]) == Enum["E_SOUTH"])
    assert(Opposite(Enum["E_EAST"]) == Enum["E_WEST"])
    assert(Opposite(Enum["E_SOUTH"]) == Enum["E_NORTH"])
    assert(Opposite(Enum["E_WEST"]) == Enum["E_EAST"])
    assert(Anticlockwise(Enum["E_NORTH"]) == Enum["E_WEST"])
    assert(Anticlockwise(Enum["E_EAST"]) == Enum["E_NORTH"])
    assert(Anticlockwise(Enum["E_SOUTH"]) == Enum["E_EAST"])
    assert(Anticlockwise(Enum["E_WEST"]) == Enum["E_SOUTH"])
    assert(ManhattanDistance(COORD(3, 2), COORD(-4, -7)) == 16)
    assert(DirectionalDistance(COORD(3, 2), COORD(-4, -7), Enum["E_NORTH"]) == -9)
    assert(DirectionalDistance(COORD(3, 2), COORD(-4, -7), Enum["E_EAST"]) == -7)
    assert(DirectionalDistance(COORD(3, 2), COORD(-4, -7), Enum["E_SOUTH"]) == 9)
    assert(DirectionalDistance(COORD(3, 2), COORD(-4, -7), Enum["E_WEST"]) == 7)

UnitTest()