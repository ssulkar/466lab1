from pprint import pprint as pp
import numpy as np

import vector
import utils

def simscore_cosine(data, other):
    """The similarity of two vectors using cosine
    Expects two numpy arrays
    """
    numerator = np.sum(np.multiply(data, other))

    data_sqrt = np.sqrt(np.sum(data**2))
    other_sqrt = np.sqrt(np.sum(other**2))
    denominator = data_sqrt * other_sqrt

    if denominator == 0: return 0
    return round(numerator / denominator, 4)

def simscore_okapi(data, other):
    """The similarity of two vectors using okapi"""
    return 0

class KNNClassifier:
    def __init__(self, vec_col, k):
        self.vec_col = vec_col
        self.k = k
        self.X = vec_col.tf_idf_table

    def classify(self, new_data):
        """Expects numpy array"""
        scores = np.zeros((new_data.shape[0], self.X.shape[0]))
        for data in new_data:
            temp = []
            for row in self.X:
                score = simscore_cosine(row, data)
                temp.append(score)
            temp = np.array(temp).reshape(1, self.X.shape[0])
            scores = np.append(temp, scores, axis=0)
        return np.array(scores)

    def classify_query(self, query):
        """Expects numpy array"""
        vocab = self.vec_col.doc_col.vocab
        # vec = np.zeros(len(vocab))
        # tf = vector.compute_TF([query], vocab)
        # pp('tf nonzeros:')
        # pp(tf[tf != 0])
        # idf = vector.compute_IDF([query], vocab)
        # pp('idf nonzeros:')
        # pp(idf[idf != 0])
        # tf_idf = vector.compute_TF_IDF(tf, idf)
        tf_idf = vector.real_compute_tfidf([query], vocab)
        return tf_idf

"""
>>> a
array([[0.01336106, 0.03264852, 0.33333333, 0.00358299, 0.03872433],
       [0.03066834, 0.02254965, 0.02408022, 0.03362333, 0.03657906],
       [0.00152462, 0.06328437, 0.01571585, 0.05676656, 0.02549035],
       [0.05357302, 0.00131684, 0.0201129 , 0.01416303, 0.02531208],
       [0.05642568, 0.0588411 , 0.00133164, 0.0335475 , 0.00161571],
       [0.0155717 , 0.0077499 , 0.05322191, 0.04608866, 0.02520263],
       [0.0185091 , 1.        , 0.02213965, 0.04138641, 0.05205222],
       [0.05966071, 0.02605257, 0.06344993, 0.02150656, 0.03232519],
       [0.02365663, 0.00557281, 0.03593433, 0.05014777, 0.06498977],
       [0.02492257, 0.06305724, 0.00856013, 0.06510266, 0.02379129]])
>>> so = np.sum(a, axis=1).argsort()[::-1]
>>> a[so]
array([[0.0185091 , 1.        , 0.02213965, 0.04138641, 0.05205222],
       [0.01336106, 0.03264852, 0.33333333, 0.00358299, 0.03872433],
       [0.05966071, 0.02605257, 0.06344993, 0.02150656, 0.03232519],
       [0.02492257, 0.06305724, 0.00856013, 0.06510266, 0.02379129],
       [0.02365663, 0.00557281, 0.03593433, 0.05014777, 0.06498977],
       [0.00152462, 0.06328437, 0.01571585, 0.05676656, 0.02549035],
       [0.05642568, 0.0588411 , 0.00133164, 0.0335475 , 0.00161571],
       [0.0155717 , 0.0077499 , 0.05322191, 0.04608866, 0.02520263],
       [0.03066834, 0.02254965, 0.02408022, 0.03362333, 0.03657906],
       [0.05357302, 0.00131684, 0.0201129 , 0.01416303, 0.02531208]])
>>> a[a < .03] = 0
>>> a
array([[0.        , 0.03264852, 0.33333333, 0.        , 0.03872433],
       [0.03066834, 0.        , 0.        , 0.03362333, 0.03657906],
       [0.        , 0.06328437, 0.        , 0.05676656, 0.        ],
       [0.05357302, 0.        , 0.        , 0.        , 0.        ],
       [0.05642568, 0.0588411 , 0.        , 0.0335475 , 0.        ],
       [0.        , 0.        , 0.05322191, 0.04608866, 0.        ],
       [0.        , 1.        , 0.        , 0.04138641, 0.05205222],
       [0.05966071, 0.        , 0.06344993, 0.        , 0.03232519],
       [0.        , 0.        , 0.03593433, 0.05014777, 0.06498977],
       [0.        , 0.06305724, 0.        , 0.06510266, 0.        ]])
>>> np.sum(a, axis=0)
array([0.20032775, 1.21783123, 0.4859395 , 0.32666289, 0.22467058])
>>> so = np.sum(a, axis=0).argsort()[::-1]
>>> a[:,so]
array([[0.03264852, 0.33333333, 0.        , 0.03872433, 0.        ],
       [0.        , 0.        , 0.03362333, 0.03657906, 0.03066834],
       [0.06328437, 0.        , 0.05676656, 0.        , 0.        ],
       [0.        , 0.        , 0.        , 0.        , 0.05357302],
       [0.0588411 , 0.        , 0.0335475 , 0.        , 0.05642568],
       [0.        , 0.05322191, 0.04608866, 0.        , 0.        ],
       [1.        , 0.        , 0.04138641, 0.05205222, 0.        ],
       [0.        , 0.06344993, 0.        , 0.03232519, 0.05966071],
       [0.        , 0.03593433, 0.05014777, 0.06498977, 0.        ],
       [0.06305724, 0.        , 0.06510266, 0.        , 0.        ]])
>>> so
array([1, 2, 3, 4, 0])
>>> np.sum(a, axis=0)[so]
array([1.21783123, 0.4859395 , 0.32666289, 0.22467058, 0.20032775])
>>>
"""