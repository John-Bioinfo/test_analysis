#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Bio.SeqIO.QualityIO import FastqGeneralIterator


f1 ="/data2/test/lohhla_test/1870124_exmpleOUT_new/1870124_tumor_sorted/1870124_tumor_sorted.chr6region.1.fastq" 
f2 ="/data2/test/lohhla_test/1870124_exmpleOUT_new/1870124_tumor_sorted/1870124_tumor_sorted.chr6region.2.fastq"

seqlen = 150

out1 = open('chr6_reg1.fastq', 'w')
for i, seq, qual in FastqGeneralIterator( open( f1 ) ):
    reclen = len(seq)
    if reclen < 150:
        addlen = 150 - reclen
        out1.write('@{0}\n{1}{2}\n+\n{3}{4}\n'.format(i, seq, 'N'*addlen, qual,  'F'*addlen))
    else:
        out1.write('@{0}\n{1}\n+\n{2}\n'.format(i, seq, qual))
out1.close()

out2 = open('chr6_reg2.fastq', 'w')
for i, seq, qual in FastqGeneralIterator( open( f2 ) ):
    reclen = len(seq)
    if reclen < 150:
        addlen = 150 - reclen
        out2.write('@{0}\n{1}{2}\n+\n{3}{4}\n'.format(i, seq, 'N'*addlen, qual, 'F'*addlen))
    else:
        out2.write('@{0}\n{1}\n+\n{2}\n'.format(i, seq, qual))
out2.close()




