# allosigma-utils

This repository contains utilities to handle and visualize AlloSigMA2 output according to the MAVISP framework (https://www.biorxiv.org/content/10.1101/2022.10.22.513328v4).
See below for the description of each individual script in details - to perform the steps as applied in MAVISp please refer to each individual subfolder and their script and readme.

## allosigma-classify

### Description

This scripts takes 

- a file with a list of mutations
- the same structure (.pdb) used on AlloSigma2 webserver
- a file with a list of side-chain volumes per residue type
- a volume cut-off
- an AlloSigMA2 session file downloaded from the website, output of the complete allosteric signaling map calculation

Allosigma-classify has two purposes, one is to quality control the input, 
that is, checking that mutations are covered by the structure and that the
structure used in the script is identical as the structure used on the webserver. 
Secondly, for each mutation covered by the structure, it calculates the difference 
between mutated and wild-type residue type:

`delta = volume(mutated_residue) - volume(wt_residue)`

and classifies the mutations according to three classes:

- `NA`, if `abs(delta) < cutoff`
- `UP`, if `abs(delta) > cutoff && delta > 0`
- `DOWN`, if `abs(delta) < cutoff && delta < 0`

this is useful to decide how to classify mutations to be given as input to the
AlloSigMA2 web server and matches its mutation model. The UP and DOWN classes
include mutation that significantly change in residue volume (in either direction)
and the NA class contains mutations that don't change significantly the residue volume.

By default, we set the volume cut-off to 5 A**3. This is because we want to discard from the
analysis mutations that impart small changes of steric hindrance (as for instance Y to F or
S to A) for which we do not expect the AlloSigma2 prediction to be reliable. Details on this
analysis are available on our publication:

    Degn K, Beltrame L, Dahl Hede F, Sora V, Nicolaci V, Vabistsevits M, Schmiegelow K, Wadt K,
    Tiberti M, Lambrughi M, Papaleo E. Cancer-related Mutations with Local or Long-range Effects 
    on an Allosteric Loop of p53. J Mol Biol. 2022 Sep 15;434(17):167663
    doi: 10.1016/j.jmb.2022.167663.

and on the GitHub repository connected to such publication:

    https://github.com/ELELAB/p53_S6-S7/tree/main/allosigma

### Requirements

- Python >= 3.7
- Pandas
- BioPandas

### Input

- muts.dat (mutation file) with your mutation list one letter code, i.e. A119G,
one mutation per line
- aminoacids.dat with volume value of each aminoacid (Ang^3), in TSV format and
single-letter code. Such a file is included in this distribution, containing
values from https://www.imgt.org/IMGTeducation/Aide-memoire//_UK/aminoacids/IMGTclasses.html
This page cites:
    - Pommié, C. et al., J. Mol. Recognit., 17, 17-32 (2004) PMID: 14872534, LIGM: 284 pdf
    - Kyte, J. and Doolittle, R.F., J. Mol. Biol., 157, 105-132 (1982).
- structure.pdb (pdb file) with the input structure.
- allosigma_run.zip (allosigma session file) from the webserver.

### Output

A single `tsv` file that contains the classification as well as information on
residue types and volumes

### Example

See the `example/allosigma-classify` directory and the do.sh script within

## allosigma-heatmap

### Description

This script takes information from

- an AlloSigMA2 session file downloaded from the website, output of the complete
allosteric signaling map calculation
- a tsv containing specific mutations, classified as UP or DOWN, output of the
allosigma-classify

allosigma-heatmap has two purposes:
* Plotting (pdf heatmaps)
* Formatting (tsv files)

If you wish to only get the formatting, you can omit the additional flags. 
If you wish to get the plot, you should use the flag --plot.

Based on these data and information, it plots heatmaps of the UP or DOWN allosteric
free energy (DgUP or DgDOWN) for the UP or DOWN (respectively) mutation sites encoded
in the input tsv file. It also writes corresponding tsv files containing the same
values.

Response sites are the whole protein by default, and can be further selected by using
option -r. Positions can be specified as residue numbers, as a comma-separated lists.
In this list, ranges can be specified as "-"-separated numbers. For instance,

	1,2,5-10,12

selects residues 1, 2, 5, 6, 7, 8, 9, 10, 12

It is possible to decide the maximum number of columns of rows for your heatmap by
specifying the -x and -y options. If more residues than what specified need to be
plotted, multiple matrices will be written.

option -f and -c allow to chnge font size and color map, respectively. Option -t
can be used to transpose the matrices.

### Requirements

- Python >= 3.7
- Pandas
- Biopython
- matplotlib

### Input

- an AlloSigMA2 session file downloaded from the website, output of the complete
allosteric signaling map calculation
- a tsv containing specific mutations, classified as UP or DOWN, output of the
allosigma-classify

### Output

- one or more pdf files, containing the aforamentioned heatmaps
- tsv files with values for up and down mutations

### Example

See the `example/allosigma-classify` directory and the do.sh script within

## allosigma-flitering 

### Description

This script takes 

- a PDB file
- a up or down {}_mutations.tsv file
- a dG cutoff value (in kcal/mol)
- a Distance cutoff: 
	Two distance calculation methods are available:
	- Cα–Cα distances 
	- Side-chain heavy atom distances (Glycine uses HA2/HA3) 
	Each method supports two threshold modes:
	- Value: a specific value (in Å - e.g. 14) 
	- Faction: a fraction of the median (e.g. 0.9)
	The method and the mode are selected using the -d flag, with four possible options:
	 Option               | Description                                       | Example                          |
	|-----------------------|---------------------------------------------------|----------------------------------|
	| `value`               | Cα–Cα distances with fixed cutoff                 | `-d value -v 10`                 |
	| `fraction`            | Cα–Cα distances as a fraction of median           | `-d fraction -f 0.5`             |
	| `sidechain_value`     | side-chain atom distances with fixed cutoff       | `-d sidechain_value -v 10`       |
	| `sidechain_fraction`  | side-chain atom distances as a fraction of median | `-d sidechain_fraction -f 0.5`   |

- an accessibility cutoff value (0-100)
- Can take the flag --pocket or --interface {file}, if a particular interface is of interest. 

The up or down file is the output file from allosigma-heatmap. 

For each mutation, the output from allosigma-heatmap is filtered based on 
the chosen cutoff values.

- Only positions with an `abs(dG) > dG cutoff` is kept. 
- From these only positions further away than the distance cutoff is kept*.
- From these positions, only positions more accessible than the accessibility 
  cutoff is kept. (This is calculated with naccess, deafault settings).
- If --pocket is chosen, fpocket will be run and the filtering of response sites is based on the pocket.
- If --interface {file} is added, the filtering of response sites is based on the interface.

### Requirements
- Python >= 3.7
- Pandas 
- Bio

### Input 

- {PDB}.pdb
- up_mutations.tsv or down_mutations.tsv (output from allosigma-heatmap). 

### Output 

- filtered_up_mutations.tsv or filtered_down_mutations.tsv. 
- up_mutations_arginine_distances_CA_CZ.csv or down_mutations_arginine_distances_CA_CZ.csv

These tables retain the format of up_ or down_mutations.tsv, with the
mutation column, a column for each of the filtered positions. A filtered
position can be empty for one mutation, while containing information
for another. The average dG value of the filtered mutations is reported
in the avg_dG column and the number of positions in then_mutations column. 

### Example

See the `example/allosigma-filtering` directory and the do.sh script within. 

## allosigma-visualization 

### Description

The script have two main modes, either with or without --putty.
Without should be the most common need, here we can have what 
is called “basic” in the example directory, and site specific. 

- basic use - pockets/regular/interface: 
  A way to create a pymol session for each mutation with 
  response sites in the pocket/interface or anywhere depending
  on your chosen input file from allosigma-filtering. 
  You can add both UP and DOWN or either of them. 

- site use - pockets/regular/interface
  A way to show a single site as a pymol session. You can add
  both UP and/or DOWN. The representation of mutation
  and response site will be spheres per default but can be 
  sticks. The site use is just a limitation of the basic use.
 
With putty (--putty) is an alternative way to show how the protein 
responds to a particular mutation according to allosigma. Here the b-factor 
of a protein is replaced with the prediced dG value, in response to
a particular mutation. 
IF you choose --putty you should only supply down or up mutations
and it is recommended to use the non filtered files, so the backbone
is sized on all carbon alphas. 
The pymol library is not able to create the putty itself, so when
you open the pymol session you have to: 

Action > Preset => b-factor putty 

Notice that there is a selection called "mutation". 

### Input
This script takes (mandatory)
--pdb PDB             Path to the PDB file

And/Or:
--up_tsv UP_TSV       Path to the up TSV file
--down_tsv DOWN_TSV   Path to the down TSV file

Optional
--site SITE          eg. P153
--structure_color     color of the cartoon representation of the structure 
--mut_color           color of the mutation
--response_color_up   color of the response site UP
--response_color_down color of the response site DOWN
--response_color_both color of the response site if overlap between up and down response sites.
--residue_representation use spheres, sticks or other pymol respresentation
if you choose spheres it will only be the CA while any other representation, the selection will be all atoms.

Additionally you can add the flag --putty if, if you do so, you can only add up_tsv OR down_tsv
and it is recommended that this is the unfiltered version!

--putty 		if you add this flag pdbs will be created with altered b-factors. 

You get the PyMOL session you need to open in pymol to inspect. Notice that if you want to see the putty 
you have to pres (in PyMOL): 

Action > Preset > b-factor putty

### Requirements
- Python >= 3.7
- Pandas 
- Bio
- PyMOL

### Output 

- pymol sessions and altered pdbs. 

### Example

See the `example/allosigma-visualization` directory and the do.sh script within. 

Here are two examples; both p53 and the P153S down mutation, the grey figure illustrate the mutaational 
site P153 with red, and the three sites in pockets affected in yellow. The other plot is the putty plot, 
where all sites P153S affects are depicted with the amount it affects them. We see some of the same 
areas as in the first plots, but also see how another loop is affected heavily in conformation. 

<p float="left">
  <img src="https://github.com/ELELAB/CSB-scripts/blob/fix%23%23307_allosigma_filtering_pocket/CSB-SB/allosigma-utils/example/allosigma-visualization/P153_sticks.png" width="300" />
  <img src="https://github.com/ELELAB/CSB-scripts/blob/fix%23%23307_allosigma_filtering_pocket/CSB-SB/allosigma-utils/example/allosigma-visualization/P153_putty.png" width="300" />
</p>

# Reference
if you use the code in this repository please cite our work:

Arnaudi M, Beltrame L, Degn K et al. MAVISp: Multi-layered Assessment of VarIants by Structure for proteins, biorxiv,  https://doi.org/10.1101/2022.10.22.513328 



