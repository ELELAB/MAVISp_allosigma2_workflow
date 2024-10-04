source /usr/local/envs/py310/bin/activate
./allosigma-heatmap  $1 $2

#$1 ../../1.allosteric_signalling_map/allosigmazip.zip
#$2 ../../2.allosigma_classify/allosigma_mut.txt 
python distribution_plot.py up_mutations.tsv up_mutations_distribution.pdf log
python distribution_plot.py down_mutations.tsv down_mutations_distribution.pdf log
