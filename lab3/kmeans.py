import matplotlib
matplotlib.use('Agg')

import sys
import math
import random
import csv

import matplotlib.pyplot as plt

PRINT_POINTS = False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Clusters are groupings of data points. Each cluster has a centroid
# that represents the average of all the points in the Cluster.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Cluster:
    def __init__(self, centroid, index):
        # needed for output
        self.index = index
        # centroid is the average of all the points. updated with recalculate()
        self.centroid = centroid
        # list of points in this cluster
        self.points = []

    def __repr__(self):
        # output based on spec
        s = 'Cluster %s:\nCenter: %s,\n' % (self.index, self.centroid)
        distances = list(map(self.distance, self.points))
        s += 'Max Dist. to Center: %s\nMin Dist. to Center: %s\nAvg Dist. to Center: %s\n' % (max(distances), min(distances), float(sum(distances)/len(distances)))
        s += '%s Points:\n' % (self.size())
        if PRINT_POINTS:
            for point in self.points:
                s += '%s\n' % str(point)
        return s

    def __contains__(self, point):
        return point in self.points

    def size(self):
        return len(self.points)

    def dimensions(self):
        return len(self.centroid)

    def add(self, point):
        self.points.append(point)

    def remove(self, point):
        self.points.remove(point)

    def distance(self, point):
        s = sum([(point[i] - self.centroid[i])**2 for i in range(0, len(point))])
        return math.sqrt(s)

    def recalculate(self):
        col_range = range(0, self.dimensions())
        temp_sum = [0 for i in col_range]

        # sum up data by column
        for point in self.points:
            temp_sum = [temp_sum[i] + point[i] for i in col_range]

        # divide each column by size to get average
        avg_point = [float(temp_sum[i]/self.size()) for i in col_range]
        self.centroid = avg_point

    def plot(self, x_index, y_index):
        plt.scatter([p[x_index] for p in self.points], [p[y_index] for p in self.points])
        plt.scatter(self.centroid[x_index], self.centroid[y_index], c='k', s=10**2, marker='^')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Main program
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def main(args):
    # command line args
    filename = args[1]
    k = int(args[2])

    global PRINT_POINTS
    # verbose cluster logging
    if '-v' in args:
        PRINT_POINTS = True

    # internal stop conditions
    MAX_ITERATIONS = 500
    MIN_CHANGES = 1

    # open file and load data
    data = getData(filename)

    # list of clusters
    clusters = []
    # deterministic cluster starting points
    if '-d' in args:
        clusters = getDistributedClusters(data, k)
    # defaults to random starting centroids
    else:
        clusters = getRandomClusters(data, k)

    # add points to closest initial centroid
    for d in data:
        closest = getClosestCluster(d, clusters)
        closest.add(d)

    # track how many points have moved
    changes = MIN_CHANGES + 1
    loopCount = 0

    # loop until no points move or hard stop
    while changes > MIN_CHANGES and loopCount < MAX_ITERATIONS:
        loopCount += 1
        changes = 0

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
                    changes += 1
                    
    # output cluster information
    for cluster in clusters:
        print(cluster)

    # OPTION: create a png image for each combination of dimensions in 2D
    # for example, a dataset with dimensions (x, y, z) will generate 3 graphs:
    # f(x,y), f(x,z), f(y,z)
    # useful for determining the overall shape of the data
    if '-a' in args:
        for i in range(0, clusters[0].dimensions()):
            for j in range(i, clusters[0].dimensions()):
                if i != j:
                    for cluster in clusters:
                        cluster.plot(i, j)
                    plt.savefig('%s_k%s_%s_%s' % (filename.split('.')[0], k, i, j))
                    plt.clf()
                    
    # OPTION: create single png image of the different clusters
    # ARGS: the index of the columns to use for graphing in 2D
    elif '-i' in args:
        x_index = int(args[args.index('-i') + 1])
        y_index = int(args[args.index('-i') + 2])
        for cluster in clusters:
            cluster.plot(x_index, y_index)
        plt.savefig('%s_k%s_%s_%s' % (filename.split('.')[0], k, x_index, y_index))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Helper functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def movePoint(point, fromCluster, toCluster):
    # transfer point from one cluster to another
    fromCluster.remove(point)
    toCluster.add(point)

def getDistributedClusters(data, k):
    # deterministic for now, to make testing easier
    # grab k evenly distributed points
    return [Cluster(data[i], index) for index, i in enumerate(range(0, len(data), math.ceil(len(data)/k)))]

def getRandomClusters(data, k):
    # pick random points from dataset, must be unique
    centroids = []
    while len(centroids) < k:
        point = data[math.floor(random.random()*len(data))]
        if point not in centroids:
            centroids.append(point)
    # wrap in Centroid object
    return [Cluster(c, i) for i, c in enumerate(centroids)]

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
        header = next(reader)
        # uses header to determine if column should be ignored
        rows = [[float(data) for i, data in enumerate(r) if header[i] != '0'] for r in reader if len(r) > 0]
    return rows

if __name__ == '__main__':
    args = sys.argv
    main(args)
