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
The following 3 files are required to run our program:

	1. project2.py - main executable
	2. id3.py - Core logic that forms the trained model and makes predictions.
	2. acidAttributes.py - Table that describes the attributes of amino acids.
	3. decisionTree.pickle - Snapshot of one our decision trees that can be used for predictions.

Please download the above mentioned files and place them in the same directory.  To classify a fasta file of protein sequences using our trained ID3 model, use the following command:

				python project2.py fasta_file.fa

where 
		-project2.py is the main executable
		-fasta_file.fa is the file containing protein sequences in MULTI-FASTA format.  fasta_file.fa can contain just a single protein sequence without the '>' line, also.
