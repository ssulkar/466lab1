import matplotlib
matplotlib.use('Agg')

import os
import csv
from pprint import pprint as pp

import numpy as np
import matplotlib.pyplot as plt

import pageRank

# ------------------------------------------------------------------------------
def test_adj_matrix():
    data = np.array([['AL', 'FL'],
                     ['AL', 'GA'],
                     ['AL', 'MS'],
                     ['AL', 'TN'],
                     ['AZ', 'CA']], dtype='<U2')
    adj_matrix, ordering = pageRank.get_adj_matrix(data)
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            assert adj_matrix[i][j] == adj_matrix[j][i]

# ------------------------------------------------------------------------------
adj_matrix2 = np.array([[0, 1], 
                        [1, 0]], dtype=np.float32)

# ------------------------------------------------------------------------------
adj_matrix3 = np.array([[0, 1, 1],
                        [1, 1, 0],
                        [1, 0, 0]], dtype=np.float32)

# ------------------------------------------------------------------------------
adj_matrix3_alt = np.array([[0, 1, 0],
                            [0, 0, 1],
                            [1, 1, 0]], dtype=np.float32)

# ------------------------------------------------------------------------------
adj_matrix4 = np.array([[0, 1, 1, 0],
                        [0, 0, 1, 0],
                        [1, 0, 0, 0],
                        [0, 0, 1, 0]], dtype=np.float32)

# ------------------------------------------------------------------------------
def test_matrix3_alt():
    adj_matrix = adj_matrix3_alt
    d = .85
    pr_arr = pageRank.calc_PR(adj_matrix, d)

    ep = .0001
    pr_arr = pageRank.calc_PR_alternate(adj_matrix, ep)

def test_matrix3():
    adj_matrix = adj_matrix3
    d = .85
    pr_arr = pageRank.calc_PR(adj_matrix, d)

    ep = .0001
    pr_arr = pageRank.calc_PR_alternate(adj_matrix, ep)

def test_text():
    # filename = './datasets/stateborders.csv'
    filename = './datasets/amazon0505.txt'
    data = pageRank.get_data(filename)
    pp(data)
