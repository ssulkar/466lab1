import math

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

def compute_TF_IDF(tf_dict, idf_dict):
    # might need to initialize this
    tf_idf_dict = {}
    for word, val in tf_dict.items():
        tf_idf_dict[word] = val * idf_dict[word]
    return tf_idf_dict

def compute_TF(doc):
    tf_dict = _make_word_dict(doc)
    # normalize each count
    max_count = max(tf_dict.values())
    for word, count in tf_dict.items():
        tf_dict[word] = _normalize(count, max_count)
    return tf_dict

def _make_word_dict(bag):
    wordDict = {}
    for word in set(bag):
        wordDict[word] = bag.count(word)
    return wordDict

def _normalize(x, max):
    return float(x / max)

def get_vocabulary(doc_list):
    vocab = set()
    for doc in doc_list:
        vocab = vocab.union(set(doc))
    return vocab

def compute_IDF(doc_list):
    vocab = get_vocabulary(doc_list)
    # might need to initialize this
    doc_counts = {}
    for word in vocab:
        doc_counts[word] = _get_doc_count(word, doc_list)

    # part of formula
    idf_dict = {}
    for word, count in doc_counts.items():
        idf_dict[word] = _calc_idf(count, doc_list)
    return idf_dict

def _get_doc_count(word, doc_list):
    c = 0
    for doc in doc_list:
        if word in doc: c += 1
    return c

def _calc_idf(count, doc_list):
    return math.log(float(len(doc_list) / count))

