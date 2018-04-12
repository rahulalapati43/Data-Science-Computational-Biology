#!/usr/bin/python -uB
import util
import featureGeneration
import argparse
import os
import cPickle
import gradientAscent as ga
import random
from functools import partial

def main(pssmFiles, rrFiles, minibatchSize):
    '''
    trainingRrFiles, testRr = util.randomSplit(rrFiles, 0.75)
    pssmsMap = featureGeneration.pssmsMap(pssmFiles)
    instances = list()
    for i, rrFile in enumerate(trainingRrFiles):
        print 'Balancing protein sequence #{0} from file {1}'.format(i + 1, rrFile)
        instances.extend(classBalance(featureGeneration.getDataset(pssmsMap, [rrFile])))
    print 'Length of dataset: {0}'.format(len(instances))
    cPickle.dump((trainingRrFiles, testRr, instances), open('training.pickle', 'wb'))
    '''
    (trainingRrFiles, testRr, instances) = cPickle.load(open('training.pickle', 'rb'))
    print 'train rr files ==================='
    print ' '.join(trainingRrFiles)
    print 'test rr files ===================='
    print ' '.join(testRr)

    epsilon = 0.0005
    # Stochastic gradient ascent using MCLE
    learningRate = lambda x,y: 0.01
    if minibatchSize is not None:
        print 'Running mini batch with size {0}'.format(minibatchSize)
        weights = ga.gradientAscent(learningRate, epsilon, ga.predict, ga.getDeltaMCLE, partial(ga.getSubsetMiniBatch, minibatchSize), instances)
    else:
        print 'Running stochastic gradient descent'
        weights = ga.gradientAscent(ga.learningRate, epsilon, ga.predict, ga.getDeltaMCLE, ga.getSubsetStochastic, instances)
    print '============================= weights ====================================='
    print weights

    if minibatchSize is None:
        cPickle.dump(weights, open('weights_training_stochastic.pickle', 'wb'))
    else:
        cPickle.dump(weights, open('weights_training_batch.pickle', 'wb'))


def classBalance(instances):
    zeros = [instance for instance in instances if instance[-1] == 0]
    ones = [instance for instance in instances if instance[-1] == 1]
    random.shuffle(zeros)
    return ones + zeros[:len(ones)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate trained model based on fasta and rr (contact map) files') 
    #parser.add_argument('blast_path', help='Path to blastpgp binary')
    #parser.add_argument('nrdb', help='Path to nr file in nr database')
    #parser.add_argument('--fasta', help='Fasta files to train on', nargs='+', required=True)
    #parser.add_argument('--temp_dir', help='Temporary directory for PSSM files generated (default CWD/.temp)', default=os.path.join(os.getcwd(), '.temp'))
    parser.add_argument('--rr', help='RR files to train train on', nargs='+', required=True)
    parser.add_argument('--pssms', help='Get PSSM files from here instead of generating from fasta', nargs='+', required=True)
    parser.add_argument('--minibatch', help='Do minibatch of size s instead of stochastic', default=None)
    args = parser.parse_args()

    main(args.pssms, args.rr, int(args.minibatch) if args.minibatch is not None else None)
