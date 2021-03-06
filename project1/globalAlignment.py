#!/usr/bin/python -uB

def globalAlignment(sequence1, sequence2, scoringMatrix):
   #TO DO look up BLOSUM mat to score
   # The current implementation uses the score used in the example, discussed in the class
          
    dpTable = constructDPTable(sequence1, sequence2, scoringMatrix)
    return traceback(dpTable, sequence1, sequence2, scoringMatrix)


def constructDPTable(sequence1, sequence2, matrix):
    # Step 1: Initialize Matrix
    dpTable = [[dict([('score', 0)]) for i in range(len(sequence2)+1)] for j in range(len(sequence1)+1)] 
   
    # Step 2: Base cases
    # consuming letters from sequence1 and aligning against space
    for j in range(1, len(sequence2)+1):
        dpTable[0][j]['score'] = dpTable[0][j-1]['score'] + matrix[' '][sequence2[j-1]]
        dpTable[0][j]['parentI'] = 0
        dpTable[0][j]['parentJ'] = j-1
    # consuming letters from sequence2 and aligning against space
    for i in range(1, len(sequence1)+1):
        dpTable[i][0]['score'] = dpTable[i-1][0]['score'] + matrix[sequence1[i-1]][' ']
        dpTable[i][0]['parentI'] = i-1
        dpTable[i][0]['parentJ'] = 0
        
    #Step 3: Fill the DP table    
    for i in range(1, len(sequence1)+1):
        for j in range(1, len(sequence2)+1):
            #Evaluate all the adjacent cell values
            south = dpTable[i-1][j]['score'] + matrix[' '][sequence1[i-1]]
            east = dpTable[i][j-1]['score'] + matrix[sequence2[j-1]][' ']
            se = dpTable[i-1][j-1]['score'] + matrix[sequence2[j-1]][sequence1[i-1]]

            if south > east:
                if south > se:
                    max = {'score': south, 'parentI': i-1, 'parentJ': j}
                else:
                    max = {'score': se, 'parentI': i-1, 'parentJ': j-1}
            elif se >= east:
                max = {'score': se, 'parentI': i-1, 'parentJ': j-1}
            else:
                max = {'score': east, 'parentI': i, 'parentJ': j-1}
            dpTable[i][j] = max
    
    return dpTable


def traceback(dpTable, sequence1, sequence2, scoringMatrix):
    j = len(sequence2)
    i = len(sequence1)
    # print dpTable
    S1 = []
    S2 = []
    S3 = []
    while i > 0 or j > 0:
        # print dpTable[i][j]['score']
        # print dpTable[i-1][j-1]['score']
        #Diagonal
        if(i-1 == dpTable[i][j]['parentI'] and j-1 == dpTable[i][j]['parentJ']):
            if(scoringMatrix[sequence1[i-1]][sequence2[j-1]] > 0):
                S3.append('|')
            else:
                S3.append('*')
            S1.append(sequence1[i-1])
            S2.append(sequence2[j-1])
        #Left
        elif (i == dpTable[i][j]['parentI'] and j-1 == dpTable[i][j]['parentJ']):
            S1.append('-')
            S2.append(sequence2[j-1])
            S3.append(' ')
        #Up
        elif (i-1 == dpTable[i][j]['parentI'] and j == dpTable[i][j]['parentJ']): 
            S1.append(sequence1[i-1])
            S2.append('-')
            S3.append(' ') 
        (i, j) = (dpTable[i][j]['parentI'], dpTable[i][j]['parentJ'])

    return (S1[::-1], S2[::-1], S3[::-1], dpTable[len(sequence1)][len(sequence2)]['score'])
    # print(S1[::-1])
    # print(S3[::-1])    
    # print(S2[::-1]) 
