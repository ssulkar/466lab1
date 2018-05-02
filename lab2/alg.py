import random
import math
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)

import d_tree

def c45(D, A, T, threshold):
    dominant, homogenous = getDomClass(D)

    # TODO these can be in the same if statement
    if homogenous:
        n = d_tree.Node(dominant)
        logger.info('homogenous (%d) -> created node: %s' % (len(D), dominant))
        return n
    # no more attributes to split on, so pick dominant classification
    elif len(A) == 0:
        n = d_tree.Node(dominant)
        logger.info('no attributes -> created node: %s' % dominant)
        return n
    else:
        splitIndex = selectSplittingAttribute(D, A, threshold)
        if splitIndex == None:
            n = d_tree.Node(dominant)
            logger.info('no split -> created node: %s' % dominant)
            return n

        splitData = split(D, A, splitIndex)

        A[splitIndex][1] = -1
        splitAttr = A[splitIndex][0] # removes attribute from future consideration
        logger.info('splitting on: %s' % splitAttr)
        n = d_tree.Node(splitAttr)
        for k, v in splitData.items():
            if len(v) != 0:
                # logger.debug('creating edge: %s' % k)
                e = d_tree.Edge(k, c45(v, A, T, threshold))
                n.edges.append(e)
        return n

def selectSplittingAttribute(D, A, threshold):
    p0 = entropy(D)
    gain = [0 for a in A]
    for k, v in A:
        # check for columns to skip
        if v != -1:
            index = A.index([k, v])
            gain[index] = p0 - entropyAttr(D, A, index)
    
    logger.debug('gain[]: %s' % gain)
    logger.debug('max(gain): %s' % max(gain))
    bestIndex = gain.index(max(gain))
    
    if gain[bestIndex] > threshold :
        logger.debug('selected splitting attribute: %s' % A[bestIndex])
        return bestIndex
    else:
        return None

# calculates the entropy of a dataset given an attribute to split on
def entropyAttr(D, A, splitIndex):
    # split into subsets
    splitData = split(D, A, splitIndex)
    lenD = len(D)
    # find entropy of each subset
    entropies = []
    for k, v in splitData.items():
        # weight each value by it's length. len(subset)/len(all)
        e = entropy(v)
        entropies.append(float(len(v)/lenD)*e)
    # add together
    return sum(entropies)

# calculates entropy of given dataset
def entropy(D):
    e = 0 # entropy of empty set is 0
    if len(D) != 0:
        classList = list(set([d[-1] for d in D]))
        classCount = [0 for i in classList]
        # count the occurances of each class
        for d in D:
            classCount[classList.index(d[-1])] += 1
        # calculate entropy
        for n in classCount:
            n = float(n / len(D))
            e += n * log(n)
    return -1*e

# splits given data based on given attribute index
def split(D, A, splitIndex):
    splitData = {}
    # populate dict with (attribute, subset) pairs
    for d in D:
        attribute = d[splitIndex]
        # creates empty list if doesn't exist
        splitData[attribute] = splitData.get(attribute, [])
        splitData[attribute].append(d)
    # OrderedDict makes algorithm deterministic
    return OrderedDict(sorted(splitData.items()))

# returns dominant class and whether it is homogenous
def getDomClass(D):
    counters = {}
    for d in D:
        counters[getClass(d)] = counters.get(getClass(d), 0) + 1

    cur_largest = 0
    cur_class = ''
    for k, v in OrderedDict(sorted(counters.items())).items():
        if int(v) > cur_largest:
            cur_largest = int(v)
            cur_class = k
    return cur_class, cur_largest == len(D)

def log(k):
    val = 0
    if k!=0:
        val = math.log(k,2)
    return val

def getClass(data):
    return data[-1]
