#!/usr/bin/python -uB
import re
import sys
from globalAlignment import globalAlignment

def main(sequenceFiles):
    seq1 = readSequence(sequenceFiles[0])
    seq2 = readSequence(sequenceFiles[1])

    mat = readMatrix('BLOSUM62.txt')
    (S1, S2, S3, score) = globalAlignment(seq1, seq2, mat)
    print 'Score: {0}'.format(score)
    printAlignment(S1, S2, S3)

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

def printAlignment(S1, S2, S3):
    str1 = (''.join(S1))
    str2 = (''.join(S3))
    str3 = (''.join(S2))
    match = S3.count('|')
    mismatch = S3.count('*')
    space = S3.count(' ')

    for i in range(0, len(str1), 80):
        print str1[i:i + 80]
        print str2[i:i + 80]
        print str3[i:i + 80]
        print '\n'
    '''print 'match :' + str(match)
    print 'mismatch :' + str(mismatch)
    print 'space :' + str(space)
    print 'score = match - mismatch - space = ' + str(match - mismatch + space)'''

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: {0} FASTA_sequence1 FASTA_sequence2".format(sys.argv[0])
        main(['human_hemoglobin_alpha.fasta.txt', 'mouse_hemoglobin_alpha.fasta.txt'])
        #sys.exit()
    else:
        main(sys.argv[1:3])
