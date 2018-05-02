import sys
import csv
import json
import xml.etree.ElementTree as ET

'''
                | classified true  |  classified false      |
|actually true  |    TP            |   FN                   |
|actually false |    FP            |   TN                   |
'''

#T is the classifier
def precision(TP, FP):
    return TP / float(TP + FP)

def recall(TP, FN):
    return TP / float (TP + FN)

def PF(FP, TN):
    return FP / float (FP + TN)
       
def updateMatrix (matrix, classified, actual):
    if classified == actual and actual == True:
        matrix[0] = matrix[0] + 1
    elif classified == actual and actual == False:
        matrix[1] = matrix[1] + 1
    elif classified == False and actual == True:
        matrix[2] = matrix[2] + 1
    elif classified == True and actual == False:
        matrix[3] = matrix[3] + 1

def main(args):    
    classifiedList = []
    actualList = []
    
    #[TP, TN, FP, FN]
    matrix = [0, 0, 0, 0]

    for i in range(len(classifiedList)):
        updateMatrix(matrix, classifiedList[i], actualList[i])
    print "TP = " + str(matrix[0])
    print "TN = " + str(matrix[1])
    print "FP = " + str(matrix[2])
    print "FN = " + str(matrix[3])    

if __name__=='__main__':

    args = sys.argv
    main(args)
