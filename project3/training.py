from util import *
import sys
import cPickle

def main(faFile, ssFile):
	proteinTuples = readData(faFile, ssFile)
        trainingProteins, testProteins = randomSplit(proteinTuples, 0.75)
        trainFA, trainSS = explodeTuples(trainingProteins)
        testFA, testSS = explodeTuples(testProteins)
        trainFAFile = writeFile(trainFA,"train.fa")
        writeFile(trainSS,"train.ss")
        writeFile(testFA,"test.fa")
        writeFile(testSS,"test.ss")
        generatePSSM("train.fa","train.pssm")
        generatePSSM("test.fa","test.pssm")
        trainHeader, train20Features = readPSSM("train.pssm")
        trainFeatures = slidingWindow(train20Features)
        trainingSet = addLabel(trainFeatures, trainSS)
	model = calculateModel(trainingSet)
	cPickle.dump(model, open('gaussianModel.pickle', 'wb'))
	print model['H']
	print len(model['H'])
	print model['E']
	print len(model['E'])
	print model['C']
	print len(model['C'])	

if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Usage: " + sys.argv[0] + "FASTA_file SecondaryStructure_File"
        else:
                main(sys.argv[1], sys.argv[2])
 
def calculateModel(inSet):
	model = {}
	HList = []
	EList = []
	CList = []

	hTemp = []
	eTemp = []
	cTemp = []

	for key in inSet.keys():
		if (inSet[key][len(inSet[key]) - 1] ==  'H'):
			hTemp.append(inSet[key][1:len(inSet[key]) - 1])
		elif (inSet[key][len(inSet[key]) - 1] ==  'E'):
			eTemp.append(inSet[key][1:len(inSet[key]) - 1])
		elif (inSet[key][len(inSet[key]) - 1] == 'C'):
			cTemp.append(inSet[key][1:len(inSet[key]) - 1])	
	
	hTuples = zip(*hTemp)
	eTuples = zip(*eTemp)
	cTuples = zip(*cTemp)
	
	tempList = [] 	
	for element in hTuples:
		tempList = list(element)
		tempList = map(int,tempList)
		HList.append(sum(tempList)/float(len(tempList)))
	
	tempList = []	
	for element in eTuples:
		tempList = list(element)
		tempList = map(int,tempList)
		EList.append(sum(tempList)/float(len(tempList)))

	tempList = []
	for element in cTuples:
		tempList = list(element)
		tempList = map(int,tempList)
		CList.append(sum(tempList)/float(len(tempList)))

	tempList = []
	for element in hTuples:
		tempList = list(element)
                tempList = map(int,tempList)
		average = sum(tempList)/float(len(tempList))
		HList.append(sum((average - value) ** 2	for value in tempList)/float(len(tempList)))

	tempList = []
        for element in eTuples:
                tempList = list(element)
                tempList = map(int,tempList)
                average = sum(tempList)/float(len(tempList))
                EList.append(sum((average - value) ** 2 for value in tempList)/float(len(tempList)))

	tempList = []
        for element in cTuples:
                tempList = list(element)
                tempList = map(int,tempList)
                average = sum(tempList)/float(len(tempList))
                CList.append(sum((average - value) ** 2 for value in tempList)/float(len(tempList)))

	HList.append(len(hTemp)/float(len(hTemp) + len(eTemp) + len(cTemp)))
	EList.append(len(eTemp)/float(len(hTemp) + len(eTemp) + len(cTemp)))
	CList.append(len(cTemp)/float(len(hTemp) + len(eTemp) + len(cTemp)))

	model['H'] = HList
	model['E'] = EList
	model['C'] = CList
	
	return model
