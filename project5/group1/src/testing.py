#!/usr/bin/python -uB
import featureGeneration
import argparse
import sys
import os
import cPickle
import math
import util
import gradientDescent as gd
from operator import itemgetter

def main(dataDir, pickle):
    
    # read model
    weights = cPickle.load(open(pickle, 'rb'))
    # print "weights==========="
    # print weights
    #weights  = [0.01,-0.65,-0.76,-0.17,-0.05,0.73,-0.13,0.51,0.78,-0.04,-0.55,-0.57,-0.1,-0.81,-0.82,0.14,-0.35,-0.16,-0.71,-0.69,-0.57,-0.66,-0.65,-0.17,0.09,0.43,0.15,0.16,0.47,-0.71,0.4,0.56,0.69,0.49,-0.15,0.28,0.63,-0.88,0.6,0.73,0.11,-0.69,0.35,0.89,-0.08,-0.55,0.64,0.26,0.54,0.11,0.22,0.13,0.71,-0.42,0.75,0.89,0.65,0.78,-0.37,0.02,0.16,0.7,0.69,0.02,-0.33,0.65,0.34,0.76,-0.03,-0.42,0.5,0.6,0.72,0.65,-0.2,0.03,-0.64,0.85,-0.51,-0.35,0.1,0.69,-0.21,0.22,0.46,0.65,0.81,0.31,-0.02,0.62,-0.42,-0.9,-0.42,0.04,0.29,-0.03,0.13,0.57,0.8,0.58,-0.87,0.24,0.8,-0.03,-0.31,-0.2,0.45,-0.09,-0.08,0.47,0.52,0.77,0.49,0.47,0.04,-0.83,-0.54,0.62,0.05,0.43,-0.58,0.31,0.88,0.89,0.09,-0.83,0.09,0.65,-0.2,0.8,0.2,-0.02,-0.71,0.21,-0.22,0.41,0.13,0.46,0.14,-0.45,-0.87,0.83,-0.82,-0.82,0.8,-0.06,0.63,0.48,-0.67,0.03,0.27,0.62,-0.15,0.76,-0.48,0.62,0.62,0.41,-0.21,-0.09,0.18,0.2,0.21,0.81,-0.46,-0.84,0.53,-0.09,0.76,0.46,0.34,-0.42,-0.22,-0.28,-0.85,-0.34,0.84,0.02,0.6,0.01,0.61,-0.29,0.25,0.04,0.88,-0.46,0.74,0.43,-0.77,-0.23,0.01,0.89,0.05,-0.56,-0.04,0.48,0.36,-0.71,0.44,0.07,0.6] #placeholder weights 

    testSet = cPickle.load(open('test_features.pickle', 'rb'))
    results = list()
    for test in testSet:
        True_TMScore = test[-1]
        Predicted_TMScore = gd.predict(test, weights)        
	Error =  (True_TMScore - Predicted_TMScore) ** 2
        print "True: " + str(True_TMScore) + " Predicted: " + str(Predicted_TMScore) + " Error: " + str(Error) + " %: " + str((Predicted_TMScore/True_TMScore)) 
        results.append(Error)
    
    Accuracy = sum(results) / float(len(results)) 
    print "Accuracy of average squared error average squared error: " + str(Accuracy)	
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testing') 
    parser.add_argument('--dataset', help='DataDir', required=True)
    parser.add_argument('--pkl', help='Use this pickle model', required=True) 
    args = parser.parse_args()
    main(args.dataset, args.pkl)
