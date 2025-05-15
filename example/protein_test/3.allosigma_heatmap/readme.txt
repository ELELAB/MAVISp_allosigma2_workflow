#heatmap allosigma

#Requirements
- output from allosigma_classify (symlinked from step 2)
- output from allosteric signalling map,  i.e. NUI8P9VE.zip (passed as argument)
- allosigma_heatmap script 

#run do.sh with the zip file and the allosigma_mut from step 2.
bash do.sh ../../1.allosteric_signalling_map/input/allosigmazip.zip  allosigma_mut.txt
python ../../../../3.allosteric_heatmap/all/distribution_plot.py up_mutations.tsv up_mutations_distribution.pdf log
python ../../../../3.allosteric_heatmap/all/distribution_plot.py down_mutations.tsv down_mutations_distribution.pdf log
