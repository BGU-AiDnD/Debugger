__author__ = 'amir'

import Planner.lrtdp.lrtdpState
import Diagnoser.ExperimentInstance
import time

states={}
epsilon=0
iterations=0
greedy_action_treshold=1
experimentInstance=None
approach = "uniform"

def setVars(experimentInstanceArg, epsilonArg, iterationsArg, greedy_action_tresholdArg, approachArg):
    global experimentInstance,epsilon, iterations, greedy_action_treshold, approach
    epsilon=epsilonArg
    iterations=iterationsArg
    greedy_action_treshold = greedy_action_tresholdArg
    experimentInstance=experimentInstanceArg
    approach = approachArg


def create_start_state():
    return generateState(experimentInstance)

def generateState(ei):
    global states
    key=repr(ei)
    if key not in states:
        state = Planner.lrtdp.lrtdpState.LrtdpState(ei, approach)
        states[key]= state
    return states[key]

def clean():
    global states
    states={}


def nextStateDist(ei,action):
    dist=ei.next_state_distribution(action)
    stateDist=[]
    for next,prob in dist:
        stateDist.append((generateState(next),prob))
    return stateDist


def lrtdp():
    global iterations
    state = create_start_state()
    steps = 0
    clean()
    while not state.isTerminal() and not state.AllTestsReached():
        for i in xrange(iterations):
            if state.isSolved:
                break
            runLrtdpTrial(state)
        if state.isSolved:
            break
        steps += 1
        action = state.greedyAction()
        print "action, time:", action, time.time()
        ei = Diagnoser.ExperimentInstance.addTests(state.experimentInstance, action)
        state = generateState(ei)
    precision, recall = state.experimentInstance.calc_precision_recall()
    return precision, recall, steps, repr(state)

def runLrtdpTrial(state):
    visited = [] # stack
    while not (state.isSolved or state.AllTestsReached()):
        visited.append(state)
        if state.isTerminal():
            break
        a = state.greedyAction(greedy_action_treshold)
        state.update(a)
        state = state.simulate_next_state(a)
    while visited:
        if not checkSolved(visited.pop()):
            break
    return

def checkSolved(s):
    global epsilon
    rv=True
    open = []
    closed = {}
    if not s.isSolved:
        open.append(s)
    while open:
        state = open.pop()
        if state.AllTestsReached():
            continue
        a = state.greedyAction()
        closed[state] = a
        if state.residual(a) > epsilon:
            rv = False
            break
        nextStateDist = state.getNextStateDist(a)
        for next,prob in nextStateDist:
            if (not next.isSolved) and (next not in open) and (next not in closed):
                open.append(next)
    if rv:
        for c in closed:
            c.isSolved = True
    else:
        for c in closed:
            if not c.AllTestsReached():
                c.update(closed[c])
    return rv

def evaluatePolicy():
    state=create_start_state()
    steps=0
    ei=state.experimentInstance
    while (not state.isSolved) and (not state.terminal_or_allReach()):
        action = state.greedyAction()
        ei = Diagnoser.ExperimentInstance.addTests(ei, action)
        state = generateState(ei)
        steps = steps + 1
    precision, recall = ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)


def multiLrtdp():
    global iterations
    state=create_start_state()
    trialsCount=0
    steps=0
    ei=state.experimentInstance
    if state.isTerminal():
        precision, recall=ei.calc_precision_recall()
        return precision, recall, 0
    while not state.isSolved:
        if trialsCount>iterations:
            return
        trialsCount=trialsCount+1
        success = runLrtdpTrial(state)
        if not success:
            return
        a=state.greedyAction()
        ei = Diagnoser.ExperimentInstance.addTests(ei, a)
        state=generateState(ei)
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps
