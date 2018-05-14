import matplotlib
matplotlib.use('Agg')

import sys
import math
import random
import csv

import matplotlib.pyplot as plt
import numpy as np

class Cluster:
    def __init__(self, centroid):
        # center is average of all the points. updated with recalculate()
        self.centroid = centroid
        # list of points in this cluster
        self.points = []

    def __repr__(self):
        return 'Centroid: center: %s, size: %s\n' % (self.centroid, self.size())

    def __contains__(self, point):
        return point in self.points

    def size(self):
        return len(self.points)

    def add(self, point):
        self.points.append(point)

    def remove(self, point):
        return self.points.remove(point)

    def distance(self, point):
        s = sum([(point[i] - self.centroid[i])**2 for i in range(0, len(point))])
        return math.sqrt(s)

    def recalculate(self):
        col_range = range(0, len(self.centroid))

        temp_sum = [0 for i in col_range]
        for point in self.points:
            temp_sum = [temp_sum[i] + point[i] for i in col_range]

        avg_point = [float(temp_sum[i]/self.size()) for i in col_range]
        self.centroid = avg_point

    def plot(self):
        plt.scatter([p[0] for p in self.points], [p[1] for p in self.points])

def main(args):
    filename = args[1]
    k = int(args[2])
    print('filename: %s' % filename)
    print('k: %s' % k)

    data = getData(filename)

    # list of Centroids, each with its list of points in its cluster
    clusters = getInitialClusters(data, k)

    # add points to closest initial centroid
    for d in data:
        closest = getClosestCluster(d, clusters)
        closest.add(d)

    # track whether any points have moved
    hasChanged = True
    loopCount = 0
    MAX_ITERATIONS = 500

    while hasChanged and loopCount < MAX_ITERATIONS:
        loopCount += 1

        # recalculate the centroid centers
        [c.recalculate() for c in clusters]

        # for each point in each centroid, calculate which centroid is closest
        # if it is closer to a different centroid, move it
        for cluster in clusters:
            for point in cluster.points:
                closest = getClosestCluster(point, clusters)
                if closest != cluster:
                    # move from cluster to closest
                    movePoint(point, cluster, closest)
                    hasChanged = True
                    
    # OPTION: create png image of the different clusters
    if '-i' in args:
        for cluster in clusters:
            cluster.plot()
        plt.savefig('%s_%s' % (filename.split('.')[0], k))

def movePoint(point, fromCluster, toCluster):
    # transfer point from one cluster to another
    fromCluster.remove(point)
    toCluster.add(point)

def getInitialClusters(data, k):
    # pick random points from dataset, must be unique
    centroids = []
    while len(centroids) < k:
        point = data[math.floor(random.random()*len(data))]
        if point not in centroids:
            centroids.append(point)
    # wrap in Centroid object
    return [Cluster(c) for c in centroids]

def getClosestCluster(point, clusters):
    closestDist = sys.maxsize
    closestCluster = None

    # loop through, keep track of closest one
    for cluster in clusters:
        dist = cluster.distance(point)
        if dist < closestDist:
            closestDist = dist
            closestCluster = cluster

    return closestCluster

def getData(filename):
    # open file, and return data in memory
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        rows = [[int(i) for i in r] for r in reader]
    return rows

if __name__ == '__main__':
    args = sys.argv
    main(args)
