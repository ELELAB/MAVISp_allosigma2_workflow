
#### NOTICE !!
#### OPTIONAL STEP IF YOU NEED TO UNDERSTAND THE OUTPUT

#requirements:
- allosigma-visualization script
- file.pdb

module load python
./allosigma-visualization --pdb file.pdb --down_tsv ../4a.allosigma_filtering/filtered_down_pockets.tsv --up_tsv ../4a.allosigma_filtering/filtered_up_pockets.tsv --residue_representation sticks

#note you can add --site P101 if there is just one mutational site you wish to investigate. 
