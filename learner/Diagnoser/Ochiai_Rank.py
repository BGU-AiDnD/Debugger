__author__ = 'amir'

import math

class Ochiai_Rank():

    def __init__(self):
        self.counters = {}
        self.counters[1]={}
        self.counters[0]={}
        self.counters[1][1] = 0.0
        self.counters[0][1] = 0.0
        self.counters[1][0] = 0.0
        self.counters[0][0] = 0.0

    def clone(self):
        cloneObj = Ochiai_Rank()
        cloneObj.counters[1][1] = self.counters[1][1]
        cloneObj.counters[0][1] = self.counters[0][1]
        cloneObj.counters[1][0] = self.counters[1][0]
        return cloneObj

    def get_rank(self):
        n11 = self.counters[1][1]
        n10 = self.counters[1][0]
        n01 = self.counters[0][1]
        if ((n11 + n01) * (n11 + n10) != 0):
            return n11 / math.sqrt((n11 + n01) * (n11 + n10))
        return 0

    def reduce_counter(self, i, j):
        self.counters[i][j] -= 1

    def advance_counter(self, i, j):
        self.counters[i][j] += 1

