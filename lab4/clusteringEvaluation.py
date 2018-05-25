import sys
import csv
import math
import numpy as np
from heapq import nsmallest
import clusteringAuthorship
import xml.etree.ElementTree as ET
import xml.dom.minidom

def main(args):
     if (len(args) < 2 or len(args) > 3):
        print("Usage: python3 hclustering <Filename> [<threshold>]")
     else:
        data = np.load(args[1])
        
        #C is a cluster list of size 50
        C = clusteringAuthorship.agglomerative(data, 50)
        newFileName = args[1]+".xml"
        clusteringAuthorship.printXML(C, newFileName) 
        
if __name__ == '__main__':
    args = sys.argv
    main(args)
