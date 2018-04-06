#!/usr/bin/python -uB
import util
import argparse
import sys
import os
import cPickle

def gradientAscent(learningRateCallback, epsilon, predictCallback, getDeltaCallback, getSubsetCallback, dataset):
    recentDeltas = list()
    weights = range(0,201)

    iterationCount = 0
    while len(recentDeltas) < 10:
        data = getSubset(dataset)
        deltas = list()
        for d in data:
            prediction = predict(d[:1], weights)
            delta = getDelta(prediction, learningRateCallback(iterationCount, delta), d, weights)
            deltas.add(delta)
        if max(columnSum(deltas)) > epsilon:
            recentDdeltas = []
        else:
            recentDeltas.add(max(columnSum(deltas)))

        weights += columnSum(deltas)

    return weights

def columnSum(listOfTuples):
    return [sum(x) for x in zip(*listOfTuples)]


if __name__ == "__main__":
    pass
