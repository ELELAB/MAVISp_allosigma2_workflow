# on our local server we have prepared a python env that needs to be sourced to run
module load python

#### NOTICE !!
#### OPTIONAL STEP IF YOU NEED TO UNDERSTAND THE OUTPUT

#requirements:
- allosigma-visualization script
- file.pdb

module load python
./allosigma-visualization --pdb  ../1.allosteric_signalling_map/wt.pdb --down_tsv ../4.allosigma_filtering/filtered_down_pockets.tsv --up_tsv ../4.allosigma_filtering/filtered_up_pockets.tsv --residue_representation sticks
#note you can add --site P101 if there is just one mutational site you wish to investigate. 
