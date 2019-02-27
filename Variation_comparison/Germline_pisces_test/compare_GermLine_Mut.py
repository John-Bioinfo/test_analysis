#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os

posFile = sys.argv[1]

pos_handle = open(   posFile  ,  'r'  )
for line in pos_handle:
    z = line.rstrip().split('\t')
    vcfFile = './res_' + z[0] + '_germline/' + z[0]  + '.recal-H.vcf'
    if os.path.exists(vcfFile):
        v_h = open(vcfFile, 'r')
        for hline in v_h:
            if hline.startswith("#"):
                continue
            else:
                x = hline.rstrip().split('\t')
                if x[0] + ':'+x[1] == z[1]+':'+z[2]:
                    print('{0}\t{1}'.format(line.rstrip(),  hline.rstrip()))
        v_h.close()
pos_handle.close()
    

