#!/usr/bin/python -uB
import util
import sys
import os
import cPickle
import gradientAscent
import featureGeneration

def main(blastpgp, nrdb, fastaFile):
    weights = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'weights_minibatch.pickle')))
    pssmFiles = util.generatePSSM(fastaFile, './', blastpgp, nrdb)
    #pssmFiles = ['./1guu.pssm']


    fastaList = util.decodeFastaformat(open(fastaFile, 'r'))
    proteinName, proteinSequence = fastaList[0]
    contactInstances = getContactPairs(proteinSequence, featureGeneration.pssmsMap(pssmFiles))

    rrFile = open(proteinName + '.rr', 'w')

    print >>sys.stdout, proteinSequence
    print >>rrFile, proteinSequence
    for instance in contactInstances:
        probability = gradientAscent.predict(instance[2], weights)
        instance[3] = probability

    contactInstances.sort(key=lambda x: x[3], reverse=True)

    for instance in contactInstances:
        i = instance[0]
        j = instance[1]
        probability = instance[3]
        print >>sys.stdout, i + ' ' + j + ' 0 8 ' + str(probability)
        print >>rrFile, i + ' ' + j + ' 0 8 ' + str(probability)

    print >>sys.stderr, 'Also wrote to rr file ' + proteinName + '.rr'

def getContactPairs(sequence, pssmsMap):
    pssmFeaturesByPosition = pssmsMap[sequence]
    pairs = list()
    for i in range(len(sequence) - 6):
        for j in range(i+6, len(sequence)): 
            features = list(pssmFeaturesByPosition[i])
            features.extend(list(pssmFeaturesByPosition[j]))
            pairs.append([str(i+1), str(j+1), features, None])

    return pairs



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " /path/to/blastpgp /path/to/nrdb/file FASTA_file"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
