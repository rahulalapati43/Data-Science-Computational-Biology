#!/usr/bin/python -uB
import math
import sys
import random
from acidAttributes import attributes as ACID_ATTRIBUTES
from acidAttributes import attributeTypes as ATTRIBUTES_MAP
import operator

#sampleSet = [('A', 'e'), ('T', '-'), ('A', 'e'), ('T', '-')]
#sample attributeTable = {'A': {'one' : 0, 'two' : 1}, 'T' : {'one': 1, 'two' : 1}}

def main(faFile, saFile):
    inSet = readData(faFile, saFile)
    inSet = filter(lambda tuple: tuple[0] != 'X', inSet)
    
    trainingSet, testSet = randomSplit(inSet, 0.25)
    print len(trainingSet)
    print len(testSet)

    decisionTree = buildDecisionTree(trainingSet, ACID_ATTRIBUTES, ATTRIBUTES_MAP)
    print treeDisplay(decisionTree, ATTRIBUTES_MAP)
    predictions(decisionTree, ACID_ATTRIBUTES)

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

def splitSetOnAttribute(fullSet, attribute, attributeTable):
    subsetNo = []
    subsetYes = []
    for t in fullSet:
        abv = t[0]
        if (attributeTable[abv][attribute] == 0):
            subsetNo.append(t)
        else:
            subsetYes.append(t)
            
    return subsetNo, subsetYes
    

def calculateEntropy(inSet):
    numTotal = len(inSet) + 0.0
    if numTotal == 0.0:
        return 0.0
    numPos = 0.0
    numNeg = 0.0
    for t in inSet:
        if t[1] == 1:
            numPos = numPos + 1
        else:
            numNeg = numNeg + 1
    propPos = numPos / numTotal
    propNeg = numNeg / numTotal
    if (propPos == 0.0 or propNeg == 0.0):
        return 0.0
    output = -propPos * math.log(propPos, 2)
    output = output - (propNeg * math.log(propNeg, 2))
    return output

def calculateGain(fullSet, subset1, subset2):
    propSubset1 = (len(subset1) + 0.0) / (len(fullSet) + 0.0)
    propSubset2 = (len(subset2) + 0.0) / (len(fullSet) + 0.0)
    output = calculateEntropy(fullSet)
    output = output - (propSubset1 * calculateEntropy(subset1))
    output = output - (propSubset2 * calculateEntropy(subset2))
    return output

def buildDecisionTree(dataset, acidAttributes, attributeMap):
    tree = dict(childYes=None, childNo=None)
    gains = dict()
    for attr in attributeMap:
       split1, split2 = splitSetOnAttribute(dataset, attr, acidAttributes)
       gains[attr] = calculateGain(dataset, split1, split2)

    gainsIterator = gains.iteritems()
    maxGainTuple = max(gainsIterator, key=operator.itemgetter(1))

    # base case - stop if there is no gain in entropy on splitting on any attribute
    if maxGainTuple[1] == 0:
        positiveCount = 0
        for tup in dataset:
            if tup[1] == 1:
                positiveCount += 1

        tree['prediction'] = float(positiveCount) / float(len(dataset))
        return tree

    subsetNo, subsetYes = splitSetOnAttribute(dataset, maxGainTuple[0], acidAttributes)
    tree['attribute'] = maxGainTuple[0]
    tree['childYes'] = buildDecisionTree(subsetYes, acidAttributes, attributeMap)
    tree['childNo'] = buildDecisionTree(subsetNo, acidAttributes, attributeMap)
    return tree

def predictions(decisionTree, acidAttributes):
    attr = decisionTree['attribute']
    predictionResult = {}
    for amino in acidAttributes:
        tree = decisionTree
        print '\namino= '+ amino + ' \n'
        while tree.get('prediction') == None:
            attr = tree['attribute']
            if (acidAttributes[amino][attr]==1):
                tree = tree['childYes']
                prediction = 'Y'
                print ' attr='+attr+" Y"
            else:
                tree = tree['childNo']
                prediction = 'N'
                print ' attr='+attr+" N"
        confidence = 1 if tree.get('prediction')>0.5 else 0
        print ' confidence='+str(confidence)+" "
        if confidence == 0: 
            if prediction == 'Y':
                prediction = 'N'
            else:
                prediction = 'Y'
        print ' prediction final='+prediction+" "
        predictionResult[amino] = prediction
    print "\n========= Predictions ==========="
    print predictionResult
    return predictionResult

def treeDisplay(decisionTree, attributeMap):
    string = ''

    if 'prediction' in decisionTree:
        string += '|-Prediction--{0}'.format(decisionTree['prediction'])
        return string
    
    attr = decisionTree['attribute']
    attrName = attributeMap[attr]['name']
    string = attrName

    if decisionTree['childYes']:
        subtreeString = treeDisplay(decisionTree['childYes'], attributeMap).split('\n')
        string += '\n|-Yes--{0}'.format(subtreeString[0])
        for line in subtreeString[1:]:
            string += '\n|------{0}'.format(line)

    if decisionTree['childNo']:
        subtreeString = treeDisplay(decisionTree['childNo'], attributeMap).split('\n')
        string += '\n|-No---{0}'.format(subtreeString[0])
        for line in subtreeString[1:]:
            string += '\n|------' + line

    return string

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: {0} fa_file sa_file".format(sys.argv[0])
        sys.exit()
    else:
        main(sys.argv[1], sys.argv[2])

