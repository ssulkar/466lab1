import matplotlib
matplotlib.use('Agg')

import sys
import math
import random
import csv

import matplotlib.pyplot as plt
import numpy as np

def main(args):
    filename = args[1]
    k = int(args[2])

    # open file and load data
    data = getData(filename)

def getData(filename):
    # open file, and return data in memory
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(data) for i, data in enumerate(r) if header[i] != '0'] for r in reader if len(r) > 0]
    return rows

if __name__ == '__main__':
    args = sys.argv
    main(args)
