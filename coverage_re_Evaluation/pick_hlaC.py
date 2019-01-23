#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Bio import SeqIO
from glob import glob
import sys
import os

filedir  = sys.argv[1]
sampleID = sys.argv[2]

cwd = os.getcwd()

fadir    = filedir + '/' + sampleID + '_hlas' 
if os.path.exists(fadir):
    os.chdir(fadir)
else:
    sys.exit('normal bed files exist!')

filename = 'types_C.fa'

n = 1
for i in SeqIO.parse(filename, 'fasta'):
    outname = 'testHLA_' + str(n) + '.bed'
    f = open(outname, 'w')
    f.write('{0}\t1\t{1}\n'.format(i.id, len(i.seq)))
    f.close()
    os.system('cp {0} {1}'.format(outname , cwd))
    n += 1


