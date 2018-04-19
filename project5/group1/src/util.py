import random
import os
import subprocess
import math
from Protein import Protein

def decodeFastaformat(fasta):
    fastaStream = open(fasta, 'rb')
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
            proteinName = line[1:]
    if proteinLine != '':
        output.append((proteinName, proteinLine))
    fastaStream.close()
    return output

def generatePSSM(multifastaFile, outfileDir, blastpgp, nrdb):
    fastaSequences = decodeFastaformat(open(multifastaFile, 'r'))
    pssmFiles = list()
    aminoAcidCount = 0
    for ind, seq in enumerate(fastaSequences):
        outname = os.path.join(outfileDir, seq[0] + '.pssm')
        process = subprocess.Popen([blastpgp, '-d', nrdb, '-j 3', '-b 1', '-a 4', '-Q', outname], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        result = process.communicate(input=seq[1])
        pssmFiles.append(outname)
        pssmFileWriteSequenceName(outname, seq[0], seq[1])
    return pssmFiles

def pssmFileWriteSequenceName(fileName, sequenceName, sequence):
    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()
    lines[0] = sequenceName
    lines[1] = sequence
    f = open(fileName, 'w')
    f.write('\n'.join(lines))
    f.close()

def readPSSM(inFile):
    count = 0
    headerList = []
    PSSM = {}
    inputFile = open(inFile,"r")
    seqname = next(inputFile)[:-1]
    sequence = next(inputFile)[:-1]
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
                
    return seqname, sequence, headerList, PSSM

def readPSSMNew(inFile):
    count = 0
    headerList = []
    PSSM = {}
    inputFile = open(inFile,"r")
    seqname = next(inputFile)[:-1]
    sequence = next(inputFile)[:-1]
    for line in inputFile:
        line = line.lstrip()
        if (count == 0):
            headerList = line.split()[:20]
            count = count + 1
        
        elif not line.strip():
            break

        else:
            tempList = []
            tempList = line.split()[:42]
            featureList = tempList[22:len(tempList)]
            PSSM[tempList[0]] = featureList
                
    return seqname, sequence, headerList, PSSM

def randomSplit(inList, rate):
    random.shuffle(inList)
    trainData = inList[:(int((len(inList)) * rate))]
    testData = inList[(int((len(inList)) * rate)):]
    return trainData, testData

def columnSum(listOfTuples):
    return [sum(x) for x in zip(*listOfTuples)]

def NormColumnAvg(listOfTuples):
    n = float(len(listOfTuples))*100
    return [sum(x)/n for x in zip(*listOfTuples)]

def normalize(features):
    squares = map(lambda x: x*x, features)
    squareSum = sum(squares)
    norm = math.sqrt(squareSum)

    return [feature / norm for feature in features]

def pssmsMap(proteins,pssmFiles):
    pssmsMap = dict()
    for pssmFile in pssmFiles:
        sequenceName, sequence, pssmHeader, pssmSequence = readPSSMNew(pssmFile)
        pssmsMap[sequence] = slidingWindow(pssmSequence, 0)
        NormalizedColAvg= NormColumnAvg(pssmsMap[sequence])
        proteins[sequenceName].setPssm(pssmSequence)
        proteins[sequenceName].setPssmAvgs(NormalizedColAvg)
    return pssmsMap

def slidingWindow(inMatrix, windowSize):
    pssmMatrix = list()

    addList = []
    for index in range(0,20):
        addList.append(-1)

    keyList = inMatrix.keys()
    keyListInt = map(int, keyList)
    keyRange = range(1, len(keyList) + 1)

    for index in keyRange:
        window = int((windowSize - 1) / 2)
        pssmEntry = []
        for i in range(0, window):
            pssmEntry += map(int, inMatrix[str(index - window + i)][1:21]) if str(index - window + i) in inMatrix else addList
        pssmEntry += map(int, inMatrix[str(index)][1:21])
        for i in range(1, window + 1):
            pssmEntry += map(int, inMatrix[str(index + i)][1:21]) if str(index + i) in inMatrix else addList
        pssmMatrix.append(pssmEntry)

    return pssmMatrix

if __name__ == "__main__":
    pass
