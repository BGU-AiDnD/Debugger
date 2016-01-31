from Planner.pomcp import STATISTIC

__author__ = 'amir'


class RESULTS(object):
    def __init__(self):
        self.Time= STATISTIC.STATISTIC()
        self.Reward= STATISTIC.STATISTIC()
        self.DiscountedReturn= STATISTIC.STATISTIC()
        self.UndiscountedReturn= STATISTIC.STATISTIC()

    def Clear(self):
        self.Time.Clear()
        self.Reward.Clear()
        self.DiscountedReturn.Clear()
        self.UndiscountedReturn.Clear()
