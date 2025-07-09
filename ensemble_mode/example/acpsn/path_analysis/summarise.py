"""
# Copyright (C) 2023 Karolina Krzesińska <kzokr@dtu.dk> 
# Danish Cancer Institute 

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Imports
import argparse
import csv
from pathlib import Path
import logging as log


def check_file_exists(file_path):
    '''Check file exists.

    The function checks if the input file exists. 

    Parameters
    ----------
    file_path: str
        Path of given file to be checked.
    '''
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    
def read_tsv(tsv_file):
    '''Read TSV file.

    The function reads and parses input TSV file. 

    Parameters 
    ----------
    tsv_file: str
        Path of TSV file. 

    Returns 
    ----------
    tsv_data: dict
        Dictionary of variant and response sites.
    '''
    tsv_data = {}
    try:
        with open(tsv_file, 'r') as tsv:
            reader = csv.reader(tsv, delimiter='\t')
            next(reader)
            for row in reader:
                # Define variant and response sites
                variant = row[0]
                mutations = row[1]
                pocket_residues = [res.strip()[1:] for res in row[2].split(',')]
                # Split up list of residues to single pairs 
                for residue in pocket_residues:
                    tsv_data.setdefault(variant, []).append((mutations, residue))
    except Exception as e:
        log.error(f"Error reading TSV file: {e}")
        raise 
    return tsv_data

def collect_result_files(directory):
    '''Identify files to be read and analysed.

    The function collects files from _paths subdirectories within the working directory.

    Parameters
    ----------
    directory : str
        Path of current working directory.

    Returns
    -------
    result_files : list
        Paths to the identified result files.
    '''
    result_files = []

    base_dir = Path(directory)
    if not base_dir.is_dir():
        raise NotADirectoryError(f"Invalid directory path: {directory}")
    try:
        for subdir in base_dir.rglob("*_paths"):
            if subdir.is_dir():
                for file in subdir.glob("shortest_*.txt"):
                    result_files.append(file)
    except Exception as e:
        raise RuntimeError(f"Unexpected error collecting files: {e}")
    if not result_files:
        raise FileNotFoundError(f"No result files found in {directory}")
    return result_files

def update_result_data(result_data, key, path, average_weight, length, sum_weights):
    '''Update dictionary with new paths.

    The function updates dictionary with paths between variant and response site,
    reporting the path with max path_avg_weight and the number of paths found.

    Parameters
    ----------
    result_data : dict
        Dictionary to update.
    key : tuple
        Key representing (variant, response site) pair.
    path : str
        Path identified between variant and response site
    length_path : float
        Length of the identified path.
    sum_weights : str
        Sum of weights of the identified path.
    path_avg_weight : float
        Average weight of the identified path.
    '''
    entry = result_data.setdefault(key, {
        'paths': [],
        'max_weight_path': None,
        'max_weight': 0.0,
        'num_paths': 0})

    entry['paths'].append({
        'path': path,
        'average_weight': average_weight,
        'length': length,
        'sum_weights': sum_weights})
    entry['num_paths'] += 1

    if average_weight > entry['max_weight']:
        entry.update({
            'max_weight': average_weight,
            'max_weight_path': path,
            'length': length,
            'sum_weights': sum_weights})

def read_result_file(result_file):
    '''Reads files returning dicts. 

    The function reads given result file, calls the update_result_data function
    and performs a path length check (>=4), returning a dictionary. 

    Parameters
    ----------
    result_file : str
        Path to the given file.

    Returns
    -------
    result_data : dict
        Dictionary containing the parsed result data.
    '''
    result_data = {}
    min_path_length = 4
    required_columns = ['path', 'source', 'target', 'length', 'sum_weights', 'avg_weight']

    try:
        with open(result_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            if not set(required_columns).issubset(reader.fieldnames):
                log.warning(f"Skipping {result_file}: Missing required columns")
                return result_data

            for row in reader:
                length = int(row['length'])
                if length < min_path_length:
                    continue

                var = row['source'][1:]
                target = row['target'][1:]
                key = (var, target)

                update_result_data(
                    result_data,
                    key,
                    row['path'],
                    float(row['avg_weight']),
                    length,
                    float(row['sum_weights']))
    except (OSError, ValueError, KeyError) as e:
        log.error(f"Error reading {result_file}: {e}")
        raise
    return result_data


def concatenate_results(result_files):
    '''Concatenate result dictionaries. 

    The function loops through files and concatenates them into a single dictionary.

    Parameters
    ----------
    result_files : list
        List of paths to result files.

    Returns
    -------
    concatenated_data : dict
        Dictionary containing concatenated results.
    '''
    concatenated_data = {}

    for result_file in result_files:
        try:
            result_data = read_result_file(result_file)
            concatenated_data.update(result_data)
        except Exception as e:
            log.error(f"Failed to process {result_file}: {e}")
            raise
    return concatenated_data


def compare_data(tsv_data, result_data):
    '''Compare AlloSigma predictions to PSN results. 

    The function performs comparison of the data predicted by AlloSigma in the TSV data with
    the results of the PSN-based path analysis and returns the final results.

    Parameters
    ----------
    tsv_data : dict
        Dictionary containing data from the initial TSV file.
    result_data : dict
        Dictionary containing concatenated PSN result data.

    Returns
    -------
    compared_data : dict
        Dictionary containing results vs predictions data.
    '''
    compared_data = {}

    for variant, residues in tsv_data.items():
        for mutations, residue in residues:
            key = (variant, residue)
            entry = result_data.get(key, {
                'num_paths': 0,
                'max_weight_path': '0',
                'max_weight': 0.0,
                'length': 0,
                'sum_weights': 0.0})
            compared_data[key] = {
                'variant': variant,
                'mutations': mutations, 
                'residue': residue, 
                'num_paths': entry['num_paths'], 
                'max_weight_path': entry['max_weight_path'], 
                'max_weight': entry['max_weight'],
                'length': entry['length'],
                'sum_weights': entry['sum_weights']}

    return compared_data

def write_output(compared_data, output_file):
    '''Write summary output text file.

    The function writes a text file containing a summary of the results. 

    Parameters
    ----------
    compared_data : dict
        Dictionary containing the final results.
    output_file : str
        Path to the output file.
    '''
    try:
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output, delimiter='\t')
            writer.writerow(['Variant_Site', 
                             'Variants', 
                             'Response_Site',
                            'Total_Paths', 
                            'Path', 
                            'Length', 
                            'Sum_Weights', 
                            'Average_Weight'])
            for data in compared_data.values():
                writer.writerow([
                    data['variant'], 
                    data['mutations'],
                    data['residue'], 
                    data['num_paths'], 
                    data['max_weight_path'],
                    data['length'], 
                    data['sum_weights'],
                    data['max_weight']])
        log.info(f"File saved to {output_file}")
    except Exception as e:
        log.error(f"Error writing to file {output_file}: {e}")
        raise

def main(tsv_file, working_dir, output_file):
    # Check if the TSV file exists
    check_file_exists(tsv_file)

    # Read TSV file
    tsv_data = read_tsv(tsv_file)

    # Collect all result text files in the subdirectories
    result_files = collect_result_files(working_dir)

    # Parse and concatenate result data from all identfied files
    concatenated_data = concatenate_results(result_files)

    # Compare TSV data to the PSN results
    compared_data = compare_data(tsv_data, concatenated_data)

    # Write final summary of results as text file
    write_output(compared_data, output_file)

if __name__ == "__main__":
    # Basic logging configuration
    log.basicConfig(level=log.INFO, \
                    format='%(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="Process TSV and result path txt files.")
    parser.add_argument('-tsv', dest="tsv_file", required=True, help="Path to the TSV file")
    parser.add_argument('-dir', dest="working_dir", required=True, help="Directory containing result subdirectories")
    parser.add_argument('-o', dest="output_file", required=True, help="Path to the output file")
    args = parser.parse_args()

    main(args.tsv_file, args.working_dir, args.output_file)
