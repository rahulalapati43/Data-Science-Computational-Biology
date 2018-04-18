#!/usr/bin/python -uB
import util
import sys
import os
import glob
from Protein import Protein
import re

def main(blastpgp, nrdb, tmalign, dataDir):
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

    for proteinName in proteins:
        print 'Protein {0} has sequence {1}'.format(proteinName, proteins[proteinName].getSequence())

def pssmsMap(pssmFiles):
    pssmsMap = dict()
    for pssmFile in pssmFiles:
        sequenceName, sequence, pssmHeader, pssmSequence = util.readPSSM(pssmFile)
        pssmsMap[sequence] = slidingWindow(pssmSequence, 5)

    return pssmsMap

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: " + sys.argv[0] + "/path/to/blastpgp /path/to/nrdb/file /path/to/tmalign data_dir/"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
