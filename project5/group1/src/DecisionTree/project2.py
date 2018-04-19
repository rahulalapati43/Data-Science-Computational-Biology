#!/usr/bin/python -uB
from id3 import predictions
from acidAttributes import attributes as ACID_ATTRIBUTES
import cPickle
import sys
import os

def predict(faFile):
    decisionTree = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'decisionTree.pickle'), 'rb'))
    predictionsMap = predictions(decisionTree, ACID_ATTRIBUTES)
    predictionsMap['X'] = '?'
    sequences = readFasta(faFile)

    for proteinSequenceTuple in sequences:
        outputSequence = ''
        for acid in proteinSequenceTuple[1].upper():
            if predictionsMap[acid] != '?':
                outputSequence += 'e' if predictionsMap[acid] == 'Y' else '-'
            else:
                outputSequence += '?'
        # print proteinSequenceTuple[0]
        # print outputSequence
    return outputSequence

def readFasta(faFile):
    fastaStream = open(faFile, 'r')
    output = list()
    proteinDescription = ''
    for line in iter(fastaStream.readline, ''):
        if line[len(line) - 1] == '\n':
            line = line[:len(line) - 1]
        if line[0] == '>':
            proteinDescription += line
        else:
            output.append((proteinDescription, line))
            proteinDescription = ''
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: {0} fa_file".format(sys.argv[0])
        sys.exit()
    else:
        predict(sys.argv[1])

