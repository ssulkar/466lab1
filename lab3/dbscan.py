import matplotlib
matplotlib.use('Agg')

import sys
import math
import random
import csv
import time

import matplotlib.pyplot as plt
import numpy as np

PRINT_POINTS = False
SHOW_CIRCLES = False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Clusters are groupings of data points. Each cluster has a centroid
# that represents the average of all the points in the Cluster.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Cluster:
    def __init__(self, start_point, index):
        # needed for output
        self.index = index
        # points with num_points
        self.core_points = [start_point]
        # list of points in this cluster
        self.reachable_points = []

    def __repr__(self):
        # output based on spec
        s = 'Cluster %s:\n' % (self.index)
        if self.reachable_points:
            distances = []
            for r in self.reachable_points:
                r_distances = []
                for p in self.core_points:
                    r_distances.append(distance(r, p))
                distances.append(min(r_distances))
            s += 'Max Dist. to Center: %s\nMin Dist. to Center: %s\nAvg Dist. to Center: %s\n' % (max(distances), min(distances), float(sum(distances)/len(distances)))
        else:
            s += 'No distance statistics, all core points\n'
        s += '%s Core Points:\n' % (len(self.core_points))
        if PRINT_POINTS:
            for point in self.core_points:
                s += '%s\n' % str(point)
        s += '%s Reachable Points:\n' % (len(self.reachable_points))
        if PRINT_POINTS:
            for point in self.reachable_points:
                s += '%s\n' % str(point)
        return s

    def __contains__(self, point):
        return point in self.core_points or point in self.reachable_points

    def expand(self, data, index, ep, dist_matrix, num_points):
        point = data[index]
        neighbors = getNeighbors(data, index, ep, dist_matrix)

        if len(neighbors) >= num_points:
            # this is a core point, must recursively expand
            if point not in self.core_points:
                self.core_points.append(point)
        else:
            if point not in self.reachable_points:
                self.reachable_points.append(point)

        for neighbor in neighbors:
            if neighbor not in self:
                # time.sleep(3)
                self.expand(data, data.index(neighbor), ep, dist_matrix, num_points) 
            
    def plot(self, x_index, y_index, ep):
        ax = plt.gca()
        if SHOW_CIRCLES:
            for p in self.reachable_points:
                circle2 = plt.Circle([p[x_index], p[y_index]], ep, color=(0, 0, 1, .5), fill=False)
                ax.add_artist(circle2)
            for p in self.core_points:
                circle2 = plt.Circle([p[x_index], p[y_index]], ep, color=(1, 0, 0, .5), fill=False)
                ax.add_artist(circle2)
        plt.scatter([p[x_index] for p in self.reachable_points], [p[y_index] for p in self.reachable_points], c='b')
        plt.scatter([p[x_index] for p in self.core_points], [p[y_index] for p in self.core_points], c='r')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Main program
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def main(args):
    filename = args[1]
    ep = float(args[2])
    num_points = int(args[3])

    global PRINT_POINTS
    # verbose cluster logging
    if '-v' in args:
        PRINT_POINTS = True

    global SHOW_CIRCLES
    if '-c' in args:
        SHOW_CIRCLES = True

    # open file and load data
    data = getData(filename)

    dist_matrix = getDistances(data)

    clusters = []
    outliers = []

    for i in range(0, len(data)):
        no_clusters = True
        for cluster in clusters:
            if data[i] in cluster:
                no_clusters = False
        if no_clusters:
            # so the point hasn't been assigned yet, either a new cluster or outlier
            neighbors = getNeighbors(data, i, ep, dist_matrix)
            if len(neighbors) >= num_points:
                c = Cluster(data[i], len(clusters))
                clusters.append(c)
                c.expand(data, i, ep, dist_matrix, num_points)

    # if the point still hasn't been added to a cluster, it's an outlier
    for i in range(0, len(data)):
        no_clusters = True
        for cluster in clusters:
            if data[i] in cluster:
                no_clusters = False
        if no_clusters:
            outliers.append(data[i])

    # output
    for cluster in clusters:
        print(cluster)

    print('%s Outliers:' % len(outliers))
    if PRINT_POINTS:
        for point in outliers:
            print(point)

    # graphing
    if '-i' in args:
        x_index = int(args[args.index('-i') + 1])
        y_index = int(args[args.index('-i') + 2])
        plt.scatter([p[x_index] for p in data], [p[y_index] for p in data], c='k')
        for c in clusters:
            c.plot(x_index, y_index, ep)
            
        for o in outliers:
            plt.scatter(o[x_index], o[y_index], c='y')

        plt.savefig('%s_dbscan_%s_%s_%s_%s' % (filename.split('.')[0], str(ep).replace('.', '_'), num_points, x_index, y_index))

def getNeighbors(data, index, ep, dist_matrix):
    # get the row that contains all distances to all points relative
    # to the given index of the point
    neighbors = []
    point = data[index]
    row = dist_matrix[index]
    for i, d in enumerate(row):
        # check epsilon and check duplicates
        if d < ep and i != index:
            neighbors.append(data[i])
    return neighbors

def getDistances(data):
    n = len(data)
    # create N x N matrix
    m = [[0 for i in range(0, n)] for j in range(0, n)]
    # compute distance for each pair of points
    for i, p1 in enumerate(data):
        for j, p2 in enumerate(data):
            m[i][j] = distance(p1, p2)

    return m

def distance(p1, p2):
    s = sum([(p1[i] - p2[i])**2 for i in range(0, len(p1))])
    return math.sqrt(s)


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
