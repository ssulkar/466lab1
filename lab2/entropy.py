import random
import math

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
