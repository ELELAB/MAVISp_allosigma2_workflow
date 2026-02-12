# on our local server we have prepared a python env that needs to be sourced to run
module load python

#### NOTICE !!
#### OPTIONAL STEP IF YOU NEED TO UNDERSTAND THE OUTPUT

#requirements:
- allosigma-visualization script
- file.pdb

module load python #on our local server only
./allosigma-visualization --pdb file.pdb --down_tsv ../4.allosigma_filtering/filtered_down_pockets.tsv --up_tsv ../4.allosigma_filtering/filtered_up_pockets.tsv --residue_representation sticks

#note you can add --site P101 if there is just one mutational site you wish to investigate. 
#note that if you have mutations with mixed_effects according to MAVISp, you can better visualize their effect in the mixed_effects_visualization/ by following the corresponding readme.txt.

The folder also contains a subfolder called 'mixed_effects_visualisation/'. Inside you can find instructions to run the mixed_effects_visualization python script for the visualization of:
- Response sites predicted stability effect- given mutation of interest
- Responce sites their pocket clusters classification according to fpocket algorithm