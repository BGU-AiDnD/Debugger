import os
import glob
from junitparser import JUnitXml, junitparser
from junitparser.junitparser import Error, Failure
from subprocess import Popen
import sys
import shutil
import xml.etree.ElementTree
import tempfile
from contextlib import contextmanager

SURFIRE_DIR_NAME = 'surefire-reports'
OBSERVE_PATH = r"c:\temp\observe"


class Test(object):
    def __init__(self, junit_test):
        self.junit_test = junit_test
        self.classname = junit_test.classname
        self.name = junit_test.name
        self.full_name = "{classname}@{name}".format(classname=self.classname, name=self.name).lower()
        result = 'pass'
        if type(junit_test.result) is Error:
            result = 'error'
        if type(junit_test.result) is Failure:
            result = 'failure'
        self.outcome = result

    def __repr__(self):
        return "{full_name}: {outcome}".format(full_name=self.full_name, outcome=self.outcome)

    def is_passed(self):
        return self.outcome == 'pass'

    def get_observation(self):
        return 0 if self.is_passed() else 1

    def as_dict(self):
        return {'_tast_name': self.full_name, '_outcome': self.outcome}


class Trace(object):
    def __init__(self, test_name, trace):
        self.test_name = test_name
        self.trace = map(lambda t: t.lower(), trace)

    def files_trace(self):
        return list(set(map(lambda x: x.split("@")[0].lower(), self.trace)))

    def get_trace(self, trace_granularity):
        if trace_granularity == 'methods':
            return list(set(self.trace))
        elif trace_granularity == 'files':
            return self.files_trace()
        assert False


class Tracer(object):
    def __init__(self):
        self.traces = {}

    @contextmanager
    def trace(self):
        yield


class AmirTracer(Tracer):
    def __init__(self, git_path, tracer_path, copy_traces_to):
        super(AmirTracer, self).__init__()
        self.tracer_path = tracer_path
        self.git_path = git_path
        self.paths_file = tempfile.mktemp()
        self.copy_traces_to = copy_traces_to
        self.traces = {}

    @contextmanager
    def trace(self):
        self.enable_tracer()
        yield
        self.collect_traces()
        os.remove(self.paths_file)

    def enable_tracer(self):
        poms = []
        for root, _, files in os.walk(self.git_path):
            poms.extend(map(lambda name: os.path.join(root, name), filter(lambda name: name == "pom.xml", files)))
        map(self.fix_pom_file, poms)

    def fix_pom_file(self, pom_path):
        xml.etree.ElementTree.register_namespace('', "http://maven.apache.org/POM/4.0.0")
        xml.etree.ElementTree.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

        def get_children_by_name(element, name):
            return filter(lambda e: e.tag.endswith(name), element.getchildren())

        def get_or_create_child(element, name):
            child = get_children_by_name(element, name)
            if len(child) == 0:
                return xml.etree.ElementTree.SubElement(element, name)
            else:
                return child[0]

        et = xml.etree.ElementTree.parse(pom_path)
        surfire_plugins = filter(lambda plugin: filter(lambda x: x.text == "maven-surefire-plugin",
                                                       get_children_by_name(plugin, "artifactId")),
                                 filter(lambda e: e.tag.endswith('plugin'), et.getroot().iter()))
        trace_text = self.get_tracer_arg_line()
        for plugin in surfire_plugins:
            configuration = get_or_create_child(plugin, 'configuration')
            argLine = get_or_create_child(configuration, 'argLine')
            argLine.text = argLine.text + trace_text if argLine.text else trace_text
        et.write(pom_path, xml_declaration=True)

    def get_tracer_arg_line(self):
        paths = [os.path.expandvars(r'%USERPROFILE%\.m2\repository'), self.git_path]
        with open(self.paths_file, 'wb') as paths_file:
            paths_file.write("\n".join(paths))
        return ' -Xms8g -Xmx20048m  -javaagent:{0}={1} '.format(self.tracer_path, self.paths_file)

    def collect_traces(self):
        traces_files = []
        for root, dirs, _ in os.walk(os.path.abspath(os.path.join(self.git_path, "..\.."))):
            traces_files.extend(map(lambda name: glob.glob(os.path.join(root, name, "TRACE_*.txt")),
                                    filter(lambda name: name == "DebuggerTests", dirs)))
        for trace_file in reduce(list.__add__, traces_files, []):
            dst = os.path.join(self.copy_traces_to, os.path.basename(trace_file))
            if not os.path.exists(dst):
                shutil.copyfile(trace_file, dst)
            test_name = trace_file.split('\\Trace_')[1].split('_')[0].lower()
            with open(trace_file) as f:
                self.traces[test_name] = Trace(test_name,
                                               map(lambda line: line.strip().split()[2].strip(), f.readlines()))


