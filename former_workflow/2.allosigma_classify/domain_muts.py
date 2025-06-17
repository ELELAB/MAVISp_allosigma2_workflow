#!/usr/bin/env python3

import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('mutations', help='file containing set of mutations to be studied')
parser.add_argument('residues', help='residues of the model, e.g. 1-200')

args = parser.parse_args()

wts = []
muts = []
nums = []
mutations = []

with open(args.mutations) as fh:
    for line in fh:
        line = line.strip()
        wts.append(line[0])
        muts.append(line[-1])
        nums.append(int(line[1:-1]))
        mutations.append(line)

data = pd.DataFrame({'mutation' : mutations,
                     'wt_residue' : wts ,
                     'position' : nums ,
                     'mutated_residue' : muts})

start_residue = int(args.residues.split("-")[0])
end_residue = int(args.residues.split("-")[1])

data = data[data.position >= start_residue]
data = data[data.position <= end_residue]

with open(f"muts_{args.residues}.dat", "w") as file:
    for mutation in list(data.mutation):
        file.write(mutation + "\n")
        
