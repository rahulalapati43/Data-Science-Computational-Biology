#!/usr/bin/python -uB
import featureGeneration
import argparse
import sys
import os
import cPickle
import math

def main(pssmFiles, rrFiles):
    
    # read model
    # weights = cPickle.load(open(Model, 'rb'))
    weights = [1] * 201
    trainRr = rrFiles
    predictedLabel = list()
    correct =0 
    instances = featureGeneration.getDataset(pssmFiles, trainRr)
    print 'Length of dataset: {0}'.format(len(instances))
    for instance in instances:
        out = [instance[0],instance[1],instance[3]]
        out.append(prediction(weights,instance[2]))
        predictedLabel.append(out)
        if out[2]==out[3]:
            correct = (correct+1)
    accuracy = float(correct*100)/len(instances)
    print "accuracy =" + str(accuracy)

def prediction(weights,x):
    sum = 0 
    for i in xrange(len(x)):
        sum += weights[i] * x[i] 
    sum += weights[200]
    expo = math.exp(sum)
    output = 0 if expo<=0 else 1
    return output


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
