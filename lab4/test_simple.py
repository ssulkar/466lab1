from pprint import pprint as pp

import vector
import parse

raw1 = "this cat a b c d cat"
raw2 = "this sentence talks about a dog"
raw3 = "this. sentence \ttalks, about \n      a dog"

def test_compute_TF_IDF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    tf_dict = vector.compute_TF(doc1)
    idf_dict = vector.compute_IDF([doc1, doc2])
    tf_idf_dict = vector.compute_TF_IDF(tf_dict, idf_dict)
    pp(tf_idf_dict)

def test_compute_IDF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    idf_dict = vector.compute_IDF([doc1, doc2])
    assert idf_dict['cat'] == 0.6931471805599453
    assert idf_dict['this'] == 0

def test_compute_TF():
    doc = raw1.split(' ')

    tf_dict = vector.compute_TF(doc)
    assert tf_dict['cat'] == 1
    assert tf_dict['this'] == .5

def test_get_vocabulary():
    doc = raw1.split(' ')
    vocab = vector.get_vocabulary([doc])
    assert len(vocab) == 6

    doc2 = raw2.split(' ')
    vocab = vector.get_vocabulary([doc, doc2])
    assert len(vocab) == 10

def test_read_file():
    filename = './datasets/C50test/AaronPressman/421829newsML.txt'
    data = parse.read_file(filename)
    assert data[0][:4] == 'U.S.'

def test_parse_doc():
    doc = parse.parse_doc(raw3)
    assert len(doc) == 6

def test_full():
    file1 = './datasets/C50test/AaronPressman/421829newsML.txt'
    file2 = './datasets/C50test/AaronPressman/424074newsML.txt'

    data1 = parse.read_file(file1)
    data2 = parse.read_file(file2)

    doc1 = parse.parse_doc(data1)
    doc2 = parse.parse_doc(data2)

    tf_dict1 = vector.compute_TF(doc1)
    tf_dict2 = vector.compute_TF(doc2)

    idf_dict = vector.compute_IDF([doc1, doc2])
    assert len(idf_dict) == 476
