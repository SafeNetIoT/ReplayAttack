from itertools import combinations

import numpy as np
from nltk import word_tokenize
from scipy.spatial import distance
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.cluster import AgglomerativeClustering


def tokenizeText(sample):
    return list(set(word_tokenize(sample)))


def jaccard_similarity(document, document1):
    intersection = set(document).intersection(set(document1))
    union = set(document).union(set(document1))
    return round(len(intersection) / len(union), 2)


def compute_FAST_similarity(text):
    # jaccard_generator = (jaccard(row1, row2) for row1, row2 in combinations([tuple(word_tokenize(t)) for t in text], r=2))
    jaccard_generator = (1 - jaccard_similarity(row1, row2) for row1, row2 in
                         combinations([tuple(tokenizeText(t)) for t in text], r=2))
    flattened_matrix = np.fromiter(jaccard_generator, dtype=np.float64)
    # since flattened_matrix is the flattened upper triangle of the matrix
    # we need to expand it.
    normal_matrix = distance.squareform(flattened_matrix)
    # replacing zeros with ones at the diagonal.
    # normal_matrix += np.identity(len(text))
    return normal_matrix


class CustomClassifier(BaseEstimator, ClassifierMixin):
    threshold = 0
    thresholdsCluster = []
    data = []
    clusters = []

    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.data = X
        similarity_matrix = compute_FAST_similarity(X)
        similarity_matrix += np.identity(len(similarity_matrix))
        max_similarities = [min(similarity_matrix[i]) for i in range(len(similarity_matrix))]
        self.threshold = round(max(max_similarities), 2) + 0.01

        clustering = AgglomerativeClustering(n_clusters=None, metric='precomputed',
                                             distance_threshold=self.threshold, linkage='complete').fit(
            similarity_matrix)
        self.clusters=[[] for i in range(len(set(clustering.labels_)))]
        for i in range(len(X)):
            label = clustering.labels_[i]
            self.clusters[label].append(X[i])

        self.thresholdsCluster = [0 for i in range(len(self.clusters))]

        for i in range(len(self.clusters)):
            matrix = compute_FAST_similarity(self.clusters[i])
            max_similarities = [max(matrix[i]) for i in range(len(matrix))]

            self.thresholdsCluster[i] = round(max(max_similarities), 2)

    def predict(self, X, y=None):
        res = []
        for word in X:
            tokenized_word = tuple(tokenizeText(word))
            found = False
            i=0
            for cluster in self.clusters:
                for p in cluster:
                    tokenized_word1 = tuple(tokenizeText(p))
                    distance = round(1 - jaccard_similarity(tokenized_word, tokenized_word1), 2)

                    if distance <= self.thresholdsCluster[i]:
                        found = True
                        break
                if found:
                    break
                i+=1

            if found:
                res.append(1)
            else:
                res.append(-1)
        return res