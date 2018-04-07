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

def randomSplit(inList, rate):
    random.shuffle(inList)
    trainData = inList[:(int((len(inList)) * rate))]
    testData = inList[(int((len(inList)) * rate)):]
    return trainData, testData

def getSubsetBatch(dataset):
    return dataset

def getSubsetStochastic(dataset):
    return random.choice(dataset)

def predict(instance, weights): #adjusts with or without bias
    i = 0 #iterator for instance
    j = 0 #iterator for weights
    temp = 0
    
    if (len(instance) + 1) == len(weights): #weights contain bias
        temp += weights[j] #bias
        j++
        
    while (i < len(instance)):
        temp += instance[i] * weights[j]
        i++
        j++
    temp = -temp
    temp = 1 + math.exp(temp)
    return = 1 / temp
    
    

if __name__ == "__main__":
    pass
