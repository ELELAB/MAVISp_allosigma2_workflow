# on our local server we have prepared a python env that needs to be sourced to run
module load python

#Requirements
- allosigma_filtering
- file.pdb
- up_mutations.tsv
- down_mutations.tsv

bash do.sh file.pdb

#running it with pockets per default. 
#default distance between heavy atoms  in the residues: 5.5 Å
#default dG value: 2 kcal/mol
#default minimum solvent accessibility: 25 %

#NOTICE!
# if you need to run filtering with no pocket limitations, just remove --pocket. 
# if you need to run filtering with a specific interface file, use the flag --interface 
# followed by a txt file with sites (style: A119). 
