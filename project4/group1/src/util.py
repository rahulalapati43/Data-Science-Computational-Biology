import random
import os
import subprocess

def decodeFastaformat(fastaStream):
    output = list()
    proteinName = ''
    proteinLine = ''
    for line in iter(fastaStream.readline, ''):
        if line[len(line) - 1] == '\n':
            line = line[:len(line) - 1]
        if line[0] != '>':
            proteinLine += line
        else:
            if proteinLine != '':
                output.append((proteinName, proteinLine))
                proteinLine = ''
            proteinName = line
    if proteinLine != '':
        output.append((proteinName, proteinLine))
    return output

def randomSplit(inList, rate):
    random.shuffle(inList)
    trainData = inList[:(int((len(inList)) * rate))]
    testData = inList[(int((len(inList)) * rate)):]
    return trainData, testData

def generatePSSM(multifastaFile, outfileDir, blastpgp, nrdb):
    fastaSequences = decodeFastaformat(open(multifastaFile), 'r')
    pssmFiles = list()
    aminoAcidCount = 0
    for ind, seq in enumerate(fastaSequences):
        outname = os.path.join(outfileDir, seq[0] + '.pssm')
        process = subprocess.Popen([blastpgp, '-d', nrdb, '-j 3', '-b 1', '-a 4', '-Q', outname], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        result = process.communicate(input=seq[1])
        pssmFiles.append(outname)
        print 'done with ' + seq
        header, pssm = readPSSM(outname)
    return pssmFiles

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

def slidingWindow(inMatrix, windowSize):
    pssmMatrix = list()

    keyList = inMatrix.keys()
    keyListInt = map(int, keyList)
    minKeyList = min(keyListInt)
    maxKeyList = max(keyListInt)

    addList = []

    for index in range(0,21):
        addList.append(-1)

    keyList = inMatrix.keys()
    keyListInt = map(int, keyList)
    minKeyList = min(keyListInt)
    maxKeyList = max(keyListInt)
    keyRange = range(1, len(keyList) + 1)

    for index in keyRange:
        pssmEntry = ((inMatrix[str(index - 1)][1:21] if str(index - 1) in inMatrix else addList[1:]) +
                    (inMatrix[str(index - 2)][1:21] if str(index - 2) in inMatrix else addList[1:]) +
                    inMatrix[str(index)] +
                    (inMatrix[str(index + 1)][1:21] if str(index + 1) in inMatrix else addList[1:]) +
                    (inMatrix[str(index + 2)][1:21] if str(index + 2) in inMatrix else addList[1:]))
        pssmMatrix.append(pssmEntry)

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


if __name__ == "__main__":
    pass
