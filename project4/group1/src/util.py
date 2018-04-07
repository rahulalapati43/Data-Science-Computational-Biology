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
            proteinName = line[1:]
    if proteinLine != '':
        output.append((proteinName, proteinLine))
    return output

def randomSplit(inList, rate):
    random.shuffle(inList)
    trainData = inList[:(int((len(inList)) * rate))]
    testData = inList[(int((len(inList)) * rate)):]
    return trainData, testData

if __name__ == "__main__":
    pass
