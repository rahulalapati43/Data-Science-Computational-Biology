#!/usr/bin/python -uB
import util
import featureGeneration
import argparse
import os
import cPickle
import gradientAscent as ga
import random
from functools import partial

def main(dataDir, minibatchSize):
    allProteinsMap = featureGeneration.getProteinsMap(dataDir)
    dataset = featureGeneration.getDataset(featureGeneration.getProteinPairs(allProteinsMap))

    epsilon = 0.0005
    learningRate = lambda x,y: 0.01
    if minibatchSize is not None:
        print 'Running mini batch with size {0}'.format(minibatchSize)
        weights = ga.gradientAscent(learningRate, epsilon, ga.predict, ga.getDelta, partial(ga.getSubsetMiniBatch, minibatchSize), dataset)
    else:
        print 'Running stochastic gradient descent'
        weights = ga.gradientAscent(ga.learningRate, epsilon, ga.predict, ga.getDelta, ga.getSubsetStochastic, dataset)
    print '============================= weights ====================================='
    print weights

    if minibatchSize is None:
        cPickle.dump(weights, open('weights_training_stochastic.pickle', 'wb'))
    else:
        cPickle.dump(weights, open('weights_training_batch.pickle', 'wb'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate trained model')
    parser.add_argument('--minibatch', help='Do minibatch of size s instead of stochastic', default=None)
    parser.add_argument('dataDir', help='Directory of fasta, pdb, and pssm files')
    args = parser.parse_args()

    main(args.dataDir, int(args.minibatch) if args.minibatch is not None else None)
