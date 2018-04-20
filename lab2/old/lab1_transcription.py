import sys
import csv
import itertools
# import pandas

def main():

    if len(sys.argv) < 4:
        print "Usage: python lab1.py filename minsup minconf"
        return
    minsup = float(sys.argv[2])
    minconf = float(sys.argv[3])
    filename = sys.argv[1]
    T = []
    goods = []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
	T = [map(str.strip, row)[1:] for row in reader][::2]
    del T[0]

    with open("factors.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        goods = [row for row in reader]
    del goods[0]

    # init itemset
    I = [str(i) for i in range(0, len(goods))]

    F =  apriori(T, I, minsup)
    sky = getSkylineItems(F)
    '''
    print "Frequent Item Sets: " + str(len(F))
    [printFreqItem(i, goods) for i in F]
    print
    '''

    print "Frequent Item Sets: " + str(len(sky))
    [printFreqItem(i, goods, T) for i in getSkylineItems(sky)]
    print

    '''
    R = genRules(F, minconf, T)
    sky = getSkylineRules(R)
    print "Association Rules: " + str(len(sky))
    [printRule(r, goods, T) for r in sky]
    '''

def getSkylineRules(R):
    r = R[:]
    for i in range(len(R) - 1):
        for j in range(i + 1, len(R)):
            f1 = R[i]
            f2 = R[j]
            
            if f1 != None and f2 != None:
                if set(f1[0]).issubset(set(f2[0])) and f1[1] == f2[1]:
                    r[i] = None
                    break

    return [x for x in r if x != None]

def getSkylineItems(F):
    r = F[:]
    for i in range(len(F) - 1):
        for j in range(i + 1, len(F)):
            f1 = F[i]
            f2 = F[j]
        
            if f1 != None and f2 != None:
                if set(f1).issubset(set(f2)):
                    r[i] = None
                    break
    
    return [x for x in r if x != None]


def getName(flavorFood):
    #return flavorFood[1].strip('\'') + ' ' + flavorFood[0].strip('\'')
    return flavorFood[0].strip('\'') + ' ' + flavorFood[1].strip('\'')

def printFreqItem(itemSet, goods, T):
    items = [goods[int(i)-1] for i in itemSet]
    print ", ".join(items) + "[sup=" + str(supportT(itemSet, T)) + "]"

def printRule(rule, goods, T):
    left = [goods[int(i)-1] for i in rule[0]]
    right = goods[int(list(rule[1])[0])-1]
    print ", ".join(left) + " ---> " + right + "[sup=" + str(support(rule[0], rule[1], T)) + ", conf=" + str(confidence(rule[0], rule[1], T)) + "]"

def supportT(X, T):
    freqs = [t for t in T if set(X).issubset(set(t))]
    return len(freqs)/float(len(T))

def confidence (X, Y, T):
    top = [t for t in T if (set().union(set(X), set(Y))).issubset(set(t))]
    bot = [t for t in T if set(X).issubset(set(t))]
    return len(top)/float(len(bot))

def support (X, Y, T):
    top = [t for t in T if (set().union(set(X), set(Y))).issubset(set(t))]
    return len(top)/float(len(T))

def apriori(T, I, minsup):
    F_k = [[i] for i in I if supportT([i], T) >= minsup]
    F = F_k[:]
    k = 2

    while F_k:
        C = candidateGen(F_k, k-1)
        count = {}
        for c in C:
            count[tuple(c)] = 0;
        for t in T:
            for c in C:
                if set(c).issubset(set(t)):
                    count[tuple(c)] += 1

        F_k = [c for c in C if count[tuple(c)]/float(len(T)) >= minsup]
        F += F_k
        k += 1
    return F

def candidateGen(F, k):
    C = []
    F_sizeK = [f for f in F if len(f) == k]
    for f1 in F_sizeK:
        for f2 in F_sizeK:
            c = list(set().union(f1, f2))

            if len(c) == k + 1:
                flag = True
                c_sizeK = [list(x) for x in list(itertools.combinations(c, k))]
                for s in c_sizeK:
                    if s not in F:
                        flag = False
                        break
                if flag:
                    #C = list(set().union(C, [c]))
                    duplicate = False
                    for x in C:
                        if set(x) == set(c):
                            duplicate = True
                            break
                    if not duplicate:
                        C.append(c)
    return C

def genRules(F, minConf, T):
    H = []
    for f in [x for x in F if len(x) >= 2]:
        for s in f:
            if confidence(list(set(f)-set([s])), [s], T) >= minConf:
                duplicate = False
                for h in H: 
                    if (set(f)-set([s]),set([s])) == h:
                        duplicate = True
                        break
                if not duplicate:
                    H.append((set(f)-set([s]), set([s])))
        #apGenRules(f, H)
    return H



if __name__ == '__main__':
    main()
