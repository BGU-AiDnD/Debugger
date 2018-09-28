import os
import utilsConf
import Bug
import csv
import random
import numbers
from sfl_diagnoser.Diagnoser.diagnoserUtils import write_planning_file, readPlanningFile
from sfl_diagnoser.Diagnoser.Diagnosis_Results import Diagnosis_Results


class AvgResults(object):
    def __init__(self):
        self.count = 0.0
        self.results = {'avg': {}}

    def update(self, other_results):
        self.results[self.count] = {}
        for key in other_results.metrics:
            if isinstance(other_results.metrics[key], numbers.Number):
                self.results[self.count][key] = other_results.metrics[key]
                self.results['avg'][key] = ((self.results['avg'].get(key, 0) * self.count) +
                                            other_results.metrics[key]) / (self.count + 1)
        self.count += 1


class ExperimentGenerator(object):
    def __init__(self, test_runner, granularity, bugged_type, num_instances=50, tests_per_instance=50,
                 bug_passing_probability=0.1):
        self.test_runner = test_runner
        self.granularity = granularity
        self.bugged_type = bugged_type
        self.num_instances = num_instances
        self.tests_per_instance = tests_per_instance
        self.bug_passing_probability = bug_passing_probability
        self.components_priors = ExperimentGenerator.get_components_probabilities(bugged_type, granularity, test_runner,
                                                                                  test_runner.get_tests())
        self.bugs = filter(lambda bug: len(bug.get_buggy_components(self.granularity, self.bugged_type)) > 0,
                           Bug.get_bugs_from_db(os.path.join(utilsConf.get_configuration().db_dir,
                                                             utilsConf.get_configuration().vers_dirs[-2]) + ".db",
                                                utilsConf.get_configuration().dates[-2],
                                                utilsConf.get_configuration().dates[-1]))
        assert len(self.bugs) > 0

    def sample_observation(self, trace, bugs):
        return 0 if random.random() < (self.bug_passing_probability ** len(set(trace) & set(bugs))) else 1

    def create_instances(self):
        MATRIX_PATH = os.path.join(utilsConf.get_configuration().experiments,
                                   "{ITERATION}_{BUG_ID}_{GRANULARITY}_{BUGGED_TYPE}.matrix")
        DESCRIPTION = 'sample bug id {BUG_ID} with bug_passing_probability = {PROB} with garnularity of {GRANULARITY} and bugged type {BUGGED_TYPE}'
        i = 0.0
        results = AvgResults()
        while i < self.num_instances:
            bug = random.choice(self.bugs)
            buggy_components = set()
            for component in set(self.components_priors.keys()):
                for buggy in bug.get_buggy_components(self.granularity, self.bugged_type):
                    if component in buggy:
                        buggy_components.add(component)
            if len(buggy_components) == 0:
                continue
            tests = reduce(set.__or__,
                           map(lambda x: self.test_runner.get_packages_tests().get(
                               '.'.join(x[:random.randint(0, len(x))]), set()),
                               map(lambda file_name: file_name.replace('.java', '').split('.'), buggy_components)),
                           set())
            if len(tests) < self.tests_per_instance:
                continue
            relevant_tests = random.sample(tests, self.tests_per_instance)
            tests_details = []
            for test_name in relevant_tests:
                trace = list(set(self.test_runner.tracer.traces[test_name].get_trace(self.granularity)) & set(
                    self.components_priors.keys()))
                tests_details.append((test_name, trace, self.sample_observation(trace, buggy_components)))
            if sum(map(lambda x: x[2], tests_details)) == 0:
                continue
            matrix = MATRIX_PATH.format(ITERATION=i, BUG_ID=bug.bug_id, GRANULARITY=self.granularity,
                                        BUGGED_TYPE=self.bugged_type)
            write_planning_file(matrix, list(buggy_components),
                                filter(lambda test: len(test[1]) > 0, tests_details),
                                priors=self.components_priors,
                                description=DESCRIPTION.format(BUG_ID=bug.bug_id, PROB=self.bug_passing_probability,
                                                               GRANULARITY=self.granularity,
                                                               BUGGED_TYPE=self.bugged_type))
            inst = readPlanningFile(matrix)
            inst.diagnose()
            res = Diagnosis_Results(inst.diagnoses, inst.initial_tests, inst.error)
            results.update(res)
            print "created instance num {ITERATION} with bugid {BUG_ID} for granularity {GRANULARITY} and type {BUGGED_TYPE}". \
                format(ITERATION=i, BUG_ID=bug.bug_id, GRANULARITY=self.granularity, BUGGED_TYPE=self.bugged_type)
            i += 1
        return results.results

    @staticmethod
    def get_components_probabilities(bugged_type, granularity, test_runner, tests):
        predictions = {}
        with open(os.path.join(utilsConf.get_configuration().web_prediction_results,
                               utilsConf.get_configuration().prediction_files[granularity][bugged_type])) as f:
            lines = list(csv.reader(f))[1:]
            predictions = dict(
                map(lambda line: (
                    line[0].replace(".java", "").replace(os.path.sep, ".").lower().replace('$', '@'), line[1]), lines))
        components_priors = {}
        components = set(reduce(list.__add__,
                                map(lambda test_name: test_runner.tracer.traces[test_name].get_trace(granularity),
                                    tests), []))
        sorted_list = sorted(map(lambda s: s[::-1], list(components) + predictions.keys()))
        for component in components:
            reversed_component = component[::-1]
            index = sorted_list.index(reversed_component) + 1
            if index < len(sorted_list):
                if sorted_list[index].startswith(reversed_component):
                    components_priors[component] = max(float(predictions[sorted_list[index][::-1]]), 0.01)
        return components_priors
