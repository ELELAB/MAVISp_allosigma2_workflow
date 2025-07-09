# Ensemble Long-Range: Allosigma2-PSN 

## Overview

This repository contains a collection of scripts designed to validate mutation-response site predictions identified with AlloSigMA2 (https://doi.org/10.1093/nar/gkaa338) using Protein-Structure Network (PSN) tool PyInteraph2 (DOI: 10.1021/acs.jcim.3c00574). This workflow integrates molecular dynamics (MD) simulations to enhance prediction accuracy by accounting for protein flexibility and persistent long-range interactions.

N.B. This workflow has been designed for a single-chain protein. (default chain ID used is A) 

### acPSN Construction 
#### Description
For the purpose of this workflow we are constructing an atomic-contact PSN using PyInteraph2 (DOI: 10.1021/acs.jcim.3c00574). Pairs of residues were retained only if their sequence distance exceeded Proxcut threshold of 1 for the edge calculations remained within a distance lower than 4.5Å. We kept edges with an occurrence higher than Pcrit 50% within the frames of the ensemble, weighted on the interaction strength Imin of 3. 

To change the aforementioned parameters, edit `1-contact.sh`.

Requirements:
- GROMACS version compatible with the ensemble (we use GROMAC 2024)
- PyInteraph2

Input: 
- Trajectory of the protein simulation, filtered to contain only protein atoms, if cofactors had been present those should also be removed
- PDB file, structure of the first frame of the simulation trajectory
- Normalization factor file, the one deposited here has been calculated for canonical amino acids (Kannan and Vishveshwara, 1999). If you have other residues please be aware the file will need to be customised. 

N.B. If your simulation also includes other non-canonical residues and you have used GROMACS, you will need the file in which you have specified the residue types (e.g. residuetypes.dat) and carry it over for this analysis.

N.B. The non-canonical residues such as HSE for HIS must be renamed prior to running the next step, otherwise the residue check will filter out these residues. 

Output: 
- acPSN graph
- log text file 
- PDB structure with chain ID 
- Python 2.7

Example  
See `ensemble/acpsn/readme.md`

### PSN Analysis
The following analysis is meant to take place in a nested directory within the one where the acPSN was generated, as in the example `/ensemble/acpsn/path_analysis/`. Here the workflow will perform the quality check on the input files and subsequently perform the PSN analysis of the communication paths. 

#### Quality Check
Within the first script of the workflow, `mut_extract.py`, the script will perform a quality check of the input files
`filtered_up_pockets.tsv` and `filtered_down_pockets.tsv`, looking at the following:
- input mutation sites and response sites are within the provided PDB structure

Here the user can also elect to include/filter the mutation sites by including a text file, using flag `-filter_file`. 

## Generation of SH scripts
Subsequently, using the output of the previous step `variant_response.tsv` the script `bash_gen.py` will then generate two SH scripts containing the commands to perform the path_analysis and the visualisation. 

The file containing the path_analysis commands `commands.sh` file should be executed first. 

This will generate a directory per each mutation site included in the analysis, wherein the PyInteraph2 path_analysis tool will be used to identify shortest paths of communication to the response sites. 

This file calls the summary script `summarise.py` which will output the final summarised results in file `results_summary.tsv`. 

The plotting file can then be executed, which calls the script `path_plot.py` and generates PSE visualisations in
each respective mutation site folder. 

### Requirements: 
- GROMACS
- PyInteraph2
- Python >= 3.7
- Pandas
- Biopython
- Pymol 

### Input:
- Simple mode Allosigma workflow output files: `filtered_up_pockets.tsv` and `filtered_down_pockets.tsv`
- PDB structure with chain ID
- acPSN graph DAT file 

### Output:
- variant_response.tsv, file containing the condensed mutation sites and respective reponse sites for analysis from the simple mode input files, that have satisfied the quality control step. 
- commands.sh, bash file containing commands for conducting the analysis 
- plot.sh, bash file containing commands to visualise the identified paths within each mutation site directory.  
- directories for each mutation site, within each a DAT and text file outputs of the path_analysis tool, containing the raw path information
- Pymol session files visualising the paths, stored within each mutation site directory
- results_summary.txt, text file containing the summarised findings of the workflow

### Example: 
See `/ensemble/acpsn/path_analysis/` and the `readme.md` file. 
N.B. to rerun the example please download the trajectory file from SMPD1 OSF repository: https://osf.io/w25ep/ (simulations_analysis/asm/membrane_bound/asm_5i85A_84-611_Man5glyN88_Man5glyN177_Man5glyN337_Man5glyN397_Man5glyN505_Man5glyN522/model1/heterogeneous/pc-34_pe-24_pi-8_ps-3_sm-6_chol-18_bmp-7/plpc_sapc_sdpc_plpe_sape_sapi_sdpi_saps_sdps_psm_lsm_chol_bmp/replicate1/charmm36/md/3.filt_trjs/traj_prot.xtc) from publication https://doi.org/10.1016/j.csbj.2024.05.049. 

