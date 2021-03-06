import math

import logging
logger = logging.getLogger(__name__)

def selectSplittingAttribute(D, A, C, threshold):
    logging.debug('len(D): %s' % len(D))
    logging.debug('A: %s' % A)
    logging.debug('C: %s' % C)

    p = {}
    gain = {}

    p0 = entropy(D, C)
    for a in A:
        logger.debug('a: %s' % a)
        if a == C:
            continue

        if len(set([x[a] for x in D])) > 6:
            x = findBestSplit(a, D, C)
            logger.debug('x: %s' % x)

            ent = entropyX(D, a, C, x)
            logger.debug('ent: %s' % ent)

            p[a] = ent
        else:
            ent = entropyA(D, a, C)
            logger.debug('ent: %s' % ent)

            p[a] = ent
        gain_a = p0 - p[a]
        logger.debug('gain_a: %s' % gain_a)
        gain[a] = gain_a
    best = findMaxGain(gain)
    gain_best = gain[best]
    logger.debug('gain_best: %s' % gain_best)

    if gain_best > threshold:
        return best
    return None

def findBestSplit(a, D, C):
    classes = set([x[C] for x in D])

    counts = {}
    gain = {}
    
    p0 = entropy(D, C)

    for c in classes:
        counts[c] = {}

    for d in D:
        for c in classes:
            if d[a] not in counts[c]:
                counts[c][d[a]] = 0

            if d[C] == c:
                counts[c][d[a]] = counts[c][d[a]] + 1
                
    for x in counts[list(counts.keys())[0]]:
        gain[x] = p0 - entropyC(D, a, x, counts)

    return findMaxGain(gain)

def entropy(D, C):
    classes = set([x[C] for x in D])
    splitLists = [[y for y in D if y[C] == x] for x in classes]

    ent = 0
    for x in splitLists:
        pr = len(x)/float(len(D))

        if pr != 0:
            ent -= pr * math.log(pr, 2)

    return ent

def entropyA(D, A, C):
    values = set([x[A] for x in D])
    splitLists = [[y for y in D if y[A] == x] for x in values]
    
    ent = 0
    for x in splitLists:
        ent += len(x)/float(len(D)) * entropy(x, C)

    return ent

def entropyX(D, A, C, X):
    splitLists = [[x for x in D if x[A] <= X],[x for x in D if x[A] > X]]
    
    ent = 0
    for x in splitLists:
        ent += len(x)/float(len(D)) * entropy(x, C)

    return ent

def entropyC(D, A, threshold, counts):
    valuesBelow = set([x[A] for x in D if x[A] <= threshold])
    valuesAbove = set([x[A] for x in D if x[A] > threshold])

    totalsBelow = {}
    totalsAbove = {}

    totalAttrBelow = 0
    totalAttrAbove = 0

    ent = 0

    for c in counts:
        total = 0
        for v in valuesBelow:
            total += counts[c][v]
        totalAttrBelow += total
        totalsBelow[c] = total

        total = 0
        for v in valuesAbove:
            total += counts[c][v]
        totalAttrAbove += total
        totalsAbove[c] = total
    
    for totalForClass in totalsBelow.values():
        if totalForClass > 0:
            pr = totalForClass / float(totalAttrBelow)
            ent += totalAttrBelow / float(len(D)) * -pr * math.log(pr,2)

    for totalForClass in totalsAbove.values():
        if totalForClass > 0:
            pr = totalForClass / float(totalAttrAbove)
            ent += totalAttrAbove / float(len(D)) * -pr * math.log(pr,2)

    return ent

def findMaxGain(gain):
    return max(gain, key=gain.get)
