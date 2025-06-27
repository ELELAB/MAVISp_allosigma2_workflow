#heatmap allosigma

# on our local server we have prepared a python env that needs to be sourced to run
module load python

#Requirements
- output from allosigma_classify
- output from allosteric signalling map,  i.e. NUI8P9VE.zip
- allosigma_heatmap script

#run do.sh with the zip file and the allosigma_mut from step 2.
bash do.sh ../../1.allosteric_signalling_map/allosigmazip.zip  ../../2.allosigma_classify/allosigma_mut.txt
python distribution_plot.py up_mutations.tsv up_mutations_distribution.pdf log
python distribution_plot.py down_mutations.tsv down_mutations_distribution.pdf log
