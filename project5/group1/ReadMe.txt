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
The following 6 files are required to run our program:

   1. project5.py - main executable.
   2. gradientDescent.py - Contains gradient descent code
   3. featureGeneration.py - Generates features for use in logistic regression from fasta & pssm files
   4. util.py - Common functions used in all modules
   5. protein.py - Protein class definition
   6. weights_training_stochastic_lr_function.pickle - Snapshot of our model.  There are other model files available under the name weights_*.pickle if you'd like to test them out.

training.py and testing.py are not required to run the program but contain the code that generated our models and accuracies.  The dataset/ folder contains the exact dataset we used after the random split.

Please download the above mentioned files and place them in the same directory.  To predict the average 3D TM alignment score of two different proteins, use the following command:

		python project5.py /path/to/blastpgp /path/to/nr_file weights_training_stochastic_lr_function.pickle fasta_file_proteinA.fasta fasta_file_proteinB.fasta

where 
		-project5.py is the main executable
		-/path/to/blastpgp is the path to the blastpgp binary (blast/bin/blastpgp in the blast archive)
		-/path/to/nr_file is the nr file in the nr database (nr/nr in the nr_database.tar.gz archive)
		-weights_training_stochastic_lr_function.pickle is one of the weights pickle files included
		-fasta_file_proteinA.fasta is the file containing the first protein sequence in FASTA format.  This file should have the first line begin with '>' and give the protein name and subsequent lines give the fasta sequence
		-fasta_file_proteinB.fasta is the file containing the second protein sequence in FASTA format.  This file should have the first line begin with '>' and give the protein name and subsequent lines give the fasta sequence
