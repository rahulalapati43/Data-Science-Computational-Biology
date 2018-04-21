#!/usr/bin/python -uB
import util
import sys
import os
import glob
from protein import Protein
import re
import random

def main(tmalign, dataDir):
    proteinsMap = getProteinsMap(dataDir)
    for proteinName in proteinsMap:
        print '\n\nProtein {0} has sequence {1}'.format(proteinName, proteinsMap[proteinName].getSequence())
        print 'Protein {0} has PssmAvgs {1}'.format(proteinName, proteinsMap[proteinName].getPssmAvgs())
        print 'Protein {0} has ExposedBurredAvgs {1}'.format(proteinName, proteinsMap[proteinName].getExposedBuriedAvgs())
        print 'Protein {0} has HECAvgs {1}'.format(proteinName, proteinsMap[proteinName].getHECAvgs())

    proteinPairs = getProteinPairs(proteinsMap)
    pair = random.choice(proteinPairs)
    print '\n\n\n{0} protein pairs found'.format(len(proteinPairs))
    print '{0} paired with {1} :::::::::: {2}'.format(pair[0].getProteinName(), pair[1].getProteinName(), pair[0].getTmScoreAvg(tmalign, pair[1]))

def getProteinsMap(dataDir):
    fastaFiles = glob.glob(os.path.join(dataDir, '*.fasta'))
    pdbFiles = glob.glob(os.path.join(dataDir, '*.pdb'))
    pssmFiles = glob.glob(os.path.join(dataDir, '*.pssm'))

    proteins = dict()
    for fasta in fastaFiles:
        proteinName = re.match('^(?:.*/)?(.+)\.fasta$', fasta).group(1)
        proteins[proteinName] = Protein(proteinName)
        proteins[proteinName].setFastaFile(fasta)

    for pdb in pdbFiles:
        proteinName = re.match('^(?:.*/)?(.+)_.*\.pdb$', pdb).group(1)
        proteins[proteinName].setPdbFile(pdb)

    for pssm in pssmFiles:
        proteinName = re.match('^(?:.*/)?(.+)\.pssm$', pssm).group(1)
        proteins[proteinName].setPssmFile(pssm)

    return proteins

def getProteinPairs(proteinsMap):
    proteinPairs = list()
    proteinNames = proteinsMap.keys()
    for i in range(0, len(proteinNames)):
        for j in range(i + 1, len(proteinNames)):
            proteinPairs.append((proteinsMap[proteinNames[i]], proteinsMap[proteinNames[j]]))

    return proteinPairs

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: " + sys.argv[0] + " /path/to/tmalign data_dir/"
    else:
        main(sys.argv[1], sys.argv[2])

