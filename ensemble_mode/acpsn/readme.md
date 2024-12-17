# Requirements
-to have an estimate of the Icrit for your protein

# symbolic link to the traj
ln -s ../../../../3.filt_trjs/traj_prot.xtc
# have residuetypes.dat 
cp ../../../../3.filt_trjs/residuetypes.dat .

# run the acPSN
tsp -N 1 ./1-contact.sh

# the log file in the folder can be used to check status of the calculation

# check last atom of the PDB and edit chainize.py using that number i.e. here chains=3087
python2.7 chainize.py reference.pdb > reference_A.pdb
# N.B. reference_A.pdb will be used in allosigma_psn 
