def candidateGen(F, k):
    C = []

    F_sizeK = list(itertools.combinations(F, k))
    for f1 in F_sizeK:
        for f2 in F_sizeK:
            c = list(set().union(f1, f2))
            if len(c) == k + 1:
                flag = true
                c_sizeK = list(itertools.combinations(c, k))
                for s in c_sizeK:
                    if s not in F:
                        flag = false
                        break
                if flag:
                    C = list(set().union(C, c))
    return C
