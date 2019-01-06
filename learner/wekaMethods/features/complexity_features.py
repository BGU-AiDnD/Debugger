import os
import subprocess

import utilsConf
from utils.monitors_manager import monitor, COMPLEXITY_FEATURES_MARKER
from utils.filesystem import convert_to_short_path, convert_to_long_path
from wekaMethods.features.features_static_data.source_monitor_xml_command import \
	SOURCE_MONITOR_XML_COMMAND


def parse_source_monitor_xml(workingDir, ver, source_monitor_exe_path):
	verDir = os.path.join(convert_to_long_path(workingDir), "vers", ver)
	verREPO = os.path.join(verDir, "repo")
	verP = os.path.join(verDir, ver)
	xml = SOURCE_MONITOR_XML_COMMAND.replace("verP", verP).replace("verREPO", verREPO)
	xmlPath = os.path.join(verDir, "sourceMonitor.xml")
	with open(xmlPath, "wb") as f:
		f.write(xml)

	return [source_monitor_exe_path, "/C", xmlPath]


def execute_blame(path, repo_path, version):
	for root, dirs, files in os.walk(repo_path):
		for name in files:
			if not os.path.splitext(name)[1].endswith("java"):
				continue
			git_file_path = os.path.join(root, name).replace(repo_path + "\\", "")
			blame_file_path = os.path.abspath(os.path.join(path, 'blame', name))
			blame_commands = ['git', 'blame', '--show-stats', '--score-debug', '-p',
			                  '--line-porcelain', '-l', version, git_file_path]
			proc = utilsConf.open_subprocess(blame_commands, stdout=subprocess.PIPE,
			                                 stderr=subprocess.PIPE, shell=True,
			                                 cwd=convert_to_short_path(repo_path))
			(out, err) = proc.communicate()
			if proc.returncode != 0:
				raise RuntimeError(
					'blame subprocess failed. args: {0}. err is {1}'.format(str(blame_commands),
					                                                        err))
			with open(blame_file_path, "w") as f:
				f.writelines(out)
	run_commands = ["dir", "/b", "/s", "*.java"]
	proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
	                                 stderr=subprocess.PIPE,
	                                 shell=True, cwd=convert_to_short_path(repo_path))
	(out, err) = proc.communicate()
	with open(os.path.join(path, "javaFiles.txt"), "wb") as f:
		f.writelines(out)


@monitor(COMPLEXITY_FEATURES_MARKER)
def extract_complexity_features(configuration):
	"""Extracting the complexity features from the cloned versions code."""
	processes = []
	for version_path, version_name, git_version in zip(configuration.vers_paths,
	                                                   configuration.vers_dirs,
	                                                   configuration.vers):
		repo_path = os.path.join(version_path, "repo")
		run_commands = parse_source_monitor_xml(configuration.workingDir, version_name,
		                                        configuration.source_monitor_exe_path)
		proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
		                                 stderr=subprocess.PIPE, shell=True)
		processes.append((proc, run_commands))
		run_commands = ["java", "-jar", configuration.checkStyle68, "-c",
		                configuration.methods_names_xml_path, "javaFile", "-o",
		                "vers/checkAllMethodsData/" + version_name + ".txt", repo_path]
		proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
		                                 stderr=subprocess.PIPE, shell=True,
		                                 cwd=convert_to_long_path(
			                                 configuration.workingDir))
		processes.append((proc, run_commands))

		run_commands = ["java", "-jar", configuration.checkStyle57, "-c",
		                configuration.all_checks_xml_path, "-r", repo_path, "-f", "xml", "-o",
		                "vers/checkAll/" + version_name + ".xml"]
		proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
		                                 stderr=subprocess.PIPE, shell=True,
		                                 cwd=convert_to_long_path(
			                                 configuration.workingDir))
		processes.append((proc, run_commands))

		execute_blame(version_path, repo_path, git_version)

	for proc, run_commands in processes:
		out, err = proc.communicate()
		if proc.returncode != 0:
			RuntimeWarning(
				'subprocess execution failed. args are {0}. err is {1}'.format(
					str(run_commands),
					err))
