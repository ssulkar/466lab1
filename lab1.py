import sys
import csv
import itertools
# import pandas

def main():

    if len(sys.argv) < 3:
        print "Usage: python lab1.py filename minsup"
        return
    minsup = float(sys.argv[2])
    filename = sys.argv[1]
    T = []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
	T = [map(str.strip, row)[1:] for row in reader]

    # init itemset
    I = [str(i) for i in range(0, 50)]
    print apriori(T, I, minsup)

def supportT(X, T):
    freqs = [t for t in T if set(X).issubset(set(t))]
    return len(freqs)/float(len(T))

def apriori(T, I, minsup):
    F_k = [[i] for i in I if supportT([i], T) >= minsup]
    F = F_k
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

        F_k = [c for c in C if count[tuple(c)]/float(len(C)) >= minsup]
        F += F_k
        k += 1
    return F

def candidateGen(F, k):
    C = []
    F_sizeK = [f for f in F if len(f) == k]
    print k
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

if __name__ == '__main__':
    main()
