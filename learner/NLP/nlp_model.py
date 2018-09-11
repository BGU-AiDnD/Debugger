import logging

import gensim
import pandas as pd
import numpy as np


class NLPModel(object):
    """Manage the building of the NLP model required for the data parsing."""

    DEFAULT_SIZE = 40
    DEFAULT_MIN_COUNT = 3
    NEGATIVE_SAMPLING = 15  # number of negative sampling per postive sample
    HIERARCHAL_SOFTMAX = 1
    DEFAULT_NUM_WORKERS = 16
    DEFAULT_ITERATION_NUM = 10
    DEFAULT_WINDOW_SIZE = 1000

    def __init__(self, file_name, num_iterations=DEFAULT_ITERATION_NUM, min_count=DEFAULT_MIN_COUNT,
                 window_size=DEFAULT_WINDOW_SIZE, size=DEFAULT_SIZE, workers=DEFAULT_NUM_WORKERS):
        self.file_name = file_name
        self.num_iterations = num_iterations
        self.window_size = window_size  # size of window context
        self.size = size  # dimensions
        self.min_count = min_count  # minimun instances of the same item
        self.num_workers = workers  # parallelism
        self.data = None

    @staticmethod
    def get_files(partial_data):
        """"""
        results = []
        for line in partial_data.files_array:
            if len(line) <= 1:
                continue

            valid_lines = [item for item in line if item[len(item) - 4:] == 'java']
            if len(np.unique(valid_lines)) > 1:
                results.append(valid_lines)

        return results

    def get_item_list(self, only_bugs=True):
        """"""
        bug_data = self.data[self.data.Bug > 0].groupby(['Bug'])['Files'].apply(
            lambda x: "%s" % ';'.join(x)).reset_index()

        bug_data['files_array'] = [bug_data.Files[i].split(';') for i in range(len(bug_data))]

        not_bug_list = self.get_files(self.data[self.data.Bug == 0])
        bug_list = self.get_files(bug_data)

        if only_bugs:
            return bug_list

        return not_bug_list + bug_list

    @staticmethod
    def _create_np_array(data_frame: str) -> np.array:
        """Create a NumPy array out of the data frame given.

        Args:
            data_frame (str): the data of the samples as a table.

        Returns:
            array. The array containing the relevant data.
        """
        return np.array(data_frame.split(';'))

    @property
    def model(self) -> gensim.models.word2vec.Word2Vec:
        """Build the NLP model based on the class's params.

        Returns:
            gensim.models.word2vec.Word2Vec. ???
        """
        self.data = pd.read_csv(self.file_name, usecols=[1, 2], names=['Bug', 'Files'])

        self.data = self.data[~self.data.Files.isnull()]
        self.data['files_array'] = self.data['Files'].apply(self._create_np_array)

        return gensim.models.word2vec.Word2Vec(self.get_item_list(only_bugs=False),
                                               iter=self.num_iterations,
                                               size=self.size,
                                               window=self.window_size,
                                               min_count=self.min_count,
                                               workers=self.num_workers,
                                               hs=self.HIERARCHAL_SOFTMAX,
                                               negative=self.NEGATIVE_SAMPLING)
