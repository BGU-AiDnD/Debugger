import Planner.lrtdp.lrtdpState

__author__ = 'amir'

singleton=None


class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
    if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance


class LRTDP(Singleton):
    def __init__(self,experimentInstance,epsilon,stackSize,numTrials):
        self.states={}
        self.epsilon=epsilon
        self.stackSize=stackSize
        self.numTrials=numTrials
        self.experimentInstance=experimentInstance



    def create_start_state(self):
        return self.generateState(self.experimentInstance)

    def generateState(self,experimentInstance):
        key=repr(experimentInstance.initial_tests)+"-"+repr([ind for ind,x in enumerate(experimentInstance.error) if x==1])
        print key
        if key in self.states:
            print key, "saved!"
            return self.states[key]
        state = Planner.lrtdp.lrtdpState.LrtdpState(experimentInstance.Copy())
        self.states[key]= state
        return self.states[key]

    def nextStateDist(self,ei,action):
        dist=ei.next_state_distribution(action)
        stateDist=[]
        for next,prob in dist:
            stateDist.append((self.generateState(next),prob))
        return stateDist


    #generate Policy!!
    def lrtdp(self):
        start=self.create_start_state()
        trialsCount=0
        if start.isTerminal():
            return
        else:
            while not start.isSolved:
                if trialsCount>self.numTrials:
                    return
                self.numTrials=self.numTrials+1
                success = self.runLrtdpTrial(start)
                if not success:
                    return
        return

    def runLrtdpTrial(self,state):
        visited=[] # stack

        while not state.isSolved:
            visited.append(state)
            if state.isTerminal():
                break
            if len(visited)>self.stackSize:
                return  False
            a=state.greedyAction()
            state.update(a)
            state = state.simulate_next_state(a)
        while len(visited)>0:
            if not self.checkSolved(visited.pop()):
                break
        return True

    def checkSolved(self,s):
        ans=True
        open=[]
        closed=[]
        if not s.isSolved:
            open.append(s)

        while len(open)>0:
            state=open.pop()
            if state.residual>self.epsilon:
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
        else:
            while len(closed)>0:
                c=closed.pop()
                c.update(c.greedyAction())
        return ans



    def evaluatePolicy(self):
        state=self.create_start_state()
        steps=0
        ei=None
        while not state.isSolved:
            a=state.greedyAction()
            ei=state.experimentInstance.Copy()
            obs=ei.addTest(a)
            state=self.generateState(ei)
            steps=steps+1
        precision, recall=ei.calc_precision_recall()
        return precision, recall, steps



def setSingleton(single):
    global singleton
    singleton=single

def getSingleton():
    return singleton
