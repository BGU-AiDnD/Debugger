__author__ = 'amir'

import Planner.lrtdp.lrtdpState

states={}
epsilon=0
stackSize=0
iterations=0
experimentInstance=None
approach = "uniform"

def setVars(experimentInstanceArg, epsilonArg, stackSizeArg, iterationsArg, approachArg):
    global experimentInstance,epsilon,stackSize, iterations, approach
    epsilon=epsilonArg
    stackSize=stackSizeArg
    iterations=iterationsArg
    experimentInstance=experimentInstanceArg
    approach = approachArg


def create_start_state():
    return generateState(experimentInstance)

def generateState(ei):
    global states
    key=repr(ei)
    if key not in states:
        state = Planner.lrtdp.lrtdpState.LrtdpState(ei.Copy(), approach)
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
    while not state.isTerminal() and not state.AllTestsReached():
        clean()
        for i in xrange(iterations):
            if state.isSolved:
                break
            runLrtdpTrial(state)
        steps += 1
        action = state.greedyAction()
        ei = state.experimentInstance.Copy()
        ei.addTest(action)
        state = generateState(ei)
        print "action: ", action
    precision, recall = state.experimentInstance.calc_precision_recall()
    return precision, recall, steps

def runLrtdpTrial(state):
    global stackSize
    visited = [] # stack
    while not (state.isSolved or state.AllTestsReached()):
        visited.append(state)
        if state.isTerminal():
            break
        if len(visited) > stackSize:
            return
        a = state.greedyAction()
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
    closed = []
    if not s.isSolved:
        open.append(s)
    while open:
        state = open.pop()
        closed.append(state)
        if state.AllTestsReached():
            continue
        try:
            a = state.greedyAction()
        except:
            x  = 96
        if state.residual(a) > epsilon:
            rv = False
            continue
        nextStateDist = state.getNextStateDist(a)
        for next,prob in nextStateDist:
            if (not next.isSolved) and (next not in open) and (next not in closed):
                open.append(next)
    if rv:
        for c in closed:
            c.isSolved = True
    else:
        while closed:
            c = closed.pop()
            if not c.AllTestsReached():
                c.update(c.greedyAction())
    return rv

def evaluatePolicy():
    state=create_start_state()
    steps=0
    ei=state.experimentInstance.Copy()
    while (not state.isSolved) and (not state.terminal_or_allReach()):
        action = state.greedyAction()
        ei = state.experimentInstance.Copy()
        obs = ei.addTest(action)
        state = generateState(ei)
        steps = steps + 1
        precision, recall = ei.calc_precision_recall()

    precision, recall = ei.calc_precision_recall()
    return precision, recall, steps, repr(ei)


def multiLrtdp():
    global iterations
    state=create_start_state()
    trialsCount=0
    steps=0
    ei=state.experimentInstance.Copy()
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
        ei=state.experimentInstance.Copy()
        obs=ei.addTest(a)
        state=generateState(ei)
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    return precision, recall, steps
