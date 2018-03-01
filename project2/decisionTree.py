import sys
import random
import math
import operator

AminoAcidAttributes = {}

AminoAcidAttributes["A"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 1, "Proline" : 0, "Tiny" : 1, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["C"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 1, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["D"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 1, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 1, "Charged" : 1}
AminoAcidAttributes["E"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 1, "Charged" : 1}
AminoAcidAttributes["F"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 1, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["G"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 1, "Proline" : 0, "Tiny" : 1, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["H"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 1, "Positive" : 1, "Negative" : 0, "Charged" : 1}
AminoAcidAttributes["I"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 1, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["K"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 1, "Negative" : 0, "Charged" : 1}
AminoAcidAttributes["L"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 1, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["M"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["N"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 1, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["P"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 1, "Proline" : 1, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["Q"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["R"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 1, "Negative" : 0, "Charged" : 1}
AminoAcidAttributes["S"] = {"Hydrophobic" : 0, "Polar" : 1, "Small" : 1, "Proline" : 0, "Tiny" : 1, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["T"] = {"Hydrophobic" : 1, "Polar" : 1, "Small" : 1, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["V"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 1, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 1, "Aromatic" : 0, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["W"] = {"Hydrophobic" : 1, "Polar" : 0, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 1, "Positive" : 0, "Negative" : 0, "Charged" : 0}
AminoAcidAttributes["Y"] = {"Hydrophobic" : 1, "Polar" : 1, "Small" : 0, "Proline" : 0, "Tiny" : 0, "Aliphatic" : 0, "Aromatic" : 1, "Positive" : 0, "Negative" : 0, "Charged" : 0}

AttributesList = ["Hydrophobic", "Polar", "Small", "Proline", "Tiny", "Aliphatic", "Aromatic", "Positive", "Negative", "Charged"]

def readData(AAfile,SAfile):
    proteinSequences = []
    solventAccessibility = []

    FASTAfile = open(AAfile, "r")
    SolventAccessibilityfile = open(SAfile, "r")

    for line in FASTAfile:
        line = line.strip()
        if not line.startswith(">"):
            proteinSequences.append(line)

    for line in SolventAccessibilityfile:
        line = line.strip()
        if not line.startswith(">"):
            solventAccessibility.append(line)

    return zip(proteinSequences,solventAccessibility)

def getAASA(proteinSequences):
    AA = []
    SA = []

    for line in proteinSequences:
        for aminoAcid in line[0]:
            AA.append(aminoAcid)

    for line in proteinSequences:
        for solAccessibility in line[1]:
            if (solAccessibility == 'e'):
                SA.append(1)
            else:
                SA.append(0)

    return zip(AA,SA)

def calculateEntropy(inputData):
    total = float(len(inputData))
    if (total == 0.0):
        return 0.0

    positives = 0.0
    negatives = 0.0
    for set in inputData:
        if (set[1] == 1):
            positives = positives + 1.0
        else:
            negatives = negatives + 1.0

    probPositives = positives/total
    probNegatives = negatives/total

    if ((probPositives == 0.0) or (probNegatives == 0.0)):
        return 0.0

    E0 = -((probPositives * math.log(probPositives,2)) + (probNegatives * math.log(probNegatives,2)))
    return E0

def calculateYesNo(inputData,attribute):
    subset1 = []
    subset2 = []
    for set in inputData:
        if (AminoAcidAttributes[set[0]][attribute] == 1):
            subset1.append(set)
        else:
            subset2.append(set)
    return subset1,subset2

def calculateInfoGains(inputData):
    infoGains = {}
    for attribute in AttributesList:
        yesList, noList = calculateYesNo(inputData,attribute)
        probYes = (float(len(yesList)) / float(len(inputData)))
        probNo = (float(len(noList)) / float(len(inputData)))
        sampleEntropy = calculateEntropy(inputData)
        E1 = calculateEntropy(yesList)
        E2 = calculateEntropy(noList)
        infoGains[attribute] = sampleEntropy - (probYes * E1) - (probNo * E2)
    return infoGains

def buildDecisionTree(inputData):
    decisionTree = dict(childYes=None, childNo=None)
    infoGainsList = calculateInfoGains(inputData)
    maxGain = max(infoGainsList.iteritems(), key=operator.itemgetter(1))

    if (maxGain[1] == 0):
        positiveCount = 0
        for set in inputData:
            if set[1] == 1:
                positiveCount += 1

        decisionTree['prediction'] = float(positiveCount) / float(len(inputData))

        return decisionTree

    yesList, noList = calculateYesNo(inputData,maxGain[0])
    decisionTree['attribute'] = maxGain[0]
    decisionTree['childYes'] = buildDecisionTree(yesList)
    decisionTree['childNo'] = buildDecisionTree(noList)
    return decisionTree


def treeDisplay(decisionTree):
    string = ''

    if 'prediction' in decisionTree:
        string += '|-Prediction--{0}'.format(decisionTree['prediction'])
        return string

    attribute = decisionTree['attribute']
    string = attribute

    if decisionTree['childYes']:
        subtreeString = treeDisplay(decisionTree['childYes']).split('\n')
        string += '\n|-Yes--{0}'.format(subtreeString[0])
        for line in subtreeString[1:]:
            string += '\n|------{0}'.format(line)

    if decisionTree['childNo']:
        subtreeString = treeDisplay(decisionTree['childNo']).split('\n')
        string += '\n|-No---{0}'.format(subtreeString[0])
        for line in subtreeString[1:]:
            string += '\n|------' + line

    return string

def calculateLabels(decisionTree):
    testLabels = {}
    for aminoAcid in AminoAcidAttributes:
        tree = decisionTree
        while (tree.get('prediction') == None):
            attribute = tree['attribute']
            if (AminoAcidAttributes[aminoAcid][attribute] == 1):
                tree = tree['childYes']
            else:
                tree = tree['childNo']

        if (tree.get('prediction') >= 0.4):
            confidence = 1
        else:
            confidence = 0

        if (confidence == 1):
            label = 'Y'
        else:
            label = 'N'

        testLabels[aminoAcid] = label

    return testLabels

def evaluateAccuracy(testData,decisionTreeResult):

    TP = 0.0
    FP = 0.0
    TN = 0.0
    FN = 0.0

    for set in testData:
        aminoAcid = set[0]
        if (set[1] == 1):
            label = 'Y'
        else:
            label = 'N'

        if ((decisionTreeResult[aminoAcid] == 'Y') and (label == 'Y')):
            TP = TP + 1.0
        elif ((decisionTreeResult[aminoAcid] == 'Y') and (label == 'N')):
            FP = FP + 1.0
        elif ((decisionTreeResult[aminoAcid] == 'N') and (label == 'Y')):
            FN = FN + 1.0
        elif ((decisionTreeResult[aminoAcid] == 'N') and (label == 'N')):
            TN = TN + 1.0

    Precision = (TP)/(TP + FP)
    Recall = (TP)/(TP + FN)
    Accuracy = (TP + TN)/(TP + TN + FP + FN)

    F1Measure = (2 * ((Precision * Recall)/(Precision + Recall)))
    MCC = (((TP * TN) - (FP * FN))/(math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))))

    print "\n========= Accuracy ==========="
    print "Precision:" + str(Precision)
    print "Recall:" + str(Recall)
    print "Accuracy:" + str(Accuracy)
    print "F-1 Measure:" + str(F1Measure)
    print "Mathews Correlation Coefficient (MCC):" + str(MCC)

def randomDivision(inputData):
    random.shuffle(inputData)
    trainData = inputData[:(int((len(inputData)) * 0.75))]
    testData = inputData[(int((len(inputData)) * 0.75)):]
    return trainData,testData

if (len(sys.argv) == 3):
    inData = readData(sys.argv[1],sys.argv[2])
    trainData, testData = randomDivision(inData)
    trainData = filter(lambda tuple: tuple[0] != 'X', getAASA(trainData))
    decisionTree = buildDecisionTree(trainData)
    print treeDisplay(decisionTree)
    decisionTreeResult = calculateLabels(decisionTree)
    print "\n========= Predictions ==========="
    print decisionTreeResult
    testData = filter(lambda tuple: tuple[0] != 'X', getAASA(testData))
    evaluateAccuracy(testData,decisionTreeResult)
else:
    print "Usage: " + sys.argv[0] + " FASTA_File SolventAccessibility_File"

