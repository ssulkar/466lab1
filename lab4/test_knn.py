import numpy as np
from pprint import pprint as pp

import knn
import parse
import vector

def test_KNNClassifier():
    # file1 = './datasets/C50test/AaronPressman/421829newsML.txt'
    # file2 = './datasets/C50test/AaronPressman/424074newsML.txt'
    # file_list = [file1, file2]

    doc_col = parse.get_doc_collection([])    
    v = vector.VectorCollection(doc_col)

    # use small sample data
    v.load_from_dir('small')
    # v.tf_idf_table = v.tf_idf_table[:5]

    k = 1
    classifier = knn.KNNClassifier(v, k)
    assert classifier.k == k

    # pp(v.doc_col.vocab[:10])
    query = ['Senators', 'Tuesday']
    scores = classifier.classify_query(query)
    pp('scores nonzeros:')
    pp(scores[scores != 0])

def test_cosine():
    index = 0
    a = np.array([2, 1])
    b = np.array([1, 2])
    score = knn.simscore_cosine(a, b)
    assert score == .8
    a = np.array([0, 1, 0, 1, 1])
    b = np.array([1, 1, 1, 0, 0])
    score = knn.simscore_cosine(a, b)
    assert score == .3333

def test_okapi():
    index = 0
    a = np.array([2, 1])
    b = np.array([1, 2])
    score = knn.simscore_okapi(a, b)
    assert score == 0
