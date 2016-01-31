__author__ = 'amir'

import random
import math

def Sign(x):

    return (x > 0) - (x < 0)


def Random(max):

    return random.randint(0,max)


def RandomMinMax(min, max):

    return random.randint(min,max)


def RandomDouble(min, max):

    return random.uniform(min,max)


def RandomSeed(seed):

    pass


def Bernoulli(p):

    return random.random() < p


def Near(x, y, tol):

    return math.fabs(x - y) <= tol


def CheckFlag(flags, bit):
    return (flags & (1 << bit)) != 0

def SetFlag( flags, bit):

    flags|= (1 << bit)
    return flags

def Contains(vec, item):

    return item in vec


def UnitTest():
    assert(Sign(+10) == +1)
    assert(Sign(-10) == -1)
    assert(Sign(0) == 0)

    n = [0 for x in range(6)]
    for i in range(10000):
        for j in range(6):
            if  (Random(j) == 0):
                n[j] += 1
    assert(Near(n[0], 10000, 0))
    assert(Near(n[1], 5000, 250))
    assert(Near(n[2], 3333, 250))
    assert(Near(n[3], 2500, 250))
    assert(Near(n[4], 2000, 250))

    c = 0
    for i in range(10000):
        c += Bernoulli(0.5)
    assert(Near(c, 5000, 250))
    assert(CheckFlag(5, 0))
    assert(not CheckFlag(5, 1))
    assert(CheckFlag(5, 2))
    assert(not CheckFlag(5, 3))
    flag = 1
    flag=SetFlag(flag, 2)
    flag=SetFlag(flag, 4)
    assert(flag == 21)


UnitTest()