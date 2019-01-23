#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

# usage : python get_Depth_v2.py 1860661-tumor_hlaB_1.dep
depG   = [1, 5, 10, 50, 100 , 200, 500, 1000, 5000, 10000]

GL     = len(depG)
depthD = dict(zip(depG, [ 0 ] * GL ))

inputDEP = sys.argv[1]

depHandle = open(  inputDEP  ,  'r'  )
for line in depHandle:
    x = line.strip().split('\t')
    d = int(x[2])
    if d > 0 :
        tmp_a =  [d//i for i in depG]
        
        a_L   =  [i for i in tmp_a if i > 0]
        
        
        for n, j in enumerate(a_L):

            depthD[depG[n]] += 1

depHandle.close()

totalBases= depthD[1]
print('{0}\t{1}\t{2}\t{3}'.format('depth', 'base_number', 'bases_percent', 'CovLength' ))
for i in depG:
    bn = depthD[i]                           ## bases number
    print('bases number {0}X\t{1}\t{2}\t{3}'.format(i, bn, bn*1.0/totalBases, totalBases ))



