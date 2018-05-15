import sys
import csv
import math
from heapq import nsmallest

def main(args):
    testingstuff()
    '''if (len(args) < 2 or len(args) > 3):
        print("Usage: python3 hclustering <Filename> [<threshold>]")
    else: 
        filename = args[1]
        threshold = 0

        rows = []
        with open(filename, 'r') as f:
           reader = csv.reader(f)
           rows = [[int(i) for i in r] for r in reader]
        
        if (len(args) == 3):
	    threshold = args[2]'''

def testingstuff():
    C = [[2,2],[2,3],[3,4],[2,1],[6,10],[1,4],[5,1]]
    print(distanceMatrix(C))


# C is a list of points ex: [[1,1],[1,2]]
# returns matrix of distances ex: [[0,1],[0,1]]
def createDistanceMatrix(C):
    matrix = []
    for i, a in enumerate(C):
        currentRow = []
        for j, b in enumerate(C):
            distance = (math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2)))
            currentRow.append(distance)
        matrix.append(currentRow)
    return matrix
    
def agglomerative(D):
    # each point is assigned its own cluster
    clusters = D[:]
    # stop merging when all clusters are merged into one cluster
    while len(clusters) > 1:
        # compute distance matrix
        d = createDistanceMatrix(clusters)
        # select a pair of clusters with the shortest distance
        minDistances = nsmallest(2, distanceMatrix)        
    return clusters

if __name__ == '__main__':
    args = sys.argv
    main(args)