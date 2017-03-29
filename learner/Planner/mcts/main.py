__author__ = 'amir'

import Diagnoser.diagnoserUtils
import Diagnoser.ExperimentInstance
import mcts

DEFAULT_BUDGET = 100

def main_mcts(ei, approach, iterations=DEFAULT_BUDGET):
    steps = 0
    state = ei
    mcts.clear_states()
    while (not state.isTerminal()) and ( not state.AllTestsReached()):
        steps += 1
        action, weight = mcts.mcts_uct(state, iterations, approach)
        state = Diagnoser.ExperimentInstance.addTests(state, action)
    precision, recall = state.calc_precision_recall()
    return precision, recall, steps, repr(state)


def test_mcts(f):
    instance = Diagnoser.diagnoserUtils.readPlanningFile(f)
    return main_mcts(instance)



if __name__=="__main__":

    file="C:\projs\ptry\lrtdp\\30_uniform_1.txt"
    print test_mcts(file)
    # file="C:\projs\ptry\lrtdp\\10_uniform_15.txt"
    # print test_mcts(file)
    # file="C:\projs\ptry\lrtdp\\10_0.6_0.0_15.txt"
    # print test_mcts(file)

