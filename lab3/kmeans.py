import matplotlib
matplotlib.use('Agg')

import sys
import math

import matplotlib.pyplot as plt
import numpy as np
import csv

def main(args):
    filename = args[1]
    k = int(args[2])
    print('filename: %s' % filename)
    print('k: %s' % k)

    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        rows = [[int(i) for i in r] for r in reader]

    # data = np.array(rows)
    data = rows

    centroids = getInitialCentroids(data, k)
    print('centroids: %s' % centroids)

    for d in data:
        closest = getClosestCentroid(d, centroids)
        print('closest: %s' % closest)

def getInitialCentroids(data, k):
    # deterministic for now, to make testing easier
    # grab k evenly distributed points
    return [data[i] for i in range(0, len(data), math.floor(len(data)/k))]

def getClosestCentroid(point, centroids):
    closestDist = sys.maxsize
    closestCentroid = None

    for centroid in centroids:
        dist = getDistanceToCentroid(point, centroid)

        if dist < closestDist:
            closestDist = dist
            closestCentroid = centroid

    return closestCentroid

def getDistanceToCentroid(point, centroid):
    s = sum([(point[i] - centroid[i])**2 for i in range(0, len(point))])
    return math.sqrt(s)

if __name__ == '__main__':
    args = sys.argv
    main(args)