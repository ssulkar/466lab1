import numpy as np

class DocumentCollection():
    def __init__(self, doc_list=[], vocab=[]):
        self.doc_list = np.array(doc_list)
        self.vocab = np.array(vocab)

    def save(self, vocab_cache, doclist_cache):
        np.save(vocab_cache, self.vocab)
        np.save(doclist_cache, self.doc_list)

    def load(self, vocab_cache, doclist_cache):
        self.vocab = np.load(vocab_cache)
        self.doc_list = np.load(doclist_cache)

def get_vocabulary(doc_list):
    vocab = []
    for doc in doc_list:
        for word in doc:
            if word not in vocab: vocab.append(word)
    return np.array(vocab)

def get_doc_collection(file_list):
    vocab = []
    doc_list = []
    for file in file_list:
        data = read_file(file)
        doc = parse_doc(data)
        doc_list.append(doc)
        for word in doc:
            if word not in vocab: vocab.append(word)
    doc_col = DocumentCollection(np.array(doc_list), np.array(vocab))
    return doc_col

def get_doc_list(file_list):
    doc_list = []
    for file in file_list:
        data = read_file(file)
        doc = parse_doc(data)
        doc_list.append(doc)
    return np.array(doc_list)
        
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
    doc = doc.split(' ')
    doc = [word for word in doc if word != '']
    return doc

def get_vocab_cache_name(folder):
    return './' + folder + '/_cache_vocab.npy'

def get_doclist_cache_name(folder):
    return './' + folder + '/_cache_doclist.npy'

def get_vector_cache_name(folder):
    return './' + folder + '/_cache_vector.npy'
