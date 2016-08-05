import Diagnoser.diagnoserUtils
__author__ = 'amir'

"""
 basic planners:
 random
 all_tests
 only_initials
 HP
 Entropy

 all functions return tuple of (precision, recall, steps)
"""

def main_HP(ei):
    steps = 0
    while not (ei.isTerminal() or ei.AllTestsReached() ):
        ei.addTest(ei.hp_next())
        steps = steps + 1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps


def main_Random(ei):
    steps = 0
    while not (ei.isTerminal() or ei.AllTestsReached() ):
        ei.addTest(ei.random_next())
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps

def only_initials(ei):
    steps = 0
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps


def all_tests(ei):
    steps = 0
    while not ei.AllTestsReached() :
        ei.addTest(ei.random_next())
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps


def main_entropy(ei):
    steps = 0
    while not (ei.isTerminal() or ei.AllTestsReached() ):
        ei.addTest(ei.entropy_next())
        steps = steps + 1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps

if __name__=="__main__":
    file = r"C:\projs\lrtdp\instances\40_uniform_8.txt"
    ei=Diagnoser.diagnoserUtils.readPlanningFile(file)
    print main_Random(ei.Copy())
    print main_HP(ei.Copy())
    print main_entropy(ei.Copy())
