__author__ = 'amir'

import sys
import Planner.planningExperiments


if __name__ == "__main__":
    f, epsilon, out_dir, stack, trials = sys.argv[1:]
    Planner.planningExperiments.one_lrtdp(f, epsilon, out_dir, stack, trials)
