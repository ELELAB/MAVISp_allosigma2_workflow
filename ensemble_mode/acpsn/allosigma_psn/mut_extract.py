"""
# Copyright (C) 2023 Karolina Krzesińska <kzokr@dtu.dk> 
# Danish Cancer Institute 

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Imports
import os
import pandas as pd
import argparse
import argcomplete
import warnings
import logging as log
import Bio.PDB
from Bio import BiopythonWarning

# Ignore PDBConstructionWarning
warnings.simplefilter('ignore', BiopythonWarning)

def check_file_exists(file_path):
    '''Check file exists.

    The function checks if the input file exists. 
        
    Parameters
    ----------
    file_path: 
        Path of given file to be checked.

    '''
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

def read_variant_filter(filter_file):
    '''Read filter file.

    This function reads file containing variants to filter for, if flag. 

    Parameters 
    ----------
    filter_file: str
        Path of filter file.  

    Returns 
    ----------
    variants_to_include: set 
        Set of residues to filter TSV files for. 
    '''
    variants_to_include = set()
    if filter_file:
        try: 
            with open(filter_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    variants_to_include.add(line)
            #print(variants_to_include)
            return variants_to_include
        except pd.errors.EmptyDataError:
            raise ValueError(f"The file {filter_file} is empty.")

def read_input_tsv(input_file):
    '''Read input TSV.

    This function reads input TSV file and drops unnecessary columns. 

    Parameters 
    ----------
    input_file: str
        Path to input file.

    Returns 
    ----------
    df: df 
        Dataframe of mutations and response sites.
    '''
    try:
        df = pd.read_csv(input_file, sep='\t', index_col='mutations')
        df.drop(['Unnamed: 0','n_mutations', 'avg_dG'], axis=1, inplace=True)
        return df
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file {input_file} is empty.")
    except pd.errors.ParserError:
        raise ValueError(f"Error parsing CSV file: {input_file}")

def distance_CA(res1, res2):
    ''' Calculate distances between CA atoms. 

    The function calculates distance between two residues CA atoms in Ångstrom.

    Parameters
    ----------
    res1: Bio.PDB.Residue.Residue
        First residue.
    res2: Bio.PDB.Residue.Residue
        Second residue.

    Returns
    ----------
    distance : int 
        Distance between 2 residues.
    '''
    distance = res1["CA"] - res2["CA"]
    return distance

def validate_residue(mutation, chain_id, res_pos, res_type, structure):
    '''Validate residues match from input in provided PDB structure.
    
    The function aims to validate both position and residue types are in
    agreement between the input files and the provided PDB. 
    
    Function is used to both validate mutation and pocket sites.
    
    Parameters 
    ----------
    mutation: str
        mutation 
    chain_id: str
        chain ID to be accessed in structure
    res_pos: str
        residue position
    res_type: str
        residue code
    structure: class object
        PDB structure. 
    Returns 
    ----------
    booleans
    '''
    try:
        # Fetch the residue from the structure
        res = structure[chain_id][res_pos]
        
        # Convert the PDB residue name to one-letter code
        pdb_res_type = Bio.PDB.Polypeptide.three_to_one(res.get_resname())
        
        # Compare the input residue type with the PDB residue type
        if pdb_res_type == res_type:
            return True
        else:
            log.warning(f"Residue mismatch: Input {mutation[:-1]}, PDB {pdb_res_type}{res_pos}")
            return False
    except KeyError:
        log.warning(f"Residue {mutation[:-1]} not found in chain {chain_id} of the PDB structure.")
        return False
    except Exception as e:
        log.error(f"Error during residue validation for {mutation}: {e}")
        return False
    
def summarize_mutations(df1, df2, variants_to_include, structure, threshold, chain_id):
    '''Summarize Variant-Response Sites.

    The function aims to summarize the variant and response sites found in down and up DF, 
    performing a distance check and if valid retained. 

    Parameters 
    ----------
    df1: df
        DF of UP variant-reponse pairs.
    df2: df
        DF of DOWN variant-reponse pairs.
    variants_to_include: set
        Nodes to filter original files on.
    structure: class object
        PDB structure. 
    threshold: int
        Distance threshold in Ångstrom (default: 15).
    chain_id: str
        ID of the chain to be accessed in structure (defualt: A).
    Returns 
    ----------
    summary_data:  df
        Dataframe containing validated variants and respective response residues.
    '''
    concatenated_df = pd.concat([df1, df2], axis=1, sort=True)
    
    # Extract the first mutation from each cell
    mutation_set = set()
    for mutation in concatenated_df.index:
        first_mutation = mutation.split()[0]
        mutation_set.add(first_mutation)

    # Filter the residues based on variants_to_include if it's provided
    if variants_to_include:
        mutation_set = {mut for mut in mutation_set if mut in variants_to_include}

    # Create a DataFrame to store the summary
    summary_data = {'Variant Sites': [], 'Response Sites': []}

    # Iterate through all mutation sites
    for mutation in mutation_set:
        res_pos, res_type = int(mutation[1:-1]), mutation[0]

        if not validate_residue(mutation, chain_id, res_pos, res_type, structure):
            continue

        res1 = structure[chain_id][res_pos]
        pocket_residues = concatenated_df.columns[concatenated_df.loc[[mut for mut in concatenated_df.index if mut.split()[0][:-1] == mutation[:-1]]].notna().any()].tolist()        

        # Check distance for each pocket residue
        valid_pocket_residues = set()

        for pocket in pocket_residues:
            pocket_pos, pocket_type = int(pocket[1:]), pocket[0]
            if not validate_residue(pocket, chain_id, res_pos, res_type, structure):
                continue
            try:
                res2 = structure[chain_id][pocket_pos]
                distance = distance_CA(res1, res2)
                if distance >= threshold:
                    valid_pocket_residues.add(pocket)
                else:
                    log.warning(f'Distance not sat for {mutation[:-1]} and {pocket} at distance {distance}')
            except KeyError:
                log.error(f"An error occurred for residue {mutation[:-1]} and pocket site {pocket}")
                continue

        # Add to summary if at least one pocket residue is above the threshold
        if valid_pocket_residues:
            summary_data['Variant Sites'].append(mutation[1:-1])
            summary_data['Response Sites'].append(','.join(sorted(valid_pocket_residues)))

    return pd.DataFrame(summary_data)

def write_pml_script(mutation, pocket_residues, pdb_file):
    '''Generate PML 
    This function writes a PML script for PyMOL visualization per mutation

    Parameters
    ----------
    mutation: str
        Mutation identifier.
    pocket_residues: str
        Comma-separated string of pocket residues.
    pdb_file: str
        Path to the PDB file.

    Returns
    ----------
    pml_script: text file
        PML file for plotting in Pymol. 
    '''
    # Write pml script
    pml_script = f"""
