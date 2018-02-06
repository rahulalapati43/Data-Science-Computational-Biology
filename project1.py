#!/usr/bin/python -uB
import re
import sys

space = -1
mismatch = -1
match = 1

def main(sequenceFiles):
    seq1 = readSequence(sequenceFiles[0])
    seq2 = readSequence(sequenceFiles[1])

    mat = readMatrix('BLOSUM62.txt')
    print mat
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

def globalAlignment(seq1, seq2, mat):
   #TO DO look up BLOSUM mat to score
   # The current implementation uses the score used in the example, discussed in the class
          
   # Step 1: Initialize Matrix 
   matrix = [[0 for i in range(len(seq2)+1)] for j in range(len(seq1)+1)] 
   matrix = constructDPTable(seq1, seq2, matrix)  
   print matrix
   traceback(matrix, seq1,seq2) 
    
def constructDPTable(seq1, seq2, matrix):    
   
    # Step 2: Base cases
    for j in range(len(seq1)+1):
        matrix[0][j] = space*j
    for i in range(len(seq2)+1):
        matrix[i][0] = space*i
        
    #Step 3: Fill the DP table    
    for i in range(1, len(seq2)+1):
        for j in range(1, len(seq1)+1):
            #Evaluate all the adjacent cell values
            Instance1 = matrix[i-1][j] + space
            Instance2 = matrix[i][j-1] + space
            if(seq1[j-1] == seq2[i-1]):
                Instance3 = matrix[i-1][j-1] + 1
            else:
                Instance3 = matrix[i-1][j-1] - 1
             #Find max value to put in the cell
            if Instance1 > Instance2:
                if Instance1 > Instance3:
                    max = Instance1
                else:
                    max = Instance3
            elif Instance2 > Instance3:
                max = Instance2
            else:
                max = Instance3
            matrix[i][j] = max
    
    return matrix


def traceback(matrix, seq1, seq2):
    j = len(seq1) 
    i = len(seq2) 
    S1 = []
    S2 = []
    S3 = []
    while i > 0 and j > 0:
        #Diagonal
        val = -1
        if(seq1[j-1] == seq2[i-1]):
            val = 1
            S3.append('|')
        
            
        if int(matrix[i][j]) == int(matrix[i-1][j-1]) + int(val): 
            S2.append(seq2[i-1])
            S1.append(seq1[j-1])
            if(val == -1):
                S3.append('*')
            i -= 1
            j -= 1
        
        #Left
        elif matrix[i][j] == matrix[i-1][j] + space: 
            S2.append(seq2[i-1])
            S1.append('_')
            S3.append('*')
            i -= 1
            
        #Right
        elif matrix[i][j] == matrix[i][j-1] + space: 
            S2.append('_')
            S1.append(seq1[j-1])
            S3.append('*')
            j -= 1
            
        #When sequences are unequal    
    while i > 0: 
       S2.append(seq2[i-1])
       S1.append('_')
       S3.append('*')
       i -= 1
       
    while j > 0:
        S2.append('_')
        S1.append(seq1[j-1])
        S3.append('*')
        j -= 1
        
    print(S1[::-1])
    print(S3[::-1])    
    print(S2[::-1]) 

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: {0} FASTA_sequence1 FASTA_sequence2".format(sys.argv[0])
        sys.exit()
    else:
        main(sys.argv[1:3])
