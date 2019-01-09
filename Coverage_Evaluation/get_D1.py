#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

depG   = [1, 5, 10, 50, 100 , 200, 250]

GL     = len(depG)
depthD = dict(zip(depG, [ 0 ] * len(depG) ))

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

for i in depG:
    print('bases number >{0}X\t{1}'.format(i, depthD[i]))



