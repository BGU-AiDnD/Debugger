# order optional test by domain knowledge
# each function recieves experiments instance and
# return sorted list of optional tests ordered by the chosen metric

import Diagnoser.ExperimentInstance
import numpy

def pass_probability(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    for test in optionals:
        probabilities.append(ei.compute_pass_prob(test))
    return [x / sum(probabilities) for x in probabilities]

def intersection_with_diags(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    for test in optionals:
        p = 0.0
        for d in ei.diagnoses:
                p += d.get_prob() * len([c for c in test if c in d.get_diag()]) / (len(d.get_diag()) + 0.0)
        probabilities.append(ei.compute_pass_prob(test))
    return [x / sum(probabilities) for x in probabilities]

def fail_count(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    failed_components = set()
    for test in ei.initial_tests:
        if ei.error[test] == 0:
            continue
        trace = Diagnoser.ExperimentInstance.pool[test]
        for c in trace:
            failed_components.add(c)
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(sum([c for c in trace if c in failed_components]))
    return [x / sum(probabilities) for x in probabilities]

def fail_sum(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    failed_components = {}
    for test in ei.initial_tests:
        if ei.error[test] == 0:
            continue
        trace = Diagnoser.ExperimentInstance.pool[test]
        for c in trace:
            failed_components[c] = failed_components.get(c, 0) + 1
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(sum([failed_components.get(c, 0) for c in trace]))
    return [x / sum(probabilities) for x in probabilities]

def num_components(ei):
    optionals = ei.get_optionals_actions()
    probabilities = []
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(len(trace))
    return [x / sum(probabilities) for x in probabilities]

def new_comps(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    components = set()
    for test in ei.initial_tests:
        trace = Diagnoser.ExperimentInstance.pool[test]
        components += set(trace)
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(len([c for c in trace if c not in components]))
    return [x / sum(probabilities) for x in probabilities]

def common_comps(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    components_activity = {}
    for test in ei.initial_tests:
        trace = Diagnoser.ExperimentInstance.pool[test]
        for c in trace:
            components_activity[c] = components_activity.get(c, 0) + 1
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(sum([components_activity.get(c, 0) for c in trace]))
    return [x / sum(probabilities) for x in probabilities]


# aggregation functions
aggragetion = [sum, max , min , numpy.median, numpy.mean]

def components_diagnoses(ei, aggregation):
    ei.diagnose()
    optionals = ei.get_optionals_actions()
    probabilities = []
    components = {}
    for d in ei.diagnoses:
        for c in d.get_diag():
            components[c] = components.get(c, 0) + 1
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(aggregation([components.get(c,0) for c in trace]))
    return [x / sum(probabilities) for x in probabilities]

def components_probabilities(ei, aggregation):
    components_probs = dict(ei.compsProbs())
    optionals = ei.get_optionals_actions()
    probabilities = []
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(reduce(aggregation, [components_probs.get(c,0) for c in trace]))
    return [x / sum(probabilities) for x in probabilities]

def split_components_probabilities(ei):
    components_probs = dict(ei.compsProbs())
    half_components_probabilities = sum(components_probs.values()) / 2.0
    optionals = ei.get_optionals_actions()
    probabilities = []
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(1- abs(half_components_probabilities-reduce(lambda x,y:x+y, [components_probs.get(c,0) for c in trace])))
    return zip(optionals, [x / sum(probabilities) for x in probabilities])

def components_activity(ei, aggregation):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    activity = {}
    for test in ei.initial_tests:
        trace = Diagnoser.ExperimentInstance.pool[test]
        for c in trace:
            activity[c] = activity.get(c, 0) + 1
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(aggregation([activity.get(c, 0) for c in trace]))
    return [x / sum(probabilities) for x in probabilities]

def components_by_similarity(ei, aggregation, similarity):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    e = [ind for ind,_ in enumerate(ei.error)]
    components = {}
    for test in ei.initial_tests:
        trace = Diagnoser.ExperimentInstance.pool[test]
        for c in trace:
            components[c] = components.get(c, []) + [test]
    similarities = dict([(c,similarity(components[c], e)) for c in components])
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        probabilities.append(aggregation([similarities.get(c, 0) for c in trace]))
    return [x / sum(probabilities) for x in probabilities]

def friends(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    components_probs = dict(ei.compsProbs())
    components_friends = {}
    for d in ei.diagnoses:
        for c in d.get_diag():
            components_friends[c] = components_friends.get(c, set()).union(set([x for x in d.get_diag() if x != c]))
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        p = 0.0
        for c in components_probs:
            if c in trace:
                continue
            p += components_probs[c] * len([x for x in components_friends[c] if x in trace])
            probabilities.append(p)
    return zip(optionals, [x / sum(probabilities) for x in probabilities])

def partitial_components_probability(ei):
    ei.diagnose()
    compsProbs = {}
    for d in ei.diagnoses:
        p = d.get_prob()
        for comp in d.get_diag():
            compsProbs[comp] = compsProbs.get(comp, 0) + p / len(d.get_diag())
    return sorted(compsProbs.items(), key=lambda x: x[1])

def seperator_hp(ei):
    ei.diagnose()
    probabilities = []
    optionals = ei.get_optionals_actions()
    components_probs = dict(ei.compsProbs())
    for test in optionals:
        trace = Diagnoser.ExperimentInstance.pool[test]
        trace_probs = map(lambda x: components_probs.get(x,1), filter(lambda x: x in components_probs, trace))
        if trace_probs == []:
            probabilities.append(0.0)
            continue
        probabilities.append(reduce(lambda x,y: x*y, trace_probs,1))
    if sum(probabilities) == 0:
        return optionals, [1/ len(optionals) for x in optionals]
    return optionals,[x / sum(probabilities) for x in probabilities]

