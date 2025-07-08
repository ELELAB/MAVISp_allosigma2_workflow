# LONG_RANGE WORKFLOWS 

This repository contains utilities to handle and visualize results from two different protocols for detecting allosteric mutations. 


In the simple_mode folder:

The first protocol is based on data from AlloSigMA2 and can be used in the simple_mode of MAVISp. This protocol is also applied as workflow for the LONG_RANGE modules of the MAVISP framework for variant effects in the simple mode (https://www.biorxiv.org/content/10.1101/2022.10.22.513328v4).


In the ensemble_mode folder:

This second protocol can be used in MAVISp ensemble_mode, and depends on the output from AlloSigMA2 and molecular dynamics simulations, and it is meant to be used to analyze results from a PSN-MD approach, i.e., the analyses of the protein conformations from a Molecular Dynamics (MD) trajectories using an atomic contact Protein Structure Network (acPSN). In particular, we used the results from path analysis from the acPSN-MD to further validate with an all-atom model and accounting for protein dynamics, the pairs of allosteric mutations and response sites proposed by the AlloSigMA2 workflow.

See below for the description of each individual script in details - to perform the steps as applied in MAVISp please refer to each individual subfolder and their script and readme. This protocol is also applied as workflow for the LONG_RANGE modules of the MAVISP framework for variant effects in the ensemble mode (https://www.biorxiv.org/content/10.1101/2022.10.22.513328v4).

Please see READMEs in the respective folders for further details
