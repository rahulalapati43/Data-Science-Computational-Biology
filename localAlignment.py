import sys

BLOSUMfile = open("BLOSUM62.txt","r")
FASTAfile1 = open(sys.argv[1],"r")
FASTAfile2 = open(sys.argv[2],"r")

BLOSUMmatrix = {}
indexList = []
count = 0

for line in BLOSUMfile:
    if (count == 0):
        indexList = line.split()
        count = count + 1
    if not line.startswith(" "):
        rowList = []
        rowList = line.split()
        newrowList = rowList[1:len(rowList)]
        BLOSUMmatrix[rowList[0]] = newrowList

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

dpTable = [[dict([("score", 0)]) for j in range(len(FASTA2)+1)] for i in range(len(FASTA1)+1)]

for i in range(1,len(FASTA1)+1):
    dpTable[i][0]["parentI"] = i-1
    dpTable[i][0]["parentJ"] = 0

for j in range(1,len(FASTA2)+1):
    dpTable[0][j]["parentI"] = 0
    dpTable[0][j]["parentJ"] = j-1

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

        if (max["score"] < 0):
            max["score"] = 0

        dpTable[i][j] = max

maxScore = 0
ivalue = 0
jvalue = 0

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

while (dpTable[i][j]["score"] > 0):

    parentI = dpTable[i][j]["parentI"]
    parentJ = dpTable[i][j]["parentJ"]

    if ((i-1 == parentI) and (j-1 == parentJ)):
        FASTAindex = indexList.index(FASTA2[j-1])
        if (int(BLOSUMmatrix[FASTA1[i-1]][FASTAindex]) > 0):
            Symbols.append('|')
        else:
            Symbols.append('*')

        Seq1.append(FASTA1[i-1])
        Seq2.append(FASTA2[j-1])

    elif ((i-1 == parentI) and (j == parentJ)):
        Symbols.append(' ')
        Seq1.append('-')
        Seq2.append(FASTA2[j-1])

    elif ((i == parentI) and (j-1 == parentJ)):
        Symbols.append(' ')
        Seq1.append(FASTA1[i-1])
        Seq2.append('-')

    i = parentI
    j = parentJ

str1 = ''.join(reversed(Symbols))
str2 = ''.join(reversed(Seq1))
str3 = ''.join(reversed(Seq2))

# str4 = ''.join(FASTA1[0:i])
# str5 = ''.join(FASTA1[ivalue:len(FASTA1)])
# str6 = ''.join(FASTA2[0:j])
# str7 = ''.join(FASTA2[jvalue:len(FASTA2)])
#
# str2 = str4 + str2 + str5
# str3 = str6 + str3 + str7
#
# len1 = len(str4)
# len2 = len(str6)
# len3 = len(str5)
# len4 = len(str7)
#
# if len1 > 0:
#     str8 = " "
#     str12 = "-"
#     for k in range(0,len1-1):
#         str8 = str8 + " "
#         str12 = str12 + "-"
# else:
#     str8 = ''
#     str12 = ''
#
# if len2 > 0:
#     str9 = " "
#     str13 = "-"
#     for k in range(0,len2-1):
#         str9 = str9 + " "
#         str13 = str13 + "-"
# else:
#     str9 = ''
#     str13 = ''
#
# if len3 > 0:
#     str10 = " "
#     str14 = "-"
#     for k in range(0,len3-1):
#         str10 = str10 + " "
#         str14 = str14 + "-"
# else:
#     str10 = ''
#     str14 = ''
#
# if len4 > 0:
#     str11 = " "
#     str15 = "-"
#     for k in range(0,len4-1):
#         str11 = str11 + " "
#         str15 = str15 + "-"
# else:
#     str11 = ''
#     str15 = ''
#
# str1 = str8 + str1 + str9
# str2 = str14 + str2 + str15
# str3 = str12 + str3 + str13

print "Score: " + str(maxScore) + "\n"

for i in range(0,len(str2),80):
    print str2[i:i+80]
    print str1[i:i+80]
    print str3[i:i+80]
    print "\n"

