# Validating Allosigma Predictions with MD-PSN  
Collection of scripts for validating mutation-response site predictions identified with Allosigma using PSN path_analysis

N.B. Filtering of Allosigma UP/DOWN predictions must have been performed prior \
N.B. acPSN must have been constructed prior

## Requirements
### Environment
. /usr/local/envs/pyinteraph/bin/activate 

### Scripts
- `mut_extract.py`
- `bash_gen.py`
- `plot_paths.py`
- `summarise.py`
### Files
Files from 4b.filtering:
-- filtered_up_pockets.tsv \
-- filtered_down_pockets.tsv \
- reference_A.pdb 

### Intended location
`/data/user/shared_projects/mavisp/{protein}/simulations_analysis/free/{WT}/{replicate1}/{CHARMM}/md/8.psn/pyinteraph2/acPSN/full_traj/path_analysis`

## Summarize and Filter Predictions
First the mutants and respective predicted response sites are extracted, written to a tsv file, optionally one can filter for specific mutants.
### Script
- `mut_extract.py`

### Usage
``mut_extract.py [-h] -up INPUT_FILE_UP -down INPUT_FILE_DOWN -out
                             OUTPUT_FILE -pdb PDB_FILE
                             [--filter_file FILTER_FILE]``
### Options
- Include a text file specifying variants of interest to filter only for those, format of variants should follow X000X.

### Output 
- PML directory containing scripts if one want to visually inspect the predictions and manually exclude 
- TSV file containing mutants and respective affected pocket residues.

## Generate Bash Script
Script to generate a bash to make directories within path_analysis for each mutant and perform path_analysis and plotting for the predicted response sites. 
Lastly the bash executes a script that summarises PSN findings, reporting number of paths identified per pair and the maximum 'average weight' of the path. 
### Scripts 
- `bash_gen.py`
- `plot_paths.py`
- `summarise.py`
### Output 
- Text file summarising the findings 
 
## Example Procedure
cp filtered_up_pockets.tsv\
cp filtered_down_pockets.tsv \
module load python/3.10
python mut_extract.py -up filtered_up_pockets.tsv -down filtered_down_pockets.tsv -out variant_response.tsv -pdb ../reference_A.pdb 
python bash_gen.py -tsv variant_response.tsv -cmd commands.sh -plot plot.sh
tsp -N 1 bash commands.sh
bash plot.sh
