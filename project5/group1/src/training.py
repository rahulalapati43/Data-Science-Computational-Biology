#!/usr/bin/python -uB
import util
import featureGeneration
import argparse
import os
import cPickle
import gradientDescent as gd
import random
from functools import partial

def main(dataDir, batchSize):
    #allProteinsMap = featureGeneration.getProteinsMap(dataDir)
    dataset = cPickle.load(open('train_features.pickle','rb')) 

    epsilon = 0.0005
    #learningRate = lambda x,y: 0.01
    if batchSize is not None:
        print 'Running batch with size {0}'.format(batchSize)
        weights = gd.gradientDescent(gd.learningRate, epsilon, gd.predict, gd.getDeltaMCLE, gd.getSubsetBatch, dataset)
    else:
        print 'Running stochastic gradient descent'
        weights = gd.gradientDescent(gd.learningRate, epsilon, gd.predict, gd.getDeltaMCLE, gd.getSubsetStochastic, dataset)
    print '============================= weights ====================================='
    print weights

    if batchSize is None:
        cPickle.dump(weights, open('weights_training_stochastic.pickle', 'wb'))
    else:
        cPickle.dump(weights, open('weights_training_batch.pickle', 'wb'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate trained model')
    parser.add_argument('--batch', help='Do batch of size s instead of stochastic', default=None)
    parser.add_argument('dataDir', help='Directory of fasta, pdb, and pssm files')
    args = parser.parse_args()

    main(args.dataDir, int(args.batch) if args.batch is not None else None)
