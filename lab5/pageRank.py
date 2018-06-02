import matplotlib
matplotlib.use('Agg')

import time
import os
import sys
import csv
from pprint import pprint as pp

import numpy as np
import matplotlib.pyplot as plt

def main():
    start_time = time.time()
    # all_files = os.listdir('./datasets')
    # filename = all_files[2]
    filename = sys.argv[1]
    data = get_data(filename)
    # array([['AL', '0', 'FL', '0'],
           # ['AL', '0', 'GA', '0'],
           # ['AL', '0', 'MS', '0'],
           # ['AL', '0', 'TN', '0'],
           # ['AZ', '0', 'CA', '0']], dtype='<U2')

    adj_matrix, ordering = get_adj_matrix(data)

    data_read_time = time.time()

    d = .85
    pr_arr = calc_PR(adj_matrix, d)

    pp('read time: %s' % (data_read_time - start_time))
    pp('calc time: %s' % (calc_time - data_read_time))

    sort_order = pr_arr.argsort()[::-1]

    ordering = ordering[sort_order]
    pr_arr = pr_arr[sort_order]
    for i, pr in enumerate(pr_arr):
        pp('%s: %s' % (ordering[i], pr_arr[i]))
    
    calc_time = time.time()

# ------------------------------------------------------------------------------
def get_data(filename):
    lines = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        lines = [list(map(lambda x: x.strip(), r)) for r in reader]
    return np.array(lines)

# ------------------------------------------------------------------------------
def get_adj_matrix(data):
    adj_list = _get_adj_list(data)
    ordering = sorted(adj_list)
    adj_matrix = _matrix_from_list(adj_list, ordering)
    return adj_matrix, np.array(ordering)

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

# ------------------------------------------------------------------------------
def calc_PR(adj_matrix, d):
    MAX_ITERATIONS = 50
    iter_count = 0
    pr_arr = np.ones(len(adj_matrix)) / len(adj_matrix)
    for i in range(MAX_ITERATIONS):
        iter_count += 1
        temp = np.zeros(len(adj_matrix))
        for page_index in range(len(pr_arr)):
            temp[page_index] = _single_pr(page_index, pr_arr, adj_matrix, d)
        pr_arr = temp
    pp('iter_count: %s' % iter_count)
    return pr_arr


def _single_pr(page_index, pr_arr, adj_matrix, d):
    n = len(adj_matrix)
    list_index = _get_list_index(page_index, adj_matrix)
    other_pr = pr_arr[list_index]
    other_outs = _get_outs(page_index, adj_matrix)
    div = other_pr / other_outs
    s = np.sum(div)
    # smaller, normalized
    # final = ((1 - d) / n) + (d * s)

    # larger, normalized
    final = ((1 - d)) + (d * s)

    debug = False
    if debug:
        pp('-'*20)
        pp('list_index: %s' % list_index)
        pp('other_pr: %s' % other_pr)
        pp('other_outs: %s' % other_outs)
        pp('div: %s' % div)
        pp('s: %s' % s)
        pp('final: %s' % final)
        pp('-'*20)

    return final

def _get_outs(page_index, adj_matrix):
    list_index = _get_list_index(page_index, adj_matrix)
    return np.sum(adj_matrix[list_index], axis=1)

def _get_list_index(page_index, adj_matrix):
    # grab column, check if it has a 1 (meaning it has a link to that page)
    col = adj_matrix[:,page_index] == 1
    return col

# ------------------------------------------------------------------------------
def calc_PR_alternate(G, ep):
    "G is N*N matrix where if j links to i then G[i][j]==1, else G[i][j]==0"
    N = len(G)
    d = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if (G[j, i] == 1):
                d[i] += 1

    r0 = np.zeros(N, dtype=np.float32) + 1.0 / N
    # construct stochastic M
    M = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for j in range(N):
            if G[j, i] == 1:
                M[j, i] = 1.0 / d[i]
    # pp(G)
    # pp(d)
    # pp(M)
    while True:
        r1 = np.dot(M, r0)
        dist = _distance(r1, r0)
        if dist < ep:
            break
        else:
            r0 = r1
    return r1

def _distance(v1, v2):
    v = v1 - v2
    v = v * v
    return np.sum(v)

if __name__ == '__main__':
    main()