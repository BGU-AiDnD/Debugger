import csv
import sys, os
import numpy.matlib
import numpy as np
from numpy.linalg import norm

def extract_vectors(dir):
    vectors = {}
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = [row for row in reader]
        dic = dict(zip(rows[0], rows[1]))
        del dic['name']
        vectors[file[13:-4]] = {key: float(val) for key, val in dic.items()}
    return vectors


def get_min_max(vectors, property):
    min_val = min(vector[property] for vector in vectors.values())
    max_val = max(vector[property] for vector in vectors.values())
    return min_val, max_val


def get_properties(vectors):
    for values in vectors.values():
        return values.keys()


def normalize(vectors, weights):
    return {key: {prop: weights[prop](val) for prop, val in vec.items()} for key, vec in vectors.items()}


def weight(min, max):
    if min == max:
        return lambda x : 1.0
    return lambda x : (x - min) / (max - min)


def project(vectors):
    selected_props = ['halsteadCumulativeLength', 'maxcc', 'numberOfStatements']
    projected = dict()
    for key, vec in vectors.items():
        projected[key] = {prop: val for prop, val in vec.items() if prop in selected_props}
    return projected


def cosine(vec1, vec2):
    vec1 = list(vec1.values())
    vec2 = list(vec2.values())
    return np.dot(vec1, vec2)/(norm(vec1)*norm(vec2))


def similarity(vectors):
    return {name: {name2: cosine(vec, vec2) for name2, vec2 in vectors.items()} for name, vec in vectors.items()}


def export_csv(dir, sim, files):
    with open(os.path.join(dir, 'similarity.csv'), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        row = [''] + list(files)
        writer.writerow(row)
        for prop in files:
            x = [prop]
            for p in files:
                x.append(sim[prop][p])
            writer.writerow(x)


if __name__ == '__main__':
    #dir = sys.argv[1]
    dir = r'D:\Debbuger\PROMISE\System'
    vectors = extract_vectors(dir)
    to_project = len(sys.argv) > 2 and sys.argv[2] == '-p'
    if to_project:
        vectors = project(vectors)
    properties = get_properties(vectors)
    minmax = {property: get_min_max(vectors, property) for property in properties}
    weights = {property: weight(*minmax[property]) for property in properties}
    normal = normalize(vectors, weights)
    sim = similarity(normal)
    print('vectors: {}'.format(vectors))
    # print('projected: {}'.format(projected))
    print('minmax: {}'.format(minmax))
    # print('weights: {}'.format(weights))
    print('normals: {}'.format(normal))
    print('similarity: {}'.format(sim))
    export_csv(dir, sim, vectors.keys())
