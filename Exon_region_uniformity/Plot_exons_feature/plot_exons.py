#!/usr/bin/env python36
# -*- coding: UTF-8 -*-

from dna_features_viewer import GraphicFeature, GraphicRecord

startP = 29909037
seq_len = 4625
inputA = 'ENST00000396634_HLA-A_exons.txt' 
seqFeat = []

fileH = open(inputA, 'r')
for line in fileH:
    x = line.rstrip().split('\t')
    chrName = x[0]
    s = int(x[3]) - startP
    e = int(x[4]) - startP

    seqFeat.append(GraphicFeature(start = s, end = e+1, strand=+1, color='#ffcccc' ))
fileH.close()
#record = GraphicRecord(sequence= seq.replace('\n', ''),  features= seqFeat)
record = GraphicRecord(sequence_length= seq_len,  features= seqFeat)

#ax,_ = record.plot(figure_width= 120)
ax,_ = record.plot(figure_width= 18)
#record.plot_sequence(ax)
record.plot(ax)
ax.figure.savefig('Gene_sequence_hlaA_exons.png', bbox_inches='tight')

