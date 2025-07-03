# Requirements
# Construction of the acPSN in the previous step in parent directory
# PDB with chain ID in parent directory
# Output filtered UP+DOWN files from simple_mode module results (Step 4)
# Python >= 3.7
# PyInteraph2

# To run the analysis
python mut_extract.py -up {filtered_UP_file} -down {filtered_DOWN_file} -out variant_response.tsv -pdb ../{PDB} 

python bash_gen.py -tsv variant_response.tsv -cmd commands.sh -plot plot.sh

tsp -N 1 bash commands.sh

bash plot.sh
