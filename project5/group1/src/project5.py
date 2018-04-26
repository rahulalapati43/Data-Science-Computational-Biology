#!/usr/bin/python -uB
import util
import sys
import os
import cPickle
import gradientDescent
from protein import Protein

def main(blastpgp, nrdb, modelPickle, proteinAFasta, proteinBFasta):
    with open(modelPickle, 'rb') as f:
        weights = cPickle.load(f)
    proteinA = Protein('proteinA')
    proteinA.setFastaFile(proteinAFasta)
    proteinA.setPssmFile(util.generatePSSM(proteinAFasta, './', blastpgp, nrdb)[0])

    proteinB = Protein('proteinB')
    proteinB.setFastaFile(proteinBFasta)
    proteinB.setPssmFile(util.generatePSSM(proteinBFasta, './', blastpgp, nrdb)[0])

    features = list(proteinA.getPssmAvgs())
    features.extend(proteinB.getPssmAvgs())
    features.extend(proteinA.getHECAvgs().values())
    features.extend(proteinB.getHECAvgs().values())
    features.extend(proteinA.getExposedBuriedAvgs().values())
    features.extend(proteinB.getExposedBuriedAvgs().values())

    predictedTMScore = gradientDescent.predict(features, weights)

    print predictedTMScore

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print "Usage: " + sys.argv[0] + " /path/to/blastpgp /path/to/nrdb/file model.pickle FASTA_file_A FASTA_file_B"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