# PyMOL script for mutation: {mutation}
load {pdb_file}
color white, {pdb_file[:-4]}
# Select mutation CA and color blue
set sphere_scale, 0.5
select {mutation}_CA, resi {mutation} and name CA
show sphere, {mutation}_CA
color red, {mutation}_CA
    """
    # For each residue found write the following lines to pml
    residues = pocket_residues.split(',') 
    for i in residues:
        # Remove first character 
        res_sel = i[1:]
        # Select pocket residue CA and color it individually
        pml_script += f"""
# Select pocket residue {res_sel} CA and color it individually
select {res_sel}_pocket_CA, resi {res_sel} and name CA
show sphere, {res_sel}_pocket_CA
color blue, {res_sel}_pocket_CA
distance dist_{mutation}_{res_sel}, {mutation}_CA, {res_sel}_pocket_CA
        """
    # Save PML file for each variant 
    save_pml(pml_script, mutation)

def save_pml(pml_script, mutation_file):
    '''Save PML file. 

    The function 

    Parameters
    ----------
    pml_script: str
    mutation_file: str

    Returns 
    ----------
    script_file: txt file
         PML script for plotting.
    '''
    # Ensure the PML directory exists
    pml_directory = "PML"
    if not os.path.exists(pml_directory):
        os.makedirs(pml_directory)

    # Save PML file for each variant 
    script_filename = os.path.join(pml_directory, f"{mutation_file}.pml")
    try:
        with open(script_filename, 'w') as script_file:
            script_file.write(pml_script)
    except Exception as e:
        raise RuntimeError(f"Error writing PML script to file {script_filename}: {e}")

def write_summary_tsv(summary_df, output_file):
    ''' Write output TSV file.

    The function writes the idenfied variant-response sites to TSV file. 

    Parameters
    ----------
    summary_df: df
        Dataframe of identified variants and response sites.  
    output_file: str 
        Name of output file.  
    '''
    try:
        # Sort the DataFrame 
        summary_df['Variant Sites'] = summary_df['Variant Sites'].apply(lambda x: int(x))
        summary_df.sort_values(by='Variant Sites', inplace=True)

        summary_df['Response Sites'] = summary_df['Response Sites'].apply(lambda x: ','.join(sorted(x.split(','), key=lambda y: int(y[1:]))))

        summary_df.to_csv(output_file, sep='\t', index=False)
        log.info(f"File saved to {output_file}")
    except Exception as e:
        log.error(f"Error writing to file {output_file}: {e}")

def main():
    # Basic logging configuration
    log.basicConfig(level=log.INFO, \
                    format='%(levelname)s - %(message)s')
    
    parser = argparse.ArgumentParser(description='Extract variants predicted to affect long-range response sites')
    parser.add_argument('-up', dest='file_up', help='Path to filtered_up.tsv', required=True,)
    parser.add_argument('-down', dest='file_down', help='Path to filtered_down.tsv', required=True, )
    parser.add_argument('-out', dest='output_file', help='Output file', required=True, )
    parser.add_argument('-pdb', dest='pdb_file', help='PDB file to be used for pml scripts', required=True,)
    parser.add_argument('-filter_file', dest='filter_file', help='Option to filter for specific variants/VUS, format: A000A', default=None)
    parser.add_argument('-dist_threshold', dest='dist_threshold', type=int, help='Distance threshold in Ångstrom (default: 15)', default=15)
    parser.add_argument('-chain', dest='chain_id', type=str, help='Chain ID (default: A)', default='A')
    args = parser.parse_args()
    argcomplete.autocomplete(parser)

    # Check if input files and PDB file exist
    check_file_exists(args.file_up)
    check_file_exists(args.file_down)
    check_file_exists(args.pdb_file)

    # Define PDB structure
    pdb_id = os.path.splitext(os.path.basename(args.pdb_file))[0]
    # Select the PDB model 0 
    structure = Bio.PDB.PDBParser().get_structure(pdb_id, args.pdb_file)[0]

    # Read input files
    df1 = read_input_tsv(args.file_up)
    df2 = read_input_tsv(args.file_down)

    # Read variants to include from the filter file
    variants_to_include = read_variant_filter(args.filter_file)

    # Summarize mutations
    summary_df = summarize_mutations(df1, df2, variants_to_include, structure, args.dist_threshold, args.chain_id)
 
    # Write summary to a TSV file
    write_summary_tsv(summary_df, args.output_file)

    # Write PML directory and save PML scripts for each variant
    for mutation, pocket_residues in zip(summary_df['Variant Sites'], summary_df['Response Sites']):
        write_pml_script(mutation, pocket_residues, args.pdb_file)

if __name__ == "__main__":
    main()