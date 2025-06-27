# on our local server we have prepared a python env that needs to be sourced to run
module load python

#Requirements
- allosigma_filtering
- file.pdb
- sites.txt
- up_mutations.tsv
- down_mutations.tsv

the sites.txt file is a simple list of residues, expressed as a [single letter residue type][residue number]
per line. For instance:

A98
C87
F298

# Here we run the filtering step without pockets but including a list of sites binding a cofactor
bash do.sh file.pdb sites.txt

#default distance between heavy atoms  in the residues: 5.5 Å
#default dG value: 2 kcal/mol
#default minimum solvent accessibility: 25 %

#NOTICE!
# if you need to run filtering with a specific interface file, use the flag --interface 
# followed by a txt file with sites (style: A119). 
