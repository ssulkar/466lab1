from pprint import pprint as pp

import vector
import parse

raw1 = "this cat a b c d cat"
raw2 = "this sentence talks about a dog"
raw3 = "this. sentence \ttalks, about \n      a dog"

def test_compute_TF_IDF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = vector.get_vocabulary(doc_list)

    tf_table = vector.compute_TF(doc_list, vocab)
    idf_table = vector.compute_IDF(doc_list, vocab)
    tf_idf_table = vector.compute_TF_IDF(tf_table, idf_table)
    pp(tf_idf_table)

def test_compute_IDF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = vector.get_vocabulary(doc_list)

    idf_table = vector.compute_IDF(doc_list, vocab)
    assert idf_table[vocab.index('cat')] == 0.6931471805599453
    assert idf_table[vocab.index('this')] == 0

def test_compute_TF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = vector.get_vocabulary(doc_list)

    tf_table = vector.compute_TF(doc_list, vocab)
    term = vocab.index('cat')
    assert tf_table[0][term] == 2
    assert tf_table[1][term] == 0

def test_get_vocabulary():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')
    
    doc_list = [doc1, doc2]
    vocab = vector.get_vocabulary([doc1, doc2])
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

    doc_list = [doc1, doc2]
    vocab = vector.get_vocabulary(doc_list)

    tf_table = vector.compute_TF(doc_list, vocab)
    idf_table = vector.compute_IDF(doc_list, vocab)
    assert len(idf_table) == 476
