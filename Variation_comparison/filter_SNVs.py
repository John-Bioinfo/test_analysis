#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
vcfFile = sys.argv[1]

handleV = open(vcfFile, 'r')
for line in handleV:
    if line.startswith('#CHROM'):
        header = line.rstrip().split('\t')
        #print("%s" % line.rstrip())
        print("%s" % '\t'.join([header[0], header[1], header[3], header[4], header[7], header[9], 'DP', 'VAF']))
    elif not line.startswith('#'):
        x = line.rstrip().split('\t')
        fields = x[9].split(':')
        if int(fields[3]) >= 500 and float(fields[4]) >= 0.01:       

            print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (x[0], x[1], x[3], x[4], x[7], x[9], fields[3], fields[4]))
        #print("%s\t%s\t%s\t%s\t%s\t%s" % (x[0], x[1], x[3], x[4], x[7], x[9]))
handleV.close()




