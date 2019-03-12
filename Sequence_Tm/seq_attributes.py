#!/usr/bin/env python36
# -*- coding: UTF-8 -*-

from Bio import SeqIO
from Bio.SeqUtils import GC
from Bio.SeqUtils import MeltingTemp as mt
import sys

fafile = sys.argv[1]

for s in SeqIO.parse(fafile, 'fasta'):
    SEQ = s.seq 
    Tm  = mt.Tm_NN(SEQ)
    ## Ref : http://biopython.org/DIST/docs/api/Bio.SeqUtils.MeltingTemp-module.html
    print('{0}\t{1}\t{2:.3f}\t{3:.2f}'.format(s.id, len(SEQ), GC(SEQ), Tm ))




