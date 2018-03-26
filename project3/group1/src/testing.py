#!/usr/bin/python -uB
from util import *
import sys
import cPickle
import math
def main(gaussianModel, pssm_file, ss_file):
	# read model
	gaussianModel = cPickle.load(open(gaussianModel, 'rb'))	

	testHeader, test20Features = readPSSM(pssm_file)
	testFeatures = slidingWindow(test20Features)

	actualShapes = ''.join(readData(ss_file))
	predictions = predict(gaussianModel,testFeatures)

	successfulPredictions = {'H': 0, 'E': 0, 'C': 0}
	for pssmKey, prediction in predictions.iteritems():
		aminoAcid = prediction[0]
		shapePrediction = prediction[1]
		actual = actualShapes[int(pssmKey) - 1]
		if actual == shapePrediction:
			successfulPredictions[actual] += 1

	print 'Total Q3 Accuracy: ' + str(sum(successfulPredictions.values()) / float(len(actualShapes)))
	print 'H Q3 Accuray:' + str(successfulPredictions['H'] / float(actualShapes.count('H')))
	print 'E Q3 Accuray:' + str(successfulPredictions['E'] / float(actualShapes.count('E')))
	print 'C Q3 Accuray:' + str(successfulPredictions['C'] / float(actualShapes.count('C')))


def pdf(x, mean, variance):
	fra = 1/ math.sqrt(2 * math.pi * variance)
	exp = math.exp(-0.5 / variance * (((x - mean)) ** 2))
	pdf = fra * exp
	return pdf

def calculateProb(features,gaussianModel):
	pdfH = pdfE = pdfC = 1
	for x in range(1, 101):
		pdfH *= pdf(float(features[x]),float(gaussianModel['H'][x-1]),float(gaussianModel['H'][x+99]))
		pdfE *= pdf(float(features[x]),float(gaussianModel['E'][x-1]),float(gaussianModel['E'][x+99]))
		pdfC *= pdf(float(features[x]),float(gaussianModel['C'][x-1]),float(gaussianModel['C'][x+99]))
	pH = pdfH * gaussianModel['H'][200]
	pE = pdfE * gaussianModel['E'][200]
	pC = pdfC * gaussianModel['C'][200]

	Max = pH
	letter = 'H'
	if pE > Max:
		Max = pE
		letter = 'E'
	if pC > Max:
		Max = pC
		letter = 'C'	
	return letter

def predict(gaussianModel,testFeatures):
	result = {};
	for key in testFeatures:
		letter = calculateProb(testFeatures[key], gaussianModel)
		result[key]=[testFeatures[key][0],letter]
	return result

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: " + sys.argv[0] + " gaussianModel.pickle pssm_file ss_file"
        else:
                main(sys.argv[1], sys.argv[2], sys.argv[3])
 
