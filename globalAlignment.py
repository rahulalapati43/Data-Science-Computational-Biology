#!/usr/bin/python -uB

def globalAlignment(sequence1, sequence2, scoringMatrix):
   #TO DO look up BLOSUM mat to score
   # The current implementation uses the score used in the example, discussed in the class
          
   # Step 1: Initialize Matrix 
    dpTable = constructDPTable(sequence1, sequence2, scoringMatrix)
    traceback(scoringMatrix, sequence1, sequence2)
    
def constructDPTable(sequence1, sequence2, matrix):
    dpTable = [[dict([('score', 0)]) for i in range(len(sequence2)+1)] for j in range(len(sequence1)+1)] 
   
    # Step 2: Base cases
    # consuming letters from seq1 and aligning against space
    for j in range(1, len(sequence1)+1):
        dpTable[0][j]['score'] = dpTable[0][j-1]['score'] + matrix[sequence1[j-1]][' ']
    # consuming letters from seq2 and aligning against space
    for i in range(1, len(sequence2)+1):
        dpTable[i][0]['score'] = dpTable[i-1][0]['score'] + matrix[' '][sequence2[i-1]]
        
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