class TestRunner(object):
    def __init__(self, git_path, tracer=None):
        self.git_path = git_path
        if tracer is None:
            tracer = Tracer()
        self.tracer = tracer
        self.observations = {}

    def run(self):
        with self.tracer.trace():
            self.run_mvn()
            pass
        self.observations = self.observe_tests()

    def run_mvn(self):
        os.system(r'mvn install -fn  -f {0}'.format(self.git_path))

    def observe_tests(self):
        outcomes = {}
        for report in self.get_surefire_files():
            try:
                for case in JUnitXml.fromfile(report):
                    test = Test(case)
                    outcomes[test.full_name] = test
            except:
                pass
        return outcomes

    def get_surefire_files(self):
        surefire_files = []
        for root, _, files in os.walk(self.git_path):
            for name in files:
                if name.endswith('.xml') and os.path.basename(root) == SURFIRE_DIR_NAME:
                    surefire_files.append(os.path.join(root, name))
        return surefire_files

    def get_tests(self):
        return set(self.tracer.traces.keys()) & set(self.observations.keys())

    def get_packages_tests(self):
        packages_tests = {}
        for test_name in self.get_tests():
            spllited = test_name.split('@')[0].split('.')
            for ind in range(len(spllited)):
                packages_tests.setdefault('.'.join(spllited[:ind]), set()).add(test_name)
        return packages_tests


def checkout_commit(commit_to_observe, git_path):
    git_commit_path = os.path.join(OBSERVE_PATH, os.path.basename(git_path), commit_to_observe)
    Popen(['git', 'clone', git_path, git_commit_path]).communicate()
    Popen(['git', 'checkout', '-f', '{0}'.format(commit_to_observe)], cwd=git_commit_path).communicate()
    return git_commit_path


if __name__ == "__main__":
    import csv

    assert len(sys.argv) == 5
    _, repo, matrix_path, prediction_path, tracer_path = sys.argv
    for x in [repo, prediction_path, tracer_path]:
        assert os.path.exists(x)
    predictions = {}
    with open(prediction_path) as f:
        lines = list(csv.reader(f))[1:]
        predictions = dict(
            map(lambda line: (line[0].replace(".java", "").replace(os.path.sep, ".").lower(), line[1]), lines))
    tr = TestRunner(repo, AmirTracer(repo, tracer_path))
    tr.run()
    from sfl_diagnoser.Diagnoser.diagnoserUtils import write_planning_file

    tests = set(tr.tracer.traces.keys()) & set(tr.observations.keys())
    components_priors = {}
    for component in set(
            reduce(list.__add__, map(lambda test_name: tr.tracer.traces[test_name].files_trace(), tests), [])):
        for prediction in predictions:
            if component in prediction:
                components_priors[component] = predictions[prediction]
    components = set(components_priors.keys())
    tests_details = map(lambda test_name: (test_name, list(set(tr.tracer.traces[test_name].files_trace()) & components),
                                           tr.observations[test_name].get_observation()),
                        tests)
    write_planning_file(matrix_path, [], filter(lambda test: len(test[1]) > 0, tests_details), priors=components_priors)
