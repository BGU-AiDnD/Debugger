import os
import subprocess

import utilsConf
from utils.monitors_manager import OO_FEATURES_MARKER, monitor, OO_OLD_FEATURES_MARKER
from utils.filesystem import convert_to_long_path


def object_orient_features_error_analyze(err):
	# get all corrupted java files in err
	lines = err.split("\n")
	wantedLines = []
	i = 0
	for l in lines:
		if "symbol:   variable " in l:
			wantedLines.append(lines[i - 3])
		i = i + 1
	knownP = ["static import only from classes and interfaces",
	          "unmappable character for encoding"]
	knownP = [""]
	dontMatter = ["does not exist", "cannot find symbol"]
	wantedLines = wantedLines + [x for x in lines if ".java:" in x]
	lines = wantedLines
	for d in dontMatter:
		lines = [x for x in lines if d not in x]
	ans = []
	for p in knownP:
		ans = ans + [x.split(".java")[0] + ".java" for x in lines if p in x]
	return ans


@monitor(OO_OLD_FEATURES_MARKER)
def extract_object_oriented_features_old(configuration):
	for version in configuration.vers:
		verPath = os.path.join(configuration.versPath, utilsConf.version_to_dir_name(version))
		command = """cd /d  """ + convert_to_long_path(
			verPath) + " & for /R .\\repo %f in (*.java) do (call javadoc -doclet com.github.markusbernhardt.xmldoclet.XmlDoclet -docletpath " + convert_to_long_path(
			configuration.docletPath) + " -filename %~nxf.xml -private -d .\Jdoc2 %f >NUL 2>NUL)"
		os.system(command)


@monitor(OO_FEATURES_MARKER)
def extract_object_oriented_features(versPath, vers, docletPath):
	for x in vers:
		verPath = os.path.join(versPath, x)
		outPath = os.path.join(verPath, "Jdoc")
		outPath = os.path.join(outPath, "javadoc.xml")
		err = ""
		open(os.path.join(verPath, "JdocFunc.txt"), "wt").writelines(
			[x for x in open(os.path.join(verPath, "javaFiles.txt"), "r").readlines()])
		run_commands = ["javadoc", "-doclet", "com.github.markusbernhardt.xmldoclet.XmlDoclet",
		                "-docletpath ", docletPath, "-private", "-d", ".\Jdoc", "@JdocFunc.txt"]
		bads = []
		if not os.path.exists(outPath):
			bads = bads + object_orient_features_error_analyze(err)
			open(os.path.join(verPath, "JdocFunc.txt"), "wb").writelines(
				[x for x in open(os.path.join(verPath, "javaFiles.txt"), "r").readlines() if
				 x not in bads])
			proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
			                                 stderr=subprocess.PIPE, shell=True,
			                                 cwd=convert_to_long_path(verPath))
			(out, err) = proc.communicate()
			bads = bads + object_orient_features_error_analyze(err)
			open(os.path.join(verPath, "JdocFunc.txt"), "wb").writelines(
				[x for x in open(os.path.join(verPath, "javaFiles.txt"), "r").readlines() if
				 x not in bads])
			proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
			                                 stderr=subprocess.PIPE, shell=True,
			                                 cwd=convert_to_long_path(verPath))
			(out, err) = proc.communicate()
