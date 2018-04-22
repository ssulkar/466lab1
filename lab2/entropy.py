import random

def entropy(D):
    if (len(D) == 0):
        return 0;
    
    classCount = []
    for i in range(len(D)):
        pass        

    val = []
    for i in range(len(D)):
        val[i] = log(D[i])

def log(k):
    val = 0
    if k!=0:
        val = math.log(k,2)
    return val

def selectSplittingAttribute (A, D, threshold):
    if len(A) < 3:
        return None
    else:
        return A[random.randint(1, len(A) - 1)]
