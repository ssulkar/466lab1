from xml.dom import minidom

class Tree:
    def __init__(self, root):
        self.root = root
        self.name = "test" # TODO

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
    return {
        "name": T.name,
        "Tree": _toJSON(T.root)
    }
    
def _toJSON(T):
    if hasattr(T, 'label'):
        return {
            "label": T.label,
            "node": _toJSON(T.node)
        }
    else:
        return {
            "value": T.value,
            "edges": [_toJSON(e) for e in T.edges]
        }

# returns to tree as a dictionary that can be written to json file
def toXML(T):
    # adds outer <Tree> tag
    rough_string = '<Tree name="{0}">{1}</Tree>'.format(T.name, _toXML(T.root))
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def _toXML(T):
    if hasattr(T, 'label'):
        return '<edge var = "{0}" num = "null">{1}</edge>'.format(T.label, _toXML(T.node))
    elif len(T.edges) == 0:
        return '<decision end="null" choice="{0}" p="null"/>'.format(T.value)
    else:
        return '<node var="{0}">{1}</node>'.format(T.value, ''.join([_toXML(e) for e in T.edges]))
