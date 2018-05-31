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

    adj_matrix, ordering = get_adj_matrix(data)

def get_data(filename):
    lines = []
    with open(os.path.join('./datasets', filename), 'r') as f:
        reader = csv.reader(f)
        lines = [list(map(lambda x: x.strip(), r)) for r in reader]
    return np.array(lines)

def get_adj_matrix(data):
    adj_list = _get_adj_list(data)
    ordering = sorted(adj_list)
    adj_matrix = _matrix_from_list(adj_list, ordering)
    return adj_matrix, ordering

def _matrix_from_list(adj_list, ordering):
    n = len(adj_list)
    matrix = np.zeros((n, n))
    for i, key in enumerate(ordering):
        for value in adj_list[key]:
            matrix[i, ordering.index(value)] = 1
    return matrix

def _get_adj_list(data):
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