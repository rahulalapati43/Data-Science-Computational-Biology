#!/usr/bin/python -uB
import util
import random
import math

def gradientDescent(learningRateCallback, epsilon, predictCallback, getDeltaCallback, getSubsetCallback, dataset):
    recentDeltas = list()
    weights = [0] * 50

    iterationCount = 0
    while len(recentDeltas) < 10:
        data = getSubsetCallback(dataset)
        deltas = list()
        etta = learningRateCallback(iterationCount, epsilon)
        
        for d in data:
            prediction = predict(d, weights)
            delta = getDeltaCallback(prediction, etta, d, weights)
            deltas.append(delta)

        colsum = [float(colDelta / len(data)) for colDelta in util.columnSum(deltas)]

        maxColusum = max([abs(col) for col in colsum])
        if maxColusum > epsilon:
            recentDeltas = []
        else:
            recentDeltas.append(maxColusum)

        weights = map(sum, zip(*[weights, colsum]))
        print 'iteration #{0}: max delta: {1} ==== learning rate was {2}'.format(iterationCount, maxColusum, etta)
        iterationCount += 1

    print '================ recent {0} deltas ================'.format(len(recentDeltas))
    print recentDeltas
    return weights

def predict(features, weights): 
    i = 0  # iterator for instance
    j = 0  # iterator for weights
    
    value = 0

    while (i < len(features)-1):
	value += (weights[j] * features[i])
	i = i + 1
        j = j + 1

    return value			

def getDeltaMCLE(predict, learningRate, dataset, weight):
    i = 0  # iterator for features
    features = dataset[0:50]
    y = dataset[-1]
    
    weightErrors = list()
  
    #w0Error = learningRate * 2 * (y - predict)
    #weightErrors.append(w0Error)
    for feature in features:
        weightErrors.append(2 * learningRate * feature * (y - predict))
    return weightErrors



def learningRate(iterationCount, epsilon):
    n = (8/2**(float(iterationCount)/512) + 1)*(epsilon * 10) # exponential slope that goes from 0.009 to 0.005 over about 2500 iterations
    return n

def getSubsetBatch(dataset):
    return dataset

def getSubsetMiniBatch(batchSize, dataset):
    random.shuffle(dataset)
    return dataset[:batchSize]

def getSubsetStochastic(dataset):
    return [random.choice(dataset)]

if __name__ == "__main__":
    pass
