import csv
import json
import os

import wekaMethods.wekaAccuracy
from experiments import ExperimentGenerator
from utils.monitors_manager import monitor, EXECUTE_TESTS
from run_mvn import TestRunner, AmirTracer
from sfl_diagnoser.Diagnoser.diagnoserUtils import write_planning_file, readPlanningFile
from utils.filesystem import convert_to_long_path


class DiagnosisRunner(object):
	"""Handle all the Diagnosis related actions."""

	def __init__(self, logger, configuration):
		self.logger = logger
		self.configuration = configuration

	@staticmethod
	def build_weka_model(weka, training, testing, namesCsv, outCsv, name, wekaJar):
		algorithm = "weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
		os.system("cd /d  " + convert_to_long_path(
			weka) + " & java -Xmx2024m  -cp " + convert_to_long_path(
			wekaJar) + " weka.Run " + algorithm + " -x 10 -d .\\model.model -t " + training + " > training" + name + ".txt")
		algorithm = "weka.classifiers.trees.RandomForest "
		os.system("cd /d  " + convert_to_long_path(
			weka) + " & java -Xmx2024m  -cp " + convert_to_long_path(
			wekaJar) + " weka.Run " + algorithm + " -l .\\model.model -T " + testing + " -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing" + name + ".csv\" ")
		os.system("cd /d  " + convert_to_long_path(
			weka) + " & java -Xmx2024m  -cp " + convert_to_long_path(
			wekaJar) + " weka.Run " + algorithm + " -l .\\model.model -T " + testing + " > testing" + name + ".txt ")
		wekaCsv = os.path.join(convert_to_long_path(weka), "testing" + name + ".csv")
		wekaMethods.wekaAccuracy.priorsCreation(namesCsv, wekaCsv, outCsv, "")

	@staticmethod
	def weka_csv_to_readable_csv(weka_csv, prediction_csv):
		out_lines = [["component_name", "fault_probability"]]
		first = 0
		with open(weka_csv, "r") as weka_csv_file:
			reader = csv.reader(weka_csv_file)
			for line in reader:
				if first == 0:
					first = 1
					continue
				component_name = line[0]
				probability = line[5].replace("*", "")
				out_lines.append([component_name, probability])

		with open(prediction_csv, "wb") as weka_csv_file:
			writer = csv.writer(weka_csv_file)
			writer.writerows(out_lines)

	@staticmethod
	def add_to_packages(packages, path, probability, threshold=0.2):
		""""""
		if float(probability) < threshold:
			return

		d = packages
		while len(path) != 1:
			name = path.pop()
			d.setdefault('_sub_packages', [])
			package = {'_name': name}
			d['_sub_packages'].append(package)
			d = package
		d.setdefault('_files', {})
		d['_files'][path[0]] = {'_probability': probability}

	def calc_all_probabilities(self, package, reduce_function):
		""""""
		if '_probability' not in package:
			sub_probabilities = [0.0]
			if '_files' in package:
				files_probabilities = map(lambda x: package['_files'][x]['_probability'],
				                          package['_files'].keys())
				sub_probabilities.extend(files_probabilities)
			if '_sub_packages' in package:
				sub_packages_probabilities = map(
					lambda x: self.calc_all_probabilities(x, reduce_function),
					package['_sub_packages'])
				sub_probabilities.extend(sub_packages_probabilities)
			package['_probability'] = reduce_function(sub_probabilities)
		return package['_probability']

	def save_json_watchers(self, precidtion_csv):
		""""""
		packges = {'_name': '_root', '_sub_packages': []}
		with open(precidtion_csv) as predictions_csv_file:
			lines = list(csv.reader(predictions_csv_file))[1:]

		map(lambda x: self.add_to_packages(packges, list(reversed(x[0].split(os.path.sep))),
		                                   float(x[1])),
		    lines)
		self.calc_all_probabilities(packges, max)
		with open(precidtion_csv.replace("csv", "json"), "wb") as predictions_csv_file:
			predictions_csv_file.write(json.dumps([packges]))

	@staticmethod
	def load_prediction_file(prediction_path):
		""""""
		with open(prediction_path) as prediction_file:
			lines = list(csv.reader(prediction_file))[1:]
			predictions = dict(map(lambda line: (
				line[0].replace(".java", "").replace(os.path.sep, ".").replace("").lower(),
				line[1]), lines))

		return predictions

	def get_components_probabilities(self, bugged_type, granularity, test_runner, tests):
		""""""
		with open(os.path.join(self.configuration.web_prediction_results,
		                       self.configuration.prediction_files[granularity][
			                       bugged_type])) as f:
			lines = list(csv.reader(f))[1:]
			predictions = dict(
				map(lambda line: (
					line[0].replace(".java", "").replace(os.path.sep, ".").lower().replace('$',
					                                                                       '@'),
					line[1]), lines))
		components_priors = {}
		for component in set(
				reduce(list.__add__, map(
					lambda test_name: test_runner.tracer.traces[test_name].get_trace(granularity),
					tests), [])):
			for prediction in predictions:
				if prediction.endswith(component):
					components_priors[component] = max(float(predictions[prediction]), 0.01)

		return components_priors

	def create_experiment(self, test_runner, num_instances=50, tests_per_instance=50,
	                      bug_passing_probability=0.05):
		""""""
		self.logger.info("Creating the experiments for the diagnoser")
		results_path = os.path.join(self.configuration.experiments,
		                            "{GRANULARITY}_{BUGGED_TYPE}")
		for granularity in self.configuration.prediction_files:
			for bugged_type in self.configuration.prediction_files[granularity]:
				eg = ExperimentGenerator(test_runner, granularity, bugged_type, num_instances,
				                         tests_per_instance, bug_passing_probability)
				results = eg.create_instances()
				with open(results_path.format(GRANULARITY=granularity, BUGGED_TYPE=bugged_type),
				          'wb') as f:
					f.write(json.dumps(results))

	@monitor(EXECUTE_TESTS)
	def execute_tests(self):
		web_prediction_results = self.configuration.web_prediction_results
		matrix_path = os.path.join(web_prediction_results, "matrix_{0}_{1}.matrix")
		outcomes_path = os.path.join(web_prediction_results, "outcomes.json")
		diagnoses_path = os.path.join(web_prediction_results, "diagnosis_{0}_{1}.matrix")
		diagnoses_json_path = os.path.join(web_prediction_results, "diagnosis_{0}_{1}.json")
		tested_repo = convert_to_long_path(
			os.path.join(self.configuration.workingDir, "testedVer", "repo"))
		test_runner = TestRunner(tested_repo,
		                         AmirTracer(tested_repo, self.configuration.amir_tracer,
		                                    self.configuration.DebuggerTests))
		test_runner.run()
		tests = test_runner.get_tests()
		json_observations = map(lambda test: test_runner.observations[test].as_dict(), tests)
		with open(outcomes_path, "wb") as f:
			f.write(json.dumps(json_observations))
		for granularity in self.configuration.prediction_files:
			for bugged_type in self.configuration.prediction_files[granularity]:
				components_priors = self.get_components_probabilities(bugged_type, granularity,
				                                                      test_runner,
				                                                      tests)
				tests_details = map(
					lambda test_name: (test_name, list(
						set(test_runner.tracer.traces[test_name].get_trace(granularity)) & set(
							components_priors.keys())),
					                   test_runner.observations[test_name].get_observation()),
					tests)
				matrix = matrix_path.format(granularity, bugged_type)
				write_planning_file(matrix, [],
				                    filter(lambda test: len(test[1]) > 0, tests_details),
				                    priors=components_priors)
				inst = readPlanningFile(matrix)
				inst.diagnose()
				named_diagnoses = sorted(inst.get_named_diagnoses(), key=lambda d: d.probability,
				                         reverse=True)
				with open(diagnoses_path.format(granularity, bugged_type), "wb") as diagnosis_file:
					diagnosis_file.writelines("\n".join(map(lambda d: repr(d), named_diagnoses)))
				with open(diagnoses_json_path.format(granularity, bugged_type),
				          "wb") as diagnosis_json:
					diagnosis_json.writelines(json.dumps(
						map(lambda d: dict([('_name', d[0])] + d[1].as_dict().items()),
						    enumerate(named_diagnoses))))
		return test_runner
