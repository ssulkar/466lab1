class Vector:
    """A class used for comparing to vectors. Represents a single row
    in the table below.

    """

    def __init__(self, doc_index, data):
        self.doc_index = doc_index
        self.data = data

    def simscore_cosine(self, other):
        """The similarity of two vectors using cosine"""
        return 0

    def simscore_okapi(self, other):
        """The similarity of two vectors using okapi"""
        return 0

class KNNClassifier:
    def __init__(self):
        pass