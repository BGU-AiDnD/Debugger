__author__ = 'amir'

import Planner.lrtdp.lrtdpState

states={}
epsilon=0
stackSize=0
numTrials=0
experimentInstance=None

def setVars(experimentInstanceArg,epsilonArg,stackSizeArg,numTrialsArg):
    global experimentInstance,epsilon,stackSize,numTrials
    epsilon=epsilonArg
    stackSize=stackSizeArg
    numTrials=numTrialsArg
    experimentInstance=experimentInstanceArg


def create_start_state():
    return generateState(experimentInstance)

def generateState(experimentInstance):
    key=repr(experimentInstance)
    if key not in states:
        state = Planner.lrtdp.lrtdpState.LrtdpState(experimentInstance.Copy())
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


#generate Policy!!
def lrtdp():
    global numTrials
    start=create_start_state()
    trialsCount=0
    if start.isTerminal():
        return
    else:
        while not start.isSolved:
            if trialsCount>numTrials:
                return
            trialsCount=trialsCount+1
            success = runLrtdpTrial(start)
            if not success:
                return
    return

def runLrtdpTrial(state):
    visited=[] # stack
    while not (state.isSolved or state.AllTestsReached()):
        visited.append(state)
        if state.isTerminal():
            break
        if len(visited)>stackSize:
            return  False
        a=state.greedyAction()
        state.update(a)
        state = state.simulate_next_state(a)
    while len(visited)>0:
        if not checkSolved(visited.pop()):
            break
    return True

def checkSolved(s):
    ans=True
    open=[]
    closed=[]
    if not s.isSolved:
        open.append(s)

    while len(open)>0:
        state=open.pop()
        if state.residual>epsilon:
            ans=False
            continue
        a = state.greedyAction()
        nextStateDist=state.getNextStateDist(a)
        for next,prob in nextStateDist:
            if (not next.isSolved) and next not in open and next not in closed:
                open.append(next)
    if ans:
        for c in closed:
            c.isSolved=True
            print "marked as Solved"
    else:
        while len(closed)>0:
            c=closed.pop()
            c.update(c.greedyAction())
    return ans

def evaluatePolicy():
    state=create_start_state()
    steps=0
    ei=state.experimentInstance.Copy()
    while (not state.isSolved) and (not state.terminal_or_allReach()):
        a=state.greedyAction()
        ei=state.experimentInstance.Copy()
        obs=ei.addTest(a)
        state=generateState(ei)
        steps=steps+1

    print "initial_tests", len(ei.initial_tests), ei.priors
    precision, recall=ei.calc_precision_recall()
    print "end",repr(ei)
    return precision, recall, steps


def multiLrtdp():
    global numTrials
    state=create_start_state()
    trialsCount=0
    steps=0
    ei=state.experimentInstance.Copy()
    if state.isTerminal():
        precision, recall=ei.calc_precision_recall()
        return precision, recall, 0
    while not state.isSolved:
        if trialsCount>numTrials:
            print "numTrials Reached" ,numTrials
            return
        trialsCount=trialsCount+1
        success = runLrtdpTrial(state)
        if not success:
            print "not success"
            return
        a=state.greedyAction()
        ei=state.experimentInstance.Copy()
        obs=ei.addTest(a)
        state=generateState(ei)
        steps=steps+1
    precision, recall=ei.calc_precision_recall()
    print "end",repr(ei)
    return precision, recall, steps