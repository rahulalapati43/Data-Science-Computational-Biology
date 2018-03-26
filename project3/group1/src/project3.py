#!/usr/bin/python -uB
import util
from testing import predict
import sys
import os
import cPickle

def main(blastPath, nrdb, faFile):
    gaussianModel = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'gaussianModel.pickle'), 'rb'))

    #util.generatePSSM(faFile, ".predictme.temp.pssm", blastPath, nrdb)
    fasta = util.decodeFastaformat(open(faFile, 'r'))
    pssmHeader, pssm20Features = util.readPSSM(".predictme.temp.pssm")
    testFeatures = util.slidingWindow(pssm20Features)
    predictions = predict(gaussianModel, testFeatures)

    counter = 1
    for proteinTuple in fasta:
        print proteinTuple[0]
        predictionSequence = ''
        sequenceLength = len(proteinTuple[1])
        for proteinAcidInd in range(counter, counter + sequenceLength):
            predictionSequence += predictions[str(proteinAcidInd)][1]
        print predictionSequence

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: " + sys.argv[0] + " /path/to/blastpgp /path/to/nrdb/file FASTA_file"
        else:
                main(sys.argv[1], sys.argv[2], sys.argv[3])
 
