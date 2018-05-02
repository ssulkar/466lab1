import sys
import csv
import json
import xml.etree.ElementTree as ET
import logging
logger = logging.getLogger(__name__)

import alg
import d_tree

def main(args):
    threshold = .01

    # TODO need to use this information in xml output
    # maybe create object to store it, then pass it down
    # Node and Edge objects will have new fileds for holding their values
    # then the export only needs to use the fields on the objects it already has
    tree = ET.parse(str(args[1]))
    root = tree.getroot()

    D = []
    with open(str(args[2]), 'r') as f:
        reader = csv.reader(f, delimiter=',')
        D = [row for row in reader]
    attributes = D[0]

    A = [0 for x in range(len(attributes))]
    for i in range(len(attributes)):
        A[i] = [attributes[i], int(D[1][i])]

    # ignore things in restrictions file
    if len(args) > 3:
        with open(str(args[3]), 'r') as f:
            reader = csv.reader(f, delimiter=',')
            ignore = [row for row in reader]
            ignore = ignore[0]
            for i, attr in enumerate(ignore):
                if int(attr) == 0:
                    A[i][1] = -1
                    logger.debug('ignoring attribute %s' % A[i][0])

    # ignore last column VOTE
    A[-1][1] = -1

    # grab main data
    D = D[3:]

    T = alg.c45(D, A, d_tree.Node('root'), threshold)
    
    xml = d_tree.toXML(d_tree.Tree(T))
    print(xml)
    tmp = ET.fromstring(xml)
    tree = ET.ElementTree(tmp)
    tree.write('output.xml')

if __name__=='__main__':
    main(sys.argv)