import sys
import csv
import json
import xml.etree.ElementTree as ET
import logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import alg
import d_tree
import Classifier

def main(args):
    csvfile = str(args[1])    
    D = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        D = [row for row in reader]
    attributes = D[0]

    use_columns = D[1]
    A = [0 for x in range(len(attributes))]
    for i in range(len(attributes)):
        A[i] = [attributes[i], int(use_columns[i])]

    # ignore last column VOTE
    A[-1][1] = -1

    # grab main data
    D = D[3:]

    # split data
    k = int(args[2]) + 1

    size = len(D)//k
    
    remainder = len(D)%k
    sets = [0 for i in range(k)]
    i = 0
    j = 0
    while j < len(D):
        end = j + size
        if remainder > 0:
             end += 1
             remainder -= 1

        sets[i] = D[j:end]
        i += 1
        j = end

    # create decision trees
    total = 0
    total_correct = 0
    total_incorrect = 0
    accuracies = []
    errors = []

    supermatrix = [0, 0, 0, 0]
    for part in sets:
        for i in range(len(attributes)):
            A[i] = [attributes[i], int(use_columns[i])]

        # ignore last column VOTE
        A[-1][1] = -1

        T = alg.c45(part, A, d_tree.Node('root'), .01)
        
        xml = d_tree.toXML(d_tree.Tree(T))
        # output xml tree
        tmp = ET.fromstring(xml)
        tree = ET.ElementTree(tmp)
        xmlfile = 'output.xml'
        tree.write(xmlfile)

        # classify remaining set using trees
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        
        training = True
        # total, total_correct, total_incorrect, accuracy, error, matrix
        measures = Classifier.classify(part, attributes, root, training)
        total += measures[0]
        total_correct += measures[1]
        total_incorrect += measures[2]

        accuracies.append(measures[3])
        errors.append(measures[4])

        matrix = measures[5]

        # compute overall metrics
        supermatrix[0] += matrix[0]
        supermatrix[1] += matrix[1]
        supermatrix[2] += matrix[2]
        supermatrix[3] += matrix[3]
    print()
    print('Overall Confusion Matrix')
    print("TP = " + str(supermatrix[0]))
    print("TN = " + str(supermatrix[1]))
    print("FP = " + str(supermatrix[2]))
    print("FN = " + str(supermatrix[3]))
    print("recall = " + str(recall(supermatrix)))
    print("precision = " + str(precision(supermatrix)))
    print("PF = " + str(PF(supermatrix)))
    print("f_measure = " + str(f_measure(supermatrix)))
    print("overall_accuracy = " + str(overall_accuracy(total, total_correct)))
    print("overall_error = " + str(overall_error(total, total_incorrect)))
    print("average_accuracy = " + str(average_accuracy(accuracies)))
    print("average_error = " + str(average_error(errors)))

def average_accuracy(accuracies):
    return float(sum(accuracies)/len(accuracies))

def average_error(errors):
    return float(sum(errors)/len(errors))

def overall_accuracy(total, total_correct):
    return float(total_correct/total)

def overall_error(total, total_incorrect):
    return float(total_incorrect/total)

def precision(matrix):
    TP = matrix[0]
    FP = matrix[2]
    return float(TP / (TP + FP))

def recall(matrix):
    TP = matrix[0]
    FN = matrix[3]
    return float(TP / (TP + FN))

def PF(matrix):
    TN = matrix[1]
    FP = matrix[2]
    return float(FP / (FP + TN))

def f_measure(matrix):
    num = 2 * precision(matrix) * recall(matrix)
    dem = precision(matrix) * recall(matrix)
    return float(num/dem)

if __name__=='__main__':
    args = sys.argv
    main(args)
