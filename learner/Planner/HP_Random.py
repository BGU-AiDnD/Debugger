import Diagnoser.diagnoserUtils
__author__ = 'amir'



def main_HP(ei):
    steps=0
    while not (ei.isTerminal() or ei.AllTestsReached() ):
        ei.addTest(ei.hp_next())
        steps=steps+1

    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps


def main_Random(ei):
    steps=0
    while not (ei.isTerminal() or ei.AllTestsReached() ):
        ei.addTest(ei.random_next())
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps


if __name__=="__main__":
    file="C:\projs\\40_weka_randomForest9.txt"
    ei=Diagnoser.diagnoserUtils.readPlanningFile(file)
    print main_Random(ei.Copy())
    print main_HP(ei.Copy())