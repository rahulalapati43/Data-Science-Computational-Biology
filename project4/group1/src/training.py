#!/usr/bin/python -uB
import util
import featureGeneration
import argparse
import sys
import os
import cPickle
import gradientAscent as ga

def main(pssmFiles, rrFiles):
    trainRr, testRr = util.randomSplit(rrFiles, 0.75)
    print trainRr
    print testRr

    instances = featureGeneration.getDataset(pssmFiles, trainRr)
    print 'Length of dataset: {0}'.format(len(instances))

    epsilon = 0.05
    #Batch gradient ascent using MCLE 
    weights = ga.gradientAscent(ga.learningRate, epsilon, ga.predict, ga.getDeltaMCLE, ga.getSubsetStochastic, instances)
    print weights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate trained model based on fasta and rr (contact map) files') 
    #parser.add_argument('blast_path', help='Path to blastpgp binary')
    #parser.add_argument('nrdb', help='Path to nr file in nr database')
    #parser.add_argument('--fasta', help='Fasta files to train on', nargs='+', required=True)
    #parser.add_argument('--temp_dir', help='Temporary directory for PSSM files generated (default CWD/.temp)', default=os.path.join(os.getcwd(), '.temp'))
    parser.add_argument('--rr', help='RR files to train train on', nargs='+', required=True)
    parser.add_argument('--pssms', help='Get PSSM files from here instead of generating from fasta', nargs='+', required=True)
    args = parser.parse_args()

    main(args.pssms, args.rr)
