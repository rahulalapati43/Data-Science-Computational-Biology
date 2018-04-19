#!/usr/bin/python -uB
import util
from testing import predict
import sys
import os
import cPickle

def main(pssm_file, faFile):
    gaussianModel = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'gaussianModel.pickle'), 'rb'))

    # util.generatePSSM(faFile, ".predictme.temp.pssm", blastPath, nrdb)
    fasta = util.decodeFastaformat(open(faFile, 'r'))
    pssmHeader, pssm20Features = util.readPSSM(pssm_file)
    testFeatures = util.slidingWindow(pssm20Features)
    predictions = predict(gaussianModel, testFeatures)

    counter = 1
    for proteinTuple in fasta:
        # print proteinTuple[0]
        predictionSequence = ''
        sequenceLength = len(proteinTuple[1])
        for proteinAcidInd in range(counter, counter + sequenceLength):
            predictionSequence += predictions[str(proteinAcidInd)][1]
        counter += sequenceLength
        # print predictionSequence
    return predictionSequence

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: " + sys.argv[0] + " pssm_file FASTA_file"
        else:
                main(sys.argv[1], sys.argv[2])
 
