class Node:
    """ 
    Tree nodes have an attribute and an edge for each  value of that attribute
    Leaf node have a classification and 0 edges leading out 
    """
    def __init__(self, value):
        self.value = value
        self.edges = []

class Edge:
    """ Edges have a label and a node they are connected to """
    def __init__(self, label, node):
        self.label = label
        self.node = node

# returns to tree as a dictionary that can be written to json file
def toJSON(T):
    if hasattr(T, 'label'):
        return {
            "label": T.label,
            "node": toJSON(T.node)
        }
    else:
        return {
            "value": T.value,
            "edges": [toJSON(e) for e in T.edges]
        }
