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

    v.load_from_dir('small')

    k = 1
    classifier = knn.KNNClassifier(k)
    assert classifier.k == k
    classifier.train(v.tf_idf_table[:5], v.doc_col.author_list)
    scores = classifier.classify(np.zeros((3, v.tf_idf_table.shape[1])))
    pp(scores)

def test_cosine():
    index = 0
    a = np.array([2, 1])
    b = np.array([1, 2])
    score = knn.simscore_cosine(a, b)
    assert score == .8

def test_okapi():
    index = 0
    a = np.array([2, 1])
    b = np.array([1, 2])
    score = knn.simscore_okapi(a, b)
    assert score == 0
