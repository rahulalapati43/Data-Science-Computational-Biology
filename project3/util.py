import random
import os

def readData(faFile, ssFile):
	proteinSequences = []
	secondaryStructure = []
	
	fastaFile = open(faFile, "r")
	ssFile = open(ssFile, "r")
	
	proteinLine = ''
	for line in fastaFile:
		if line[len(line) - 1] == '\n':
			line = line[:len(line) - 1] 
		if not line.startswith(">"):
				proteinLine += line
		else:
			if proteinLine != '':
				proteinSequences.append(proteinLine)
			proteinLine = ''

	if proteinLine != '':
		proteinSequences.append(proteinLine)
	
	proteinLine = ''
	for line in ssFile:
		if line[len(line) - 1] == '\n':
			line = line[:len(line) - 1]
		if not line.startswith(">"):
			if line.strip():
				proteinLine += line
		else:
			if proteinLine != '':
				secondaryStructure.append(proteinLine)
			proteinLine = ''

	if proteinLine != '':
		secondaryStructure.append(proteinLine)
	
	return zip(proteinSequences, secondaryStructure)

def randomSplit(inList, rate):
	random.shuffle(inList)
	trainData = inList[:(int((len(inList)) * rate))]
	testData = inList[(int((len(inList)) * rate)):]
	return trainData, testData

def explodeTuples(tuplesList):
	aminoAcids = []
	ssClass = []

	for tup in tuplesList:
		aminoAcids.append(tup[0])
		ssClass.append(tup[1])
	
	return aminoAcids, ssClass
				
def writeFile(inList,name):
	outFile = open(name,"w+")
	for line in range(0,len(inList)):
		outFile.write(inList[line] + "\n")
	outFile.close()
	
def generatePSSM(inFile,name):
	pssm_cmd = "apps/blast/bin/blastpgp -d nrdatabase/nr/nr -j 3 -b 1 -a 4 -i" + ' ' + str(inFile) + ' ' +  "-Q" + ' ' + name  #+ ' ' + "& > /dev/null 2>&1"
	os.system(pssm_cmd)

def readPSSM(inFile):
	count = 0
	headerList = []
	PSSM = {}
	inputFile = open(inFile,"r")
	next(inputFile)
	next(inputFile)
	for line in inputFile:
		line = line.lstrip()
		if (count == 0):
			headerList = line.split()[:20]
			count = count + 1
		
		elif not line.strip():
			break

		else:
			tempList = []
			tempList = line.split()[:22]
			featureList = tempList[1:len(tempList)]
			PSSM[tempList[0]] = featureList
				
	return headerList, PSSM

def slidingWindow(inMatrix):
	pssmMatrix = {}
	keyList = []
	keyList = inMatrix.keys()
	addList = []
	
	for index in range(0,21):
		addList.append(-1)
	
	inMatrix[str(max(map(int,keyList)) + 1)] = addList
	inMatrix[str(max(map(int,keyList)) + 2)] = addList
	inMatrix[str(min(map(int,keyList)) - 1)] = addList
	inMatrix[str(min(map(int,keyList)) - 2)] = addList 
	
	keyList = inMatrix.keys()
		
	for index in range(0,len(keyList)):
		if (int(keyList[index]) > (min(map(int,keyList)) + 1) and int(keyList[index]) < (max(map(int,keyList)) - 1)):
			pssmMatrix[keyList[index]] = (inMatrix[keyList[index]] + inMatrix[str(int(keyList[index]) - 1)][1:] + 
							inMatrix[str(int(keyList[index]) - 2)][1:] + 
							inMatrix[str(int(keyList[index]) + 1)][1:] + inMatrix[str(int(keyList[index]) + 2)][1:])

	return pssmMatrix		 

def addLabel(inMatrix,ssList):
	keyList = inMatrix.keys()
	inkeyList = map(int,keyList)
	inkeyList.sort()
	keyList = map(str,inkeyList)

	newLine = ''.join(ssList)
	ssList = list(newLine)

	for key in keyList:
		inMatrix[key].append(ssList[int(key) - 1])

	return inMatrix
	
