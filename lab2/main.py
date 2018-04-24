import sys
import csv
import json
import xml.etree.ElementTree

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
    # attributes = attributes[1:-1]
    data = data[3:]
    T = alg.c45(data, attributes, d_tree.Node('root'), 1.0)
    # print(json.dumps(d_tree.toJSON(T), sort_keys=True, indent=4))
    xml = d_tree.toXML(d_tree.Tree(T))
    print(xml)
    # tmp = ElementTree.fromstring(xml)
    # tree = ElementTree.ElementTree(tmp)
    # tree.write('output.xml')

def log(x):
    val = 0
    if x != 0:
        val = math.log(x,2)
    return val

if __name__=='__main__':
    main()