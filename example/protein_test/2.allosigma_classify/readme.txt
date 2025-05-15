#mutations2allosigma
#to match the mutation to the UP or DOWN model of allosigma
#NA is used in cases of mutations that cannot be modelled due to small changes in size

#source python env.
#module load python
##Requirements
  - allosigma-classify (used from the main code database)
  - aminoacids.dat with volume value of aminoacid (Ang^3)
  - muts.dat with your mutation list one letter code, i.e. A119G
  - {file}.pdb, the file you used in the webserver
  - {allosigmazipfile}.zip, downloaded from the Allosigma webserver (passed as argument)

##Input folder
  - aminoacids.dat
  - muts.dat
  - {file}.pdb

#the muts.dat in this case is a copy of mutation_list.txt from the cancermuts folder

cp ../../../../cancermuts/mutlist_DDMMYYYY.txt muts.dat 

#IF you have multiple domains you need to run the domains script: 

python ../../../../2.allosigma_classify/domain_muts.py mutations residues

#mutations   file containing set of mutations to be studied
#residues    residues of the model, e.g. 1-200

#e.g. python domain_muts.py muts.dat 1-200

#run:

bash do.sh file.pdb ../../1.allosteric_signalling_map/input/allosigmazipfile.zip muts.dat

#IF you have multiple domains:
bash do.sh file.pdb ../../1.allosteric_signalling_map/input/allosigmazipfile.zip muts_1-200.dat

naccess file.pdb

