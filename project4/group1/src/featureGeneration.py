#!/usr/bin/python -uB
import util
import sys
import os
import subprocess

def main(blastpgp, nrdb, outdir, fastaFiles):
    for multifasta in fastaFiles:
        generatePSSM(multifasta, outdir, blastpgp, nrdb)

def generatePSSM(multifastaFile, outfileDir, blastpgp, nrdb):
    fastaSequences = util.decodeFastaformat(open(multifastaFile, 'r'))
    pssmFiles = list()
    aminoAcidCount = 0
    for ind, seq in enumerate(fastaSequences):
        outname = os.path.join(outfileDir, seq[0] + '.pssm')
        process = subprocess.Popen([blastpgp, '-d', nrdb, '-j 3', '-b 1', '-a 4', '-Q', outname], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        result = process.communicate(input=seq[1])
        pssmFiles.append(outname)
        pssmFileWriteSequenceName(outname, seq[0], seq[1])
        sequenceName, sequence, header, pssm = readPSSM(outname)
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

def readRr(rrFile):
    rr2dMap = dict()
    f = open(rrFile, 'r')
    sequence = next(f)

    j = len(sequence)
    i = j - 6
    while i <= len(sequence) - 6:
        j = i + 6
        while j <= len(sequence):
            if str(i) not in rr2dMap:
                rr2dMap[str(i)] = dict()
            rr2dMap[str(i)][str(j)] = 0
            j += 1
        i += 1

    for line in f:
        lsplit = line.split()
        i = lsplit[0]
        j = lsplit[1]
        inContact = 0 if float(lsplit[4]) > 8 else 1
        rr2dMap[i][j] = inContact

    f.close()

    # flatten 2dMap
    rrList = list()
    iListInt = map(int, rr2dMap.keys())
    iListInt.sort()
    for i in map(str, iListInt):
        jListInt = map(int, rr2dMap[i].keys())
        jListInt.sort()
        for j in map(str, jListInt):
            rrList.append((i, j, rr2dMap[i][j]))
    return sequence, rrList

def readPSSM(inFile):
    count = 0
    headerList = []
    PSSM = {}
    inputFile = open(inFile,"r")
    seqname = next(inputFile)[1:]
    sequence = next(inputFile)
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

def getInstances(pssmFiles, rrFiles):
    pssmsMap = dict()
    rrSequencesList = list()
    for pssmFile in pssmFiles:
        sequenceName, sequence, pssmHeader, pssmSequence = readPSSM(pssmFile)
        pssmsMap[sequence] = slidingWindow(pssmSeqeunce, 5)

    for rr in rrFiles:
        sequence, rrList = readRr(rr)
        rrSequencesList.append((seqeunce, rrList))

    instances = list()
    for rrInfo in rrSequencesList:
        sequence = rrInfo[0]
        rrList = rrInfo[1]
        i = rrList[0]
        j = rrList[1]
        label = rrList[3]
        instances.append((i, j, pssmsMap[sequence], label))

    return instances

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: " + sys.argv[0] + "/path/to/blastpgp /path/to/nrdb/file out_pssm_dir/ FASTA_files..."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
