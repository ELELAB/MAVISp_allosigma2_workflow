source /usr/local/envs/py310/bin/activate

cd input/

ln -s ../../2.allosigma_classify/output/allosigma_mut.txt

../../../../3.allosigma_heatmap/all/allosigma-heatmap  $1 allosigma_mut.txt

#$1 ../../1.allosteric_signalling_map/input/allosigmazip.zip

python ../../../../3.allosigma_heatmap/all/distribution_plot.py up_mutations.tsv up_mutations_distribution.pdf log
python ../../../../3.allosigma_heatmap/all/distribution_plot.py down_mutations.tsv down_mutations_distribution.pdf log

mv *.tsv *.pdf log ../output/
