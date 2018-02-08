#!/usr/bin/python -uB

def globalAlignment(sequence1, sequence2, scoringMatrix):
   #TO DO look up BLOSUM mat to score
   # The current implementation uses the score used in the example, discussed in the class
          
   # Step 1: Initialize Matrix 
    dpTable = constructDPTable(sequence1, sequence2, scoringMatrix)
    traceback(dpTable, sequence1, sequence2)
    
def constructDPTable(sequence1, sequence2, matrix):
    dpTable = [[dict([('score', 0)]) for i in range(len(sequence2)+1)] for j in range(len(sequence1)+1)] 
   
    # Step 2: Base cases
    # consuming letters from sequence1 and aligning against space
    for j in range(1, len(sequence1)+1):
        dpTable[0][j]['score'] = dpTable[0][j-1]['score'] + matrix[sequence1[j-1]][' ']
        dpTable[0][j]['parentI'] = 0
        dpTable[0][j]['parentJ'] = j-1
    # consuming letters from sequence2 and aligning against space
    for i in range(1, len(sequence2)+1):
        dpTable[i][0]['score'] = dpTable[i-1][0]['score'] + matrix[' '][sequence2[i-1]]
        dpTable[i][0]['parentI'] = i-1
        dpTable[0][j]['parentJ'] = 0
        
    #Step 3: Fill the DP table    
    for i in range(1, len(sequence2)+1):
        for j in range(1, len(sequence1)+1):
            #Evaluate all the adjacent cell values
            south = dpTable[i-1][j]['score'] + matrix[' '][sequence2[i-1]]
            east = dpTable[i][j-1]['score'] + matrix[sequence1[j-1]][' ']
            se = dpTable[i-1][j-1]['score'] + matrix[sequence1[j-1]][sequence2[i-1]]

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


def traceback(dpTable, sequence1, sequence2):
    j = len(sequence1)
    i = len(sequence2)
    # print dpTable
    S1 = []
    S2 = []
    S3 = []
    while i > 0 and j > 0:       
        # print dpTable[i][j]['score']
        # print dpTable[i-1][j-1]['score']
        #Diagonal
        if(i-1 == dpTable[i][j]['parentI'] and j-1 == dpTable[i][j]['parentJ']):
            if(sequence1[i-1]==sequence2[j-1]):
                S3.append('|')
            else:
                S3.append('-')
            S1.append(sequence1[i-1])
            S2.append(sequence2[j-1])
        #Left
        elif (i == dpTable[i][j]['parentI'] and j-1 == dpTable[i][j]['parentJ']):
            S2.append('_')
            S1.append(sequence1[j-1])
            S3.append('*')
        #Right
        elif (i-1 == dpTable[i][j]['parentI'] and j == dpTable[i][j]['parentJ']): 
            S2.append(sequence2[i-1])
            S1.append('_')
            S3.append('*') 
        i= dpTable[i][j]['parentI']
        j= dpTable[i][j]['parentJ']
        
    # print(S1[::-1])
    # print(S3[::-1])    
    # print(S2[::-1]) 
    print(' '.join(S1))
    print(' '.join(S3))
    print(' '.join(S2))
    match = S3.count('|')
    mismatch = S3.count('-')
    space = S3.count('*')
    print 'match :'+ str(match)
    print 'mismatch :'+str(mismatch)
    print 'space :'+str(space)