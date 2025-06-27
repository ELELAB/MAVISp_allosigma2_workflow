source /usr/local/envs/py310/bin/activate
./allosigma-heatmap  $1 $2 -m dg
./allosigma-heatmap  $1 $2 -m dh

#$1 ../../1.allosteric_signalling_map/allosigmazip.zip
#$2 ../../2.allosigma_classify/allosigma_mut.txt 

#analysis of dGs
python distribution_plot.py up_mutations.tsv up_mutations_distribution.pdf log
python distribution_plot.py down_mutations.tsv down_mutations_distribution.pdf log
python analyze_free_energies.py down_mutations.tsv down_mutations_analysis
python analyze_free_energies.py up_mutations.tsv up_mutations_analysis
python threshold.py up_mutations.tsv --output_plot distribution_with_thresholds_UP.png --output_thresholds threshold_UP.txt
python threshold.py down_mutations.tsv --output_plot distribution_with_thresholds_DOWN.png --output_thresholds thresholds_DOWN.txt
