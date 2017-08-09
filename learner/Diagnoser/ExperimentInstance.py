import copy
import math
import random
import numpy
import Diagnoser.diagnoserUtils
import Planner.domain_knowledge
from math import ceil

__author__ = 'amir'

TERMINAL_PROB = 0.7

instances = {}
priors = []
bugs = []
pool = []

def clear():
    global instances, priors, bugs, pool
    instances = {}
    priors = []
    bugs = []
    pool = []

def set_values(priors_arg, bugs_arg, pool_arg):
    clear()
    global instances, priors, bugs, pool
    priors = priors_arg
    bugs = bugs_arg
    pool = pool_arg

def get_instance(key):
    global instances
    if key not in instances:
        instances[key] = create_instance_from_key(key)
    return instances[key]

def create_instance_from_key(key):
    initial, failed = key.split('-')
    error = [1 if i in eval(failed) else 0 for i in xrange(len(pool))]
    return ExperimentInstance(eval(initial), error)

class ExperimentInstance:
    def __init__(self, initial_tests, error):
        self.initial_tests=initial_tests
        self.error = error
        self.diagnoses=[]

    def initials_to_DS(self):
        ds=Diagnoser.diagnoserUtils.dynamicSpectrum()
        ds.TestsComponents = copy.deepcopy([x for ind,x in enumerate(pool) if ind in self.initial_tests ])
        ds.probabilities=list(priors)
        ds.error=[x for ind,x in enumerate(self.error) if ind in self.initial_tests ]
        return ds

    def get_optionals_actions(self):
        optionals = [x for x in range(len(pool)) if x not in self.initial_tests]
        return optionals

    def get_optionals_probabilities(self):
        optionals = self.get_optionals_actions()
        probabilites = [ 1.0/len(optionals) for x in optionals]
        return  optionals, probabilites

    def get_optionals_probabilities_by_approach(self, approach, *args, **kwargs):
        optionals, probabilities = [], []
        if approach == "uniform":
            optionals, probabilities = self.get_optionals_probabilities()
        elif approach == "hp":
            optionals, probabilities = self.next_tests_by_hp()
        elif approach == "entropy":
            optionals, probabilities = self.next_tests_by_entropy(*args, **kwargs)
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
            p = d.get_prob()
            for comp in d.get_diag():
                compsProbs[comp] = compsProbs.get(comp,0) + p
        return sorted(compsProbs.items(),key=lambda x: x[1])

    def next_tests_by_hp(self):
        """
        order tests by probabilities of the components
        return tests and probabilities
        """
        compsProbs = self.compsProbs()
        comps_probabilities = dict(compsProbs)
        optionals = self.get_optionals_actions()
        assert  len(optionals) > 0
        tests_probabilities = []
        for test in optionals:
            trace = pool[test]
            test_p = 0.0
            for comp in trace:
                test_p += comps_probabilities.get(comp, 0)
            tests_probabilities.append(test_p)
        if sum(tests_probabilities) == 0.0:
            return self.get_optionals_probabilities()
        tests_probabilities = [abs(x) for x in tests_probabilities]
        tests_probabilities = [x / sum(tests_probabilities) for x in tests_probabilities]
        return optionals, tests_probabilities

    def next_tests_by_bd(self):
        self.diagnose()
        probabilities = []
        optionals = self.get_optionals_actions()
        for test in optionals:
            p = 0.0
            trace = pool[test]
            for d in self.diagnoses:
                p += (d.get_prob() / len(d.get_diag())) * ([x for x in d.get_diag() if x in trace])
            probabilities.append(p)
        probabilities = [abs(x) for x in probabilities]
        probabilities = [x / sum(probabilities) for x in probabilities]
        return optionals, probabilities

    def next_tests_by_entropy(self, threshold = 1.0):
        """
        order by InfoGain using entropy
        return tests and probabilities
        """
        probabilities = []
        optionals = []
        threshold_sum = 0.0
        # optionals = self.get_optionals_actions()
        optionals_seperator, tests_probabilities = Planner.domain_knowledge.seperator_hp(self)
        # optionals, tests_probabilities = self.next_tests_by_hp()
        for t, p in sorted(zip(optionals_seperator, tests_probabilities), key=lambda x: x[1], reverse=True)[:int(ceil(len(optionals_seperator) * threshold))]:
            # if threshold_sum > threshold:
            #     break
            info = self.info_gain(t)
            if info > 0:
                threshold_sum += p
                probabilities.append(info)
                optionals.append(t)
        if sum(probabilities) == 0.0:
            return self.get_optionals_probabilities()
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
            sum -= p * math.log(p)
        return sum

    def childs_probs_by_hp(self):
        """
        compute HP for the optionals tests and return dict of (test, prob)
        """
        comps_prob = dict(self.compsProbs()) # tuples of (comp, prob)
        optionals = self.get_optionals_actions()
        assert len(optionals) > 0
        optionals_probs = {}
        for op in optionals:
            trace = pool[op]
            prob = 0
            for comp in trace:
                prob += comps_prob.get(comp, 0)
            optionals_probs[op] = prob
        return optionals_probs

    def bd_next(self):
        optionals, probabilities =  self.next_tests_by_bd()
        return numpy.random.choice(optionals, 1, p = probabilities).tolist()[0]

    def hp_next(self):
        optionals, probabilities =  self.next_tests_by_hp()
        return numpy.random.choice(optionals, 1, p = probabilities).tolist()[0]

    def entropy_next(self, threshold = 1.2, batch=1):
        optionals, information =  self.next_tests_by_entropy(threshold)
        return map(lambda x: x[0], sorted(zip(optionals, information), reverse=True, key = lambda x: x[1])[:batch])
        # return numpy.random.choice(optionals, batch, p = information).tolist()

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

    def compute_pass_prob(self,action):
        trace = pool[action]
        probs=dict(self.compsProbs())
        pass_Probability = 1.0
        for comp in trace:
            pass_Probability *= 0.999 # probability of 1 fault for each 1000 lines of code
            if comp in probs:
                pass_Probability *= (1-probs[comp]) # add known faults
        return round(pass_Probability, 6)

    def next_state_distribution(self,action):
        pass_Probability=self.compute_pass_prob(action)
        ei_fail = simulateTestOutcome(self, action,0)
        ei_pass = simulateTestOutcome(self, action,1)
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
        recall_accum=0
        precision_accum=0
        validComps=[x for x in range(max(reduce(list.__add__, pool))) if x not in bugs]
        for d in self.diagnoses:
            dg=d.diagnosis
            pr=d.probability
            precision, recall = self.precision_recall_diag(bugs, dg, pr, validComps)
            if(recall!="undef"):
                recall_accum=recall_accum+recall
            if(precision!="undef"):
                precision_accum=precision_accum+precision
        return precision_accum,recall_accum

    def count_different_cases(self):
        """
        :return: the number of different test cases in the diagnosis
        """
        optional_tests = map( lambda enum: enum[1],filter(lambda enum: enum[0] in self.initial_tests, enumerate(pool)))
        return len(set(map(str, optional_tests)))


    def __repr__(self):
        return repr(self.initial_tests)+"-"+repr([ind for ind,x in enumerate(self.error) if x==1])


def create_key(initial_tests, error):
    return repr(sorted(initial_tests))+"-"+repr(sorted([ind for ind,x in enumerate(error) if x==1]))

def addTests(ei, next_tests):
    """
    add tests with real outcome
    """
    tests_to_add = [next_tests] if type(next_tests) != list else next_tests
    for t in tests_to_add:
        ei = simulateTestOutcome(ei, t, ei.error[t])
    return ei

def simulateTestOutcome(ei, next_test, outcome):
    initial_tests = copy.deepcopy(ei.initial_tests)
    initial_tests.append(next_test)
    error = list(ei.error)
    error[next_test] = outcome
    return get_instance(create_key(initial_tests, error))
