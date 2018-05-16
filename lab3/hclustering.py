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
    D = [[2,2],[2,3],[3,4],[2,1],[6,10],[1,4],[5,1]]
    #print(createDistanceMatrix(C))
    #print(nsmallest(1,createDistanceMatrix(C)[0]))
    #print(getMinimumValue(createDistanceMatrix(C)))
    agglomerative(D))

def distanceFormula(a, b):
    return (math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2)))
    
def initializeDistanceMatrix(dimension):
    distanceMatrix = [[0 for i in range(dimension)] for j in range(dimension)]
    return distanceMatrix

def argMin (distanceMatrix):
    smallestValue = 0
    row, col = 0, 0
    for i in range(len(distanceMatrix)):
        for j in range(len(distanceMatrix)):
            currentValue = distanceMatrix[i][j]
            if (smallestValue == 0):
                smallestValue = currentValue 
                row, col = i, j
            elif (currentValue != 0 and currentValue < smallestValue):
                smallestValue = currentValue
                row, col = i, j
    return row, col    

#def averageLinkMethod():
def agglomerative(D):
    C = D[:]
    i = 1
    while len(C) > 1:
        distanceMatrix = initializeDistanceMatrix(len(C))
        for j in range(len(C)):
            for k in range(j+1, len(C)):
                distanceMatrix[j][k] = distanceFormula(C[j], C[k])
        s, r = argMin(distanceMatrix)
        #TODO need to use averageLink to merge clusters.
        '''for j in range(len(C)-1):
            if j != r and j != s:
                C[j+1] = C[j]
            elif j == r:
                C[j] = C[r], C[s]'''
        print (distanceMatrix)
        print (s, r)
        break
    
if __name__ == '__main__':
    args = sys.argv
    main(args)