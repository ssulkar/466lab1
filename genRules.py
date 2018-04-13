def genRules(F, minCof):
    for f in [x for x in F if len(x) >= 2]:
        H = []
        for s in f:
            if confidenceT(f, [s]) >= minConf:
                duplicate = False
                for h in H:
                    if set(f-[s]->[s]) == set(h):
                        duplicate = True
                        break
                if not duplicate:
                    H.append(f-[s]->[s])
        #apGenRules(f, H)

