#activate python environment
source /usr/local/envs/py310/bin/activate
#go into input directory where .pdb and .tsv files are located
cd input
#run UP filtering
../../../4a.allosigma_filtering/allosigma-filtering -s $1 -i up_mutations.tsv -t 2 -d sidechain_fraction -f 0.9 -a 20 --pocket
#run DOWN filtering
../../../4a.allosigma_filtering/allosigma-filtering -s $1 -i down_mutations.tsv -t 2 -d sidechain_fraction -f 0.9 -a 20 --pocket
#move results into output/
mv filtered_*.tsv pocket_residues.txt *.rsa *.asa *.log *_out ../output/

