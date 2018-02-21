import math

#sampleSet = [('A', 'e'), ('T', '-'), ('A', 'e'), ('T', '-')]
#sample attributeTable = {'A': {'one' : 0, 'two' : 1}, 'T' : {'one': 1, 'two' : 1}}

def splitSet(fullSet, attribute, attributeTable):
    subset1 = []
    subset2 = []
    for t in fullSet:
        abv = t[0]
        if (attributeTable[abv][attribute] == 0):
            subset1.append(t)
        else:
            subset2.append(t)
            
    return subset1, subset2
    

def calculateEntropy(set):
    numTotal = len(set) + 0.0
    if numTotal == 0.0:
        return 0.0
    numPos = 0.0
    numNeg = 0.0
    for t in set:
        if t[1] == 'e':
            numPos = numPos + 1
        else:
            numNeg = numNeg + 1
    propPos = numPos / numTotal
    propNeg = numNeg / numTotal
    if (propPos == 0.0 or propNeg == 0.0):
        return 0.0
    output = -propPos * math.log2(propPos)
    output = output - (propNeg * math.log2(propNeg))
    return output

def calculateGain(fullSet, subset1, subset2):
    propSubset1 = (len(subset1) + 0.0) / (len(fullSet) + 0.0)
    propSubset2 = (len(subset2) + 0.0) / (len(fullSet) + 0.0)
    output = calculateEntropy(fullSet)
    output = output - (propSubset1 * calculateEntropy(subset1))
    output = output - (propSubset2 * calculateEntropy(subset2))
    return output
