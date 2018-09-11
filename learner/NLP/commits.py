import re
import sys
import git
import csv
import logging


class Commit(object):
    """Class representation of a single commit."""

    def __init__(self, git_commit, bug_id):
        self._git_commit = git_commit
        self._bug_id = bug_id
        self._commit_id = self._git_commit.hexsha
        self._files = self._git_commit.stats.files.keys()

    def to_list(self):
        """Create a list representation on the commit data."""
        return [self._commit_id, str(self._bug_id), ";".join(self._files)]


class CommitsHandler(object):
    """Handles all the actions related to the parsing of commits."""

    REDUNDANT_CHARACTERS_REGEX = r"[:|#|-|_]"

    def __init__(self, output_path, git_file_path, bugs_file_path):
        self.output_path = output_path
        self.git_file_path = git_file_path
        self.bugs_file_path = bugs_file_path

    @staticmethod
    def _remove_redundant_characters(match_obj):
        """Remove redundant characters from the string.

        Args:
            match_obj (re.MatchObject): the object to test.
        """
        if match_obj.group(0) == "#" or match_obj.group(0) == ":":
            return ""
        if match_obj.group(0) == "_" or match_obj.group(0) == "-":
            return " "

        return match_obj

    def get_bug_num_from_commit_text(self, commit_text, bugs_ids):
        """Get the bug number from the commit text after running regex extraction.

        Args:
            commit_text (str): the commit unprocessed.
            bugs_ids (list): list of IDs of bugs.

        Returns:
            str. The string representation of the bug id.
        """
        result = re.sub(self.REDUNDANT_CHARACTERS_REGEX, self._remove_redundant_characters,
                        commit_text.lower())

        for word in result:
            if word.isdigit():
                if word in bugs_ids:
                    return word

        return "0"  # Invalid bug number - no bugs in file?

    def parse_bugs_file(self, bugs_file):
        """Parse the bugs file and retrieve the relevant data.

        Args:
            bugs_file (str): the bugs file path to open and fetch the data from.

        Note:
            The input file path should lead to a CSV file only.

        Returns:
            list. The IDs of the bugs found in the csv input file.
        """
        bugs_ids = []
        reader = csv.reader(open(bugs_file, "rb"))
        for index, row in enumerate(reader, start=1):
            if index == 1:
                continue

            bugs_ids.append(row[0])

        return bugs_ids

    def extract_clean_commit_message(self, commit_message):
        """Extract only the real commit message out of the message that contains the issue key.

        Args:
            commit_message (str): the commit message as displayed in the source control tool.

        Returns:
            str. The clean commit message without the issue key addition.
        """
        if "git-svn-id" in commit_message:
            return commit_message.split("git-svn-id")[0]

        return commit_message

    def match_commit_and_bugs(self):
        """Match the commit text to the bug ID.

        Returns:
            list. All the matched commits and bug IDs.
        """
        repo = git.Repo(self.git_file_path)
        bugs_ids = self.parse_bugs_file(self.bugs_file_path)

        commits = []
        for git_commit in repo.iter_commits():
            commit_text = self.extract_clean_commit_message(git_commit.message)
            bug_index = self.get_bug_num_from_commit_text(commit_text, bugs_ids)
            logging.info("Parsing the commit: %s\n with the bug index %s.", commit_text, bug_index)
            commits.append(Commit(git_commit, bug_index))

        return commits

    def write_data_to_csv(self):
        """Write the output CSV file from the parsed data."""
        logging.info("Starting to parse the data of the bug file and the commit file.")
        commits = self.match_commit_and_bugs()

        with open(self.output_path, "wb") as output_file:
            writer = csv.writer(output_file)
            writer.writerows([commit.to_list() for commit in commits])


if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)
    handler = CommitsHandler(r"C:\Temp\NLP.csv", r"C:\Users\User\Downloads\orientdb",
                             r"C:\Users\User\AppData\Local\Temp\tmpwbfvow.csv")
    handler.write_data_to_csv()
