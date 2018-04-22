import d_tree
import entropy

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
        splitAttr = entropy.selectSplittingAttribute(A, D, threshold)
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