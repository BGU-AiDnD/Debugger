import copy
import random
import Diagnoser.diagnoserUtils

__author__ = 'amir'


class ExperimentInstance:
    def __init__(self,priors, bugs, initial_tests, failed_tests,  pool	,error):
        self.priors = priors
        self.bugs = bugs
        self.initial_tests=initial_tests
        self.failed_tests=failed_tests
        self.pool = pool
        self.error = error
        self.diagnoses=[]

    def Copy(self):
        exp= ExperimentInstance(copy.deepcopy(self.priors), copy.deepcopy(self.bugs), copy.deepcopy(self.initial_tests), copy.deepcopy(self.failed_tests),  copy.deepcopy(self.pool)	,copy.deepcopy(self.error))
        exp.diagnoses=[x.clone() for x in self.diagnoses]
        return exp

    def initials_to_DS(self):
        ds=Diagnoser.diagnoserUtils.dynamicSpectrum()
        ds.TestsComponents=copy.deepcopy([x for ind,x in enumerate(self.pool) if ind in self.initial_tests ])
        ds.probabilities=list(self.priors)
        ds.error=[x for ind,x in enumerate(self.error) if ind in self.initial_tests ]
        return ds

    def get_optionals_actions(self):
        optionals = [x for x in range(len(self.pool)) if x not in self.initial_tests]
        return optionals

    def compsProbs(self):
        self.diagnose()
        compsProbs={}
        for d in self.diagnoses:
            p=d.probability
            for comp in d.diagnosis:
                if comp not in compsProbs:
                    compsProbs[comp]=0
                compsProbs[comp]=compsProbs[comp]+p
        return sorted(compsProbs.items(),key=lambda x: x[1])

    def next_tests_by_hp(self):
        orderedComps=[x[0] for x in  self.compsProbs()]
        optionals=self.get_optionals_actions()
        if len(optionals)==0:
            print "next_tests_by_hp","len(optionals)==0:"
        tests_by_copms={}
        for op in optionals:
            trace=self.pool[op]
            for comp in trace:
                if comp not in tests_by_copms:
                    tests_by_copms[comp]=[]
                tests_by_copms[comp].append(op)
        for comp in orderedComps: # return tests that contains the most faulty comp
            if comp in tests_by_copms:
                return tests_by_copms[comp]
        # else all optional tests contains un diagnosed comps- return all of them
            return optionals


    def hp_next(self):
        return random.choice(self.next_tests_by_hp())

    def random_next(self):
        return random.choice(self.get_optionals_actions())

    def getMaxProb(self):
        self.diagnose()
        maxP=max([x.probability for x in self.diagnoses])
        return maxP

    def isTerminal(self):
        return self.getMaxProb()>0.7

    def AllTestsReached(self):
        return len(self.get_optionals_actions())==0

    def addTest(self,next_test):
        self.addTestOutcome(next_test,self.error[next_test])
        return self.error[next_test]


    def addTestOutcome(self,next_test,outcome):
        self.initial_tests.append(next_test)
        self.error[next_test]=outcome
        if self.error[next_test]==1:
            self.failed_tests=list(set(self.failed_tests+[next_test]))
        self.diagnoses=[]
        return self.error[next_test]

    def SimulateADDTest(self,ind,observation):
        optionals = self.get_optionals_actions()
        if optionals==[]:
            return -1
        next_test=optionals[ind % len(optionals)]
        self.initial_tests.append(next_test)
        self.error[next_test]=observation # set observation!
        if self.error[next_test]==1:
            self.failed_tests.append(next_test)
        self.diagnoses=[]
        return self.error[next_test]


    def compute_pass_prob(self,action):
        optionals = self.get_optionals_actions()
        if optionals==[]:
            return -1
        next_test=optionals[action % len(optionals)]
        trace=self.pool[next_test]
        probs=dict(self.compsProbs())
        pass_Probability=1
        for comp in trace:
            pass_Probability=pass_Probability*0.9 # all components has chance of 0.1 to be faulty
            if comp in probs:
                pass_Probability=pass_Probability*(1-probs[comp]) # add known faults
        return pass_Probability


    def next_state_distribution(self,action):
        pass_Probability=self.compute_pass_prob(action)
        zeroOut=self.Copy()
        zeroOut.addTestOutcome(action,0)
        oneOut=self.Copy()
        oneOut.addTestOutcome(action,1)
        return [(zeroOut,pass_Probability),(oneOut,1-pass_Probability)]


    def simulate_next_test_outcome(self,action):
        pass_Probability=self.compute_pass_prob(action)
        if random.random() <= pass_Probability:
            return 0
        else:
            return 1


    def simulate_next_ei(self,action):
        outcome=self.simulate_next_test_outcome(action)
        return outcome,self.next_state_distribution(action)[outcome][0]



    def diagnose(self):
        if self.diagnoses==[]:
            self.diagnoses=self.initials_to_DS().diagnose()



    def precision_recall_diag(self,buggedComps, dg, pr, validComps):
        fp = len([i1 for i1 in dg if i1 in validComps])
        fn = len([i1 for i1 in buggedComps if i1 not in dg])
        tp = len([i1 for i1 in dg if i1 in buggedComps])
        tn = len([i1 for i1 in validComps if i1 not in dg])
        if ((tp + fp) == 0):
            precision = "undef"
        else:
            precision = (tp + 0.0) / float(tp + fp)
            a = precision
            precision = precision * float(pr)
        if ((tp + fn) == 0):
            recall = "undef"
        else:
            recall = (tp + 0.0) / float(tp + fn)
            recall = recall * float(pr)
        return precision, recall


    def calc_precision_recall(self):
        self.diagnose()
        recall_accum=0
        precision_accum=0
        validComps=[x for x in range(max(reduce(list.__add__, self.pool))) if x not in self.bugs]
        for  d in self.diagnoses:
            dg=d.diagnosis
            pr=d.probability
            precision, recall = self.precision_recall_diag(self.bugs, dg, pr, validComps)
            if(recall!="undef"):
                recall_accum=recall_accum+recall
            if(precision!="undef"):
                precision_accum=precision_accum+precision
        return recall_accum,precision_accum

    def __repr__(self):
        return repr(self.initial_tests)+"-"+repr([ind for ind,x in enumerate(self.error) if x==1])
