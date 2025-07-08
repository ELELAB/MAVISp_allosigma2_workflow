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
from pymol import cmd

def parse_args():
    parser = argparse.ArgumentParser(description="PyMOL script for visualizing paths in a PDB structure.")
    parser.add_argument("pdb_file", help="Input PDB file")
    parser.add_argument("txt_file", help="Input text file with path information")
    parser.add_argument("output_file", help="Output PyMOL session file")
    return parser.parse_args()

args = parse_args()

# Load your PDB structure once
structure_name = "reference"
cmd.load(args.pdb_file, structure_name)

# Set the overall structure to grey and slightly transparent
cmd.set("cartoon_color", "grey")
cmd.set("cartoon_transparency", 0.8)
cmd.set_color("path", [0.00392156862745098,0.1607843137254902,0.37254901960784315])

# Dictionary to store path information
paths_info = {}

with open(args.txt_file, 'r') as file:
    # Skip the header line
    next(file)
    for line in file:
        columns = line.strip().split('\t')
        path = columns[0]

        # Remove 'A' in front of each residue and split the path into individual residues
        residues = [residue[1:] for residue in path.split(',')]

        # Store path information
        start_residue, end_residue = residues[0], residues[-1]
        paths_info[path] = {'residues': residues, 'start_residue': start_residue, 'end_residue': end_residue}

# Display sequential paths
for path, info in paths_info.items():
    residues = info['residues']

    # Select CA atoms for each residue in the path
    selection_expr = ' + '.join([f"{structure_name} and resi {residue} and name CA" for residue in residues])

    # Create a named selection for each path
    path_name = f"path_{'_'.join(residues)}"
    cmd.select(path_name, selection_expr)

    # Create bonds between consecutive residues in the path and display them as sticks
    for i in range(len(residues) - 1):
        resid1, resid2 = residues[i], residues[i + 1]

        cmd.distance(f"{structure_name} and resi {resid1} and name CA", f"{structure_name} and resi {resid2} and name CA")

        # Set path display 
        cmd.set("dash_width", 4)
        cmd.set("dash_color", "path")
        cmd.set("dash_gap", 0.0)

        cmd.show("sticks", f"{structure_name} and resi {resid1} and name CA + {structure_name} and resi {resid2} and name CA")

        # Hide distance labels
        cmd.hide("labels")

    # Display spheres for the starting and end residues
    start_residue = info['start_residue']
    end_residue = info['end_residue']
    cmd.show("spheres", f"{structure_name} and resi {start_residue} and name CA")
    cmd.show("spheres", f"{structure_name} and resi {end_residue} and name CA")
    cmd.color("magenta", f"{structure_name} and resi {start_residue} and name CA")
    cmd.color("blue",  f"{structure_name} and resi {end_residue} and name CA")
    cmd.set("sphere_scale", 0.5, f"{structure_name} and resi {start_residue} and name CA")
    cmd.set("sphere_scale", 0.5, f"{structure_name} and resi {end_residue} and name CA")

# Adjust the view
cmd.zoom()

# Save the PyMOL session
session_file = args.output_file
cmd.save(session_file)

