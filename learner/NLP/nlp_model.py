import gensim, logging
import pandas as pd
import numpy as np

def get_files(data):
    results = []
    for line in data.FilesArr:
        if len(line) > 1:
            valid_line = []
            for item in line:
                if item[len(item) - 4:] == 'java':
                    valid_line.append(item)
            if len(np.unique(valid_line)) > 1:
                results.append(valid_line)
    return results

def get_item_list(flag):
    bug_data = data[data.Bug > 0].groupby(['Bug'])['Files'].apply(lambda x: "%s" % ';'.join(x)).reset_index()
    bug_data['FilesArr'] = [bug_data.Files[i].split(';') for i in range(len(bug_data))]
    not_bug_list = get_files(data[data.Bug == 0])
    bug_list = get_files(bug_data)
    if flag == 1:
        return bug_list
    return (not_bug_list + bug_list)


def find_simialrity(a, b, model):
    return model.similarity(a, b)

def build_model(file_name, iteration = 10, window = 1000, min_count = 3, size = 40, workers = 16):
    global data
    data = pd.read_csv(file_name, usecols=[1, 2], names=['Bug', 'Files'])
    data = data[~data.Files.isnull()]
    data['FilesArr'] = data['Files'].apply(lambda x: np.array(x.split(';')))
    only_bug = 0

    # dimensions
      # size of window context
      # minimun instances of the same item
      # parallelism
    hs = 1  # hierarchical softmax
    negative = 15  # number of negative sampling per postive sample
    # sample = 1e-2 #sample the data per frequency
    return gensim.models.word2vec.Word2Vec(get_item_list(only_bug), iter=iteration, size=size, window=window,
                                            min_count=min_count,
                                            workers=workers, hs=hs, negative=negative)


if __name__ == "__main__":
    file_name = r"C:\Temp\Ant_for_NLP.csv"
    build_model(file_name)
