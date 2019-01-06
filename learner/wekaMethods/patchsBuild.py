import glob
import os
import re
import shutil
import subprocess

import utilsConf
# git format-patch --root origin
from utils.monitors_manager import monitor, PATCHS_FEATURES_MARKER
from utils.filesystem import convert_to_short_path, create_directory_if_not_exists


def checkStyleCreateDict(checkOut, changesDict):
	methods = {}
	lines = []
	with open(checkOut, "r") as f:
		lines = f.readlines()[1:-3]
	for line in filter(lambda line: "@" in line and len(line.split()) == 2, lines):
		file, data = line.split(" ")
		file = file.split(".java")[0] + ".java"
		fileNameSplited = file.split(os.path.sep)
		fileName = fileNameSplited[-1].replace("_", os.path.sep)
		commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
		if not (fileName, commitID) in changesDict.keys():
			continue
		key = ""
		inds = []
		deleted, insertions, is_new_file, is_deleted_file, is_renamed_file = changesDict[
			(fileName, commitID)]
		if "before" in file:
			key = "deletions"
			inds = deleted
		if "after" in file:
			key = "insertions"
			inds = insertions
		name, begin, end = data.split("@")
		both = set(map(str, inds)) & set(map(str, range(int(begin) - 1, int(end))))
		keyChange = len(both)
		if keyChange == 0:
			continue
		methodDir = fileName + "$" + name
		tup = (methodDir, commitID)
		if not tup in methods:
			methods[tup] = {}
		methods[tup][key] = keyChange
		methods[tup].setdefault("methodName", name)
		methods[tup].setdefault("fileName", fileName)
		methods[tup].setdefault("commitID", commitID)
		methods[tup].setdefault("is_new_file", is_new_file)
		methods[tup].setdefault("is_deleted_file", is_deleted_file)
		methods[tup].setdefault("is_renamed_file", is_renamed_file)
	return methods


def readChangesFile(change):
	dict = {}
	rows = []
	with open(change, "r") as f:
		for line in f:
			fileName, commitSha, dels, Ins, is_new_file, is_deleted_file, is_renamed_file = line.strip().split(
				"@")
			fileName = fileName.replace("_", os.path.sep)
			dict[(fileName, commitSha)] = map(eval, [dels, Ins, is_new_file, is_deleted_file,
			                                         is_renamed_file])
			rows.append(map(str, [fileName, commitSha, len(dels), len(Ins), len(dels) + len(Ins),
			                      is_new_file, is_deleted_file, is_renamed_file]))
	return dict, rows


def analyzeCheckStyle(checkOut, changeFile):
	changesDict, filesRows = readChangesFile(changeFile)
	methods = checkStyleCreateDict(checkOut, changesDict)
	all_methods = []
	for tup in methods:
		methodDir = tup[0]
		dels = methods[tup].setdefault("deletions", 0)
		ins = methods[tup].setdefault("insertions", 0)
		fileName = methods[tup].setdefault("fileName", "")
		methodName = methods[tup].setdefault("methodName", "")
		commitID = methods[tup].setdefault("commitID", "")
		is_new_file = methods[tup].setdefault("is_new_file", 0)
		is_deleted_file = methods[tup].setdefault("is_deleted_file", 0)
		is_renamed_file = methods[tup].setdefault("is_renamed_file", 0)
		all_methods.append(map(str,
		                       [commitID, methodDir, fileName, methodName, dels, ins, dels + ins,
		                        is_new_file, is_deleted_file, is_renamed_file]))
	return all_methods, filesRows


