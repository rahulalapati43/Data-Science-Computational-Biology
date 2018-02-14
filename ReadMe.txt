-------------------------------
Effort Certification (5-point scale)
-------------------------------

1) Anuj Gupta : 5/5

2) Rahul Alapati : 5/5

3) Vineet Nayak : 5/5

4) Sritika Chakladar : 5/5

5) Austin Ream : 5/5



------------------
Usage Instructions
------------------
Describe how to run your program.

The following are the 4 files which are required to run our program:

1. project1.py (acts as a driver for globalAlignment.py)
2. globalAlignment.py
3. localAlignment.py
4. BLOSUM62.txt (We are opening this file in our program, so it has to be in the same directory and with the same name).

Please download the above mentioned files and place them in the same directory.

To generate the global alignment between 2 sequences use the following command:

python project1.py human_hemoglobin_alpha.fasta.txt mouse_hemoglobin_alpha.fasta.txt

where project1.py is the program name 
      
      human_hemoglobin_alpha.fasta.txt is the FASTA Sequence 1

      mouse_hemoglobin_alpha.fasta.txt is the FASTA Sequence 2.

To generate the local alignment between 2 sequences use the following command:

python localAlignment.py human_hemoglobin_alpha.fasta.txt mouse_hemoglobin_alpha.fasta.txt

where localAlignment.py is the program name
   
      human_hemoglobin_alpha.fasta.txt is the FASTA Sequence 1

      mouse_hemoglobin_alpha.fasta.txt is the FASTA Sequence 2.   

  
