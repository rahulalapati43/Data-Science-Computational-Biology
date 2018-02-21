import sys
import os

# open the BLOSUM and the input FASTA sequence files
BLOSUMfile = open(os.path.join(os.path.dirname(__file__), "BLOSUM62.txt"),"r")
FASTAfile1 = open(sys.argv[1],"r")
FASTAfile2 = open(sys.argv[2],"r")

BLOSUMmatrix = {}
indexList = []
count = 0

#read the BLOSUM file and store in a list
#indexList is a list consisting of all the characters of the BLOSUM62. It is later used while filling the dpTable.
for line in BLOSUMfile:
    if (count == 0):
        indexList = line.split()
        count = count + 1
    if not line.startswith(" "):
        rowList = []
        rowList = line.split()
        newrowList = rowList[1:len(rowList)]
        BLOSUMmatrix[rowList[0]] = newrowList

#read the input FASTA files and store them in lists
FASTA1 = []
line1 = ''
for line in FASTAfile1:
    line = line.strip()
    if not line.startswith(">"):
        line1 = line1 + line

FASTA1 = list(line1)

FASTA2 = []
line2 = ''
for line in FASTAfile2:
    line = line.strip()
    if not line.startswith(">"):
        line2 = line2 + line

FASTA2 = list(line2)

#dpTable declaration based on the input sequence lengths
dpTable = [[dict([("score", 0)]) for j in range(len(FASTA2)+1)] for i in range(len(FASTA1)+1)]

#populating the base cases in the dpTable
for i in range(1,len(FASTA1)+1):
    dpTable[i][0]["parentI"] = i-1
    dpTable[i][0]["parentJ"] = 0

for j in range(1,len(FASTA2)+1):
    dpTable[0][j]["parentI"] = 0
    dpTable[0][j]["parentJ"] = j-1

#calculating the other cells in the dpTable based on general recurrences
for i in range(1,len(FASTA1)+1):
    for j in range(1,len(FASTA2)+1):
        FASTAindex = indexList.index("*")
        FASTA2index = indexList.index(FASTA2[j-1])
        horizontal = dpTable[i][j-1]["score"] + int(BLOSUMmatrix["*"][FASTA2index])
        vertical = dpTable[i-1][j]["score"] + int(BLOSUMmatrix[FASTA1[i-1]][FASTAindex])
        diagonal = dpTable[i-1][j-1]["score"] + int(BLOSUMmatrix[FASTA1[i-1]][FASTA2index])

        if (vertical > horizontal):
            if (vertical > diagonal):
                max = {"score" : vertical, "parentI" : i - 1, "parentJ" : j}
            else:
                max = {"score": diagonal, "parentI": i - 1, "parentJ": j - 1}

        elif (diagonal >= horizontal):
            max = {"score": diagonal, "parentI": i - 1, "parentJ": j - 1}

        else:
            max = {"score" : horizontal, "parentI" : i, "parentJ" : j - 1}

#if the resulting is negative, replace with zero
        if (max["score"] < 0):
            max["score"] = 0

        dpTable[i][j] = max

maxScore = 0
ivalue = 0
jvalue = 0

#calculating the maximum score in the dpTable
for i in range(0,len(FASTA1)+1):
    for j in range(0,len(FASTA2)+1):
        if (dpTable[i][j]["score"] > maxScore):
            maxScore = dpTable[i][j]["score"]
            ivalue = i
            jvalue = j

i = ivalue
j = jvalue

Symbols= []
Seq1 = []
Seq2 = []

#traceback until we encounter a zero in the dpTable
while (dpTable[i][j]["score"] > 0):

    parentI = dpTable[i][j]["parentI"]
    parentJ = dpTable[i][j]["parentJ"]

#diagonal elements, use | for positive score and '*' for non positive scores
    if ((i-1 == parentI) and (j-1 == parentJ)):
        FASTAindex = indexList.index(FASTA2[j-1])
        if (int(BLOSUMmatrix[FASTA1[i-1]][FASTAindex]) > 0):
            Symbols.append('|')
        else:
            Symbols.append('*')

        Seq1.append(FASTA1[i-1])
        Seq2.append(FASTA2[j-1])

#vertical element
    elif ((i-1 == parentI) and (j == parentJ)):
        Symbols.append(' ')
        Seq1.append('-')
        Seq2.append(FASTA2[j-1])

#horisontal element
    elif ((i == parentI) and (j-1 == parentJ)):
        Symbols.append(' ')
        Seq1.append(FASTA1[i-1])
        Seq2.append('-')

    i = parentI
    j = parentJ

#reversing the sequences
str1 = ''.join(reversed(Symbols))
str2 = ''.join(reversed(Seq1))
str3 = ''.join(reversed(Seq2))

#appending the remaining sequences and inserting gaps if required
str4 = ''.join(FASTA1[0:i])
str5 = ''.join(FASTA1[ivalue:len(FASTA1)])
str6 = ''.join(FASTA2[0:j])
str7 = ''.join(FASTA2[jvalue:len(FASTA2)])

if (len(str4) >= len(str6)):

    for k in range(0,len(str4)):
        str1 = " " + str1

    str2 = str4 + str2
    str3 = str6 + str3

    for k in range(0,(len(str4)-len(str6))):
        str3 = "-" + str3

else:
    for k in range(0,len(str6)):
        str1 = " " + str1

    str2 = str4 + str2
    str3 = str6 + str3

    for k in range(0,(len(str6)-len(str4))):
        str2 = "-" + str2

if (len(str5) >= len(str7)):

    str2 = str2 + str5
    str3 = str3 + str7

    for k in range(0,(len(str5)-len(str7))):
        str3 = str3 + "-"

else:

    str2 = str2 + str5
    str3 = str3 + str7

    for k in range(0,(len(str7)-len(str5))):
        str2 = str2 + "-"

#printing the score
print "Score: " + str(maxScore) + "\n"

#printing the sequences with respective symbols and formatting the length of each line to 80.
for i in range(0,len(str2),80):
    print str2[i:i+80]
    print str1[i:i+80]
    print str3[i:i+80]
    print "\n"

