import unittest
import json
import xml.etree.ElementTree

from d_tree import *

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

    n3 = Node('Gender')
    n3.edges.append(Edge('Female', n))
    n3.edges.append(Edge('Male', n2))
    tree = Tree(n3)
    return tree

class TestDecisionTree(unittest.TestCase):
    def test_toJSON(self):
        with open('example_format.json', 'r') as f:
            expect = json.load(f)
            self.assertEqual(toJSON(buildTestTree()), expect)

    def test_toXML(self):
        with open('example_format.xml', 'r') as f:
            tmp = ElementTree.fromstring(toXML(buildTestTree()))
            tree = ElementTree.ElementTree(tmp)
            tree.write('decision_tree.xml')
            
            expect = ElementTree.parse(f)
            # print(ElementTree.tostring(tree.getroot()))
            # print(ElementTree.tostring(expect.getroot()))

if __name__ == '__main__':
    unittest.main()