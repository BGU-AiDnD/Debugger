"""Module to handle common actions on the filesystem."""
import os
import shutil

USE_LONG_PATHS = True
LONG_PATH_MAGIC = u"\\\\?\\"


def create_directory_if_not_exists(dir):
	if not os.path.isdir(dir):
		os.mkdir(dir)


def convert_to_long_path(path):
	drive_letter, other_path = os.path.splitdrive(path)
	if USE_LONG_PATHS:
		return os.path.join(LONG_PATH_MAGIC + drive_letter, other_path)
	else:
		return path


def convert_to_short_path(path):
	return path.replace(LONG_PATH_MAGIC, "")


def copy(src, dst):
	if os.path.isfile(src):
		if os.path.exists(dst):
			os.remove(dst)
		shutil.copyfile(src, dst)

	else:   # src is a directory
		if os.path.exists(dst):
			shutil.rmtree(dst)
		shutil.copytree(src, dst)