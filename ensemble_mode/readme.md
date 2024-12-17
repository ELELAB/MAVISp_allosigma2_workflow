# Ensemble Long-Range: Allosigma2-PSN 

## Overview

This repository contains a collection of scripts designed to validate mutation-response site predictions identified with Allosigma using Protein-Structure Network (PSN) path analysis. This workflow integrates molecular dynamics (MD) simulations to enhance prediction accuracy by accounting for protein flexibility and persistent long-range interactions.

N.B. This workflow has been designed for a single-chain protein. 

### acPSN Construction 
#### Description
For the purpose of this workflow we are constructing an atomic-contact PSN using PyInteraph (ref). Pairs of residues were retained only if their sequence distance exceeded Proxcut threshold of 1 for the edge calculations remained within a distance lower than 4.5Å. We kept edges with an occurrence higher than Pcrit 50% within the frames of the ensemble, weighted on the interaction strength Imin of 3. 

To change the aforementioned parameters, edit `1-contact.sh`.

Requirements: 
- `source /usr/local/gromacs-2024/bin/GMXRC.bash`
- `. /usr/local/envs/pyinteraph/bin/activate`

Input: 
- Trajectory of the protein simulation, filtered to contain only protein atoms, if cofactors had been present those should also be removed
- PDB file, structure of the first frame of the simulation trajectory
- Normalization factor file, the one deposited here has been calculated for canonical amino acids (Kannan and Vishveshwara, 1999). If you have other residues please be aware the file will need to be customised. 

N.B. If your simulation also includes other non-canonical residues and you have used GROMACS, you will need the file in which you have specified the residue types (e.g. residuetypes.dat) and carry it over for this analysis.

Output: 
- acPSN graph
- log text file 
- PDB structure with chain ID 

Example  
See `ensemble/acpsn/readme.md`

### PSN Analysis
The following analysis is meant to take place in a nested directory within the one where the acPSN was generated, as in the example `/ensemble/acpsn/allosigma_psn/`. Here the workflow will perform the quality check on the input files and subsequently perform the PSN analysis of the communication paths. 

#### Quality Check
Within the first script of the workflow, `mut_extract.py`, the script will perform a quality check of the input files
`filtered_up_pockets.tsv` and `filtered_down_pockets.tsv`, looking at the following:
- input mutation sites and response sites are within the provided PDB structure
- input mutations sites and response sites satisfy the chosen distance threshold 

Here the user can also elect to include/filter the mutation sites and response sites by including a text file, using flag `-filter_file` or to change the distance threshold from default 15A by flag `-dist_threshold`. 

#### PSN analysis 
The workflow will make a directory per each mutation site included in the analysis, wherein the PyInteraph path_analysis tool will be used to identify shortest paths of communication to the response sites. 

Requirements: 
- `source /usr/local/gromacs-2024/bin/GMXRC.bash`
- `. /usr/local/envs/pyinteraph/bin/activate`
- Python >= 3.7
- Pandas
- Biopython
- Pymol 

Input:
- Simple mode Allosigma workflow 4b.filtering output files: `filtered_up_pockets.tsv` and `filtered_down_pockets.tsv`
- PDB structure with chain ID
- acPSN graph DAT file 

Output:
- variant_response.tsv, file containing the condensed mutation sites and respective reponse sites for analysis from the simple mode input files, that have satisfied the quality control step. 
- commands.sh, bash file containing commands for conducting the analysis 
- plot.sh, bash file containing commands to visualise the identified paths within each mutation site directory. 
- PML directory, containing PML scripts for user to visualise predicted mutation sites and respective response sites, prior to identification of paths. 
- directories per mutation sites, within each a DAT and text file outputs of the path_analysis tool, containing the raw path information
- Pymol Session Files visualising the paths, stored within each mutation site directory
- results_summary.txt, text file containing the summarised findings of the workflow

Example: 
See `/ensemble/acpsn/allosigma_psn/` and the `do.txt` file. 


