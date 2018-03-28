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

	1. project3.py - main executable.
	2. training.py - File that can make a new gaussianModel.pickle file.
	3. testing.py - File that can test the accuracy of a guassianModel given a test pssm and ss files.
        4. util.py - Common functions used in both training.py and testing.py
	5. gaussianModel.pickle - Snapshot of one our generated gaussian model.

Please download the above mentioned files and place them in the same directory.  To classify a multifasta file of protein sequences using our trained gaussian model, use the following command:

				python project3.py /path/to/blastpgp /path/to/nr_file multifasta_file.fa

where 
		-project3.py is the main executable
                -/path/to/blastpgp is the path to the blastpgp binary (blast/bin/blastpgp in the blast archive)
                -/path/to/nr_file is the nr file in the nr database (nr/nr in the nr_database.tar.gz archive)
		-multifasta_file.fa is the file containing protein sequences in MULTI-FASTA format.
