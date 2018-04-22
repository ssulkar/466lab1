import csv
import json

import alg
import d_tree

def main():
    data = []
    with open('tree_testing/tree03-20-words.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = [row for row in reader]
    attributes = data[0]
    # attributes = attributes[1:-1]
    data = data[3:]
    T = alg.c45(data, attributes, d_tree.Node('root'), 0)
    print(json.dumps(d_tree.toJSON(T), sort_keys=True, indent=4))

def log(x):
    val = 0
    if x != 0:
        val = math.log(x,2)
    return val

if __name__=='__main__':
    main()