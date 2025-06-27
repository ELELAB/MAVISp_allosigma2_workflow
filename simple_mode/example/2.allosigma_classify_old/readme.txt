#mutations2allosigma
#to match the mutation to the UP or DOWN model of allosigma
#NA is used in cases of mutations that cannot be modelled due to small changes in size

#source python env.
#module load python
#Requirements
- allosigma-classify
- aminoacids.dat with volume value of aminoacid (Ang^3)
- muts.dat with your mutation list one letter code, i.e. A119G
- {file}.pdb, the file you used in the webserver

#the muts.dat in this case is a copy of mutation_list.txt from the cancermuts folder

#cp ../../../../cancermuts/mutlist_DDMMYYYY.txt muts.dat 

#IF you have multiple domains you need to run the domains script: 

python domain_muts.py muts.dat 228-351

#mutations   file containing set of mutations to be studied
#residues    residues of the model, e.g. 1-200

#e.g. python domain_muts.py muts.dat 1-200

#run:

bash do.sh wt.pdb ../1.allosteric_signalling_map/NUI8P9VE.zip muts.dat

naccess file.pdb

