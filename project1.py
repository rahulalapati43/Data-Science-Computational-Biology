#!/usr/bin/python -uB
import re
import sys
from globalAlignment import globalAlignment

def main(sequenceFiles):
    seq1 = readSequence(sequenceFiles[0])
    seq2 = readSequence(sequenceFiles[1])

    mat = readMatrix('BLOSUM62.txt')
    globalAlignment(seq1, seq2, mat)

def readSequence(fileName):
    fileStream = open(fileName, 'r')
    seq = fileStream.read().decode('utf-8')
    seq = ''.join(seq.split('\n')[1:])
    return seq

def readMatrix(fileName):
    fileStream = open(fileName, 'r')
    strMatrix = fileStream.read().decode('utf-8')

    lines = strMatrix.split('\n')
    header = re.sub(' +', ' ', lines[0].strip()).split(' ')
    header = re.sub('\*', ' ', '|'.join(header)).split('|')

    outDict = dict()
    for line in lines[1:]:
        cols = re.sub(' +', ' ', line.strip()).split(' ')
        if cols[0] == '*':
            cols[0] = ' '
        outDict[cols[0]] = dict(zip(header, [int(col) for col in cols[1:]]))
    return outDict

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: {0} FASTA_sequence1 FASTA_sequence2".format(sys.argv[0])
        sys.exit()
    else:
        main(sys.argv[1:3])
