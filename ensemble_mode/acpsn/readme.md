# Requirements
# Trajectory filtered for protein atoms only
# Residuetypes.dat file (if applicable)
# PDB of the initial frame of the simulation
# Normalization file (may need to be customised)

# Activate the pyinteraph environment
# Load Python >= 3.7

# run the acPSN
tsp -N 1 ./1-contact.sh PDB TRAJ

# The log file in the folder can be used to check status of the calculation

# Check the last atom number of the PDB and edit chainize.py using that number
python2.7 chainize.py {PDB}.pdb > {PDB}_A.pdb

# Go to dir: path_analysis to continue
