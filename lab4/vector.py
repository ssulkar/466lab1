import math

import numpy as np

class Vector:
    """A class for storing tf-idf vector representations of text documents

    Want to store data in a format like this:

        |     | word  | word  | word  | word  | word  | word  | word  | word  |
        -----------------------------------------------------------------------
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
        | doc | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |

    Do I store it as:
        vocabulary = [word, ...]
        docs = [doc, ...]
        tf-idf = [[0.001, ...], ...]

    """

    def __init__(self):
        pass

    def __repr__(self):
        return 'TODO repr'

    def simscore_cosine(self, other):
        """The similarity of two vectors using cosine"""
        return 0

    def simscore_okapi(self, other):
        """The similarity of two vectors using okapi"""
        return 0

def compute_TF_IDF(tf_table, idf_table):
    tf_idf_table = np.zeros(shape=tf_table.shape)
    for i, doc in enumerate(tf_table):
        for j, term in enumerate(doc):
            tf_idf_table[i][j] = term * idf_table[j]
    return tf_idf_table

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
            tf_table[i][j] = _get_term_count(term, doc)
    return tf_table

def _get_term_count(term, doc):
    return doc.count(term)

def _normalize(x, max):
    return float(x / max)

def get_vocabulary(doc_list):
    vocab = []
    for doc in doc_list:
        for word in doc:
            if word not in vocab: vocab.append(word)
    return vocab

def compute_IDF(doc_list, vocab):
    vocab = get_vocabulary(doc_list)
    # might need to initialize this
    doc_counts = []
    for word in vocab:
        doc_counts.append(_get_doc_count(word, doc_list))
    
    # part of formula
    idf_table = []
    for count in doc_counts:
        idf_table.append(_calc_idf(count, doc_list))
    return np.array(idf_table)

def _get_doc_count(word, doc_list):
    c = 0
    for doc in doc_list:
        if word in doc: c += 1
    return c

def _calc_idf(count, doc_list):
    return math.log(float(len(doc_list) / count))

