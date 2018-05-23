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
