#!/usr/bin/python -uB
import featureGeneration
import argparse
import sys
import os
import cPickle
import math
import util
import gradientAscent as ga
from operator import itemgetter

def main(pssmFiles, rrFiles, pickle):
    
    # read model
    weights = cPickle.load(open(pickle, 'rb'))
    # print "weights==========="
    # print weights
    #weights  = [0.01,-0.65,-0.76,-0.17,-0.05,0.73,-0.13,0.51,0.78,-0.04,-0.55,-0.57,-0.1,-0.81,-0.82,0.14,-0.35,-0.16,-0.71,-0.69,-0.57,-0.66,-0.65,-0.17,0.09,0.43,0.15,0.16,0.47,-0.71,0.4,0.56,0.69,0.49,-0.15,0.28,0.63,-0.88,0.6,0.73,0.11,-0.69,0.35,0.89,-0.08,-0.55,0.64,0.26,0.54,0.11,0.22,0.13,0.71,-0.42,0.75,0.89,0.65,0.78,-0.37,0.02,0.16,0.7,0.69,0.02,-0.33,0.65,0.34,0.76,-0.03,-0.42,0.5,0.6,0.72,0.65,-0.2,0.03,-0.64,0.85,-0.51,-0.35,0.1,0.69,-0.21,0.22,0.46,0.65,0.81,0.31,-0.02,0.62,-0.42,-0.9,-0.42,0.04,0.29,-0.03,0.13,0.57,0.8,0.58,-0.87,0.24,0.8,-0.03,-0.31,-0.2,0.45,-0.09,-0.08,0.47,0.52,0.77,0.49,0.47,0.04,-0.83,-0.54,0.62,0.05,0.43,-0.58,0.31,0.88,0.89,0.09,-0.83,0.09,0.65,-0.2,0.8,0.2,-0.02,-0.71,0.21,-0.22,0.41,0.13,0.46,0.14,-0.45,-0.87,0.83,-0.82,-0.82,0.8,-0.06,0.63,0.48,-0.67,0.03,0.27,0.62,-0.15,0.76,-0.48,0.62,0.62,0.41,-0.21,-0.09,0.18,0.2,0.21,0.81,-0.46,-0.84,0.53,-0.09,0.76,0.46,0.34,-0.42,-0.22,-0.28,-0.85,-0.34,0.84,0.02,0.6,0.01,0.61,-0.29,0.25,0.04,0.88,-0.46,0.74,0.43,-0.77,-0.23,0.01,0.89,0.05,-0.56,-0.04,0.48,0.36,-0.71,0.44,0.07,0.6] #placeholder weights 

    testRr = rrFiles
    results = list()
    for x in xrange(0,len(rrFiles)):
        instances = featureGeneration.getDataset(featureGeneration.pssmsMap(pssmFiles), [testRr[x]])
        f = open(testRr[x], 'r')
        sequence = next(f)[:-1]
        f.close()
        l = len(sequence)
        Fname = testRr[x].split("/")[3]
        results.append(calculateForRR(instances,weights,l,Fname))
    
    sumResults = [0,0,0,0,0,0,0]
    print "Protein \tL10 \t\t\t\tL5  \t\t\t\tL2 \t\t\t\t\t\t\tTP \t\t\tTN \t\t\tFP \t\t\tFN"
    for result in results:
        for x in xrange(0,7):
            sumResults[x] += result[x+1]
        print result[0] + "\t\t" + str(result[1]).ljust(13) + " %\t\t" + str(result[2]).ljust(13) + " %\t\t" + str(result[3]).ljust(13) + " %\t\t\t\t" + str(result[4]).ljust(5) + "\t\t" + str(result[5]).ljust(5) + "\t\t" + str(result[6]).ljust(5) + "\t\t" + str(result[7]).ljust(5)

    if (sumResults[4]+sumResults[6])!=0:
        accuracyZero = float(sumResults[4])*100/(sumResults[4]+sumResults[6])
    else:
        accuracyZero = 0

    if (sumResults[3]+sumResults[5])!=0:
        accuracyOnes = float(sumResults[3])*100/(sumResults[3]+sumResults[5])
    else:
        accuracyOnes = 0


    avgL10 = sumResults[0]/len(results)
    avgL5 = sumResults[1]/len(results)
    avgL2 = sumResults[2]/len(results)

    
    print "Average L/10 = " + str(avgL10)+ " %\t\t"
    print "Average L/5 = " + str(avgL5)+ " %\t\t"
    print "Average L/2 = " + str(avgL2)+ " %\t\t"
    print "Average accuracy positive contacts = " + str(accuracyOnes)+ " %\t\t"
    print "Average accuracy negetive contacts = " + str(accuracyZero)+ " %\t\t"

def calculateForRR(instances,weights,l,protienName):
    predictedLabel = list()
    
    print 'Length of dataset: {0}'.format(len(instances))
    
    for instance in instances:
        out = [instance[0],instance[1],instance[3]]
        # out.append(prediction(weights,instance[2]))
        probability = ga.predict(instance[2],weights)
        outputLabel = 0 if probability<0.5 else 1
        out.append(outputLabel)
        out.append(probability)
        predictedLabel.append(out)

    predictedLabel.sort(key=lambda x: x[4], reverse=True)
    # print "prediction ==========="
    # print predictedLabel

    #l = len(predictedLabel)
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for label in predictedLabel:
        if(label[2]==1):
            if label[3]==1:
                TP+=1
            else:
                FN+=1
        else:
            if label[3]==0:
                TN+=1
            else:
                FP+=1
    L10 = accuracy(l/10,predictedLabel)
    L5 = accuracy(l/5,predictedLabel)
    L2 = accuracy(l/2,predictedLabel)
    return (protienName,L10,L5,L2,TP,TN,FP,FN)

def accuracy(l,predictedLabel):
    correct =0
    for x in xrange(1,l):
        if predictedLabel[x][2]==predictedLabel[x][3]:
            correct+=1
    accuracyPercent = float(correct*100)/l
    return accuracyPercent

# def prediction(weights,x):
#     sum = 0 
#     for i in xrange(len(x)):
#         sum += weights[i+1] * x[i] 
#     sum += weights[0]
#     expo = sum
#     output = 0 if expo<0.5 else 1
#     return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate trained model based on fasta and rr (contact map) files') 
    #parser.add_argument('blast_path', help='Path to blastpgp binary')
    #parser.add_argument('nrdb', help='Path to nr file in nr database')
    #parser.add_argument('--fasta', help='Fasta files to train on', nargs='+', required=True)
    #parser.add_argument('--temp_dir', help='Temporary directory for PSSM files generated (default CWD/.temp)', default=os.path.join(os.getcwd(), '.temp'))
    parser.add_argument('--rr', help='RR files to train train on', nargs='+', required=True)
    parser.add_argument('--pssms', help='Get PSSM files from here instead of generating from fasta', nargs='+', required=True)
    parser.add_argument('--pkl', help='Use this pickle model', required=True)
    args = parser.parse_args()
    main(args.pssms, args.rr, args.pkl)
