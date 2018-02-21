#!/usr/bin/python -uB
import math
import sys
import random
from acidAttributes import attributes as ACID_ATTRIBUTES

#sampleSet = [('A', 'e'), ('T', '-'), ('A', 'e'), ('T', '-')]
#sample attributeTable = {'A': {'one' : 0, 'two' : 1}, 'T' : {'one': 1, 'two' : 1}}

def main(faFile, saFile):
    inSet = readData(faFile, saFile)
    
    trainingSet, testSet = randomSplit(inSet, 0.25)
    inSet = None
    print len(trainingSet)
    print len(testSet)

def readData(faFile, saFile):
    faStream = open(faFile, 'r')
    saStream = open(saFile, 'r')
    
    faContent = faStream.read().decode('utf-8').split()[1::2]
    acids = [acid for proteinSequence in faContent for acid in proteinSequence]

    saContent = saStream.read().decode('utf-8')
    outputs = [isExposed for line in saContent.split()[1::2] for isExposed in line]
    outputs = [1 if isExposed == 'e' else 0 for isExposed in outputs]

    return zip(acids, outputs)

# Splits the input list `inList` into two.
# Items get sent to the second list randomly at the rate specified by `rate`
def randomSplit(inList, rate):
    list1 = list()
    list2 = list()

    random.seed()
    for item in inList:
        roll = random.random()
        if roll <= rate:
            list2.append(item)
        else:
            list1.append(item)
    
    return list1, list2

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
    

def calculateEntropy(inSet):
    numTotal = len(inSet) + 0.0
    if numTotal == 0.0:
        return 0.0
    numPos = 0.0
    numNeg = 0.0
    for t in inSet:
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: {0} fa_file sa_file".format(sys.argv[0])
        sys.exit()
    else:
        main(sys.argv[1], sys.argv[2])
