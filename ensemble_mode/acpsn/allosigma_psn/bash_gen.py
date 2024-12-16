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
import argparse
import pandas as pd

def read_input_file(input_file):
    '''Read input TSV.

    This function reads input TSV file. 

    Parameters 
    ----------
    input_file: tsv file

    Returns 
    ----------
    df: zip object
        Dataframe of mutations and response residues
    '''
    try:
        df = pd.read_csv(input_file, sep='\t')
        return zip(df.iloc[:, 0], df.iloc[:, 1])
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file {input_file} is empty.")
    except pd.errors.ParserError:
        raise ValueError(f"Error parsing CSV file: {input_file}")

def gen_sh_file(data, output_sh, input_file, path_plot_sh):
    '''Writes two bash files.

    The function writes two bash files, one for performing directory making, running path_analysis
    and running summary script; the other for plotting the results.  

    Parameters
    ----------
    data: df
        data contained in tsv file
    Returns 
    ----------
    output_sh: sh file 
        Text file containing path_analysis and summary commands.
    path_plot_sh: sh file 
        Text file containing path_plot commands. 
    '''
    try:
        with open(output_sh, 'w') as main_script, open(path_plot_sh, 'w') as plot_script:
            # Write command to load modules/envs
            main_script.write(f"#Load necessary modules\n" \
                              f". /usr/local/envs/pyinteraph/bin/activate\n")
            plot_script.write(f"#Load necessary modules\n" \
                              f"module load python/3.10\n")

            for mutation, pockets in data:
                # Define directory names and add chain ID prefix 
                mut_chain_id = f'A{mutation}'
                mut_dir = f"{mutation}_paths"

                # Add chain ID to pocket residues 
                pocket_chain_id = [f'A{pocket[1:]}' for pocket in pockets.split(',')]

                # Join pocket residues 
                pocket_list = ','.join(pocket_chain_id)

                # Define name of path_analysis output files
                output = f"shortest_{mut_chain_id.replace('/', '_')}"

                # Write path_analysis commands for each variant 
                main_script.write(
                    f"# {mutation}\n" \
                    f"mkdir {mut_dir}\n" \
                    f"path_analysis -i ../acpsn-graph_all.dat -r ../reference_A.pdb -s {mut_chain_id} -t {pocket_list} -p -a ./{mut_dir}/{output}\n"
                )

                # Write path_plot commands for each variant
                plot_script.write(
                    f"# {mutation}\n" \
                    f"python path_plot.py ../reference_A.pdb ./{mut_dir}/{output}.txt ./{mut_dir}/{mut_dir}_session.pse\n\n"
                )

            # Run path_summary to obtain overall results     
            main_script.write(f"#Final output for validation of long_range effects of variants\n" \
                              f"python summarise.py -tsv {input_file} -dir . -o results_summary.txt\n")

    except (IOError, Exception) as e:
        raise RuntimeError(f"Error writing to files {output_sh} or {path_plot_sh}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Generates sh files for use in path_analysis')
    parser.add_argument('-tsv', dest='input_file', required=True, help='Input TSV file.')
    parser.add_argument('-cmd', dest='output_sh', required=True, help='Output bash script for performing path_analysis.')
    parser.add_argument('-plot', dest='path_plot_sh', required=True, help='Output bash script for visualising paths.')
    args = parser.parse_args()

    # Read input file
    data = read_input_file(args.input_file)

    # Generate bash scripts
    gen_sh_file(data, args.output_sh, args.input_file, args.path_plot_sh)

if __name__ == "__main__":
    main()
