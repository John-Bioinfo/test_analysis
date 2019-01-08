
samtools index in.bam
samtoops depth in.bam > test.dep

python plot_Depth.py test.dep
python dep_grad_stats.py test1.txt