class PatchesBuilder(object):
	"""Create patches needed to run the algorithm."""

	# Git notations for diff changes
	REMOVED = '---'
	ADDED = '+++'

	DEV_NULL = '/dev/null'

	# Prepare each commit with its patch in one file per commit,
	# formatted to resemble UNIX mailbox format.
	GIT_PATCH_COMMAND = "git format-patch --root -o ..\patch --function-context --unified=900000"

	def __init__(self, configuration, logger):
		self.configuration = configuration
		self.logger = logger
		self.commits_files_dir_path = None
		self.patches_dir_path = None

	def _create_patches_work_tree(self):
		self.logger.info("Creating the patches directory tree")
		self.patches_dir_path = os.path.join(self.configuration.workingDir, "patch")
		self.commits_files_dir_path = os.path.join(self.configuration.workingDir,
		                                      "commitsFiles")
		create_directory_if_not_exists(self.patches_dir_path)
		create_directory_if_not_exists(self.commits_files_dir_path)

	def run_checkstyle(self):
		"""Runs the checkstyle tool to check for warnings in the java code. """
		self.logger.info("Running the checkstyle algorithm on the repositories")
		run_commands = ["java", "-jar", self.configuration.checkStyle68, "-c",
		                self.configuration.methods_names_xml_path, "javaFile", "-o",
		                self.configuration.MethodsParsed,
		                self.commits_files_dir_path]
		utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		                          shell=True).communicate()
	@staticmethod
	def fix_enum(line):
		if "enum =" in line:
			line = line.replace("enum =", "enumAmir =")
		if "enum=" in line:
			line = line.replace("enum=", "enumAmir=")
		if "enum," in line:
			line = line.replace("enum,", "enumAmir,")
		if "enum." in line:
			line = line.replace("enum.", "enumAmir.")
		if "enum;" in line:
			line = line.replace("enum;", "enumAmir;")
		if "enum)" in line:
			line = line.replace("enum)", "enumAmir)")
		return line

	@staticmethod
	def fix_assert(l):
		if "assert " in l:
			l = l.replace("assert ", "assertAmir ")
			if ":" in l:
				l = l.replace(":", ";//")
		if "assert(" in l:
			l = l.replace("assert(", "assertAmir(")
			if ":" in l:
				l = l.replace(":", ";//")
		return l

	def handle_diffs(self, diff_lines, output_path, commit_id, change_file):
		diff_files = diff_lines[0].split()
		if len(diff_files) < 3:
			raise ValueError("Somehow there are not enough lines in the diff file.")

		removed_data_lines = filter(lambda x: x.startswith(self.REMOVED), diff_lines)
		added_data_lines = filter(lambda x: x.startswith(self.ADDED), diff_lines)
		if len(removed_data_lines) != 1 or len(added_data_lines) != 1:
			return

		removed_file_name = removed_data_lines[0].split()[1]
		added_file_name = added_data_lines[0].split()[1]
		added_file_name_source_path = added_file_name[2:]
		deleted_file_name_source_path = removed_file_name[2:]

		is_new_file = removed_file_name == self.DEV_NULL
		is_deleted_file = added_file_name == self.DEV_NULL
		is_renamed_file = not is_deleted_file and not is_new_file and \
		                          added_file_name_source_path != deleted_file_name_source_path

		is_removed_file = is_renamed_file or is_deleted_file
		file_names = [(added_file_name, 0)] + ([(removed_file_name, 1)] if is_removed_file else [])

		for name, removed in file_names:
			fileName = os.path.normpath(name[2:]).replace(os.path.sep, "_")
			if not fileName.endswith('.java'):
				continue
			start_line = filter(lambda line: line[1].startswith('+++'), enumerate(diff_lines))
			if len(start_line) != 1:
				return  # no file
			diff_lines = diff_lines[start_line[0][0] + 1:]
			befLines = []
			afterLines = []
			deletedInds = []
			addedInds = []
			delind = 0
			addind = 0
			for l in diff_lines:
				if "\ No newline at end of file" in l:
					continue
				if "1.9.4.msysgit.2" in l:
					continue
				if "- \n" == l:
					continue
				if "-- \n" == l:
					continue
				l = self.fix_enum(l)
				l = self.fix_assert(l)
				replaced = re.sub(r'@@(-|\+|,| |[0-9])*@@', '', l)
				if replaced.startswith("*"):
					replaced = "\\" + replaced
				if replaced.startswith("+"):
					afterLines.append(replaced[1:])
					addedInds.append(addind)
					addind = addind + 1
				elif replaced.startswith("-"):
					befLines.append(replaced[1:])
					deletedInds.append(delind)
					delind = delind + 1
				else:
					afterLines.append(replaced)
					befLines.append(replaced)
					delind = delind + 1
					addind = addind + 1

			with open(os.path.join(output_path, "before", fileName), "wb") as bef:
				bef.writelines(befLines)
			with open(os.path.join(output_path, "after", fileName), "wb") as after:
				after.writelines(afterLines)
			with open(os.path.join(output_path, fileName + "_deletsIns.txt"), "wb") as f:
				f.writelines('\n'.join(map(str,
				                           ["deleted", deletedInds, "added", addedInds, is_new_file,
				                            removed, is_renamed_file])))
			change_file.write("@".join(map(str,
			                               [fileName, commit_id, deletedInds, addedInds, is_new_file,
			                           removed,
			                           is_renamed_file])) + "\n")

	@staticmethod
	def _create_commit_patch_dirs(output_dir, commit_id):
		o = output_dir + "\\" + commit_id
		if not (os.path.isdir(o)):
			os.mkdir(o)
		o = output_dir + "\\" + commit_id + "\\before"
		if not (os.path.isdir(o)):
			os.mkdir(o)
		o = output_dir + "\\" + commit_id + "\\after"
		if not (os.path.isdir(o)):
			os.mkdir(o)
		o = output_dir + "\\" + commit_id + "\\parser"
		if not (os.path.isdir(o)):
			os.mkdir(o)

	def _get_diffs(self, lines):
		# filters only the lines that start with 'diff --git'
		filtered_lines = \
			filter(lambda line_data: line_data[1].startswith("diff --git"), enumerate(lines))
		# Taking the line index so that later we would filter the content of th DIFF
		diffs_indexes = map(lambda x: x[0], filtered_lines) + [len(lines)]  # Add the last index
		diff_lines = map(lambda diff: lines[diff[0]: diff[1]],
		                 zip(diffs_indexes, diffs_indexes[1:]))
		return diff_lines

	def parse_patch_file(self, patch_file, change_file):
		"""Parse the patch file and outputs the diffs between the versions."""
		self.logger.info("Parsing the patch file - %s", patch_file)
		with open(patch_file, 'r') as f:
			lines = f.readlines()[:-3]

		if len(lines) == 0:
			return

		# patch file line-0 looks like this:
		# From e0880e263e4bf8662ba3848405200473a25dfc9f Mon Sep 17 00:00:00 2001
		commit_id = str(lines[0].split()[1])  # line 0 word 1
		self._create_commit_patch_dirs(self.commits_files_dir_path, commit_id)

		diff_lines = self._get_diffs(lines)
		shutil.copyfile(patch_file, os.path.join(self.commits_files_dir_path, commit_id,
		                                         os.path.basename(patch_file)))
		for diff in diff_lines:
			if len(diff) == 0:
				self.logger.error("Parsing error, somehow supposed to have diffs but there are "
				                  "none.")
				raise ValueError

			self.handle_diffs(diff, os.path.join(self.commits_files_dir_path, commit_id), commit_id,
			                  change_file)

	def build_patches(self):
		""""""
		# Opens the files that contains the insertions and deletions from the original file
		self.logger.info("Building the patches to run CheckStyle on them.")
		with open(self.configuration.changeFile, "wb") as change_file:
			for patch_path in glob.iglob(os.path.join(self.patches_dir_path, "*.patch")):
				self.parse_patch_file(patch_path, change_file)

	@monitor(PATCHS_FEATURES_MARKER)
	def labeling(self):
		""""""
		self.logger.info("running the labeling part of the algorithm")
		self._create_patches_work_tree()
		run_commands = self.GIT_PATCH_COMMAND.split()
		proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE,
		                                 stderr=subprocess.PIPE, shell=True,
		                                 cwd=convert_to_short_path(self.configuration.LocalGitPath))
		proc.communicate()
		self.build_patches()
		self.run_checkstyle()
