# mixed_effects_visualization

# Requirements:

# 1.AlloSigma workflow completed up to 4.allosigma_filtering
# 2.MAVISp csv file available (e.g. GENENAME-simple_mode.csv)

# Where to run:
# Inside the mixed_effects_visualization/ dir in the 5.allosigma_visualisation/ folder of the protein of interest. You can find the MAVISp this file in the downstream_analysis folder of the curated MAVISp protein of choice. 

# How to run:
module load python
./mixed_effects_visualization -m MUTATION -c mavisp_file.csv

# Example of command line:
./mixed_effects_visualization -m L245F -c ARID3A-simple_mode.csv
