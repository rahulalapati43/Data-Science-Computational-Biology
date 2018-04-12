#!/usr/bin/python -uB
import util
import random
import math

def gradientAscent(learningRateCallback, epsilon, predictCallback, getDeltaCallback, getSubsetCallback, dataset):
    recentDeltas = list()
    weights = [0] * 201

    iterationCount = 0
    while len(recentDeltas) < 10:
        data = getSubsetCallback(dataset)
        deltas = list()
        etta = learningRateCallback(iterationCount, epsilon)
        for d in data:
            i, j, features, label = d
            prediction = predictCallback(features, weights)
            delta = getDeltaCallback(prediction, etta, d, weights)
            deltas.append(delta)

        colsum = [float(colDelta / len(data)) for colDelta in util.columnSum(deltas)]
        #colsum = util.columnSum(deltas)
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

def predict(instance, weights):  # adjusts with or without bias
    i = 0  # iterator for instance
    j = 0  # iterator for weights
    temp = 0

    if (len(instance) + 1) == len(weights):  # weights contain bias
        temp += weights[j]  # bias
        j += 1

    while (i < len(instance)):
        temp += instance[i] * weights[j]
        i += 1
        j += 1

    return float(1) / float(1 + math.exp(-temp))

def getDeltaMCLE(prediction, learningRate, instance, weight):
    i = 0  # iterator for features
    features = instance[2]
    y = instance[-1]
    weightErrors = list()
    w0Error = learningRate * 1 * (y - prediction)
    weightErrors.append(w0Error)
    for feature in features:
        weightErrors.append(learningRate * feature * (y - prediction))
    return weightErrors

def getDeltaMAP(prediction, learningRate, instance, weights):
    lambdaa = 0.25
    i = 0 #iterator for features
    features = instance[2]
    y = instance[3]
    weightedErrorSum = 0
    for feature in features:
        weightedErrorSum += feature * (y - prediction)
    delta = learningRate * weightedErrorSum - learningRate * lambdaa * weights
    return delta

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
