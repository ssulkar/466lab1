import os
import numpy as np

class DocumentCollection():
    def __init__(self, doc_list, vocab, author_list=[]):
        self.doc_list = np.array(doc_list)
        self.vocab = np.array(vocab)
        self.author_list = np.array(author_list)

    def save(self, out_dir):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        np.save(get_vocab_cache_name(out_dir), self.vocab)
        np.save(get_doclist_cache_name(out_dir), self.doc_list)
        np.save(get_athorlist_cache_name(out_dir), self.author_list)

    def load(self, in_dir):
        self.vocab = np.load(get_vocab_cache_name(in_dir))
        self.doc_list = np.load(get_doclist_cache_name(in_dir))
        self.author_list = np.load(get_athorlist_cache_name(in_dir))

def get_vocabulary(doc_list):
    vocab = []
    for doc in doc_list:
        for word in doc:
            if word not in vocab: vocab.append(word)
    return np.array(vocab)

def get_doc_collection(file_list):
    vocab = []
    doc_list = []
    author_list = []

    for file in file_list:
        # get class label from dir name
        dirs = file.split('/')
        author = dirs[-2]

        data = read_file(file)
        doc = parse_doc(data)

        author_list.append(author)
        doc_list.append(doc)
        for word in doc:
            if word not in vocab: vocab.append(word)

    doc_list = np.array(doc_list)
    vocab = np.array(vocab)
    author_list = np.array(author_list)
    doc_col = DocumentCollection(doc_list, vocab, author_list)
    return doc_col
        
def read_file(filename):
    data = []
    with open(filename, 'r') as f:
        data = [line for line in f]
    return data

def parse_doc(raw):
    doc = ''.join(raw)
    stopwords = ['.', ',', '\n', '\t', '"']
    for word in stopwords:
        doc = doc.replace(word, '')
    doc = np.array(list(doc.split(' ')))
    doc = doc[doc != '']
    return doc

def get_vocab_cache_name(folder):
    return './' + folder + '/_cache_vocab.npy'

def get_doclist_cache_name(folder):
    return './' + folder + '/_cache_doclist.npy'

def get_athorlist_cache_name(folder):
    return './' + folder + '/_cache_authorlist.npy'

def get_vector_cache_name(folder):
    return './' + folder + '/_cache_vector.npy'
