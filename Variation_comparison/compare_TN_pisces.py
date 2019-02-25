#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

sampleNum = sys.argv[1]
inFile    = "/data2/test/zyqiao_test/mut_compare/FFPE_samples/" + sampleNum +  "_selected_pair.xls"


piscesOut = sys.argv[2]


d         = {}

handleP   = open(inFile,  'r')
for line in handleP:
    if not line.startswith('level'):
        xp = line.rstrip().split('\t')
        d[xp[9] + ':' + xp[10]] = 1
handleP.close()


pisces_handle = open(piscesOut, 'r')
for line in pisces_handle:
    if line.startswith('#CHROM'):
        print("{0}".format(line.rstrip()))
    elif not line.startswith('#'):
        x = line.rstrip().split('\t')
        if x[0]+':'+x[1] in d:
            print("{0}".format(line.rstrip()))
pisces_handle.close()


