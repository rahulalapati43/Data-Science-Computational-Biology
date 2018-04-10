import random
import os
import subprocess
import math

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
            proteinName = line[1:]
    if proteinLine != '':
        output.append((proteinName, proteinLine))
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

def randomSplit(inList, rate):
    random.shuffle(inList)
    trainData = inList[:(int((len(inList)) * rate))]
    testData = inList[(int((len(inList)) * rate)):]
    return trainData, testData

def columnSum(listOfTuples):
    return [sum(x) for x in zip(*listOfTuples)]

if __name__ == "__main__":
    pass
