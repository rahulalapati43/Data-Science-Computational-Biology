#!/bin/bash

iter=0
for f in $@
do
	../project3/apps/blast/bin/blastpgp -d ../project3/nrdatabase/nr/nr -j 3 -b 1 -a 4 -i "$f" -Q "${f%.*}.pssm"
	iter=$(expr $iter + 1)
	echo $iter done
done
