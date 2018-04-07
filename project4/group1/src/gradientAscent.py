#!/usr/bin/python -uB
import util
import random

def gradientAscent(learningRateCallback, epsilon, predictCallback, getDeltaCallback, getSubsetCallback, dataset):
    recentDeltas = list()
    weights = [0] * 200

    iterationCount = 0
    while len(recentDeltas) < 10:
        data = getSubset(dataset)
        deltas = list()
        for d in data:
            i, j, features, label = d
            prediction = predict(features, weights)
            delta = getDelta(prediction, learningRateCallback(iterationCount, delta), d, weights)
            deltas.add(delta)

        colsum = columnSum(deltas)
        if max(colsum) > epsilon:
            recentDdeltas = []
        else:
            recentDeltas.add(max(colsum))

        weights += colsum

    return weights

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
        j += 1
        
    while (i < len(instance)):
        temp += instance[i] * weights[j]
        i += 1
        j += 1
    temp = -temp
    temp = 1 + math.exp(temp)
    return 1 / temp

if __name__ == "__main__":
    pass
