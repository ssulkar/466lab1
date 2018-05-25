import math

import numpy as np

import utils

class VectorCollection:
    """A class for storing tf-idf vector representations of text documents

    Store data in a numpy array format like this:

        |     | word  | word  | word  | word  | word  |
        -----------------------------------------------
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |

    """

    def __init__(self, doc_col):
        self.doc_col = doc_col
        self.tf_table = None
        self.idf_table = None
        self.tf_idf_table = None

    def __repr__(self):
        return 'TODO repr'

    def compute_TF_IDF(self):
        self.tf_table = compute_TF(self.doc_col.doc_list, self.doc_col.vocab)
        self.idf_table = compute_IDF(self.doc_col.doc_list, self.doc_col.vocab)
        self.tf_idf_table = compute_TF_IDF(self.tf_table, self.idf_table)
        return self.tf_idf_table    

    def load(self, filename):
        self.tf_idf_table = np.load(filename)

    def save(self, filename):
        np.save(filename, self.tf_idf_table)

    def save_to_dir(self, out_dir):
        self.doc_col.save(out_dir)
        np.save(utils.get_vector_cache_name(out_dir), self.tf_idf_table)

    def load_from_dir(self, in_dir):
        self.doc_col.load(in_dir)
        self.tf_idf_table = np.load(utils.get_vector_cache_name(in_dir))

    def flip_all(self):
        self.doc_col.doc_list = self.doc_col.doc_list.T
        self.doc_col.vocab = self.doc_col.vocab.T
        self.doc_col.author_list = self.doc_col.author_list.T
        self.tf_table = self.tf_table.T
        self.idf_table = self.idf_table.T
        self.tf_idf_table = self.tf_idf_table.T

def real_compute_tfidf(doc_list, vocab):
    tf_table = compute_TF(doc_list, vocab)
    idf_table = compute_IDF(doc_list, vocab)
    tf_idf_table = compute_TF_IDF(tf_table, idf_table)
    return tf_idf_table

def compute_TF_IDF(tf_table, idf_table):
    return tf_table * idf_table

def compute_TF_normalized(doc_list, vocab):
    tf_table = compute_TF(doc_list, vocab)
    tf_table = [[_normalize(data, max(row)) for data in row] for row in tf_table]
    return np.array(tf_table)

def compute_TF(doc_list, vocab):
    rows = len(doc_list)
    cols = len(vocab)

    tf_table = np.zeros(shape=(rows, cols))
    for i, doc in enumerate(doc_list):
        for j, term in enumerate(vocab):
            count = _get_term_count(term, doc)
            # print('count: %s' % count)
            tf_table[i][j] = count
    return tf_table

def _get_term_count(term, doc):
    return np.count_nonzero(np.array(doc) == term)

def _normalize(x, max):
    return float(x / max)

def compute_IDF(doc_list, vocab):
    # might need to initialize this
    dfs = get_doc_freq(doc_list, vocab)
    print('dfs: %s' % dfs)
    temp = np.reciprocal(dfs)
    temp[temp == np.inf] = 0
    idf = np.log(temp * len(doc_list))
    idf[idf == np.inf] = 0
    print(idf)
    return idf

def get_doc_freq(doc_list, vocab):
    df = np.zeros(len(vocab))
    for i, doc in enumerate(doc_list):
        for j, word in enumerate(vocab):
            if word in doc: df[j] += 1
    return df

def _calc_idf(count, doc_list):
    if count == 0: return 0
    return math.log(float(len(doc_list) / count))

