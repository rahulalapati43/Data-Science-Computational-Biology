#!/usr/bin/python -uB
import util
from testing import predict
import sys
import os
import cPickle

def main(blastpgp, nrdb, fastaFile):
	pass

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: " + sys.argv[0] + " /path/to/blastpgp /path/to/nrdb/file FASTA_file"
        else:
                main(sys.argv[1], sys.argv[2], sys.argv[3])
 
