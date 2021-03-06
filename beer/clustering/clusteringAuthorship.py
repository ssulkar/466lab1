import sys
import csv
import math
import numpy as np
from heapq import nsmallest
import xml.etree.ElementTree as ET
import xml.dom.minidom

def main(args):
    if (len(args) < 2 or len(args) > 3):
        print("Usage: python3 hclustering <Filename> [<threshold>]")
    else:
        #data = np.load(args[1])
        #data = [[1, 0], [3, 0], [6, 0]]
        filename = args[1]
        
        
        data = []
        
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            data = [[float(data) for i, data in enumerate(r) if header[i] != '0'] for r in reader if len(r) > 0]

        
        
        C = agglomerative(data, 1)
        newFileName = args[1]+".xml"
        printXML(C, newFileName) 
        
# distance between n-D points
def distanceFormula(a, b):
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
        

def agglomerative(D, csize):
    C = [(tuple(point)) for point in D]
    
    # create distanceMatrix
    distanceMatrix = initializeDistanceMatrix(len(C))
    for j in range(len(C)):
        for k in range(j+1, len(C)):
            distanceMatrix[j][k] = distanceFormula(C[j], C[k])
    while len(C) > csize:
        print(len(C))
        # indexes of two closest clusters
        s, r, height = argMin(distanceMatrix)
        # recalculate distance matrix
        distanceMatrix = singleLinkMethod(distanceMatrix, s, r)
        # merge clusters
        C[s] = [C[s], C[r], height]
        C.pop(r)
    return C
 
#[[[(1, 0), (3, 0), 2.0], (6, 0), 5.0]]

def printXML (C, newFileName):
    root = None
    for i in range(len(C[0])):
        if(isinstance(C[0][i], float)):
            root = ET.Element("Tree")
            root.text = "Height: " + str(C[0][i])
            
            #C[0].pop(i)
            printXMLHelper(C[0], root)
            break
    
    uglyxml = ET.tostring(root, encoding='utf8', method='xml')
    parsexml = xml.dom.minidom.parseString(uglyxml)
    
    f = open(newFileName, "w")
    f.write(parsexml.toprettyxml())
    f.close()
    
def printXMLHelper(C, root):
    #tuple
    leaves = []
    #list
    nodes = []#None
    #float  
    
    currentRoot = root
    
    for i in range(len(C)):
        if(isinstance(C[i], tuple)):
            leaves.append(C[i])
        elif(isinstance(C[i], list)):
            nodes.append(C[i])
       
            
            
    if(len(nodes) != 0):
        height = None
        for i in range(len(nodes)):
            for j in range(len(nodes[i])):
                if(isinstance(nodes[i][j], float)):
                    height = nodes[i][j]
                    break
            currentRoot = ET.SubElement(root, "Node")
            currentRoot.text = "Height: " + str(height)
            printXMLHelper(nodes[i], currentRoot)
        #root.append(currentRoot)
        #printXMLHelper(node, root)        
    
    if(len(leaves) != 0):
        for i in range(len(leaves)):
            currentRoot = ET.SubElement(root, "Leaf")
            currentRoot.text = str(leaves[i])
            #ElementTree.SubElement(root, currentRoot)
            #root.append(currentRoot)
    
   
if __name__ == '__main__':
    args = sys.argv
    main(args)
