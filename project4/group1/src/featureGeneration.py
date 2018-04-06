#!/bin/python -uB
import util
import sys

def main(blastpgp, nrdb, outdir, fastaFiles):
    for multifasta in fastaFiles:
        util.generatePssm(multifasta, outdir, blastpgp, nrdb)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: " + sys.argv[0] + "/path/to/blastpgp /path/to/nrdb/file out_pssm_dir/ FASTA_files..."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
