source /usr/local/envs/py310/bin/activate


./allosigma-filtering -s $1 -i up_mutations.tsv -t 2 -d allatoms_value -v 5.5 -a 25 --interface $2
./allosigma-filtering  -s $1 -i down_mutations.tsv -t 2 -d allatoms_value -v 5.5 -a 25 --interface $2
