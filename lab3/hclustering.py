import sys
import csv
import math
import numpy as np
from heapq import nsmallest

def main(args):
    if (len(args) < 2 or len(args) > 3):
        print("Usage: python3 hclustering <Filename> [<threshold>]")
    else: 
        filename = args[1]
        
        #Threshold???
        threshold = 0
        if(len(args) == 3):
            threshold = args[2]
        
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(data) for i, data in enumerate(r) if header[i] != '0'] for r in reader if len(r) > 0]
        
        C = agglomerative(rows)
        
        #print XML???
        printXML(C)
        
# distance between n-D points
def distanceFormula(a, b):
    #return (math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2)))
    sum = 0
    for i in range(len(a)):
        sum += (a[i]-b[i])**2
    return math.sqrt(sum)
    
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
    return row, col, smallestValue

def singleLinkMethod(distanceMatrix, s, r):
    for i in range(s):
        distanceMatrix[s][i] = min(distanceMatrix[s][i], distanceMatrix[r][i])
        distanceMatrix[i][s] = min(distanceMatrix[i][s], distanceMatrix[i][r])
    #trim row r
    distanceMatrix.pop(r)
    #trim col r
    for i in range(len(distanceMatrix)):
        distanceMatrix[i].pop(r)
    
    return distanceMatrix
        

def agglomerative(D):
    C = [(tuple(point)) for point in D]
    
    # create distanceMatrix
    distanceMatrix = initializeDistanceMatrix(len(C))
    for j in range(len(C)):
        for k in range(j+1, len(C)):
            distanceMatrix[j][k] = distanceFormula(C[j], C[k])
      
    while len(C) > 1:
        # indexes of two closest clusters
        s, r, height = argMin(distanceMatrix)
        # recalculate distance matrix
        distanceMatrix = singleLinkMethod(distanceMatrix, s, r)
        # merge clusters
        C[s] = [C[s], C[r], height]
        C.pop(r)
    return C
 
def printXML (C):
    print(C)
        
if __name__ == '__main__':
    args = sys.argv
    main(args)