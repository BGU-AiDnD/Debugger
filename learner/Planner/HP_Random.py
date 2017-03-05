__author__ = 'amir'
import Diagnoser.diagnoserUtils
import Diagnoser.ExperimentInstance

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
        ei = Diagnoser.ExperimentInstance.addTests(ei, ei.hp_next())
        steps = steps + 1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)


def main_Random(ei):
    steps = 0
    while not (ei.isTerminal() or ei.AllTestsReached() ):
        ei = Diagnoser.ExperimentInstance.addTests(ei, ei.random_next())
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)

def only_initials(ei):
    steps = 0
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)


def all_tests(ei):
    steps = 0
    while not ei.AllTestsReached() :
        ei = Diagnoser.ExperimentInstance.addTests(ei, ei.random_next())
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)


def main_entropy(ei, *args, **kwargs):
    steps = 0
    while not (ei.isTerminal() or ei.AllTestsReached()):
        ei = Diagnoser.ExperimentInstance.addTests(ei, ei.entropy_next(*args, **kwargs))
        steps = steps + 1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)

if __name__=="__main__":
    file = r"C:\projs\lrtdp\instances\40_uniform_8.txt"
    ei=Diagnoser.diagnoserUtils.readPlanningFile(file)
    print main_Random(ei)
    print main_HP(ei)
    print main_entropy(ei)
