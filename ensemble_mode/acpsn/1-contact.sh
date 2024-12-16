#!/bin/bash
source /usr/local/gromacs-2024/bin/GMXRC.bash
. /usr/local/envs/pyinteraph/bin/activate

# N.B. if protein has a cofactor it should be removed from trajectory
# and topology prior to PSN constructuion 

# N.B. custome normalization factor file may be needed in case
# of other residues 

# copy first frame of trajectory as PDB file
cp ../../../../4.frames/pdbmovie_1.pdb reference.pdb
pdb=reference.pdb

# use trajectory with only protein atoms 
traj=traj_prot.xtc

#acPSN with Imin 3.0
pyinteraph -v \
	-s $pdb\
	-t $traj\
       	-r $pdb --acpsn\
	--acpsn-proxco 1\
        --acpsn-imin 3.0\
	--acpsn-co 4.5\
	 --acpsn-perco 50\
	--acpsn-ew strength\
	--acpsn-graph acpsn-graph.dat\
	--acpsn-nf-file normalization_factors.ini &> log
