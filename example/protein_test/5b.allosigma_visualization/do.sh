source /usr/local/envs/py310/bin/activate

cd input/

ln -s ../../4b.allosigma_filtering/output/filtered_down_pockets.tsv
ln -s ../../4b.allosigma_filtering/output/filtered_up_pockets.tsv

../../../../5b.allosigma_visualization/allosigma-visualization --pdb $1 --down_tsv filtered_down_pockets.tsv --up_tsv filtered_up_pockets.tsv --residue_representation sticks

#note you can add --site P101 if there is just one mutational site you wish to investigate.

#move results into output/
mv pymol_sessions ../output/
