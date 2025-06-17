source /usr/local/envs/py310/bin/activate

ln -s ../3.allosigma_heatmap/all/up_mutations.tsv
ln -s ../3.allosigma_heatmap/all/down_mutations.tsv

./allosigma-filtering -s $1 -i up_mutations.tsv -t 2 -d fraction -f 0.9  -a 20 --pocket
./allosigma-filtering -s $1 -i down_mutations.tsv -t 2 -d fraction -f 0.9  -a 20 --pocket

