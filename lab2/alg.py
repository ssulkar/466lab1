import random
import math

import d_tree

def c45(D, A, T, threshold):
    dominant, homogenous = getDomClass(D)

    # TODO these can be in the same if statement
    if homogenous:
        n = d_tree.Node(dominant)
        return n
    # no more attributes to split on, so pick dominant classification
    elif len(A) == 0:
        n = d_tree.Node(dominant)
        return n
    else:
        splitAttr = selectSplittingAttribute(A, D, threshold)
        if splitAttr == None:
            n = d_tree.Node(dominant)
            return n

        splitIndex = A.index(splitAttr)
        A.remove(splitAttr) # removes attribute from future consideration
        
        splitData = {}
        for d in D:
            splitData[d[splitIndex]] = splitData.get(d[splitIndex], [])
            splitData[d[splitIndex]].append(d)

        n = d_tree.Node(splitAttr)
        for k, v in splitData.items():
            if len(v) != 0:
                e = d_tree.Edge(k, c45(v, A, T, threshold))
                n.edges.append(e)
        return n

# returns dominant class and whether it is homogenous
def getDomClass(D):
    counters = {}
    for d in D:
        counters[getClass(d)] = counters.get(getClass(d), 0) + 1

    cur_largest = 0
    cur_class = ''
    for k, v in counters.items():
        if int(v) > cur_largest:
            cur_largest = int(v)
            cur_class = k
    return cur_class, cur_largest == len(D)

def getClass(data):
    return data[-1]

def entropy(dataSet):
    e = float(0) #when dataSet is empty the entropy is 0
    if len(dataSet) != 0:
        classList = list(set([d[-1] for d in dataSet])) #get classes and remove duplicates
        classCount = [float(0) for i in classList]
        for d in dataSet:
            classCount[classList.index(d[-1])] += 1 #increment the numerator
        
        for n in classCount:
            n = n/len(dataSet) #divide by the dataSet size
            e += n * log (n)
    
    return -1*e

def log(k):
    val = 0
    if k!=0:
        val = math.log(k,2)
    return val

#TODO
def selectSplittingAttribute (A, D, threshold):
    p0 = entropy(D)
    gain = [0 for a in A]
    for i in range(len(gain)):
        gain[i] = p0 - entropy(A[i])
    
    bestIndex = gain.index(max(gain))
    
    if gain[bestIndex] > threshold :
        return A[bestIndex]
    else:
        return None    
    '''
    if len(A) < 3:
        return None
    else:
        return A[random.randint(1, len(A) - 1)]'''
