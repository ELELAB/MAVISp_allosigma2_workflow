# Requirements
# Construction of the acPSN in the previous step in parent directory
# PDB with chain ID in parent directory
# Output filtered UP+DOWN files from simple_mode module results (Step 4)
# Python >= 3.7
# PyInteraph2

# To run the analysis
module load python
python mut_extract.py -up filtered_up_pockets.tsv -down filtered_down_pockets.tsv -out variant_response.tsv -pdb ../reference_A_renum.pdb 
python bash_gen.py -tsv variant_response.tsv -cmd commands.sh -plot plot.sh -pdb reference_A_renum.pdb
tsp -N 1 bash commands.sh
bash plot.sh
