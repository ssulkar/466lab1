import unittest

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

def main():
    showTree(buildTestTree(), 0)

def alg_c45(D, A, T, theshold):
    pass

# utility function for displaying decision tree
def showTree(T, level):
    if len(T.edges) == 0:
        print('\t'*level, '*', T.value)
    else:
        print('\t'*level, T.value)
        level += 1
        for e in T.edges:
            print('\t'*level, '-', e.label)
            showTree(e.node, level + 1)

# for testing only
def buildTestTree():
    e = Edge('Approve', Node('McCain'))
    e2 = Edge('Disapprove', Node('Obama'))

    n = Node('Bush Approval')
    n.edges.append(e)
    n.edges.append(e2)

    e3 = Edge('Liberal', Node('Obama'))
    e4 = Edge('Moderate', Node('Obama'))
    e5 = Edge('Conservative', Node('McCain'))

    n2 = Node('Ideology')
    n2.edges.append(e3)
    n2.edges.append(e4)
    n2.edges.append(e5)

    tree = Node('Gender')
    tree.edges.append(Edge('Female', n))
    tree.edges.append(Edge('Male', n2))
    return tree

if __name__=='__main__':
    main()