------------------------------------
Effort Certification (5-point scale)
------------------------------------
1) Vineet Nayak : 5/5

2) Rahul Alapati : 5/5

3) Anuj Gupta : 5/5

4) Sritika Chakladar : 5/5

5) Austin Ream : 5/5

------------------
Usage Instructions
------------------
The following 5 files are required to run our program:

   1. project4.py - main executable.
   2. gradientAscent.py - Contains gradient ascent code
   3. featureGeneration.py - Generates features for use in logistic regression from fasta & pssm files
   4. util.py - Common functions used in all modules
   5. weights_minibatch.pickle - Snapshot of our better model
   6. weights_stochastic.pickle - snapshot of our stochastic gradient ascent model.  This does not predict any 1s and is not useful but included for illustration purposes

Please download the above mentioned files and place them in the same directory.  To classify a multifasta file of protein sequences using our trained gaussian model, use the following command:

		python project4.py /path/to/blastpgp /path/to/nr_file model.pickle fasta_file.fa

where 
		-project4.py is the main executable
		-/path/to/blastpgp is the path to the blastpgp binary (blast/bin/blastpgp in the blast archive)
		-/path/to/nr_file is the nr file in the nr database (nr/nr in the nr_database.tar.gz archive)
		-model.pickle is one of the weights pickle files included (ie.: weights_minibatch.pickle)
		-fasta_file.fa is the file containing a protein sequences in FASTA format.  This file should have the first line begin with '>' and give the protein name and subsequent lines give the fasta sequence
