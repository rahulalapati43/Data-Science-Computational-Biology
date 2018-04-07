#!/usr/bin/python -uB
import util
import featureGeneration
import argparse
import sys
import os
import cPickle

def main(blastpgp, nrdb, fastaFiles, rrFiles, tempDir):
    pssmFiles = list()
    for multifasta in fastaFiles:
        pssmFiles.extend(util.generatePSSM(multifasta, tempDir, blastpgp, nrdb))

    generateModel(pssmFiles, rrFiles)

def generateModel(pssmFiles, rrFiles):
    featureMatricies = list()

    instances = featureGeneration.getDataset(pssmFiles, rrFiles)
    print instances

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate trained model based on fasta and rr (contact map) files') 
    #parser.add_argument('blast_path', help='Path to blastpgp binary')
    #parser.add_argument('nrdb', help='Path to nr file in nr database')
    #parser.add_argument('--fasta', help='Fasta files to train on', nargs='+', required=True)
    #parser.add_argument('--temp_dir', help='Temporary directory for PSSM files generated (default CWD/.temp)', default=os.path.join(os.getcwd(), '.temp'))
    parser.add_argument('--rr', help='RR files to train train on', nargs='+', required=True)
    parser.add_argument('--pssms', help='Get PSSM files from here instead of generating from fasta', nargs='+', required=True)
    args = parser.parse_args()

    if args.pssms is not None:
        generateModel(args.pssms, args.rr)
    else:
        main(args.blast_path, args.nrdb, args.fasta, args.rr, args.temp_dir)
