from pprint import pprint as pp

import vector
import parse
import shutil
import os

raw1 = "this cat a b c d cat"
raw2 = "this sentence talks about a dog"
raw3 = "this. sentence \ttalks, about \n      a dog"

def test_DocumentCollection():
    file1 = './datasets/C50test/AaronPressman/421829newsML.txt'
    file2 = './datasets/C50test/AaronPressman/424074newsML.txt'
    file_list = [file1, file2]

    doc_col = parse.get_doc_collection(file_list)    

    idf_table = vector.compute_IDF(doc_col.doc_list, doc_col.vocab)
    assert len(idf_table) == 476

    assert len(doc_col.doc_list) == 2
    assert len(doc_col.author_list) == 2
    assert len(doc_col.vocab) == 476

def test_Vector():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = parse.get_vocabulary(doc_list)
    doc_col = parse.DocumentCollection(doc_list, vocab)

    v = vector.VectorCollection((parse.DocumentCollection(doc_list, vocab)))
    v.compute_TF_IDF()
    assert v.tf_idf_table[0][1] == 1.3862943611198906

def test_Vector_file():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = parse.get_vocabulary(doc_list)
    doc_col = parse.DocumentCollection(doc_list, vocab)

    v1 = vector.VectorCollection(parse.DocumentCollection(doc_list, vocab))
    v1.compute_TF_IDF()
    v2 = vector.VectorCollection(parse.DocumentCollection([], []))

    folder = '__temp__'
    v1.save_to_dir(folder)
    v2.load_from_dir(folder)
    shutil.rmtree('__temp__')
    assert (v1.tf_idf_table == v2.tf_idf_table).all()

def test_compute_TF_IDF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = parse.get_vocabulary(doc_list)
    doc_col = parse.DocumentCollection(doc_list, vocab)

    tf_table = vector.compute_TF(doc_col.doc_list, doc_col.vocab)
    idf_table = vector.compute_IDF(doc_col.doc_list, doc_col.vocab)
    tf_idf_table = vector.compute_TF_IDF(tf_table, idf_table)
    assert tf_idf_table[0][1] == 1.3862943611198906
    assert tf_idf_table.shape[1] == len(vocab)

def test_compute_IDF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = parse.get_vocabulary(doc_list)
    doc_col = parse.DocumentCollection(doc_list, vocab)

    idf_table = vector.compute_IDF(doc_col.doc_list, doc_col.vocab)
    assert idf_table[1] == 0.6931471805599453
    assert idf_table[0] == 0

def test_compute_TF():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')

    doc_list = [doc1, doc2]
    vocab = parse.get_vocabulary(doc_list)
    doc_col = parse.DocumentCollection(doc_list, vocab)

    tf_table = vector.compute_TF(doc_col.doc_list, doc_col.vocab)
    term = 1
    assert tf_table[0][term] == 2.0
    assert tf_table[1][term] == 0

def test_get_vocabulary():
    doc1 = raw1.split(' ')
    doc2 = raw2.split(' ')
    
    doc_list = [doc1, doc2]
    doc_col = parse.DocumentCollection(doc_list, [])
    vocab = parse.get_vocabulary(doc_col.doc_list)
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

    doc_col = parse.get_doc_collection([file1, file2])

    tf_table = vector.compute_TF(doc_col.doc_list, doc_col.vocab)
    idf_table = vector.compute_IDF(doc_col.doc_list, doc_col.vocab)
    assert len(idf_table) == 476
