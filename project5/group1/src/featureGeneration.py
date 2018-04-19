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

    pssmMap = util.pssmsMap(proteins,pssmFiles)

    for proteinName in proteins:
        proteins[proteinName].setExposedBuriedAvgs()
        proteins[proteinName].setHECAvgs()

    for proteinName in proteins:
        print '\n\nProtein {0} has sequence {1}'.format(proteinName, proteins[proteinName].getSequence())
        print 'Protein {0} has PssmAvgs {1}'.format(proteinName, proteins[proteinName].getPssmAvgs())
        print 'Protein {0} has ExposedBurredAvgs {1}'.format(proteinName, proteins[proteinName].getExposedBuriedAvgs())
        print 'Protein {0} has HECAvgs {1}'.format(proteinName, proteins[proteinName].getHECAvgs())


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: " + sys.argv[0] + "/path/to/blastpgp /path/to/nrdb/file /path/to/tmalign data_dir/"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

