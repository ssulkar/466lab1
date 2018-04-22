import unittest

import d_tree
from d_tree import Node, Edge

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

class TestDecisionTree(unittest.TestCase):
    def test_toJSON(self):
        expect = {
            "value": "Gender",
            "edges": [
                {
                    "label": "Female",
                    "node": {
                        "value": "Bush Approval",
                        "edges": [
                            {
                                "label": "Approve",
                                "node": {
                                    "value": "McCain",
                                    "edges": []
                                }
                            },
                            {
                                "label": "Disapprove",
                                "node": {
                                    "value": "Obama",
                                    "edges": []
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "Male",
                    "node": {
                        "value": "Ideology",
                        "edges": [
                            {
                                "label": "Liberal",
                                "node": {
                                    "value": "Obama",
                                    "edges": []
                                }
                            },
                            {
                                "label": "Moderate",
                                "node": {
                                    "value": "Obama",
                                    "edges": []
                                }
                            },
                            {
                                "label": "Conservative",
                                "node": {
                                    "value": "McCain",
                                    "edges": []
                                }
                            }
                        ]
                    }
                }
            ]
        }
        self.assertEqual(d_tree.toJSON(buildTestTree()), expect)

if __name__ == '__main__':
    unittest.main()