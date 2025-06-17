#source python env.
module load python

#Requirements
- allosigma_filtering
- file.pdb
#having run classify and heatmap


bash do.sh wt.pdb

#running it with pockets per default. 
#default distance between CA in the residues: 10 Å
#default dG value: 2 kcal/mol
#default minimum solvent accessibility: 20

#NOTICE!
# if you need to run filtering with no pocket limitations, just remove --pocket. 
# if you need to run filtering with a specific interface file, use the flag --interface 
# followed by a txt file with sites (style: A119). 
