import random
import os
import subprocess

def readData(File):
    Sequences = []
    File = open(File, "r")

    SeqLine = ''
    for line in File:
        if line[len(line) - 1] == '\n':
            line = line[:len(line) - 1] 
        if not line.startswith(">"):
            SeqLine += line
        else:
            if SeqLine != '':
                Sequences.append(SeqLine)
            SeqLine = ''

    if SeqLine != '':
        Sequences.append(SeqLine)

    return Sequences

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
        outFile.write(">sequence\n")
        outFile.write(inList[line] + "\n")
    outFile.close()
    
def generatePSSM(inFile, name, blastpgp, nrdb):
    fastaSequences = readData(inFile)
    print str(len(fastaSequences)) + '   ' + inFile
    aminoAcidCount = 0
    pssms = {}
    for ind, seq in enumerate(fastaSequences):
        process = subprocess.Popen([blastpgp, '-d', nrdb, '-j 3', '-b 1', '-a 4', '-Q', name], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        result = process.communicate(input=seq)
        print 'done with ' + seq
        #pssms.append(result[0])
        header, pssm = readPSSM(name)
        keyList = map(int, pssm.keys())
        keyList.sort()
        for key in keyList:
            aminoAcidCount += 1
            pssms[str(aminoAcidCount)] = pssm[str(key)]
            
    of = open(name, 'w')
    of.write('\n\n        ')
    of.write(' '.join(header))
    of.write('\n')
    keyList = map(int, pssms.keys())
    keyList.sort()
    for key in keyList:
        of.write(str(key) + ' ')
        of.write(' '.join(pssms[str(key)]))
        of.write('\n')
    of.write('\n')
    of.close()

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

    keyList = inMatrix.keys()
    keyListInt = map(int, keyList)
    minKeyList = min(keyListInt)
    maxKeyList = max(keyListInt)

    addList = []
    
    for index in range(0,21):
        addList.append(-1)
    
    '''inMatrix[str(maxKeyList + 1)] = addList
    inMatrix[str(maxKeyList + 2)] = addList
    inMatrix[str(minKeyList - 1)] = addList
    inMatrix[str(minKeyList - 2)] = addList'''

    keyList = inMatrix.keys()
    keyListInt = map(int, keyList)
    minKeyList = min(keyListInt)
    maxKeyList = max(keyListInt)
    keyRange = range(1, len(keyList) + 1)
        
    for index in keyRange:
        pssmMatrix[str(index)] = (inMatrix[str(index)] +
                    (inMatrix[str(index - 1)][1:21] if str(index - 1) in inMatrix else addList[1:]) +
                    (inMatrix[str(index - 2)][1:21] if str(index - 2) in inMatrix else addList[1:]) +
                    (inMatrix[str(index + 1)][1:21] if str(index + 1) in inMatrix else addList[1:]) +
                    (inMatrix[str(index + 2)][1:21] if str(index + 2) in inMatrix else addList[1:]))

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
    fasta = open('sample.fa', 'r')
    print decodeFastaformat(fasta)
