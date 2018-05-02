import sys
import csv
import json
import xml.etree.ElementTree as ET

import logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(args):
    csvfile = str(args[1])
    xmlfile = str(args[2])

    D = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        D = [row for row in reader]
    attributes = D[0]

    # grab main data
    D = D[3:]

    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    training = True
    classify(D, attributes, root, training)

def classify(D, A, tree, training):
    total = len(D)
    total_correct = 0

    name = tree[0].attrib['var']
    for d in D:
        goal = d[A.index(name)]
        c = _classify(d, A, goal, tree[0])

        if training:
            iscorrect = d[-1] == c
            if iscorrect: total_correct += 1

            print('%s, %s' % (d, c))
            # print('%s, %s' % (d[0], c))
        else:
            print('%s, %s' % (d, c))

    if training:
        total_incorrect = total - total_correct
        print('Total classified: %s' % total)
        print('Total correct: %s' % total_correct)
        print('Total incorrect: %s' % total_incorrect)
        print('Accuracy: %s' % float(total_correct/total))
        print('Error rate: %s' % float(total_incorrect/total))

def _classify(d, A, goal, node):
    logger.debug('category: %s' % node.attrib['var'])
    logger.debug('goal: %s' % goal)

    for edge in node:
        name = edge.attrib["var"]
        if name == goal:
            child = edge[0]
            if 'var' in child.attrib:
                name = child.attrib['var']
                goal = d[A.index(name)]
                return _classify(d, A, goal, child)
            # decision node
            else:
                choice = child.attrib['choice']
                actual = d[-1]
                return choice

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('Invalid args')
        sys.exit(1)

    args = sys.argv
    main(args)