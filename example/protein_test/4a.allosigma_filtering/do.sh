source /usr/local/envs/py310/bin/activate

cd input/

ln -s ../../3.allosigma_heatmap/output/up_mutations.tsv
ln -s ../../3.allosigma_heatmap/output/down_mutations.tsv

../../../../4a.allosigma_filtering/allosigma-filtering -s $1 -i up_mutations.tsv -t 2 -d fraction -f 0.9  -a 20 --pocket
../../../../4a.allosigma_filtering/allosigma-filtering -s $1 -i down_mutations.tsv -t 2 -d fraction -f 0.9  -a 20 --pocket

#move results into output/
mv filtered_*.tsv pocket_residues.txt *.rsa *.asa *.log *_out *.csv ../output/
