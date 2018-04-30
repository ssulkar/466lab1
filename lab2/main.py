import sys
import csv
import json
import xml.etree.ElementTree

import logging
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

import alg
import d_tree

def main():
    # tree = ET.parse(str(sys.argv[1]))
    # root = tree.getroot()

    data = []
    with open(str(sys.argv[2]), 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = [row for row in reader]
    attributes = data[0]
    A = [0 for x in range(len(data[0]))]
    for i in range(len(data[0])):
        A[i] = [attributes[i], int(data[1][i])]

    A[-1][1] = -1
    data = data[3:]

    threshold = .01
    T = alg.c45(data, A, d_tree.Node('root'), threshold)
    
    xml = d_tree.toXML(d_tree.Tree(T))
    print(xml)
    # tmp = ElementTree.fromstring(xml)
    # tree = ElementTree.ElementTree(tmp)
    # tree.write('output.xml')

if __name__=='__main__':
    main()