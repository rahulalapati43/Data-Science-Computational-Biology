#!/usr/bin/python -uB
import util
import sys
import os
import subprocess

def main(blastpgp, nrdb, outdir, fastaFiles):
    for multifasta in fastaFiles:
        util.generatePSSM(multifasta, outdir, blastpgp, nrdb)


def readRr(rrFile):
    rr2dMap = dict()
    f = open(rrFile, 'r')
    sequence = next(f)[:-1]

    i = 1
    while i <= len(sequence) - 6:
        j = i + 6
        rr2dMap[str(i)] = dict()
        while j <= len(sequence):
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

def getDataset(pssmFiles, rrFiles):
    pssmsMap = dict()
    rrSequencesList = list()
    for pssmFile in pssmFiles:
        sequenceName, sequence, pssmHeader, pssmSequence = util.readPSSM(pssmFile)
        pssmsMap[sequence] = slidingWindow(pssmSequence, 5)

    for rr in rrFiles:
        sequence, rrList = readRr(rr)
        rrSequencesList.append((sequence, rrList))

    instances = list()
    for rrInfo in rrSequencesList:
        sequence = rrInfo[0]
        pairContactInfoTuples = rrInfo[1]
        instances.extend(getProteinInstances(pssmsMap[sequence], pairContactInfoTuples))

    return instances

def getProteinInstances(proteinPssm, contactTuples):
    instances = list()
    for contactTuple in contactTuples:
        i = contactTuple[0]
        j = contactTuple[1]
        features = list(proteinPssm[int(i) - 1])
        features.extend(list(proteinPssm[int(j) - 1]))
        label = contactTuple[2]
        instances.append((i, j, features, label))

    return instances

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: " + sys.argv[0] + "/path/to/blastpgp /path/to/nrdb/file out_pssm_dir/ FASTA_files..."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
