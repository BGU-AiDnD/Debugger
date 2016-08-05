import copy
import math
import random
import numpy
import Diagnoser.diagnoserUtils

__author__ = 'amir'


TERMINAL_PROB = 0.7

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

    def get_optionals_probabilities(self):
        optionals = self.get_optionals_actions()
        probabilites = [ 1.0/len(optionals) for x in optionals]
        return  optionals, probabilites

    def get_optionals_probabilities_by_approach(self, approach):
        optionals, probabilities = [], []
        if approach == "uniform":
            optionals, probabilities = self.get_optionals_probabilities()
        elif approach == "hp":
            optionals, probabilities = self.next_tests_by_hp()
        elif approach == "entropy":
            optionals, probabilities = self.next_tests_by_entropy()
        else:
            raise RuntimeError("self.approach is not configured")
        return optionals, probabilities

    def compsProbs(self):
        """
        calculate for each component c the sum of probabilities of the diagnoses that include c
        return dict of (component, probability)
        """
        self.diagnose()
        compsProbs={}
        for d in self.diagnoses:
            p = d.probability
            for comp in d.diagnosis:
                if comp not in compsProbs:
                    compsProbs[comp] = 0
                compsProbs[comp] = compsProbs[comp] + p
        return sorted(compsProbs.items(),key=lambda x: x[1])

    def next_tests_by_hp(self):
        """
        order tests by probabilities of the components
        return tests and probabilities
        """
        compsProbs = self.compsProbs()
        comps_probabilities = dict(compsProbs)
        optionals = self.get_optionals_actions()
        if len(optionals)==0:
            print "next_tests_by_hp","len(optionals)==0:"
        tests_probabilities = []
        for test in optionals:
            trace = self.pool[test]
            test_p = 0.0
            for comp in trace:
                test_p += comps_probabilities.get(comp, 0)
            tests_probabilities.append(test_p)
        tests_probabilities = [abs(x) for x in tests_probabilities]
        tests_probabilities = [x / sum(tests_probabilities) for x in tests_probabilities]
        return optionals, tests_probabilities

    def next_tests_by_entropy(self):
        """
        order by InfoGain using entropy
        return tests and probabilities
        """
        probabilities = []
        optionals = self.get_optionals_actions()
        for t in optionals:
            probabilities.append(self.info_gain(t))
        probabilities = [abs(x) for x in probabilities]
        probabilities = [x / sum(probabilities) for x in probabilities]
        return optionals, probabilities

    def info_gain(self, test):
        """
        calculate the information gain by test
        """
        fail_test, pass_test = self.next_state_distribution(test)
        ei_fail, p_fail = fail_test
        ei_pass, p_pass = pass_test
        return self.entropy() - (p_fail * ei_fail.entropy() + p_pass * ei_pass.entropy())

    def entropy(self):
        self.diagnose()
        sum = 0.0
        for d in self.diagnoses:
            p = d.get_prob()
            sum += p * math.log(p)
        return sum

    def childs_probs_by_hp(self):
        """
        compute HP for the optionals tests and return dict of (test, prob)
        """
        comps_prob = dict(self.compsProbs()) # tuples of (comp, prob)
        optionals = self.get_optionals_actions()
        if len(optionals)==0:
            print "next_tests_by_hp","len(optionals)==0:"
        optionals_probs = {}
        for op in optionals:
            trace = self.pool[op]
            prob = 0
            for comp in trace:
                prob += comps_prob.get(comp, 0)
            optionals_probs[op] = prob
        return optionals_probs

    def hp_next(self):
        optionals, probabilities =  self.next_tests_by_hp()
        return numpy.random.choice(optionals, 1, p = probabilities).tolist()[0]

    def entropy_next(self):
        optionals, probabilities =  self.next_tests_by_entropy()
        return numpy.random.choice(optionals, 1, p = probabilities).tolist()[0]

    def random_next(self):
        return random.choice(self.get_optionals_actions())

    def getMaxProb(self):
        self.diagnose()
        maxP=max([x.probability for x in self.diagnoses])
        return maxP

    def isTerminal(self):
        return self.getMaxProb() > TERMINAL_PROB

    def AllTestsReached(self):
        return len(self.get_optionals_actions())== 0

    def addTest(self,next_test):
        """
        add test with real outcome
        """
        self.simulateTestOutcome(next_test,self.error[next_test])
        return self.error[next_test]


    def simulateTestOutcome(self,next_test,outcome):
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
            pass_Probability=pass_Probability * 0.9 # all components has chance of 0.1 to be faulty
            if comp in probs:
                pass_Probability=pass_Probability * (1-probs[comp]) # add known faults
        return pass_Probability


    def next_state_distribution(self,action):
        pass_Probability=self.compute_pass_prob(action)
        ei_fail=self.Copy()
        ei_fail.simulateTestOutcome(action,0)
        ei_pass=self.Copy()
        ei_pass.simulateTestOutcome(action,1)
        return [(ei_fail,pass_Probability),(ei_pass,1-pass_Probability)]


    def simulate_next_test_outcome(self,action):
        pass_Probability=self.compute_pass_prob(action)
        if random.random() <= pass_Probability:
            return 0
        else:
            return 1


    def simulate_next_ei(self,action):
        outcome = self.simulate_next_test_outcome(action)
        return outcome,self.next_state_distribution(action)[outcome][0]

    def diagnose(self):
        if self.diagnoses == []:
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
        s=sum([d.probability for d in self.diagnoses ])
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
        return precision_accum,recall_accum

    def __repr__(self):
        return repr(self.initial_tests)+"-"+repr([ind for ind,x in enumerate(self.error) if x==1])
