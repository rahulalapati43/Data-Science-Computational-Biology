from util import *
import sys
import cPickle
import math
def main(gaussianModel, faFile):
	# read model
	gaussianModel = cPickle.load(open(gaussianModel, 'rb'))	
	#read faFile
	proteinSequences = readData(faFile)
	testHeader, test20Features = readPSSM("test.pssm")
	testFeatures = slidingWindow(test20Features)
	
	result = predict(gaussianModel,testFeatures)
	print result


def pdf(x,mean,sd):
	fra = 1/ math.sqrt(2* math.pi * (sd**2))
	exp = math.exp(-0.5 * (((x - mean)/sd)**2))
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
        if len(sys.argv) < 3:
                print "Usage: " + sys.argv[0] + "gaussianModel.pickle FASTA_file"
        else:
                main(sys.argv[1], sys.argv[2])
 
