#!/bin/bash

# PDB file
pdb=$1

# Trajectory file  
traj=$2

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
