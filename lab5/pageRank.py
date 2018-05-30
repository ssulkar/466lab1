import matplotlib
matplotlib.use('Agg')

import os
import csv
from pprint import pprint as pp

import numpy as np
import matplotlib.pyplot as plt

class Node:
    """ Nodes of a graph. Each has a list of nodes that it shares an edge with """
    def __init__(self, neighbors, value):
        self.neighbors = neighbors
        self.value = value

    def __repr__(self):
        return '(node %s)' % self.value

    def str_neighbors(self):
        return str(self) + str(self.neighbors)

def main():
    # x = np.arange(20)
    # y = np.random.rand((20))
    # fig = plt.figure()
    # plt.scatter(x, y)

    # fig.savefig('test.png')

    all_files = os.listdir('./datasets')
    filename = all_files[2]
    data = get_data(filename)
    # array([['AL', '0', 'FL', '0'],
           # ['AL', '0', 'GA', '0'],
           # ['AL', '0', 'MS', '0'],
           # ['AL', '0', 'TN', '0'],
           # ['AZ', '0', 'CA', '0']], dtype='<U2')

    # state = data[0][0]
    # node = Node([], state)
    # for neighbor in data[data[:,0] == state]:
    #     node.neighbors.append(Node([node], neighbor[2]))
    # pp(node.str_neighbors())

    adj_list = get_adjacency_list(data)
    pp(len(adj_list))
    adj_matrix = convert_to_adjacency_matrix(adj_list)
    pp(adj_matrix[:5, :5])

def get_data(filename):
    lines = []
    with open(os.path.join('./datasets', filename), 'r') as f:
        reader = csv.reader(f)
        lines = [list(map(lambda x: x.strip(), r)) for r in reader]
    return np.array(lines)

def convert_to_adjacency_matrix(adj_list):
    labels = sorted(adj_list)
    n = len(adj_list)
    matrix = np.zeros((n, n))
    for i, key in enumerate(sorted(adj_list)):
        for value in adj_list[key]:
            matrix[i, labels.index(value)] = 1
    return matrix

def get_adjacency_list(data):
    adj_list = {}
    for row in data:
        col_1 = row[0]
        col_2 = row[2]
        l = adj_list.get(col_1, [])
        if col_2 not in l:
            adj_list[col_1] = l + [col_2]

        l = adj_list.get(col_2, [])
        if col_1 not in l:
            adj_list[col_2] = l + [col_1]
    return adj_list

if __name__ == '__main__':
    main()