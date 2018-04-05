import util
import sys
import cPickle

def main(blastpgp, nrdb, fastaFiles, fakeRrFiles):
    pass

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: " + sys.argv[0] + "/path/to/blastpgp /path/to/nrdb/file FASTA_file secondaryStructure_File"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
