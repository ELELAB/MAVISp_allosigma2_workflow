# mixed_effects_visualization

# Requirements:

# 1.AlloSigma workflow completed up to 4.allosigma_filtering
# 2.MAVISp csv file available (e.g. GENENAME-simple_mode.csv)

# Where to run:
# Inside the mixed_effects_visualization/ dir in the 5.allosigma_visualisation/ folder of the protein of interest.

# How to run:
module load python
./mixed_effects_visualization -m MUTATION -c mavisp_file.csv

# Example of command line:
./mixed_effects_visualization -m R1781A -c /data/raw_data/computational_data/mavisp_database_downstream/ALPK2/downstream_analysis_15082025/simple/mavisp_csv/15082025/ALPK2-simple_mode.csv
